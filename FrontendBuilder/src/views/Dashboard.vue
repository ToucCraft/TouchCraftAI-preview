<template>
  <div v-if="isI18nLoaded" class="p-5 md:p-10 relative min-h-full flex flex-col">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ t('dashboard.title') }}</h1>

    <div v-if="loading" class="flex-1 flex justify-center items-center p-20">
      <div class="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 h-12 w-12"></div>
    </div>

    <div v-else-if="projects.length === 0" class="flex-1 flex flex-col items-center justify-center py-20 px-4 text-center text-gray-400 bg-white rounded-3xl border border-dashed border-gray-300">
      <i class="fas fa-globe text-6xl mb-4 opacity-50 text-blue-300"></i>
      <p class="text-xl font-bold text-gray-600">{{ t('dashboard.empty.title') }}</p>
      <p class="text-sm text-gray-400 mt-2 mb-6">{{ t('dashboard.empty.desc') }}</p>
      <router-link to="/create" class="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-blue-700 transition shadow-md hover:shadow-lg">
        {{ t('dashboard.empty.btn') }}
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="site in projects" :key="site.id" @click.stop
           class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden flex flex-col hover:shadow-md transition group">

        <div class="h-32 bg-slate-800 flex items-center justify-center relative overflow-hidden">
          <img v-if="site.thumbnail" :src="site.thumbnail" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" alt="Site Hero">
          <div v-else class="flex flex-col items-center justify-center text-slate-700">
            <i class="fas fa-window-maximize text-4xl"></i>
          </div>
          <div class="absolute bottom-2 right-2 flex gap-1 z-10">
            <span :class="site.status === 'active' ? 'bg-green-500' : (site.status === 'stopped' ? 'bg-gray-500' : 'bg-yellow-500')" class="w-3 h-3 rounded-full border-2 border-white shadow-sm"></span>
          </div>
          <div v-if="site.thumbnail" class="absolute inset-0 bg-black/10 group-hover:bg-black/0 transition-colors"></div>
        </div>

        <div class="p-6 relative">
          <div class="absolute top-4 right-4 z-10">
            <button @click.stop="toggleMenu(site.id)" class="text-gray-400 hover:text-gray-600 p-2 rounded-full hover:bg-gray-100 transition">
              <i class="fas fa-ellipsis-v"></i>
            </button>
            <div v-if="activeMenuId === site.id" class="absolute right-0 mt-2 w-48 bg-white border border-gray-100 rounded-xl shadow-xl z-20 py-2 overflow-hidden transform origin-top-right">
              <button @click="viewLogs(site.id)" class="w-full text-left px-4 py-2 text-xs text-gray-600 hover:bg-slate-50 flex items-center transition">
                <i class="fas fa-terminal w-5 text-blue-500"></i> {{ t('dashboard.menu.logs') }}
              </button>
              <button v-if="site.status === 'active'" @click="confirmStop(site.id)" class="w-full text-left px-4 py-2 text-xs text-yellow-600 hover:bg-yellow-50 flex items-center transition">
                <i class="fas fa-pause w-5"></i> {{ t('dashboard.menu.stop') }}
              </button>

              <button v-if="site.status === 'stopped'" @click="confirmStart(site.id)" class="w-full text-left px-4 py-2 text-xs text-green-600 hover:bg-green-50 flex items-center transition">
                <i class="fas fa-play w-5"></i> {{ t('dashboard.menu.start') }}
              </button>
              <div class="border-t border-gray-50 my-1"></div>
              <button @click="confirmDelete(site.id)" class="w-full text-left px-4 py-2 text-xs text-red-500 hover:bg-red-50 flex items-center transition font-bold">
                <i class="fas fa-trash-alt w-5"></i> {{ t('dashboard.menu.delete') }}
              </button>
            </div>
          </div>

          <h3 class="font-bold text-lg text-gray-800 truncate mb-1 pr-8">{{ site.name }}</h3>
          <p class="text-xs text-gray-400 mb-4 italic">{{ site.id }}</p>

          <div class="grid grid-cols-2 gap-2">
            <a v-if="site.url && site.status === 'active'" :href="site.url" target="_blank" class="bg-blue-50 text-blue-600 py-2 rounded flex items-center justify-center text-xs font-bold hover:bg-blue-100 transition border border-blue-100">
              <i class="fas fa-external-link-alt mr-1"></i> {{ t('dashboard.card.visit') }}
            </a>
            <button v-else-if="site.status !== 'active'" @click="quickDeploy(site.id)" class="bg-yellow-50 text-yellow-600 py-2 rounded text-center text-xs font-bold hover:bg-yellow-100 transition border border-yellow-200">
              <i class="fas fa-rocket mr-1"></i> {{ t('dashboard.card.deploy') }}
            </button>

            <button @click="loadProject(site.id)" class="hidden md:block bg-gray-900 text-white py-2 rounded text-center text-xs font-bold hover:bg-black transition">
              <i class="fas fa-edit mr-1"></i> {{ t('dashboard.card.edit') }}
            </button>

            <button disabled class="md:hidden bg-gray-200 text-gray-400 py-2 rounded text-center text-xs font-bold cursor-not-allowed" :title="t('dashboard.card.editMobileTitle')">
              <i class="fas fa-desktop mr-1"></i> {{ t('dashboard.card.editMobile') }}
            </button>
          </div>

          <div class="flex justify-between mt-4">
            <span class="text-[10px] text-gray-400 uppercase font-bold" :class="site.status === 'active' ? 'text-green-600' : (site.status === 'stopped' ? 'text-gray-500' : '')">{{ site.status }}</span>            <span class="text-[10px] text-gray-400">{{ site.created_at }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showLogs" class="fixed inset-0 bg-slate-900/90 flex items-center justify-center z-50 backdrop-blur-md">
      <div class="bg-black w-3/4 h-3/4 rounded-3xl p-8 flex flex-col shadow-2xl border border-slate-800">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-blue-400 font-mono text-xs uppercase font-black tracking-widest">{{ t('dashboard.modal.logsTitle') }}</h3>
          <button @click="showLogs = false" class="text-slate-500 hover:text-white transition"><i class="fas fa-times text-2xl"></i></button>
        </div>
        <pre class="flex-1 bg-slate-950 p-6 rounded-2xl text-green-500 font-mono text-[9px] overflow-auto whitespace-pre-wrap border border-slate-900 shadow-inner">{{ logs }}</pre>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/client';
import { useModal } from '../composables/useModal';

import { useSubscription } from '../composables/useSubscription';
const { checkLimit, triggerUpgrade } = useSubscription();

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
const projects = ref([]);
const loading = ref(true);
const activeMenuId = ref(null);

const showLogs = ref(false);
const logs = ref('');

const fetchProjects = async () => {
  loading.value = true;
  try {
    const res = await api.get('/list');
    projects.value = res.data;
  } catch(e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

const toggleMenu = (id) => {
  activeMenuId.value = activeMenuId.value === id ? null : id;
};

const closeMenu = () => activeMenuId.value = null;

const loadProject = (id) => {
  router.push(`/edit/${id}`);
};

const viewLogs = async (id) => {
  logs.value = t('dashboard.alerts.connectingLogs') || "Connecting...";
  showLogs.value = true;
  activeMenuId.value = null;
  try {
    const res = await api.get(`/${id}/logs`);
    logs.value = res.data.logs;
  } catch(e) {
    logs.value = t('dashboard.alerts.logsUnavailable') || "Logs unavailable";
  }
};

const confirmDelete = async (id) => {
  const isConfirmed = await showConfirm(
      t('common.alerts.confirm'),
      t('dashboard.alerts.confirmDelete'),
      'warning'
  );

  if (!isConfirmed) return;

  try {
    await api.delete(`/${id}`);
    projects.value = projects.value.filter(p => p.id !== id);

    showAlert(
        t('common.alerts.success'),
        t('common.alerts.deleteSuccess'),
        'success'
    );
  } catch (e) {
    showAlert(
        t('common.alerts.error'),
        t('common.alerts.actionFailed'),
        'error'
    );
  }
};

const quickDeploy = async (id) => {
  if (!checkLimit('max_sites')) {
    triggerUpgrade(t('upgrade.maxActiveSites'), 'starter');
    return;
  }

  // 2. Если всё ок, спрашиваем подтверждение
  const isConfirmed = await showConfirm(
      t('common.alerts.info'),
      t('dashboard.alerts.confirmDeploy'),
      'info'
  );

  if (!isConfirmed) return;

  const project = projects.value.find(p => p.id === id);
  if (project) project.status = 'building';

  try {
    await api.post(`/${id}/deploy`);
    fetchProjects();

    showAlert(
        t('common.alerts.success'),
        t('common.alerts.deploySuccess'),
        'success'
    );
  } catch (e) {
    if (e.response && e.response.status === 403) {
      triggerUpgrade(t('upgrade.maxActiveSites') || "Limit reached. Stop a site or upgrade.", 'starter');
    } else {
      showAlert(
          t('common.alerts.error'),
          t('common.alerts.actionFailed'),
          'error'
      );
    }
    fetchProjects();
  }
};

const confirmStop = async (id) => {
  const isConfirmed = await showConfirm(
      t('common.alerts.confirm'),
      t('dashboard.alerts.confirmStop'),
      'warning'
  );

  if (!isConfirmed) return;
  closeMenu();

  try {
    await api.post(`/${id}/stop`);
    const project = projects.value.find(p => p.id === id);
    if (project) project.status = 'stopped';

    showAlert(
        t('common.alerts.success'),
        t('dashboard.alerts.stopSuccess'),
        'success'
    );
  } catch (e) {
    showAlert(t('common.alerts.error'), t('common.alerts.actionFailed'), 'error');
  }
};

const confirmStart = async (id) => {
  closeMenu();

  if (!checkLimit('max_sites')) {
    triggerUpgrade(t('upgrade.maxActiveSites'), 'starter');
    return;
  }

  const isConfirmed = await showConfirm(
      t('common.alerts.info'),
      t('dashboard.alerts.confirmStart'),
      'info'
  );

  if (!isConfirmed) return;

  try {
    await api.post(`/${id}/start`);
    const project = projects.value.find(p => p.id === id);
    if (project) project.status = 'active';

    showAlert(
        t('common.alerts.success'),
        t('dashboard.alerts.startSuccess'),
        'success'
    );
  } catch (e) {
    if (e.response && e.response.status === 403) {
      triggerUpgrade(t('upgrade.maxActiveSites') || "Limit reached. Stop a site or upgrade.", 'starter');
    } else {
      showAlert(t('common.alerts.error'), t('common.alerts.actionFailed'), 'error');
    }
  }
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  fetchProjects();
  document.addEventListener('click', closeMenu);
});

onUnmounted(() => {
  document.removeEventListener('click', closeMenu);
});
</script>