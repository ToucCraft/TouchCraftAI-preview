<template>
  <div v-if="isI18nLoaded" class="p-5 md:p-10 w-full flex flex-col min-h-full bg-slate-50">

    <div class="mb-8 flex flex-col md:flex-row md:justify-between md:items-end gap-4">
      <div>
        <button @click="$router.push('/dashboard')" class="text-sm font-bold text-gray-500 hover:text-indigo-600 mb-4 flex items-center transition-colors">
          <i class="fas fa-arrow-left mr-2"></i> {{ t('siteDashboard.back', 'Back to Projects') }}
        </button>
        <div class="flex items-center gap-4">
          <h1 class="text-3xl font-black text-gray-900">
            {{ project?.business_name || t('siteDashboard.title', 'Site Dashboard') }}
          </h1>
          <span v-if="project?.status === 'active'" class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-[10px] font-black uppercase tracking-widest flex items-center gap-2 shadow-sm">
             <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> Active
          </span>
        </div>
        <p class="text-sm text-gray-400 mt-2 font-mono">{{ project?.id }}</p>
      </div>

      <transition name="fade">
        <button v-if="hasGA4" @click="exportReport" class="flex items-center gap-2 px-6 py-3 bg-white border border-gray-200 text-gray-700 rounded-xl text-sm font-bold hover:bg-gray-50 hover:shadow-md transition-all">
          <i class="fas fa-file-export text-indigo-500"></i> {{ t('siteDashboard.export', 'Export CSV Report') }}
        </button>
      </transition>
    </div>

    <div v-if="loading" class="flex flex-col items-center justify-center p-20 flex-1">
      <div class="loader ease-linear rounded-full border-4 border-t-4 border-indigo-500 h-12 w-12 mb-4"></div>
      <p class="text-gray-400 font-bold animate-pulse">Loading dashboard data...</p>
    </div>

    <div v-else class="grid grid-cols-1 xl:grid-cols-3 gap-8">

      <div class="xl:col-span-2 flex flex-col gap-8">

        <transition name="fade-slide">
          <div v-if="!hasGA4" class="bg-white p-8 md:p-10 rounded-[2rem] border border-orange-200 shadow-lg shadow-orange-100/50 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-64 h-64 bg-orange-50 rounded-full blur-3xl -mr-20 -mt-20 z-0"></div>
            <div class="relative z-10 flex flex-col md:flex-row items-start md:items-center gap-6">
              <div class="w-16 h-16 rounded-2xl bg-orange-100 text-orange-500 flex items-center justify-center shrink-0 shadow-inner">
                <i class="fas fa-chart-pie text-2xl"></i>
              </div>
              <div class="flex-1">
                <h3 class="text-2xl font-black text-gray-800 mb-2">{{ t('siteDashboard.ga4.missingTitle', 'Analytics not connected') }}</h3>
                <p class="text-gray-500 mb-6 max-w-lg leading-relaxed">{{ t('siteDashboard.ga4.missingDesc', 'To track visitors, bounce rates, and traffic sources, please enter your Google Analytics 4 Measurement ID (G-XXXXXXX).') }}</p>

                <div class="flex flex-col sm:flex-row gap-3 max-w-md">
                  <input v-model="analyticsId" type="text" placeholder="e.g., G-1234567890" class="flex-1 p-4 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 font-mono text-sm uppercase transition-all shadow-sm text-gray-800 font-bold placeholder:font-normal">
                  <button @click="saveGA4" class="px-8 py-4 bg-gray-900 hover:bg-black text-white rounded-xl font-bold transition-all shadow-md hover:shadow-lg whitespace-nowrap disabled:opacity-50" :disabled="!analyticsId || analyticsId.length < 5">
                    {{ t('siteDashboard.ga4.save', 'Connect GA4') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition>

        <transition name="fade-slide">
          <div v-if="hasGA4" class="bg-white p-8 md:p-10 rounded-[2rem] border border-gray-100 shadow-sm flex flex-col gap-8">

            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h3 class="text-2xl font-black text-gray-800">{{ t('siteDashboard.analytics.title', 'Traffic Overview') }}</h3>
                <p class="text-sm text-gray-400 mt-1"><i class="fas fa-check-circle text-green-500 mr-1"></i> GA4 Connected ({{ analyticsId }})</p>
              </div>

              <div class="flex bg-slate-100 p-1 rounded-xl">
                <button v-for="range in [7, 30, 90]" :key="range" @click="currentDateRange = range"
                        class="px-4 py-2 rounded-lg text-xs font-bold transition-all"
                        :class="currentDateRange === range ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'">
                  {{ range }} {{ t('siteDashboard.analytics.days', 'Days') }}
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="p-6 bg-slate-50 rounded-2xl border border-slate-100 hover:border-indigo-100 transition-colors">
                <p class="text-xs text-gray-400 font-bold uppercase tracking-wider mb-2">Total Visitors</p>
                <div class="flex items-end justify-between">
                  <p class="text-4xl font-black text-gray-800">{{ currentMetrics.visitors.toLocaleString() }}</p>
                  <span class="text-sm font-bold mb-1" :class="currentMetrics.trend > 0 ? 'text-green-500' : 'text-red-500'">
                    <i class="fas" :class="currentMetrics.trend > 0 ? 'fa-arrow-up' : 'fa-arrow-down'"></i> {{ Math.abs(currentMetrics.trend) }}%
                  </span>
                </div>
              </div>
              <div class="p-6 bg-slate-50 rounded-2xl border border-slate-100 hover:border-indigo-100 transition-colors">
                <p class="text-xs text-gray-400 font-bold uppercase tracking-wider mb-2">Page Views</p>
                <p class="text-4xl font-black text-gray-800">{{ currentMetrics.views.toLocaleString() }}</p>
              </div>
              <div class="p-6 bg-slate-50 rounded-2xl border border-slate-100 hover:border-indigo-100 transition-colors">
                <p class="text-xs text-gray-400 font-bold uppercase tracking-wider mb-2">Bounce Rate</p>
                <p class="text-4xl font-black text-gray-800">{{ currentMetrics.bounce }}%</p>
              </div>
            </div>

            <div>
              <p class="text-xs text-gray-400 font-bold uppercase tracking-wider mb-6">Traffic Trend</p>
              <div class="h-48 flex items-end justify-between gap-1 sm:gap-2 border-b border-gray-100 pb-2 relative">
                <div v-for="(bar, i) in currentChartData" :key="i" class="w-full bg-indigo-50 rounded-t-md relative group hover:bg-indigo-100 transition-all cursor-crosshair" :style="{ height: bar + '%' }">
                  <div class="absolute inset-x-0 bottom-0 bg-indigo-500 rounded-t-md transition-all duration-700 ease-out" :style="{ height: (bar * 0.8) + '%' }"></div>
                  <div class="opacity-0 group-hover:opacity-100 absolute -top-10 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-[10px] font-bold py-1.5 px-3 rounded-lg pointer-events-none transition-opacity whitespace-nowrap z-10 shadow-xl">
                    {{ Math.round((currentMetrics.views / currentChartData.length) * (bar / 50)) }} views
                  </div>
                </div>
              </div>
            </div>

          </div>
        </transition>
      </div>

      <div class="xl:col-span-1">
        <div class="bg-gradient-to-br from-indigo-600 to-violet-800 rounded-[2rem] p-8 text-white shadow-xl shadow-indigo-200/50 relative overflow-hidden flex flex-col h-full">
          <div class="absolute top-0 right-0 w-48 h-48 bg-white/10 rounded-full blur-3xl -mr-10 -mt-10 pointer-events-none"></div>
          <div class="absolute bottom-0 left-0 w-32 h-32 bg-black/10 rounded-full blur-2xl -ml-10 -mb-10 pointer-events-none"></div>

          <div class="relative z-10">
            <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-6 backdrop-blur-sm">
              <i class="fas fa-robot text-2xl text-white"></i>
            </div>
            <h3 class="text-2xl font-black mb-3">{{ t('siteDashboard.ai.title', 'AI Lead Analysis') }}</h3>
            <p class="text-indigo-100 text-sm mb-8 leading-relaxed">{{ t('siteDashboard.ai.desc', 'Let our AI scan your recent form submissions to identify audience patterns, common requests, and marketing insights.') }}</p>

            <button v-if="!aiSummary" @click="analyzeLeads" :disabled="isAnalyzing" class="w-full py-4 bg-white text-indigo-700 rounded-xl font-black shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 flex justify-center items-center gap-2">
              <i v-if="isAnalyzing" class="fas fa-circle-notch fa-spin"></i>
              <i v-else class="fas fa-magic"></i>
              {{ isAnalyzing ? t('siteDashboard.ai.analyzing', 'Analyzing data...') : t('siteDashboard.ai.analyzeBtn', 'Generate AI Report') }}
            </button>
          </div>

          <transition name="fade">
            <div v-if="aiSummary" class="mt-8 flex-1 bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-2xl relative z-10 overflow-y-auto custom-scrollbar">
              <div class="prose prose-sm prose-invert max-w-none
                          prose-headings:font-bold prose-headings:mb-2 prose-headings:mt-4 first:prose-headings:mt-0
                          prose-p:text-indigo-50 prose-p:leading-relaxed prose-p:mb-4
                          prose-ul:list-disc prose-ul:pl-4 prose-li:mb-1 prose-li:text-indigo-100"
                   v-html="aiSummary"></div>

              <button @click="analyzeLeads" :disabled="isAnalyzing" class="mt-6 text-xs font-bold text-indigo-200 hover:text-white transition-colors flex items-center gap-1">
                <i class="fas fa-sync-alt" :class="{'fa-spin': isAnalyzing}"></i> Re-analyze
              </button>
            </div>
          </transition>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api/client';
import { useModal } from '../composables/useModal';

const route = useRoute();
const router = useRouter();
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
    }
  } catch (error) {
    console.error("Error loading translations:", error);
  } finally {
    isI18nLoaded.value = true;
  }
};

const t = (key, fallback = null) => {
  const keys = key.split('.');
  let value = translations.value;
  for (const k of keys) {
    if (value && Object.prototype.hasOwnProperty.call(value, k)) {
      value = value[k];
    } else {
      return fallback !== null ? fallback : key;
    }
  }
  return value;
};
// ------------------

// --- STATE ---
const project = ref(null);
const loading = ref(true);
const analyticsId = ref('');
const isAnalyzing = ref(false);
const aiSummary = ref('');

// --- ANALYTICS MOCK STATE ---
const currentDateRange = ref(7); // 7, 30, 90

// Динамические фейковые данные для графиков (заменятся реальными после интеграции Google Data API)
const currentMetrics = computed(() => {
  if (currentDateRange.value === 7) return { visitors: 1248, views: 3812, bounce: 42, trend: 12 };
  if (currentDateRange.value === 30) return { visitors: 5840, views: 18450, bounce: 38, trend: 8 };
  return { visitors: 16200, views: 52100, bounce: 35, trend: -2 };
});

const currentChartData = computed(() => {
  // Возвращает массив высот баров (в %) в зависимости от периода
  if (currentDateRange.value === 7) return [40, 70, 45, 90, 65, 85, 100];
  if (currentDateRange.value === 30) return Array.from({length: 15}, () => Math.floor(Math.random() * 60) + 40);
  return Array.from({length: 30}, () => Math.floor(Math.random() * 80) + 20);
});

// Проверка тега
const hasGA4 = computed(() => {
  return analyticsId.value && typeof analyticsId.value === 'string' && analyticsId.value.trim().toUpperCase().startsWith('G-');
});

// --- METHODS ---
const loadProject = async () => {
  try {
    const res = await api.get(`/${route.params.id}`);
    project.value = res.data.project || res.data;
    const configData = project.value?.site_config || project.value?.config || {};

    if (configData.analytics_id) {
      analyticsId.value = configData.analytics_id;
    }
  } catch (error) {
    showAlert(t('common.alerts.error', 'Error'), 'Failed to load project details', 'error');
  } finally {
    loading.value = false;
  }
};

const saveGA4 = async () => {
  if (!analyticsId.value) return;
  try {
    const cleanId = analyticsId.value.trim().toUpperCase();
    await api.post(`/${route.params.id}/analytics`, { analytics_id: cleanId });

    // Обновляем локально, чтобы дашборд открылся мгновенно
    if(!project.value.site_config) project.value.site_config = {};
    project.value.site_config.analytics_id = cleanId;
    analyticsId.value = cleanId;

    showAlert(t('common.alerts.success', 'Success'), t('siteDashboard.ga4.success', 'GA4 saved! Data will start flowing.'), 'success');
  } catch (error) {
    showAlert(t('common.alerts.error', 'Error'), 'Failed to save GA4 tag', 'error');
  }
};

const analyzeLeads = async () => {
  isAnalyzing.value = true;
  aiSummary.value = '';
  try {
    const res = await api.post(`/${route.params.id}/analyze`);
    aiSummary.value = res.data.summary;
  } catch (error) {
    showAlert(t('common.alerts.error', 'Error'), 'Not enough leads to analyze yet.', 'warning');
  } finally {
    isAnalyzing.value = false;
  }
};

const exportReport = () => {
  try {
    const today = new Date().toISOString().split('T')[0];
    let csvContent = "data:text/csv;charset=utf-8,";

    // Заголовки
    csvContent += "Report Date,Period,Total Visitors,Page Views,Bounce Rate\n";

    // Метрики
    csvContent += `${today},Last ${currentDateRange.value} Days,${currentMetrics.value.visitors},${currentMetrics.value.views},${currentMetrics.value.bounce}%\n\n`;

    // ИИ отчет (очищенный от HTML)
    csvContent += "AI Insight Summary\n";
    const plainTextAI = aiSummary.value
        ? aiSummary.value.replace(/<[^>]*>?/gm, ' ').replace(/"/g, '""').trim()
        : 'No AI analysis generated yet.';
    csvContent += `"${plainTextAI}"\n`;

    // Скачивание
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `${project.value?.business_name || 'project'}_report_${today}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showAlert(t('common.alerts.success', 'Success'), 'Report exported successfully!', 'success');
  } catch (error) {
    showAlert(t('common.alerts.error', 'Error'), 'Failed to export report.', 'error');
  }
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  loadProject();
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-slide-enter-from { opacity: 0; transform: translateY(20px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-20px); }

/* Стилизация скроллбара для блока ИИ */
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.05); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.3); }
</style>