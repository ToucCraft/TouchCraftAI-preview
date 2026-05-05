<template>
  <div class="bg-slate-900 rounded-xl border border-slate-800 shadow-xl overflow-hidden transition-all duration-500 ease-in-out flex flex-col shrink-0"
       :class="isOpen ? 'h-[80vh]' : 'h-[50px]'">
    <button @click="toggleChat" class="w-full h-[50px] px-4 flex justify-between items-center hover:bg-slate-800 transition-colors shrink-0 cursor-pointer outline-none">
      <h3 class="font-bold text-[10px] text-blue-400 uppercase flex items-center">
        <i class="fas fa-robot mr-2 text-lg" :class="{'animate-pulse text-blue-300': isChatLoading}"></i>
        {{ isOpen ? 'AI Assistant' : t('editSite.tabs.ai.title') }}
      </h3>
      <div class="flex items-center gap-2">
        <span v-if="!isOpen" class="text-[8px] bg-blue-600/20 text-blue-400 px-2 py-0.5 rounded-full uppercase font-bold tracking-wider">Beta</span>
        <i class="fas text-gray-400" :class="isOpen ? 'fa-times hover:text-white transition-colors' : 'fa-chevron-down'"></i>
      </div>
    </button>

    <div v-if="isOpen" class="flex-1 flex flex-col bg-slate-900 border-t border-slate-800 overflow-hidden relative">
      <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        <div class="flex flex-col items-start">
          <div class="max-w-[85%] p-3 rounded-2xl rounded-tl-none bg-slate-800 text-slate-300 text-xs shadow-sm border border-slate-700/50 leading-relaxed">
            Hello! Let's build your website iteratively. Tell me what to change!
          </div>
        </div>

        <div v-for="(msg, idx) in messages" :key="idx" class="flex flex-col" :class="msg.role === 'user' ? 'items-end' : 'items-start'">
          <div class="max-w-[85%] p-3 rounded-2xl text-xs shadow-sm leading-relaxed whitespace-pre-wrap"
               :class="msg.role === 'user'
                  ? 'bg-blue-600 text-white rounded-tr-none'
                  : 'bg-slate-800 text-slate-300 rounded-tl-none border border-slate-700/50'">
            {{ msg.text }}
          </div>
        </div>
      </div>

      <div class="p-3 bg-slate-900 border-t border-slate-800 shrink-0">
        <div class="relative flex items-center bg-slate-800 rounded-xl border border-slate-700 focus-within:border-blue-500 transition-colors shadow-inner overflow-hidden">
          <input
              v-model="chatMessage"
              @keyup.enter="editWithAi"
              :disabled="isChatLoading"
              placeholder="Type your request..."
              class="flex-1 bg-transparent py-3.5 pl-4 pr-12 text-xs text-white outline-none placeholder-slate-500 disabled:opacity-50"
          >
          <button
              @click="editWithAi"
              :disabled="isChatLoading || !chatMessage.trim()"
              class="absolute right-1.5 w-8 h-8 flex items-center justify-center rounded-lg bg-blue-600 text-white hover:bg-blue-500 transition disabled:opacity-50 disabled:hover:bg-blue-600"
          >
            <i class="fas" :class="isChatLoading ? 'fa-circle-notch fa-spin' : 'fa-arrow-up'"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, nextTick } from 'vue';
import { useSubscription } from '../../../composables/useSubscription';
import { useModal } from '../../../composables/useModal';
import api from '../../../api/client'; // <-- 1. Import your Axios client (Adjust the path if necessary!)

const props = defineProps({ isOpen: { type: Boolean, required: true } });
const emit = defineEmits(['update:isOpen']);

const config = inject('siteConfig');
const t = inject('t');
const projectId = inject('projectId');

const { checkLimit, triggerUpgrade } = useSubscription();
const { showAlert } = useModal();

const chatMessage = ref('');
const isChatLoading = ref(false);
const messages = ref([]);
const chatContainer = ref(null);

const toggleChat = () => {
  emit('update:isOpen', !props.isOpen);
  if (!props.isOpen) scrollToBottom();
};

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
};

const editWithAi = async () => {
  if (!checkLimit('ai_generations')) {
    return triggerUpgrade("AI Assistant requires the Starter plan.", 'starter');
  }

  const text = chatMessage.value.trim();
  if (!text || isChatLoading.value) return;

  messages.value.push({ role: 'user', text: text });
  chatMessage.value = '';
  isChatLoading.value = true;

  const aiMessageIndex = messages.value.length;
  messages.value.push({ role: 'ai', text: '' });
  scrollToBottom();

  try {
    const payloadMessages = messages.value
        .slice(0, -1)
        .map(m => ({ role: m.role, text: m.text }));

    // 2. Grab the base URL and Auth header directly from your configured Axios instance
    const baseUrl = api.defaults.baseURL;
    const authHeader = api.defaults.headers.common['Authorization'];

    const response = await fetch(`${baseUrl}/${projectId.value}/chat-edit-stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authHeader // <-- Automatically syncs with your Auth0 token
      },
      body: JSON.stringify({ messages: payloadMessages })
    });

    if (!response.ok) throw new Error('Network response was not ok');

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let aiFullResponse = "";
    let visibleText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      aiFullResponse += chunk;

      const jsonStartIndex = aiFullResponse.indexOf('```json');

      if (jsonStartIndex === -1) {
        visibleText = aiFullResponse;
      } else {
        visibleText = aiFullResponse.substring(0, jsonStartIndex).trim();
      }

      messages.value[aiMessageIndex].text = visibleText || "Thinking...";
      scrollToBottom();
    }

    const jsonMatch = aiFullResponse.match(/```json\s*([\s\S]*?)\s*```/);
    if (jsonMatch && jsonMatch[1]) {
      try {
        const newConfig = JSON.parse(jsonMatch[1]);
        config.value = newConfig;
        messages.value[aiMessageIndex].text += "\n\n✨ Website updated!";
      } catch (e) {
        console.error("Failed to parse AI JSON on frontend", e);
        messages.value[aiMessageIndex].text += "\n\n⚠️ Encountered an issue applying changes.";
      }
    } else {
      messages.value[aiMessageIndex].text += "\n\n⚠️ No configuration changes detected.";
    }

  } catch (e) {
    console.error("AI Edit Error:", e);
    messages.value[aiMessageIndex].text = 'Sorry, I encountered an error and could not complete the request.';
    showAlert('Error', 'AI failed to process request.', 'error');
  } finally {
    isChatLoading.value = false;
    scrollToBottom();
  }
};
</script>