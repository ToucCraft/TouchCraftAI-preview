<template>
  <div v-if="config" class="min-h-screen transform-gpu overflow-x-hidden">
    <SitePreview :config="config" />
  </div>
  <div v-else class="h-screen flex items-center justify-center bg-white text-slate-300">
    <i class="fas fa-circle-notch fa-spin text-3xl"></i>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import SitePreview from '../components/SitePreview.vue';

const config = ref(null);
let readyInterval = null; // Храним ID интервала

const handleMessage = (event) => {
  if (event.data.type === 'UPDATE_CONFIG') {
    config.value = event.data.config;
    // Как только получили конфиг — убиваем интервал
    if (readyInterval) {
      clearInterval(readyInterval);
      readyInterval = null;
    }
  }
};

onMounted(() => {
  window.addEventListener('message', handleMessage);

  // Сообщаем родителю, что рендерер готов получать данные
  if (window.parent) {
    window.parent.postMessage({ type: 'RENDERER_READY' }, '*');
  }

  // ЗАЩИТА: продолжаем запрашивать конфиг каждые 300мс,
  // пока родитель нам его не пришлет (помогает избежать любых зависаний).
  readyInterval = setInterval(() => {
    if (!config.value && window.parent) {
      window.parent.postMessage({ type: 'RENDERER_READY' }, '*');
    }
  }, 300);
});

onUnmounted(() => {
  window.removeEventListener('message', handleMessage);
  if (readyInterval) clearInterval(readyInterval);
});
</script>

<style>
/* Полный сброс для чистого отображения внутри iframe */
body { margin: 0; padding: 0; overflow-x: hidden; background: white; }
::-webkit-scrollbar { width: 0px; background: transparent; }
</style>