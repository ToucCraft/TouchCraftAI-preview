<template>
  <div v-if="isI18nLoaded">
    <div class="bg-blue-50 rounded-2xl p-6 mb-8 border border-blue-100 flex justify-between items-center">
      <div>
        <p class="text-blue-800 font-bold mb-1">{{ t('billing.currentPlan') }} <span class="capitalize">{{ currentUserTier }}</span></p>
        <p class="text-sm text-blue-600">{{ t('billing.usingLimits', { tier: currentUserTier }) }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

      <div class="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm flex flex-col" :class="{ 'ring-2 ring-gray-400 bg-gray-50': currentUserTier === 'freemium' }">
        <h3 class="text-lg font-black text-gray-800 mb-1">{{ t('billing.freemium.title') || 'Freemium' }}</h3>
        <p class="text-sm text-gray-500 mb-4">{{ t('billing.freemium.desc') }}</p>
        <div class="text-3xl font-black mb-6">€0<span class="text-sm text-gray-400 font-medium">/m</span></div>
        <ul class="space-y-3 mb-8 flex-1 text-sm font-medium text-gray-600">
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.freemium.f1') }}</li>
          <li><i class="fas fa-times text-gray-300 mr-2"></i> {{ t('billing.freemium.f2') }}</li>
          <li><i class="fas fa-times text-gray-300 mr-2"></i> {{ t('billing.freemium.f3') }}</li>
          <li><i class="fas fa-times text-gray-300 mr-2"></i> {{ t('billing.freemium.f4') }}</li>
        </ul>

        <button v-if="currentUserTier === 'freemium'" disabled class="w-full py-3 rounded-xl font-bold bg-gray-200 text-gray-500 cursor-not-allowed">
          {{ t('billing.buttons.current') }}
        </button>
        <button v-else-if="planOrder[currentUserTier] > planOrder['freemium']" @click="handleSubscribe('freemium')" class="w-full py-3 rounded-xl font-bold bg-gray-100 text-gray-600 hover:bg-gray-200 transition">
          {{ t('billing.buttons.downgrade', { tier: 'Freemium' }) }}
        </button>
      </div>

      <div class="bg-white rounded-2xl border-2 p-6 shadow-md relative flex flex-col transform md:-translate-y-2" :class="currentUserTier === 'starter' ? 'border-blue-500 bg-blue-50/30' : 'border-blue-400'">
        <div class="absolute top-0 right-1/2 translate-x-1/2 -translate-y-1/2 bg-blue-500 text-white px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider">
          {{ t('billing.starter.badge') || 'Most Popular' }}
        </div>
        <h3 class="text-lg font-black text-gray-800 mb-1">{{ t('billing.starter.title') || 'Starter' }}</h3>
        <p class="text-sm text-gray-500 mb-4">{{ t('billing.starter.desc') }}</p>
        <div class="text-3xl font-black mb-6">€15<span class="text-sm text-gray-400 font-medium">/m</span></div>
        <ul class="space-y-3 mb-8 flex-1 text-sm font-medium text-gray-600">
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.starter.f1') }}</li>
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.starter.f2') }}</li>
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.starter.f3') }}</li>
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.starter.f4') }}</li>
          <li><i class="fas fa-times text-gray-300 mr-2"></i> {{ t('billing.starter.f5') }}</li>
        </ul>

        <button v-if="currentUserTier === 'starter'" disabled class="w-full py-3 rounded-xl font-bold bg-blue-200 text-blue-600 cursor-not-allowed">
          {{ t('billing.buttons.current') }}
        </button>
        <button v-else-if="planOrder[currentUserTier] > planOrder['starter']" @click="handleSubscribe('starter')" class="w-full py-3 rounded-xl font-bold bg-gray-100 text-gray-600 hover:bg-gray-200 transition">
          {{ t('billing.buttons.downgrade', { tier: 'Starter' }) }}
        </button>
        <button v-else @click="handleSubscribe('starter')" class="w-full py-3 rounded-xl font-bold bg-blue-600 text-white hover:bg-blue-700 transition">
          {{ t('billing.buttons.upgrade', { tier: 'Starter' }) }}
        </button>
      </div>

      <div class="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm flex flex-col" :class="{ 'ring-2 ring-gray-200 bg-gray-50': currentUserTier === 'pro' }">
        <h3 class="text-lg font-black text-gray-800 mb-1">{{ t('billing.pro.title') || 'Pro' }}</h3>
        <p class="text-sm text-gray-500 mb-4">{{ t('billing.pro.desc') }}</p>
        <div class="text-3xl font-black mb-6">€25<span class="text-sm text-gray-400 font-medium">/m</span></div>
        <ul class="space-y-3 mb-8 flex-1 text-sm font-medium text-gray-600">
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.pro.f1') }}</li>
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.pro.f2') }}</li>
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.pro.f3') }}</li>
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.pro.f4') }}</li>
          <li><i class="fas fa-check text-green-500 mr-2"></i> {{ t('billing.pro.f5') }}</li>
        </ul>

        <button v-if="currentUserTier === 'pro'" disabled class="w-full py-3 rounded-xl font-bold bg-gray-300 text-gray-600 cursor-not-allowed">
          {{ t('billing.buttons.current') }}
        </button>
        <button v-else @click="handleSubscribe('pro')" class="w-full py-3 rounded-xl font-bold bg-gray-900 text-white hover:bg-black transition">
          {{ t('billing.buttons.upgrade', { tier: 'Pro' }) }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useSubscription } from '../composables/useSubscription';
import { useModal } from '../composables/useModal';
import { PLAN_LIMITS } from '../config/plans';
import { useRoute } from 'vue-router';
import api from '../api/client';

const route = useRoute();

const { currentUserTier, currentUserStats } = useSubscription();
const { showAlert, showConfirm } = useModal();

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

onMounted(async () => {
  await loadTranslations(currentLang.value);

  const targetPlan = route.query.plan;
  if (targetPlan && (targetPlan === 'starter' || targetPlan === 'pro')) {
    setTimeout(() => {
      handleSubscribe(targetPlan);
    }, 800);
  }
});

const planOrder = {
  freemium: 0,
  starter: 1,
  pro: 2
};

const handleSubscribe = async (targetPlan) => {
  const currentLevel = planOrder[currentUserTier.value];
  const targetLevel = planOrder[targetPlan];
  const tTier = targetPlan.toUpperCase();

  if (targetLevel < currentLevel) {
    const targetLimits = PLAN_LIMITS[targetPlan];
    const activeSites = currentUserStats.value.active_project_count || 0;

    if (activeSites > targetLimits.max_sites) {
      await showAlert(
          t('common.alerts.warning'),
          t('billing.alerts.cannotDowngradeMsg', {
            sites: activeSites,
            tier: tTier,
            limit: targetLimits.max_sites
          }),
          'warning'
      );
      return;
    }

    const isConfirmed = await showConfirm(
        t('common.alerts.confirm'),
        t('billing.alerts.confirmDowngradeMsg', { tier: tTier }),
        'warning'
    );

    if (!isConfirmed) return;
  }

  try {
    const res = await api.post('/stripe/create-checkout-session', { plan: targetPlan });

    if (res.data.url) {
      window.location.href = res.data.url;
    } else {
      throw new Error("No URL returned from server");
    }
  } catch (e) {
    console.error("Stripe Checkout Error:", e);
    showAlert(
        t('common.alerts.error'),
        t('common.alerts.actionFailed'),
        'error'
    );
  }
};
</script>