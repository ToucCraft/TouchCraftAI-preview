<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
    <button @click="isOpen = !isOpen" class="w-full p-4 flex justify-between items-center bg-slate-50 hover:bg-slate-100 transition-colors">
      <h3 class="font-bold text-[10px] text-gray-700 uppercase flex items-center">
        <i class="fas fa-crown mr-2 text-blue-500"></i> Logo & Favicon
      </h3>
      <i class="fas text-gray-400" :class="isOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
    </button>

    <div v-show="isOpen" class="p-4 border-t border-slate-100 bg-white space-y-6">
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <h3 class="font-bold text-[10px] text-gray-500 uppercase">Main Logo</h3>
          <select v-model="config.logo_mode" class="p-1 border border-slate-200 rounded text-[9px] bg-slate-50 uppercase font-bold outline-none text-blue-600">
            <option value="text">Text Only</option>
            <option value="logo">Logo Only</option>
            <option value="both">Logo + Text</option>
          </select>
        </div>
        <div class="flex items-center gap-4">
          <div class="w-16 h-12 rounded border p-1 bg-slate-50 flex items-center justify-center relative overflow-hidden">
            <img v-if="config.logo_url" :src="config.logo_url" class="w-full h-full object-contain">
            <i v-else class="fas fa-image text-slate-300"></i>
          </div>
          <div class="flex-1">
            <span v-if="loadingStates['logo']" class="text-blue-500 animate-pulse text-[9px] font-bold">Processing...</span>
            <div class="space-y-2 mt-2 w-full">
              <input v-model="prompts['logo']" type="text"
                     :placeholder="t('editSite.tabs.favicon.logoPromptPlaceholder') || 'Describe your logo...'"
                     class="w-full p-1.5 border border-blue-100 rounded bg-blue-50/30 text-[10px] outline-none focus:border-blue-400 focus:bg-white transition-colors placeholder-blue-300"
                     :disabled="loadingStates['logo']" @keyup.enter="generateAiAsset('logo')">
              <div class="flex gap-3">
                <button @click="generateAiAsset('logo')" :disabled="loadingStates['logo']" class="text-blue-600 text-[10px] font-bold hover:underline disabled:opacity-50"><i class="fas fa-magic mr-1"></i> AI Generate</button>
                <label class="text-gray-500 text-[10px] font-bold hover:underline cursor-pointer" :class="{'opacity-50 pointer-events-none': loadingStates['logo']}">
                  <i class="fas fa-upload mr-1"></i> Upload <input type="file" @change="(e) => uploadAsset(e, 'logo')" class="hidden" accept=".png,.svg,.jpg,.jpeg" :disabled="loadingStates['logo']">
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="border-t border-slate-100"></div>

      <div>
        <h3 class="font-bold text-[10px] text-gray-500 uppercase mb-2">Browser Favicon</h3>
        <div class="flex items-center gap-4">
          <img :src="config.favicon || 'https://placehold.co/64?text=Icon'" class="w-10 h-10 rounded border p-1 bg-white object-contain">
          <div class="flex-1">
            <span v-if="loadingStates['favicon']" class="text-purple-500 animate-pulse text-[9px] font-bold">Processing...</span>
            <div class="space-y-2 mt-2 w-full">
              <input v-model="prompts['favicon']" type="text"
                     :placeholder="t('editSite.tabs.favicon.faviconPromptPlaceholder') || 'Describe favicon...'"
                     class="w-full p-1.5 border border-purple-100 rounded bg-purple-50/30 text-[10px] outline-none focus:border-purple-400 focus:bg-white transition-colors placeholder-purple-300"
                     :disabled="loadingStates['favicon']" @keyup.enter="generateAiAsset('favicon')">
              <div class="flex gap-3">
                <button @click="generateAiAsset('favicon')" :disabled="loadingStates['favicon']" class="text-purple-600 text-[10px] font-bold hover:underline disabled:opacity-50"><i class="fas fa-magic mr-1"></i> AI Generate</button>
                <label class="text-gray-500 text-[10px] font-bold hover:underline cursor-pointer" :class="{'opacity-50 pointer-events-none': loadingStates['favicon']}">
                  <i class="fas fa-upload mr-1"></i> Upload <input type="file" @change="(e) => uploadAsset(e, 'favicon')" class="hidden" accept=".png,.ico,.jpg" :disabled="loadingStates['favicon']">
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
import api from '../../../api/client';
import { useSubscription } from '../../../composables/useSubscription';
import { useModal } from '../../../composables/useModal';

const config = inject('siteConfig');
const t = inject('t');
const projectId = inject('projectId');
const { checkLimit, triggerUpgrade } = useSubscription();
const { showAlert } = useModal();

const isOpen = ref(false);
const loadingStates = ref({ logo: false, favicon: false });
const prompts = ref({ logo: '', favicon: '' });

const uploadAsset = async (e, type) => {
  const file = e.target.files[0];
  if(!file) return;
  loadingStates.value[type] = true;
  const fd = new FormData();
  fd.append('file', file);
  try {
    const res = await api.post(`/${projectId.value}/upload-asset?asset_type=${type}`, fd);
    const freshUrl = `${res.data.url}?t=${Date.now()}`;
    if (type === 'favicon') config.value.favicon = freshUrl;
    if (type === 'logo') {
      config.value.logo_url = freshUrl;
      if (config.value.logo_mode === 'text') config.value.logo_mode = 'both';
    }
  } catch(e) {
    showAlert('Error', t('editSite.alerts.uploadFail') || 'File upload failed.', 'error');
  } finally {
    loadingStates.value[type] = false;
    e.target.value = '';
  }
};

const generateAiAsset = async (type) => {
  if (!checkLimit('ai_generations')) return triggerUpgrade(t('editSite.upgrade.aiImage'), 'starter');
  loadingStates.value[type] = true;
  try {
    const res = await api.post(`/${projectId.value}/generate-asset`, {
      asset_type: type, prompt: prompts.value[type]
    });
    const freshUrl = `${res.data.url}?t=${Date.now()}`;
    if (type === 'favicon') config.value.favicon = freshUrl;
    if (type === 'logo') {
      config.value.logo_url = freshUrl;
      if (config.value.logo_mode === 'text') config.value.logo_mode = 'both';
    }
    prompts.value[type] = '';
  } catch(e) {
    showAlert('Error', t('editSite.alerts.aiGenError'), 'error');
  } finally {
    loadingStates.value[type] = false;
  }
};
</script>