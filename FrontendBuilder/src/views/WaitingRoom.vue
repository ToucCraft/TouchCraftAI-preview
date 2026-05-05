<template>
  <div v-if="isI18nLoaded" class="h-screen w-full flex flex-col items-center justify-center bg-slate-900 p-6 text-center">
    <div class="bg-white p-12 rounded-3xl shadow-2xl max-w-md w-full border border-slate-200">
      <div class="text-6xl mb-6 animate-bounce">⏳</div>
      <h1 class="text-2xl font-black text-slate-900 mb-2">{{ t('waitingRoom.title') }}</h1>
      <p class="text-sm text-slate-500 mb-8 leading-relaxed">
        {{ t('waitingRoom.message') }}
      </p>

      <button @click="checkStatus" class="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition">
        {{ t('waitingRoom.refreshBtn') }}
      </button>

      <div class="mt-6 pt-6 border-t border-slate-100">
        <button @click="logout" class="text-xs text-slate-400 hover:text-slate-600 font-bold uppercase tracking-widest">
          {{ t('waitingRoom.logoutBtn') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';
import { useRouter } from 'vue-router';
import api from '../api/client';

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

const { logout: auth0Logout } = useAuth0();
const router = useRouter();

const checkStatus = async () => {
  try {
    const response = await api.get('/user/me');

    if (response.data) {
      router.push('/dashboard');
    }
  } catch (error) {
    // 403
    console.log("Account is still pending activation.");
  }
};

const logout = () => {
  auth0Logout({ logoutParams: { returnTo: window.location.origin } });
};

onMounted(() => {
  loadTranslations(currentLang.value);
  checkStatus();
});
</script>