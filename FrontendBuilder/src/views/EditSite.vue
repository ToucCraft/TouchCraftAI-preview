<template>
  <div v-if="isI18nLoaded" class="flex h-full bg-slate-100 text-left overflow-x-hidden">

    <EditorSidebar
        v-model:isOpen="isSidebarOpen"
        :isProcessing="isProcessing"
        @save="saveConfig"
        @deploy="deploySite"
    />

    <EditorPreview
        v-model:isOpen="isSidebarOpen"
    />

  </div>
</template>

<script setup>
import { ref, provide, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api/client';
import { useSubscription } from '../composables/useSubscription';
import { useModal } from '../composables/useModal';

// Импорт наших новых компонентов (пути могут немного отличаться в зависимости от вашей структуры папок)
import EditorSidebar from '../components/editor/EditorSidebar.vue';
import EditorPreview from '../components/editor/EditorPreview.vue';
const route = useRoute();
const router = useRouter();
const { checkLimit, triggerUpgrade, updateUserData } = useSubscription();
const { showAlert, showConfirm } = useModal();

// --- Глобальное состояние приложения ---
const isSidebarOpen = ref(true);
const projectId = ref(route.params.id);
const isProcessing = ref(false);
const isInitialLoading = ref(true);
const userProfile = ref(null);
const deployedUrl = ref('');

// Главный объект конфигурации сайта
const config = ref({
  palette: { primary: '#3B82F6', secondary: '#10B981', background: '#FFFFFF', text: '#1F2937' },
  font: 'Inter',
  blocks: [],
  analytics_id: '',
  cookie_banner: false,
  favicon: '',
  logo_url: '',
  logo_mode: 'text',
  business_name: '',
  contact: {
    legal_name: '', address: '', tax_id: '', email: '', phone: '',
    socials: { instagram: '', 'x-twitter': '', youtube: '', tiktok: '', telegram: '', whatsapp: '' }
  }
});

// --- I18N (Мультиязычность) ---
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
    } else return key;
  }
  return value;
};

// --- Вычисляемые свойства ---
const isSmtpConfigured = computed(() => {
  const smtp = userProfile.value?.smtp_config;
  return !!(smtp && smtp.host && smtp.username && smtp.password);
});

// ==========================================
// ПРОВАЙДЕРЫ (Раздаем данные всем компонентам)
// ==========================================
provide('siteConfig', config);
provide('t', t);
provide('projectId', projectId);
provide('isInitialLoading', isInitialLoading);
provide('isSmtpConfigured', isSmtpConfigured);

// --- Работа с API ---
const loadProject = async () => {
  isInitialLoading.value = true;
  try {
    const res = await api.get(`/${projectId.value}`);
    const loadedConfig = res.data.site_config || res.data.config || {};
    loadedConfig.id = res.data.id;

    if (loadedConfig.blocks) {
      loadedConfig.blocks.forEach(b => {
        if (b.type === 'HeroBlock' && b.props.cta_url === undefined) {
          b.props.cta_url = '#contacts';
        }
      });
    }

    config.value = {
      ...config.value,
      ...loadedConfig,
      contact: { ...config.value.contact, ...(loadedConfig.contact || {}) }
    };
    if (!config.value.contact.socials) config.value.contact.socials = {};
    deployedUrl.value = res.data.preview_url || res.data.url;
  } catch (e) {
    showAlert('Error', t('editSite.alerts.errorLoad') || 'Failed to load project', 'error');
    router.push('/dashboard');
  } finally {
    isInitialLoading.value = false;
  }
};

const saveConfig = async () => {
  try {
    await api.patch(`/${projectId.value}`, { site_config: config.value });
  } catch (e) {
    console.error("Save error", e);
  }
};

const deploySite = async () => {
  if (!checkLimit('max_sites')) {
    return triggerUpgrade(t('upgrade.maxActiveSites') || "You have reached the limit of active sites.", 'starter');
  }

  const isConfirmed = await showConfirm(
      t('editSite.publish.confirmTitle') || 'Ready to publish?',
      t('editSite.publish.confirmDesc') || 'This will build and update your live website.',
      'info'
  );
  if (!isConfirmed) return;

  isProcessing.value = true;
  await saveConfig();

  try {
    const res = await api.post(`/${projectId.value}/deploy`);
    deployedUrl.value = res.data.url;
    showAlert('Success', t('editSite.alerts.deploySuccess') || 'Website published!', 'success');
    router.push('/domains');
  } catch (e) {
    if (e.response && e.response.status === 403) {
      triggerUpgrade(t('upgrade.maxActiveSites') || "Limit reached.", 'starter');
    } else {
      showAlert('Error', t('editSite.alerts.deployFail') || 'Failed to deploy.', 'error');
    }
  } finally {
    isProcessing.value = false;
  }
};

// --- Инициализация ---
onMounted(async () => {
  await loadTranslations(currentLang.value);
  if (projectId.value) {
    await loadProject();
  }
  try {
    const res = await api.get('/user/me');
    userProfile.value = res.data;
    updateUserData(res.data);
  } catch (e) {
    console.error("Profile load error");
  }
});
</script>