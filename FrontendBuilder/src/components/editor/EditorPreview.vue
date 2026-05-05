<template>
  <div class="flex-1 flex flex-col relative bg-slate-200 min-w-0 transition-all duration-500 ease-in-out">

    <div class="h-14 flex items-center justify-center gap-4 border-b border-slate-300 bg-white/50 backdrop-blur-md z-10 shrink-0 relative">
      <button @click="toggleSidebar"
              class="absolute left-4 w-9 h-9 rounded-lg flex items-center justify-center bg-white shadow-sm border border-slate-200 text-slate-500 hover:text-blue-600 transition-all z-20"
              :title="isOpen ? t('editSite.toolbar.hide') : t('editSite.toolbar.show')">
        <i class="fas" :class="isOpen ? 'fa-chevron-left' : 'fa-chevron-right'"></i>
      </button>

      <button v-for="mode in ['mobile', 'tablet', 'desktop']" :key="mode" @click="viewMode = mode"
              class="w-9 h-9 rounded-lg flex items-center justify-center transition-all duration-300 shadow-sm"
              :class="viewMode === mode ? 'bg-white text-blue-600 scale-110 shadow-md border-blue-100 border' : 'text-slate-400 hover:text-slate-600'">
        <i class="fas" :class="mode === 'desktop' ? 'fa-desktop' : (mode === 'tablet' ? 'fa-tablet-alt' : 'fa-mobile-alt')"></i>
      </button>
    </div>

    <div class="flex-1 p-4 flex justify-center items-start overflow-hidden relative">
      <div
          v-if="!isInitialLoading"
          class="transition-all duration-500 ease-in-out h-full shadow-2xl bg-white relative overflow-hidden"
          :style="{ width: viewMode === 'desktop' ? '100%' : (viewMode === 'tablet' ? '765px' : '375px'), maxWidth: '100%' }">

        <iframe
            src="/preview-render"
            ref="previewFrame"
            class="w-full h-full border-none"
        ></iframe>
      </div>

      <div v-else class="flex items-center justify-center w-full h-full text-gray-500">
        <i class="fas fa-spinner fa-spin text-4xl"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, watch, onMounted, nextTick } from 'vue';

// 1. Принимаем и отдаем состояние сайдбара (v-model:isOpen)
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['update:isOpen']);

// 2. Инжектим глобальные данные из главного файла (EditSite.vue)
const config = inject('siteConfig');
const isInitialLoading = inject('isInitialLoading');
const t = inject('t');

// 3. Локальное состояние
const viewMode = ref('desktop');
const previewFrame = ref(null);

const toggleSidebar = () => {
  emit('update:isOpen', !props.isOpen);
};

// 4. Логика синхронизации Iframe
const syncIframe = () => {
  nextTick(() => {
    if (previewFrame.value && previewFrame.value.contentWindow && config.value) {
      previewFrame.value.contentWindow.postMessage({
        type: 'UPDATE_CONFIG',
        config: JSON.parse(JSON.stringify(config.value))
      }, '*');
    }
  });
};

// Реактивно следим за ЛЮБЫМИ изменениями в config и шлем их в iframe
watch(() => config.value, () => {
  syncIframe();
}, { deep: true });

onMounted(() => {
  // Слушаем сообщение от iframe, когда он готов принять конфиг
  window.addEventListener('message', (e) => {
    if(e.data.type === 'RENDERER_READY') {
      console.log("Renderer is ready, syncing...");
      syncIframe();
    }
  });
});
</script>