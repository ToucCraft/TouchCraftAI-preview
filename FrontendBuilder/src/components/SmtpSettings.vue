<template>
  <div v-if="isI18nLoaded" class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
    <div class="flex items-center mb-6">
      <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center text-blue-600 mr-4">
        <i class="fas fa-envelope-open-text text-xl"></i>
      </div>
      <div>
        <h2 class="text-xl font-black text-gray-800">{{ t('smtpSettings.title') }}</h2>
        <p class="text-sm text-gray-500">{{ t('smtpSettings.subtitle') }}</p>
      </div>
    </div>

    <form @submit.prevent="saveSmtp" class="space-y-5">
      <div class="grid grid-cols-2 gap-5">
        <div>
          <label class="block text-xs font-bold text-gray-600 uppercase mb-2">{{ t('smtpSettings.labels.host') }}</label>
          <input v-model="form.host" type="text" :placeholder="t('smtpSettings.placeholders.host')" required
                 class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-sm">
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-600 uppercase mb-2">{{ t('smtpSettings.labels.port') }}</label>
          <input v-model="form.port" type="number" :placeholder="t('smtpSettings.placeholders.port')" required
                 class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-sm">
        </div>
      </div>

      <div class="grid grid-cols-2 gap-5">
        <div>
          <label class="block text-xs font-bold text-gray-600 uppercase mb-2">{{ t('smtpSettings.labels.username') }}</label>
          <input v-model="form.username" type="email" :placeholder="t('smtpSettings.placeholders.username')" required
                 class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-sm">
        </div>
        <div>
          <label class="block text-xs font-bold text-gray-600 uppercase mb-2">{{ t('smtpSettings.labels.password') }}</label>
          <input v-model="form.password" type="password" :placeholder="t('smtpSettings.placeholders.password')" required
                 class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-sm">
        </div>
      </div>

      <div>
        <label class="block text-xs font-bold text-gray-600 uppercase mb-2">{{ t('smtpSettings.labels.fromEmail') }}</label>
        <input v-model="form.from_email" type="email" :placeholder="t('smtpSettings.placeholders.fromEmail')" required
               class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-sm">
      </div>

      <div class="pt-4 border-t border-gray-100 flex items-center justify-between">
        <span class="text-xs text-gray-400">
          <i class="fas fa-info-circle mr-1"></i> {{ t('smtpSettings.recommendation') }}
        </span>
        <button type="submit" :disabled="isLoading"
                class="bg-blue-600 text-white px-6 py-3 rounded-xl font-bold text-sm hover:bg-blue-700 transition shadow-md disabled:opacity-50">
          <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
          {{ isLoading ? t('smtpSettings.buttons.saving') : t('smtpSettings.buttons.save') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/client';
import { useSubscription } from '../composables/useSubscription';

const { checkLimit, triggerUpgrade, updateUserData } = useSubscription();

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

const form = ref({
  host: '',
  port: 587,
  username: '',
  password: '',
  from_email: ''
});

const loadSmtp = async () => {
  try {
    const res = await api.get('/user/me');
    updateUserData(res.data);
    if (res.data.smtp_config) {
      form.value = res.data.smtp_config;
    }
  } catch (e) {
    console.log("No existing config or failed to load");
  }
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  loadSmtp();
});

const saveSmtp = async () => {
  isLoading.value = true;
  try {
    await api.post('/user/smtp', form.value);
    showAlert(t('common.alerts.success'), t('smtpSettings.alerts.success') || 'Settings saved', 'success');
  } catch (e) {
    showAlert(t('common.alerts.error'), t('smtpSettings.alerts.error') || 'Error saving', 'error');
    console.error(e);
  } finally {
    isLoading.value = false;
  }
};
</script>