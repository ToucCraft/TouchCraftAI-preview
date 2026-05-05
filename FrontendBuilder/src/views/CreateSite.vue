<template>
  <div v-if="isI18nLoaded" class="p-5 md:p-10">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ t('createSite.title') }}</h1>

  <div class="max-w-[1400px] mx-auto w-full">
    <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 space-y-6">

      <div class="grid grid-cols-2 gap-4">
        <div class="col-span-2 md:col-span-1">
          <label class="block text-xs font-bold text-gray-400 uppercase mb-1.5">{{ t('createSite.labels.businessName') }}</label>
          <input v-model="form.business_name" class="w-full p-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 bg-slate-50 outline-none">
        </div>
        <div class="col-span-2 md:col-span-1">
          <label class="block text-xs font-bold text-gray-400 uppercase mb-1.5">{{ t('createSite.labels.niche') }}</label>
          <input v-model="form.niche" class="w-full p-2.5 border rounded-xl text-sm focus:ring-2 focus:ring-blue-500 bg-slate-50 outline-none" :placeholder="t('createSite.labels.nichePlaceholder')">
        </div>
      </div>

      <div>
        <label class="block text-xs font-bold text-gray-400 uppercase mb-1.5">{{ t('createSite.labels.description') }}</label>
        <textarea v-model="form.business_description" rows="2" class="w-full p-2.5 border rounded-xl text-sm bg-slate-50 outline-none focus:ring-2 focus:ring-blue-500"></textarea>
      </div>

      <div>
        <label class="block text-xs font-bold text-gray-400 uppercase mb-2">{{ t('createSite.labels.sections') }}</label>
        <div class="flex flex-wrap gap-2">
          <div v-for="section in availableSections" :key="section.id" class="relative group">
            <button
                @click="toggleSection(section.id)"
                type="button"
                :disabled="section.requiresSmtp && !isSmtpConfigured"
                :class="[
                'px-4 py-2 rounded-xl text-xs font-bold transition-all border flex items-center',
                form.sections.includes(section.id)
                  ? 'bg-blue-600 border-blue-600 text-white shadow-md'
                  : 'bg-white border-gray-200 text-gray-500 hover:border-blue-400',
                section.requiresSmtp && !isSmtpConfigured ? 'opacity-50 cursor-not-allowed bg-gray-100' : ''
              ]"
            >
              <i class="fas mr-2" :class="form.sections.includes(section.id) ? 'fa-check-circle' : 'fa-circle'"></i>
              {{ t(`createSite.sections.${section.id}`) }}
            </button>

            <div v-if="section.requiresSmtp && !isSmtpConfigured"
                 class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-2 bg-gray-800 text-white text-[10px] rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50 text-center shadow-xl">
              {{ t('createSite.smtpWarning') }}
              <router-link to="/settings" class="text-blue-400 underline ml-1 pointer-events-auto">{{ t('createSite.setupNow') }}</router-link>
              <div class="absolute top-full left-1/2 -translate-x-1/2 border-8 border-transparent border-t-gray-800"></div>
            </div>
          </div>
        </div>
      </div>

      <div>
        <label class="block text-xs font-bold text-gray-400 uppercase mb-2">{{ t('createSite.labels.languages') }}</label>
        <div class="flex flex-wrap gap-2">
          <button
              v-for="lang in availableLanguages"
              :key="lang.code"
              @click="toggleLanguage(lang.code)"
              type="button"
              :class="[
              'px-4 py-2 rounded-xl text-xs font-bold transition-all border flex items-center',
              form.languages.includes(lang.code)
                ? 'bg-blue-600 border-blue-600 text-white shadow-md'
                : 'bg-white border-gray-200 text-gray-500 hover:border-blue-400'
            ]"
          >
            <i class="fas mr-2" :class="form.languages.includes(lang.code) ? 'fa-check-circle' : 'fa-circle'"></i>
            {{ t(`languages.${lang.code}`) }}
          </button>
        </div>
      </div>

      <div class="bg-gray-50 p-4 rounded-xl border border-gray-100 space-y-2.5">
        <h4 class="text-xs font-black text-gray-400 uppercase">{{ t('createSite.labels.legal') }}</h4>
        <div class="grid grid-cols-2 gap-2.5">
          <input v-model="form.contact_details.legal_name" :placeholder="t('createSite.labels.legalName')" class="p-2.5 border rounded-lg text-xs outline-none focus:border-blue-500 bg-white">
          <input v-model="form.contact_details.tax_id" :placeholder="t('createSite.labels.taxId')" class="p-2.5 border rounded-lg text-xs outline-none focus:border-blue-500 bg-white">
          <input v-model="form.contact_details.address" :placeholder="t('createSite.labels.address')" class="col-span-2 p-2.5 border rounded-lg text-xs outline-none focus:border-blue-500 bg-white">
          <input v-model="form.contact_details.phone" :placeholder="t('createSite.labels.phone')" class="p-2.5 border rounded-lg text-xs outline-none focus:border-blue-500 bg-white">
          <input v-model="form.contact_details.email" :placeholder="t('createSite.labels.email')" class="p-2.5 border rounded-lg text-xs outline-none focus:border-blue-500 bg-white">
        </div>
      </div>

      <button @click="generateDraft" :disabled="isProcessing" class="w-full bg-blue-600 text-white py-3.5 rounded-xl font-bold text-lg hover:bg-blue-700 disabled:opacity-50 transition shadow-md mt-2">
        <i class="fas" :class="isProcessing ? 'fa-spinner fa-spin' : 'fa-magic'"></i>
        {{ isProcessing ? t('createSite.buttons.generating') : t('createSite.buttons.generate') }}
      </button>
    </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/client';

import { useSubscription } from '../composables/useSubscription';
import { useModal } from '../composables/useModal';

const { checkLimit, triggerUpgrade, updateUserData, currentLimits } = useSubscription();
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

const router = useRouter();
const isProcessing = ref(false);
const userProfile = ref(null);

const availableLanguages = [
  { code: 'en' },
  { code: 'es' },
  { code: 'fr' },
  { code: 'de' },
  { code: 'it' },
  { code: 'ru' },
  { code: 'uk' },
  { code: 'ee' },
  { code: 'ca' }
];

onMounted(async () => {
  await Promise.all([
    loadTranslations(currentLang.value),
    (async () => {
      try {
        const res = await api.get('/user/me');
        userProfile.value = res.data;
        updateUserData(res.data);
      } catch (e) {
        console.error("Failed to load user profile");
      }
    })()
  ]);
});

const isSmtpConfigured = computed(() => {
  const config = userProfile.value?.smtp_config;
  return !!(config && config.host && config.username && config.password);
});

const form = reactive({
  business_name: '',
  business_description: '',
  niche: '',
  languages: ['en'],
  sections: ['hero', 'about', 'features'],
  contact_details: {
    legal_name: '', address: '', tax_id: '', email: '', phone: '',
    socials: { instagram: '', 'x-twitter': '', youtube: '', tiktok: '', telegram: '', whatsapp: '' }
  }
});

const availableSections = [
  { id: 'hero' },
  { id: 'about' },
  { id: 'features' },
  { id: 'faq' },
  { id: 'map' },
  { id: 'contacts' },
  { id: 'form', requiresSmtp: true },
  { id: 'gallery' }
];

const toggleSection = (id) => {
  if (id === 'form' && !checkLimit('lead_forms')) {
    return triggerUpgrade(t('createSite.upgrade.leadForms') || "Lead Forms require the Starter plan.", 'starter');
  }

  const index = form.sections.indexOf(id);
  if (index > -1) form.sections.splice(index, 1);
  else form.sections.push(id);
};

const toggleLanguage = (code) => {
  const index = form.languages.indexOf(code);

  if (index > -1) {
    // Если язык уже выбран - удаляем его
    form.languages.splice(index, 1);
  } else {
    // Проверяем лимиты тарифа перед добавлением
    if (form.languages.length >= currentLimits.value.max_languages) {
      if (currentLimits.value.max_languages === 1) {
        triggerUpgrade(t('createSite.upgrade.maxLanguages') || "Multiple languages require the Starter plan.", 'starter');
      } else if (currentLimits.value.max_languages === 3) {
        triggerUpgrade(t('createSite.upgrade.maxLanguagesPro') || "Starter plan is limited to 3 languages.", 'pro');
      } else {
        showAlert('Limit Reached', t('createSite.alerts.maxLanguages') || "Maximum languages reached.", 'warning');
      }
      return;
    }
    form.languages.push(code);
  }
};

const generateDraft = async () => {
  if (form.sections.includes('form') && !checkLimit('lead_forms')) {
    return triggerUpgrade(t('createSite.upgrade.leadForms') || "Lead Forms require the Starter plan.", 'starter');
  }

  if (!form.business_name || !form.niche) {
    return showAlert('Warning', t('createSite.alerts.reqNameNiche') || "Business name and niche are required.", 'warning');
  }
  if (form.languages.length === 0) {
    return showAlert('Warning', t('createSite.alerts.reqLang') || "Please add at least one language.", 'warning');
  }

  isProcessing.value = true;

  const payload = JSON.parse(JSON.stringify(form));
  if (payload.contact_details?.socials) {
    Object.keys(payload.contact_details.socials).forEach(key => {
      if (!payload.contact_details.socials[key]) delete payload.contact_details.socials[key];
    });
  }

  try {
    const res = await api.post('/generate', payload);
    router.push(`/edit/${res.data.project_id}`);
  } catch (e) {
    showAlert('Error', t('createSite.alerts.genFailed') || "Failed to generate site.", 'error');
  } finally {
    isProcessing.value = false;
  }
};
</script>
