<template>
  <div v-if="showUpgradeModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900/60 backdrop-blur-sm px-4">
    <div class="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl relative text-center">
      <button @click="showUpgradeModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
        <i class="fas fa-times text-xl"></i>
      </button>

      <div class="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
        <i class="fas fa-rocket"></i>
      </div>

      <h3 class="text-2xl font-black text-gray-800 mb-2">{{ t('upgradeModal.title') || 'Upgrade Required' }}</h3>
      <p class="text-gray-500 mb-6 font-medium">{{ upgradeMessage }}</p>

      <div class="bg-gray-50 rounded-xl p-4 mb-6 border border-gray-100 text-left">
        <p class="text-xs font-bold text-gray-400 uppercase tracking-wide mb-2">{{ t('upgradeModal.unlockFeatures') || 'Unlock features:' }}</p>
        <ul class="text-sm text-gray-600 space-y-2 font-medium">
          <li v-if="requiredTier === 'starter' || requiredTier === 'pro'"><i class="fas fa-check text-green-500 mr-2"></i> {{ t('upgradeModal.features.customDomains') || 'Custom Domains' }}</li>
          <li v-if="requiredTier === 'starter' || requiredTier === 'pro'"><i class="fas fa-check text-green-500 mr-2"></i> {{ t('upgradeModal.features.aiGenerations') || 'AI Generations' }}</li>
          <li v-if="requiredTier === 'starter' || requiredTier === 'pro'"><i class="fas fa-check text-green-500 mr-2"></i> {{ t('upgradeModal.features.leadForms') || 'Lead Forms (SMTP)' }}</li>
          <li v-if="requiredTier === 'pro'"><i class="fas fa-check text-green-500 mr-2"></i> {{ t('upgradeModal.features.catalogs') || 'Product Catalogs' }}</li>
        </ul>
      </div>

      <button @click="goToPricing" class="w-full bg-blue-600 text-white py-3 rounded-xl font-bold text-lg hover:bg-blue-700 transition shadow-lg">
        {{ t('upgradeModal.upgradeTo', { tier: requiredTier.charAt(0).toUpperCase() + requiredTier.slice(1) }) }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useSubscription } from '../composables/useSubscription';

const router = useRouter();
const { showUpgradeModal, upgradeMessage, requiredTier } = useSubscription();

// --- I18N LOGIC ---
const currentLang = ref(localStorage.getItem('app_lang') || 'en');
const translations = ref({});

const loadTranslations = async (lang) => {
  try {
    const response = await fetch(`/i18n/${lang}.json`);
    if (response.ok) {
      translations.value = await response.json();
    } else {
      if (lang !== 'en') await loadTranslations('en');
    }
  } catch (error) {
    console.error(error);
  }
};

const t = (key, params = {}) => {
  const keys = key.split('.');
  let value = translations.value;
  for (const k of keys) {
    if (value && Object.prototype.hasOwnProperty.call(value, k)) {
      value = value[k];
    } else return key;
  }
  if (typeof value === 'string') {
    for (const [k, v] of Object.entries(params)) {
      value = value.replace(new RegExp(`{${k}}`, 'g'), v);
    }
  }
  return value;
};

onMounted(() => {
  loadTranslations(currentLang.value);
});
// ------------------

const goToPricing = () => {
  showUpgradeModal.value = false;
  router.push('/settings?tab=billing');
};
</script>