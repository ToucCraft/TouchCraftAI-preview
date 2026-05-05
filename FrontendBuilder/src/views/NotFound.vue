<template>
  <div v-if="isI18nLoaded" class="min-h-screen bg-[#020617] text-white font-sans flex items-center justify-center relative overflow-hidden">

    <div class="absolute top-[-10%] left-1/2 -translate-x-1/2 w-[600px] h-[500px] bg-blue-600/20 blur-[120px] rounded-full pointer-events-none transform-gpu"></div>
    <div class="absolute bottom-[-10%] left-1/4 w-[400px] h-[400px] bg-cyan-600/10 blur-[100px] rounded-full pointer-events-none transform-gpu"></div>

    <div class="relative z-10 text-center px-6">
      <h1 class="text-[12rem] md:text-[15rem] font-black leading-none tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-blue-400 to-blue-900 opacity-50 mb-20">
        {{ t('notFound.title') }}
      </h1>

      <div class="mt-[-2rem] md:mt-[-4rem]">
        <h2 class="text-3xl md:text-5xl font-extrabold mb-4">
          {{ t('notFound.subtitle') }}
        </h2>
        <p class="text-slate-400 text-lg md:text-xl max-w-md mx-auto mb-10 leading-relaxed">
          {{ t('notFound.description') }}
        </p>

        <router-link to="/" class="inline-flex items-center px-8 py-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold transition-all transform hover:scale-105 shadow-[0_0_30px_rgba(37,99,235,0.4)]">
          <i class="fas fa-arrow-left mr-3"></i>
          {{ t('notFound.backBtn') }}
        </router-link>
      </div>
    </div>

    <div class="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const currentLang = ref(localStorage.getItem('app_lang') || 'en');
const translations = ref({});
const isI18nLoaded = ref(false);

const loadTranslations = async (lang) => {
  try {
    const response = await fetch(`/i18n/${lang}.json`);
    if (response.ok) {
      translations.value = await response.json();
      isI18nLoaded.value = true;
    }
  } catch (error) {
    console.error("Error loading translations:", error);
    isI18nLoaded.value = true;
  }
};

const t = (key) => {
  const keys = key.split('.');
  let value = translations.value;
  for (const k of keys) {
    if (value && Object.prototype.hasOwnProperty.call(value, k)) {
      value = value[k];
    } else {
      return key;
    }
  }
  return value;
};

onMounted(() => {
  loadTranslations(currentLang.value);
});
</script>

<style scoped>
/* Дополнительные стили если нужно */
</style>