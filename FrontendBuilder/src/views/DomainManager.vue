<template>
  <div v-if="isI18nLoaded" class="p-5 md:p-10">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ t('domainManager.title') }}</h1>

    <div class="mb-8 bg-blue-50 border border-blue-100 rounded-2xl p-4 md:p-6 flex flex-col md:flex-row items-start md:items-center gap-4 shadow-sm">
      <div class="w-12 h-12 bg-blue-500 text-white rounded-xl flex items-center justify-center shrink-0 shadow-blue-200 shadow-lg">
        <i class="fas fa-network-wired text-xl"></i>
      </div>

      <div class="flex-1">
        <h3 class="text-blue-900 font-bold text-sm uppercase tracking-wider mb-1">
          {{ t('domainManager.dns.title') }}
        </h3>
        <p class="text-blue-700 text-xs md:text-sm leading-relaxed">
          {{ t('domainManager.dns.instruction') }}
        </p>
      </div>

      <div class="w-full md:w-auto flex items-center bg-white border border-blue-200 rounded-xl p-2 pl-4 gap-3">
        <div class="flex flex-col text-left">
          <span class="text-[10px] uppercase font-bold text-gray-400">Type A / Value</span>
          <span class="text-sm font-mono font-bold text-slate-800">217.160.204.89</span>
        </div>
        <button
            @click="copyIp"
            class="ml-auto w-10 h-10 rounded-lg transition-all flex items-center justify-center cursor-pointer"
            :class="isCopied ? 'bg-green-100 text-green-600' : 'bg-blue-50 hover:bg-blue-100 text-blue-600'"
        >
          <i class="fas" :class="isCopied ? 'fa-check' : 'fa-copy'"></i>
        </button>
      </div>
    </div>
    <div v-if="loading" class="flex justify-center p-20">
      <div class="loader ease-linear rounded-full border-4 border-t-4 border-gray-400 h-12 w-12"></div>
    </div>

    <div v-else-if="projects.length === 0" class="bg-white rounded-xl shadow-sm border border-gray-200 py-20 flex flex-col items-center justify-center text-gray-400">
      <i class="fas fa-globe text-5xl mb-4 opacity-50"></i>
      <p class="text-lg font-bold text-gray-600">{{ t('domainManager.empty') }}</p>
    </div>

    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse min-w-[600px]">
        <thead>
        <tr class="bg-gray-50 border-b border-gray-200 text-xs uppercase text-gray-500 tracking-wider">
          <th class="p-4 font-bold">{{ t('domainManager.table.projectName') }}</th>
          <th class="p-4 font-bold">{{ t('domainManager.table.currentDomain') }}</th>
          <th class="p-4 font-bold">{{ t('domainManager.table.status') }}</th>
          <th class="p-4 font-bold">{{ t('domainManager.table.attachCustom') }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="site in projects" :key="site.id" class="border-b border-gray-100 hover:bg-slate-50">
          <td class="p-4 font-bold text-gray-800">{{ site.name || t('domainManager.table.withoutName') }}</td>
          <td class="p-4">
            <a v-if="site.url" :href="site.url" target="_blank" class="text-blue-600 hover:underline text-sm font-medium">
              {{ site.url }} <i class="fas fa-external-link-alt ml-1 text-[10px]"></i>
            </a>
            <span v-else class="text-gray-400 italic text-sm">{{ t('domainManager.table.notDeployed') }}</span>
          </td>
          <td class="p-4">
               <span :class="site.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'" class="px-2 py-1 rounded text-[10px] font-bold uppercase">
                 {{ getStatusText(site.status) }}
               </span>
          </td>

          <td class="p-4">
            <div v-if="site.status === 'active'" class="flex gap-2 max-w-xs">
              <input v-model="domainInput[site.id]" :placeholder="t('domainManager.table.placeholder')" class="flex-1 p-2 border rounded-lg text-xs outline-none focus:ring-1 focus:ring-blue-500">
              <button @click="setupDomain(site)" :disabled="isProcessingDomain[site.id]" class="bg-slate-800 text-white px-3 py-2 rounded-lg text-xs font-bold hover:bg-black disabled:opacity-50 transition shadow-sm">
                {{ isProcessingDomain[site.id] ? t('domainManager.buttons.wait') : t('domainManager.buttons.set') }}
              </button>
            </div>
            <span v-else class="text-xs text-gray-400">{{ t('domainManager.table.deployFirst') }}</span>
          </td>
        </tr>
        </tbody>
      </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/client';
import { useSubscription } from '../composables/useSubscription';
import { useModal } from '../composables/useModal';

const { checkLimit, triggerUpgrade, updateUserData } = useSubscription();
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

const getStatusText = (status) => {
  if (!status) return '';
  const key = `domainManager.status.${status.toLowerCase()}`;
  const translation = t(key);
  return translation === key ? status : translation;
};
// ------------------

const isCopied = ref(false);

const copyIp = () => {
  const ip = "217.160.204.89";
  navigator.clipboard.writeText(ip).then(() => {
    isCopied.value = true;
    // Возвращаем иконку копирования через 2 секунды
    setTimeout(() => {
      isCopied.value = false;
    }, 2000);
  });
};

const projects = ref([]);
const loading = ref(false);

const domainInput = ref({});
const isProcessingDomain = ref({});
const userProfile = ref(null);

const fetchData = async () => {
  loading.value = true;
  try {
    const userRes = await api.get('/user/me');
    userProfile.value = userRes.data;
    updateUserData(userRes.data);

    const res = await api.get('/list');
    projects.value = res.data;
  } catch(e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

const setupDomain = async (project) => {
  if (!checkLimit('custom_domains')) {
    return triggerUpgrade(t('domainManager.upgrade.customDomains') || "Custom Domains are only available on the Starter plan.", 'starter');
  }

  const domain = domainInput.value[project.id];
  if(!domain) return showAlert('Warning', t('domainManager.alerts.enterDomain') || "Please enter a domain", 'warning');

  isProcessingDomain.value[project.id] = true;
  try {
    const res = await api.post(`/${project.id}/setup-domain?domain=${domain}`);
    project.url = res.data.url;
    showAlert('Success', t('domainManager.alerts.success') || "Domain updated successfully!", 'success');
  } catch(e) {
    showAlert('Error', t('domainManager.alerts.error') || "Failed to setup domain.", 'error');
  } finally {
    isProcessingDomain.value[project.id] = false;
  }
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  fetchData();
});
</script>