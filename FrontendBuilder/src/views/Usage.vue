<template>
  <div v-if="isI18nLoaded" class="p-5 md:p-10 w-full flex flex-col min-h-full">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ t('usage.title') }}</h1>
      <p class="text-gray-500">{{ t('usage.subtitle') }}</p>
    </div>

    <div v-if="loading" class="flex-1 flex justify-center items-center">
      <div class="loader ease-linear rounded-full border-4 border-t-4 border-blue-500 h-12 w-12"></div>
    </div>

    <div v-else-if="userData" class="space-y-8">

      <div class="bg-gradient-to-r from-gray-900 to-slate-800 rounded-3xl p-8 text-white shadow-lg relative overflow-hidden">
        <div class="relative z-10 flex justify-between items-center">
          <div>
            <p class="text-slate-400 font-bold uppercase tracking-wider text-xs mb-1">{{ t('usage.plan.current') }}</p>
            <h2 class="text-3xl font-black capitalize">{{ userData.subscription_tier }}</h2>
          </div>
          <div class="text-right">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase"
                  :class="userData.subscription_status === 'active' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'">
              {{ userData.subscription_status }}
            </span>
          </div>
        </div>
        <i class="fas fa-gem absolute -right-10 -bottom-10 text-9xl text-white opacity-5"></i>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

        <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <div class="flex justify-between items-center mb-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
                <i class="fas fa-window-maximize"></i>
              </div>
              <h3 class="font-bold text-gray-800">{{ t('usage.stats.sites') }}</h3>
            </div>
            <span class="text-sm font-bold text-gray-500">{{ userData.project_count }} / {{ userData.limits.max_sites }}</span>
          </div>

          <div class="w-full bg-gray-100 rounded-full h-2.5 mb-2">
            <div class="bg-blue-600 h-2.5 rounded-full transition-all duration-500"
                 :style="{ width: Math.min((userData.project_count / userData.limits.max_sites) * 100, 100) + '%' }"></div>
          </div>
          <p class="text-xs text-gray-400">{{ t('usage.stats.sitesDesc') }}</p>
        </div>

        <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <div class="flex justify-between items-center mb-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
                <i class="fas fa-magic"></i>
              </div>
              <h3 class="font-bold text-gray-800">{{ t('usage.stats.ai') }}</h3>
            </div>
            <span class="text-sm font-bold text-gray-500">{{ userData.ai_generations_used }}</span>
          </div>

          <div class="w-full bg-gray-100 rounded-full h-2.5 mb-2">
            <div class="bg-purple-600 h-2.5 rounded-full transition-all duration-500 w-full"
                 :class="userData.ai_generations_used > 0 ? 'bg-purple-500' : 'bg-gray-300'"
                 :style="{ width: userData.ai_generations_used > 0 ? '100%' : '0%' }"></div>
          </div>
          <p class="text-xs text-gray-400">{{ t('usage.stats.aiDesc') }}</p>
        </div>
      </div>

      <div>
        <h3 class="text-lg font-bold text-gray-800 mb-4">{{ t('usage.features.title') }}</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">

          <div class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4">
            <div :class="userData.limits.custom_domains ? 'text-green-500 bg-green-50' : 'text-gray-400 bg-gray-50'" class="w-10 h-10 rounded-full flex items-center justify-center">
              <i class="fas" :class="userData.limits.custom_domains ? 'fa-check' : 'fa-times'"></i>
            </div>
            <div>
              <p class="font-bold text-sm text-gray-800">{{ t('usage.features.domains') }}</p>
            </div>
          </div>

          <div class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4">
            <div :class="userData.limits.lead_forms ? 'text-green-500 bg-green-50' : 'text-gray-400 bg-gray-50'" class="w-10 h-10 rounded-full flex items-center justify-center">
              <i class="fas" :class="userData.limits.lead_forms ? 'fa-check' : 'fa-times'"></i>
            </div>
            <div>
              <p class="font-bold text-sm text-gray-800">{{ t('usage.features.leads') }}</p>
            </div>
          </div>

          <div class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex items-center gap-4">
            <div :class="userData.limits.catalogs ? 'text-green-500 bg-green-50' : 'text-gray-400 bg-gray-50'" class="w-10 h-10 rounded-full flex items-center justify-center">
              <i class="fas" :class="userData.limits.catalogs ? 'fa-check' : 'fa-times'"></i>
            </div>
            <div>
              <p class="font-bold text-sm text-gray-800">{{ t('usage.features.catalogs') }}</p>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/client.js';

// --- I18N LOGIC ---
const currentLang = ref(localStorage.getItem('app_lang') || 'en');
const translations = ref({});
const isI18nLoaded = ref(false);

const loadTranslations = async (lang) => {
  try {
    const response = await fetch(`/i18n/${lang}.json`);
    if (response.ok) {
      translations.value = await response.json();
      isI18nLoaded.value = true;
    } else {
      if (lang !== 'en') await loadTranslations('en');
    }
  } catch (error) {
    isI18nLoaded.value = true;
  }
};

const t = (key) => {
  const keys = key.split('.');
  let value = translations.value;
  for (const k of keys) {
    if (value && Object.prototype.hasOwnProperty.call(value, k)) {
      value = value[k];
    } else return key;
  }
  return value;
};
// ------------------

const loading = ref(true);
const userData = ref(null);

const fetchUsageData = async () => {
  try {
    const res = await api.get('/user/me');
    userData.value = res.data;
  } catch (error) {
    console.error("Failed to load usage data", error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  fetchUsageData();
});
</script>