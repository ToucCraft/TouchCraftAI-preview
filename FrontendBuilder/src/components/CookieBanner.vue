<template>
  <transition name="slide-up">
    <div v-if="isVisible && isI18nLoaded" class="fixed bottom-4 left-4 right-4 md:left-auto md:right-8 md:w-[480px] bg-[#0f172a]/95 backdrop-blur-2xl border border-slate-700/50 rounded-3xl p-6 shadow-[0_20px_50px_rgba(0,0,0,0.5)] z-[100] text-slate-300 font-sans">

      <div class="flex items-center gap-3 mb-3">
        <div class="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center shrink-0">
          <i class="fas fa-cookie-bite text-xl text-blue-400"></i>
        </div>
        <h3 class="text-lg font-bold text-white">{{ t('cookieBanner.title') }}</h3>
      </div>

      <p class="text-sm leading-relaxed mb-6 text-slate-400">
        {{ t('cookieBanner.description') }}
        <router-link to="/privacy" class="text-blue-400 hover:underline">{{ t('cookieBanner.privacyLink') }}</router-link>.
      </p>

      <div class="space-y-3 mb-6">
        <div class="bg-slate-900/50 p-4 rounded-xl border border-slate-800 flex justify-between items-center">
          <div class="pr-4">
            <span class="font-bold text-white text-sm block mb-0.5">{{ t('cookieBanner.necessary.title') }}</span>
            <span class="text-xs text-slate-500 leading-tight block">{{ t('cookieBanner.necessary.desc') }}</span>
          </div>
          <div class="relative inline-flex items-center opacity-50 cursor-not-allowed shrink-0">
            <div class="w-11 h-6 bg-blue-600 rounded-full"></div>
            <div class="absolute left-[2px] top-[2px] bg-white border border-gray-300 rounded-full h-5 w-6 translate-x-4"></div>
          </div>
        </div>

        <div class="bg-slate-900/50 p-4 rounded-xl border border-slate-800 flex justify-between items-center transition-colors" :class="{'border-blue-500/40 bg-blue-900/10': preferences.analytics}">
          <div class="pr-4">
            <span class="font-bold text-white text-sm block mb-0.5">{{ t('cookieBanner.analytics.title') }}</span>
            <span class="text-xs text-slate-500 leading-tight block">{{ t('cookieBanner.analytics.desc') }}</span>
          </div>
          <label class="relative inline-flex items-center cursor-pointer shrink-0">
            <input type="checkbox" v-model="preferences.analytics" class="sr-only peer">
            <div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:bg-blue-600 transition-colors duration-300"></div>
            <div class="absolute left-[2px] top-[2px] bg-white border border-gray-300 rounded-full h-5 w-6 transition-transform duration-300 peer-checked:translate-x-4"></div>
          </label>
        </div>
      </div>

      <div class="flex flex-col gap-3">
        <button @click="acceptAll" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl transition-colors shadow-lg shadow-blue-500/20">
          {{ t('cookieBanner.buttons.acceptAll') }}
        </button>
        <div class="flex gap-3">
          <button @click="savePreferences" class="flex-1 py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl border border-slate-600 transition-colors">
            {{ t('cookieBanner.buttons.save') }}
          </button>
          <button @click="rejectOptional" class="flex-1 py-2.5 bg-transparent hover:bg-slate-800 text-slate-400 hover:text-white font-bold rounded-xl transition-colors">
            {{ t('cookieBanner.buttons.reject') }}
          </button>
        </div>
      </div>

    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue';

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
      console.warn(`Translation file for ${lang} not found, falling back to English`);
      if (lang !== 'en') await loadTranslations('en');
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
// ------------------

const GA_MEASUREMENT_ID = 'G-GPTS4K4Q3H';

const isVisible = ref(false);

const preferences = ref({
  necessary: true,
  analytics: true
});

onMounted(async () => {
  await loadTranslations(currentLang.value);

  const consent = localStorage.getItem('touchcraft_cookie_consent');
  if (!consent) {
    setTimeout(() => { isVisible.value = true; }, 1000);
  } else {
    const parsed = JSON.parse(consent);
    if (parsed.analytics) {
      initGA4();
    }
  }
});

const applyConsent = (analyticsConsent) => {
  const consentData = {
    necessary: true,
    analytics: analyticsConsent,
    timestamp: new Date().toISOString()
  };

  localStorage.setItem('touchcraft_cookie_consent', JSON.stringify(consentData));
  isVisible.value = false;

  if (analyticsConsent) {
    initGA4();
  } else {
    if (window.gtag) {
      window.gtag('consent', 'update', { 'analytics_storage': 'denied' });
    }
  }
};

const acceptAll = () => applyConsent(true);
const rejectOptional = () => applyConsent(false);
const savePreferences = () => applyConsent(preferences.value.analytics);

const initGA4 = () => {
  if (window.dataLayer && window.gtag) {
    window.gtag('consent', 'update', { 'analytics_storage': 'granted' });
    return;
  }

  const gtagScript = document.createElement('script');
  gtagScript.async = true;
  gtagScript.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
  document.head.appendChild(gtagScript);

  const inlineScript = document.createElement('script');
  inlineScript.innerHTML = `
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', { 'analytics_storage': 'granted' });
    gtag('js', new Date());
    gtag('config', '${GA_MEASUREMENT_ID}');
  `;
  document.head.appendChild(inlineScript);

  console.log('GA4 Initialized tracking for:', GA_MEASUREMENT_ID);
};
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(150%);
  opacity: 0;
}
</style>