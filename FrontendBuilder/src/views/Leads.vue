<template>
  <div v-if="isI18nLoaded" class="p-5 md:p-10 w-full flex flex-col h-full">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-top mb-8 gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ t('leads.title') }}</h1>
        <p class="text-gray-500">{{ t('leads.subtitle') }}</p>
      </div>

      <div v-if="projects.length > 0" class="w-full md:w-72 mt-4">
        <label class="block text-xs font-bold text-gray-500 uppercase mb-2 ml-1">{{ t('leads.chooseWebsite') }}</label>
        <div class="relative">
          <select v-model="selectedProjectId" @change="fetchLeads" class="w-full p-3 bg-white border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 appearance-none font-medium text-gray-800 shadow-sm cursor-pointer">
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name || t('leads.withoutName') }}
            </option>
          </select>
          <i class="fas fa-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"></i>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="flex-1 flex flex-col items-center justify-center text-gray-400">
      <i class="fas fa-circle-notch fa-spin text-4xl mb-4 text-blue-500"></i>
      <p class="text-sm font-bold uppercase tracking-widest">{{ t('leads.loading') }}</p>
    </div>

    <div v-else-if="projects.length === 0" class="flex-1 flex flex-col items-center justify-center text-gray-400 bg-white rounded-3xl border border-dashed border-gray-300">
      <i class="fas fa-folder-open text-6xl mb-4 opacity-50"></i>
      <p class="text-lg font-bold text-gray-600">{{ t('leads.empty.title') }}</p>
      <router-link to="/create" class="mt-4 bg-blue-600 text-white px-6 py-2 rounded-xl font-bold hover:bg-blue-700 transition">{{ t('leads.empty.btn') }}</router-link>
    </div>

    <div v-else class="flex-1">
      <div v-if="leads.length === 0" class="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-300">
        <i class="fas fa-inbox text-5xl mb-4 text-gray-300"></i>
        <p class="text-gray-500 font-medium">{{ t('leads.noLeads') }}</p>
      </div>

      <div v-else class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
            <tr class="bg-gray-50 border-b border-gray-200">
              <th class="py-4 px-6 text-xs font-bold text-gray-500 uppercase tracking-wider">
                {{ t('leads.table.date') }}
              </th>
              <th v-for="header in tableHeaders" :key="header" class="py-4 px-6 text-xs font-bold text-gray-500 uppercase tracking-wider">
                {{ getFieldTranslation(header) }}
              </th>
              <th class="py-4 px-6 text-xs font-bold text-gray-500 uppercase tracking-wider">
                {{ t('leads.table.status') }}
              </th>
            </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
            <tr v-for="lead in leads" :key="lead.id" class="hover:bg-gray-50 transition-colors">
              <td class="py-4 px-6 text-sm text-gray-600 whitespace-nowrap">
                {{ formatDate(lead.created_at) }}
              </td>

              <td v-for="header in tableHeaders" :key="header" class="py-4 px-6 text-sm text-gray-800">
                <div class="truncate max-w-xs" :title="lead.form_data[header]">
                  {{ lead.form_data[header] || '—' }}
                </div>
              </td>

              <td class="py-4 px-6 whitespace-nowrap">
                <span class="bg-blue-50 text-blue-600 text-[10px] font-bold px-2 py-1 rounded uppercase">{{ t('leads.table.new') }}</span>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
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

// Функция для перевода динамических полей формы
const getFieldTranslation = (key) => {
  if (!key) return '';
  const translationKey = `leads.fields.${key}`;
  const translated = t(translationKey);

  // Если перевод найден (он не равен самому ключу 'leads.fields.x'), возвращаем его
  if (translated !== translationKey) {
    return translated;
  }
  // Фолбэк для неизвестных полей: заменяем подчеркивания на пробелы
  return key.replace(/_/g, ' ');
};
// ------------------

const projects = ref([]);
const selectedProjectId = ref('');
const leads = ref([]);
const isLoading = ref(true);

const tableHeaders = computed(() => {
  if (!leads.value || leads.value.length === 0) return [];
  const keys = new Set();
  leads.value.forEach(lead => {
    if (lead.form_data) {
      Object.keys(lead.form_data).forEach(key => keys.add(key));
    }
  });
  return Array.from(keys);
});

const loadData = async () => {
  try {
    isLoading.value = true;
    const res = await api.get('/list');

    const fetchedProjects = res.data.projects || res.data || [];
    projects.value = Array.isArray(fetchedProjects) ? fetchedProjects : [];

    if (projects.value.length > 0) {
      selectedProjectId.value = projects.value[0].id;
      await fetchLeads();
    } else {
      isLoading.value = false;
    }
  } catch (error) {
    console.error(t('leads.alerts.errorProjects'), error);
    isLoading.value = false;
  }
};

const fetchLeads = async () => {
  if (!selectedProjectId.value) return;
  isLoading.value = true;
  leads.value = [];
  try {
    const res = await api.get(`/${selectedProjectId.value}/leads`);
    leads.value = res.data.leads || [];
  } catch (error) {
    console.error(t('leads.alerts.errorLeads'), error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  loadData();
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString(currentLang.value === 'ru' ? 'ru-RU' : 'en-US', {
    month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit'
  });
};
</script>