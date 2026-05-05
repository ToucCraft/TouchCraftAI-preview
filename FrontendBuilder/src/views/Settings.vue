<template>
  <div v-if="isI18nLoaded" class="p-5 md:p-10 w-full flex flex-col h-full overflow-y-auto">

    <div class="mb-8 shrink-0">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ t('settings.title', 'Settings') }}</h1>
      <p class="text-gray-500">{{ t('settings.subtitle', 'Manage your account and subscription plans.') }}</p>
    </div>

    <div class="flex border-b border-gray-200 mb-8 overflow-x-auto no-scrollbar shrink-0">
      <button
          @click="currentTab = 'general'"
          :class="currentTab === 'general' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
          class="pb-3 px-4 font-bold text-sm border-b-2 transition-colors whitespace-nowrap">
        <i class="fas fa-envelope-open-text mr-2"></i> {{ t('settings.tabs.general', 'General (SMTP)') }}
      </button>
      <button
          @click="currentTab = 'profile'"
          :class="currentTab === 'profile' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
          class="pb-3 px-4 font-bold text-sm border-b-2 transition-colors whitespace-nowrap">
        <i class="fas fa-user mr-2"></i> {{ t('settings.tabs.profile', 'Profile') }}
      </button>
      <button
          @click="currentTab = 'billing'"
          :class="currentTab === 'billing' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
          class="pb-3 px-4 font-bold text-sm border-b-2 transition-colors whitespace-nowrap">
        <i class="fas fa-credit-card mr-2"></i> {{ t('settings.tabs.billing', 'Billing & Plans') }}
      </button>
      <button
          @click="currentTab = 'support'"
          :class="currentTab === 'support' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700'"
          class="pb-3 px-4 font-bold text-sm border-b-2 transition-colors whitespace-nowrap">
        <i class="fas fa-life-ring mr-2"></i> {{ t('settings.tabs.support', 'Support & Contact') }}
      </button>
    </div>

    <div class="">
      <div v-show="currentTab === 'general'">
        <SmtpSettings />
      </div>

      <div v-show="currentTab === 'profile'">
        <UserProfile />
      </div>

      <div v-show="currentTab === 'billing'">
        <BillingPlans />
      </div>
    </div>

    <div class="">
      <div v-show="currentTab === 'support'">
        <SupportContact />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../api/client';
import { useSubscription } from '../composables/useSubscription';

import SmtpSettings from '../components/SmtpSettings.vue';
import UserProfile from '../components/UserProfile.vue';
import BillingPlans from '../components/BillingPlans.vue';
import SupportContact from '../components/SupportContact.vue';

const route = useRoute();
const { updateUserData } = useSubscription();

const currentTab = ref(route.query.tab || 'general');

watch(() => route.query.tab, (newTab) => {
  if (newTab) currentTab.value = newTab;
});

// --- I18N LOGIC ---
const currentLang = ref(localStorage.getItem('app_lang') || 'en');
const translations = ref({});
const isI18nLoaded = ref(false);

const loadTranslations = async (lang) => {
  try {
    const response = await fetch(`/i18n/${lang}.json`);
    if (response.ok) {
      translations.value = await response.json();
    }
  } catch (error) {
    console.warn("Error loading translations", error);
  } finally {
    isI18nLoaded.value = true;
  }
};

const t = (key, fallback) => {
  const keys = key.split('.');
  let value = translations.value;
  for (const k of keys) {
    if (value && Object.prototype.hasOwnProperty.call(value, k)) {
      value = value[k];
    } else return fallback;
  }
  return value || fallback;
};
// ------------------

onMounted(async () => {
  await loadTranslations(currentLang.value);

  try {
    const res = await api.get('/user/me');
    updateUserData(res.data);
  } catch (e) {
    console.error("Failed to load user profile in Settings", e);
  }
});
</script>