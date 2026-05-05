<template>
  <div v-if="isI18nLoaded" class="p-5 md:p-10 w-full flex flex-col h-full">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-top mb-8 gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ t('seo.title') }}</h1>
        <p class="text-gray-500">{{ t('seo.subtitle') }}</p>
      </div>

      <div v-if="projects.length > 0" class="w-full md:w-72 mt-4">
        <label class="block text-xs font-bold text-gray-500 uppercase mb-2 ml-1">{{ t('seo.chooseWebsite') }}</label>
        <div class="relative">
          <select v-model="selectedProjectId" @change="loadProjectData" class="w-full p-3 bg-white border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 appearance-none font-medium text-gray-800 shadow-sm cursor-pointer">
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name || t('seo.unnamedProject') }}
            </option>
          </select>
          <i class="fas fa-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="flex-1 flex flex-col items-center justify-center text-gray-400">
      <i class="fas fa-circle-notch fa-spin text-4xl mb-4 text-blue-500"></i>
    </div>

    <div v-else-if="projects.length === 0" class="flex-1 flex flex-col items-center justify-center text-gray-400 bg-white rounded-3xl border border-dashed border-gray-300">
      <i class="fas fa-folder-open text-6xl mb-4 opacity-50"></i>
      <p class="text-lg font-bold text-gray-600">{{ t('seo.noProjects') }}</p>
    </div>

    <div v-else-if="projectConfig" class="flex-1 space-y-6">
      <div class="flex justify-between items-center bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
        <div class="flex items-center gap-4">
          <span class="font-bold text-gray-700"><i class="fas fa-language text-blue-500 mr-2"></i> {{ t('seo.editingLanguage') }}</span>
          <select v-model="editingLang" class="p-1 border rounded text-xs outline-none bg-slate-50 uppercase font-bold cursor-pointer">
            <option v-for="lang in availableLanguages" :key="lang" :value="lang">{{ lang }}</option>
          </select>
        </div>

        <div class="flex items-center gap-3">
          <button @click="generateAISeo" :disabled="isGenerating || isSaving" class="bg-gradient-to-r from-purple-600 to-blue-500 text-white px-4 py-2 rounded-lg font-bold text-sm hover:opacity-90 transition disabled:opacity-50 flex items-center shadow-md">
            <i class="fas mr-2" :class="isGenerating ? 'fa-spinner fa-spin' : 'fa-magic'"></i>
            {{ isGenerating ? t('seo.generating') : t('seo.autoGenerate') }}
          </button>

          <button @click="saveSEO" :disabled="isGenerating || isSaving" class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-bold text-sm hover:bg-gray-200 transition disabled:opacity-50 flex items-center">
            <i class="fas mr-2" :class="isSaving ? 'fa-spinner fa-spin' : 'fa-save'"></i>
            {{ isSaving ? t('seo.deploying') : t('seo.saveDeploy') }}
          </button>
        </div>
      </div>

      <div class="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm space-y-6">
        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">{{ t('seo.metaTitle') }} ({{ editingLang }})</label>
          <input v-model="seo.title[editingLang]" placeholder="e.g. TouchCraft - Best AI Website Builder" class="w-full p-3 border border-slate-200 rounded-xl bg-white outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 font-medium text-gray-800 transition">
          <p class="text-xs text-gray-400 mt-1">{{ t('seo.titleRec') }}</p>
        </div>

        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">{{ t('seo.metaDesc') }} ({{ editingLang }})</label>
          <textarea v-model="seo.description[editingLang]" rows="3" placeholder="Write a short summary of the page..." class="w-full p-3 border border-slate-200 rounded-xl bg-white outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 font-medium text-gray-800 transition"></textarea>
          <p class="text-xs text-gray-400 mt-1">{{ t('seo.descRec') }}</p>
        </div>

        <div>
          <label class="block text-sm font-bold text-gray-700 mb-2">{{ t('seo.keywords') }} ({{ editingLang }})</label>
          <input v-model="seo.keywords[editingLang]" placeholder="e.g. ai builder, create website, touchcraft" class="w-full p-3 border border-slate-200 rounded-xl bg-white outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 font-medium text-gray-800 transition">
          <p class="text-xs text-gray-400 mt-1">{{ t('seo.keywordsRec') }}</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
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
// ------------------

const projects = ref([]);
const selectedProjectId = ref('');
const projectConfig = ref(null);
const isLoading = ref(true);
const isSaving = ref(false);
const isGenerating = ref(false);
const editingLang = ref('en');

const seo = ref({
  title: {},
  description: {},
  keywords: {}
});

const availableLanguages = computed(() => {
  if (projectConfig.value && projectConfig.value.translations) {
    return Object.keys(projectConfig.value.translations);
  }
  return ['en'];
});

watch(availableLanguages, (langs) => {
  if (langs.length > 0 && !langs.includes(editingLang.value)) {
    editingLang.value = langs[0];
  }
}, { immediate: true });

const loadProjects = async () => {
  try {
    isLoading.value = true;
    const res = await api.get('/list');
    projects.value = res.data || [];
    if (projects.value.length > 0) {
      selectedProjectId.value = projects.value[0].id;
      await loadProjectData();
    } else {
      isLoading.value = false;
    }
  } catch (error) {
    isLoading.value = false;
  }
};

const loadProjectData = async () => {
  if (!selectedProjectId.value) return;
  isLoading.value = true;
  try {
    const res = await api.get(`/${selectedProjectId.value}`);
    projectConfig.value = res.data.site_config || res.data.config || {};

    if (projectConfig.value.seo) {
      seo.value = projectConfig.value.seo;
    } else {
      seo.value = { title: {}, description: {}, keywords: {} };
      // Предзаполняем тайтл названием бизнеса
      availableLanguages.value.forEach(l => {
        seo.value.title[l] = projectConfig.value.business_name || '';
      });
    }
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

const generateAISeo = async () => {
  if (!checkLimit('ai_generations')) {
    return triggerUpgrade(t('seo.upgrade.aiGenerations') || "AI SEO generation requires the Starter plan.", 'starter');
  }

  if (!selectedProjectId.value) return;
  isGenerating.value = true;
  try {
    const res = await api.post(`/${selectedProjectId.value}/generate-seo`);
    seo.value = res.data.seo;
    projectConfig.value.seo = res.data.seo;
  } catch (error) {
    console.error("AI Generation failed:", error);
    showAlert('Error', t('seo.alerts.genFail') || 'Failed to generate SEO', 'error');
  } finally {
    isGenerating.value = false;
  }
};

const saveSEO = async () => {
  if (!selectedProjectId.value) return;
  isSaving.value = true;
  projectConfig.value.seo = seo.value;

  try {
    await api.patch(`/${selectedProjectId.value}`, { site_config: projectConfig.value });
    await api.post(`/${selectedProjectId.value}/deploy`);
    showAlert('Success', t('seo.alerts.saveSuccess') || 'Saved successfully!', 'success');
  } catch (e) {
    console.error(e);
    showAlert('Error', t('seo.alerts.saveError') || 'Error saving SEO', 'error');
  } finally {
    isSaving.value = false;
  }
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  try {
    const userRes = await api.get('/user/me');
    updateUserData(userRes.data);
  } catch (e) {
    console.error("Failed to load user profile for SEO Manager", e);
  }
  loadProjects();
});
</script>