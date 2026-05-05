<template>
  <div v-if="isI18nLoaded" class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 mb-8">
    <div class="flex items-center mb-6">
      <div class="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 mr-4">
        <i class="fas fa-user text-xl"></i>
      </div>
      <div>
        <h2 class="text-xl font-black text-gray-800">{{ t('userProfile.title') }}</h2>
        <p class="text-sm text-gray-500">{{ t('userProfile.subtitle') }}</p>
      </div>
    </div>

    <form @submit.prevent="saveProfile" class="space-y-5">
      <div class="grid grid-cols-2 gap-5 mb-4">
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-2">{{ t('userProfile.labels.id') }}</label>
          <div class="p-3 bg-gray-100 border border-gray-200 rounded-xl text-sm text-gray-500 font-mono truncate">
            {{ profile.id || '—' }}
          </div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-2">{{ t('userProfile.labels.email') }}</label>
          <div class="p-3 bg-gray-100 border border-gray-200 rounded-xl text-sm text-gray-500 truncate">
            {{ profile.email || '—' }}
          </div>
        </div>
      </div>

      <div>
        <label class="block text-xs font-bold text-gray-600 uppercase mb-2">{{ t('userProfile.labels.fullName') }}</label>
        <input v-model="profile.full_name" type="text" :placeholder="t('userProfile.placeholders.fullName')" required
               class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all text-sm">
      </div>

      <div class="grid grid-cols-3 gap-5 pt-4">
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-2">{{ t('userProfile.labels.tier') }}</label>
          <div class="text-sm font-semibold text-indigo-600 capitalize">
            {{ profile.subscription_tier || 'Freemium' }}
          </div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-2">{{ t('userProfile.labels.status') }}</label>
          <div class="text-sm font-semibold text-gray-700 capitalize">
            {{ profile.subscription_status || 'Active' }}
          </div>
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-500 uppercase mb-2">{{ t('userProfile.labels.aiUsed') }}</label>
          <div class="text-sm font-semibold text-gray-700">
            {{ profile.ai_generations_used || 0 }}
          </div>
        </div>
      </div>

      <div class="pt-6 border-t border-gray-100 flex items-center justify-end">
        <button type="submit" :disabled="isLoading"
                class="bg-indigo-600 text-white px-6 py-3 rounded-xl font-bold text-sm hover:bg-indigo-700 transition shadow-md disabled:opacity-50">
          <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
          {{ isLoading ? t('userProfile.buttons.saving') : t('userProfile.buttons.save') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/client';
import { useModal } from '../composables/useModal';

const { showAlert } = useModal();

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

const isLoading = ref(false);
const profile = ref({
  id: '',
  email: '',
  full_name: '',
  subscription_tier: '',
  subscription_status: '',
  ai_generations_used: 0
});

const loadProfile = async () => {
  try {
    const res = await api.get('/user/me');
    profile.value = res.data;
  } catch (e) {
    console.error("Error loading profile", e);
  }
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  loadProfile();
});

const saveProfile = async () => {
  isLoading.value = true;
  try {
    await api.patch('/user/me', { full_name: profile.value.full_name });
    showAlert(t('common.alerts.success'), t('userProfile.alerts.success'), 'success');
  } catch (e) {
    showAlert(t('common.alerts.error'), t('userProfile.alerts.error'), 'error');
    console.error(e);
  } finally {
    isLoading.value = false;
  }
};
</script>