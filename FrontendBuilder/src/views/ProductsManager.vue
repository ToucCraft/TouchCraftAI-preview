<template>
  <div v-if="isI18nLoaded" class="p-5 md:p-10 w-full flex flex-col h-full">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-top mb-8 gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ t('products.title') }}</h1>
        <p class="text-gray-500">{{ t('products.subtitle') }}</p>
      </div>

      <div v-if="projects.length > 0" class="w-full md:w-72 mt-4">
        <label class="block text-xs font-bold text-gray-500 uppercase mb-2 ml-1">{{ t('products.chooseWebsite') }}</label>
        <div class="relative">
          <select v-model="selectedProjectId" @change="loadProjectData" class="w-full p-3 bg-white border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 appearance-none font-medium text-gray-800 shadow-sm cursor-pointer">
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name || t('products.withoutName') }}
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
      <p class="text-lg font-bold text-gray-600">{{ t('products.empty.title') }}</p>
      <router-link to="/create" class="mt-4 bg-blue-600 text-white px-6 py-2 rounded-xl font-bold hover:bg-blue-700 transition">{{ t('products.empty.btn') }}</router-link>
    </div>

    <div v-else-if="projectConfig" class="flex-1">
      <div v-if="!hasCatalogPage" class="text-center py-20 bg-white rounded-3xl border border-dashed border-blue-200 bg-blue-50/50">
        <i class="fas fa-store text-5xl mb-4 text-blue-400"></i>
        <p class="text-gray-700 font-bold text-xl mb-2">{{ t('products.enable.title') }}</p>
        <p class="text-gray-500 text-sm mb-6 max-w-md mx-auto">{{ t('products.enable.desc') }}</p>
        <button @click="enableCatalog" :disabled="isSaving" class="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold shadow hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center mx-auto">
          <i class="fas mr-2" :class="isSaving ? 'fa-spinner fa-spin' : 'fa-power-off'"></i>
          {{ isSaving ? t('products.enable.loading') : t('products.enable.btn') }}
        </button>
      </div>

      <div v-else class="space-y-6">
        <div class="flex justify-between items-center bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
          <div class="flex items-center gap-4">
            <span class="font-bold text-gray-700">{{ products.length }} / 25 {{ t('products.header.productsCount') || 'Products' }}</span>
            <select v-model="editingLang" class="p-1 border rounded text-xs outline-none bg-slate-50 uppercase font-bold cursor-pointer">
              <option v-for="lang in availableLanguages" :key="lang" :value="lang">{{ lang }}</option>
            </select>
          </div>
          <div class="flex items-center gap-3">
            <button @click="saveCatalog" :disabled="isSaving" class="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-bold text-sm hover:bg-gray-200 transition disabled:opacity-50 flex items-center">
              <i class="fas mr-2" :class="isSaving ? 'fa-spinner fa-spin' : 'fa-save'"></i>
              {{ isSaving ? t('products.header.deploying') : t('products.header.saveBtn') }}
            </button>
            <button @click="addProduct" :disabled="isSaving" class="bg-green-600 text-white px-4 py-2 rounded-lg font-bold text-sm hover:bg-green-700 transition disabled:opacity-50">
              <i class="fas fa-plus mr-2"></i> {{ t('products.header.addBtn') }}
            </button>
          </div>
        </div>

        <datalist id="category-suggestions">
          <option v-for="cat in uniqueCategories" :key="cat" :value="cat"></option>
        </datalist>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 pb-10">
          <div v-for="(product, idx) in products" :key="product.id" class="bg-white rounded-2xl border border-gray-200 p-4 shadow-sm relative group transition-all">

            <div class="absolute top-2 right-2 flex gap-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity">
              <button @click="translateProduct(product)" :disabled="isTranslating[product.id]" class="bg-white/90 backdrop-blur text-purple-600 p-2 rounded-lg hover:bg-purple-50 shadow-sm disabled:opacity-50 transition" title="Auto-Translate to other languages">
                <i class="fas" :class="isTranslating[product.id] ? 'fa-spinner fa-spin' : 'fa-language'"></i>
              </button>
              <button @click="removeProduct(idx)" class="bg-white/90 backdrop-blur text-red-500 p-2 rounded-lg hover:bg-red-50 shadow-sm transition" title="Delete product">
                <i class="fas fa-trash"></i>
              </button>
            </div>

            <div class="space-y-2 mb-4">
              <label class="block text-[9px] font-bold text-gray-400 uppercase">{{ t('products.card.images') || 'Images' }}</label>
              <div class="grid grid-cols-5 gap-1">
                <div v-for="n in 5" :key="n" class="relative group/img h-12 bg-slate-100 rounded-lg border border-dashed border-slate-300 overflow-hidden">
                  <template v-if="product.images && product.images[n-1]">
                    <img :src="product.images[n-1]" class="w-full h-full object-cover">
                    <div class="absolute inset-0 bg-black/40 opacity-0 group-hover/img:opacity-100 transition-opacity flex items-center justify-center gap-1">
                      <button @click="removeProductImage(product, n-1)" class="text-white text-[8px] hover:text-red-400"><i class="fas fa-trash"></i></button>
                      <label class="cursor-pointer text-white text-[8px] hover:text-blue-400">
                        <i class="fas fa-pen"></i>
                        <input type="file" @change="(e) => uploadProductImage(e, product, n-1)" class="hidden" accept="image/*">
                      </label>
                    </div>
                  </template>
                  <label v-else class="w-full h-full flex items-center justify-center cursor-pointer hover:bg-slate-200 transition">
                    <i class="fas fa-plus text-slate-400 text-xs"></i>
                    <input type="file" @change="(e) => uploadProductImage(e, product, n-1)" class="hidden" accept="image/*">
                  </label>
                </div>
              </div>
            </div>

            <div class="space-y-3">
              <div>
                <label class="text-[9px] font-bold text-gray-400 uppercase flex justify-between">
                  <span>{{ t('products.card.title') }} ({{ editingLang }})</span>
                  <span v-if="isTranslating[product.id]" class="text-purple-500 animate-pulse">Translating...</span>
                </label>
                <input v-model="product.title[editingLang]" class="w-full p-2 border border-slate-200 rounded text-xs bg-white outline-none focus:border-blue-500 font-bold">
              </div>

              <div>
                <label class="text-[9px] font-bold text-gray-400 uppercase">{{ t('products.card.category') || 'Category' }} ({{ editingLang }})</label>
                <input list="category-suggestions" v-model="product.category[editingLang]" class="w-full p-2 border border-slate-200 rounded text-xs bg-white outline-none focus:border-blue-500" :placeholder="t('products.card.categoryPlaceholder') || 'e.g. Electronics'">
              </div>

              <div>
                <label class="text-[9px] font-bold text-gray-400 uppercase">{{ t('products.card.description') }} ({{ editingLang }})</label>
                <textarea v-model="product.description[editingLang]" rows="2" class="w-full p-2 border border-slate-200 rounded text-xs bg-white outline-none focus:border-blue-500"></textarea>
              </div>

              <div class="flex flex-col gap-3">
                <div>
                  <label class="text-[9px] font-bold text-gray-400 uppercase">{{ t('products.card.price') }}</label>
                  <div class="relative">
                    <span class="absolute left-2 top-1/2 -translate-y-1/2 text-gray-400 text-xs">$</span>
                    <input v-model="product.price" class="w-full p-2 pl-6 border border-slate-200 rounded text-xs bg-white outline-none font-bold">
                  </div>
                </div>

                <div>
                  <label class="text-[9px] font-bold text-red-400 uppercase mb-1 block flex items-center gap-1">
                    <i class="fas fa-eye-slash"></i> {{ t('products.card.hideIn') }}
                  </label>
                  <div class="flex flex-wrap gap-1 p-1.5 border border-red-200 rounded bg-red-50 focus-within:ring-1 focus-within:ring-red-400 min-h-[34px] items-center">
                    <span v-for="(lang, lIdx) in product.excluded_langs" :key="lIdx" class="bg-red-100 text-red-700 px-1.5 py-0.5 rounded text-[10px] font-bold flex items-center">
                      {{ lang }}
                      <button @click="removeExcludedLang(product, lIdx)" class="ml-1 text-red-400 hover:text-red-800">
                        <i class="fas fa-times"></i>
                      </button>
                    </span>
                    <input @keydown.enter.prevent="addExcludedLang($event, product)" :placeholder="t('products.card.hidePlaceholder')" class="flex-1 bg-transparent outline-none text-[10px] px-1 text-red-800 placeholder-red-300 min-w-[50px]">
                  </div>
                </div>
              </div>
            </div>

          </div>
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

const { checkLimit, triggerUpgrade } = useSubscription();
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
      if (lang !== 'en') await loadTranslations('en');
    }
  } catch (error) {
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
// ------------------

const projects = ref([]);
const selectedProjectId = ref('');
const projectConfig = ref(null);
const isLoading = ref(true);
const isSaving = ref(false);
const editingLang = ref('en');
const isTranslating = ref({}); // <-- Стейт для загрузки перевода

const hasCatalogPage = computed(() => projectConfig.value?.has_catalog === true);
const products = computed(() => projectConfig.value?.products || []);

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

const uniqueCategories = computed(() => {
  const cats = new Set();
  products.value.forEach(p => {
    if (p.category && p.category[editingLang.value]) {
      cats.add(p.category[editingLang.value]);
    }
  });
  return Array.from(cats);
});

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

    if (projectConfig.value.products) {
      projectConfig.value.products.forEach(p => {
        if (typeof p.category === 'string') {
          p.category = { en: p.category };
        }
        if (!p.category) p.category = { en: 'General' };

        availableLanguages.value.forEach(l => {
          if (!p.category[l]) p.category[l] = p.category['en'] || 'General';
          if (!p.title[l]) p.title[l] = p.title['en'] || 'New Product';
          if (!p.description[l]) p.description[l] = p.description['en'] || '';
        });
      });
    }
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

const translateProduct = async (product) => {
  if (!checkLimit('ai_generations')) {
    return triggerUpgrade(t('products.upgrade.ai') || "AI Translations require the Starter plan.", 'starter');
  }

  const targetLangs = availableLanguages.value.filter(l => l !== editingLang.value);
  if (targetLangs.length === 0) {
    return showAlert('Info', 'No other languages available to translate to.', 'info');
  }

  if (!product.title[editingLang.value]) {
    return showAlert('Warning', 'Please enter a title before translating.', 'warning');
  }

  isTranslating.value[product.id] = true;
  try {
    const res = await api.post(`/${selectedProjectId.value}/translate-product`, {
      product: product,
      source_lang: editingLang.value,
      target_langs: targetLangs
    });

    const data = res.data;
    targetLangs.forEach(lang => {
      if (data.title && data.title[lang]) product.title[lang] = data.title[lang];
      if (data.description && data.description[lang]) product.description[lang] = data.description[lang];
      if (data.category && data.category[lang]) product.category[lang] = data.category[lang];
    });

    showAlert('Success', 'Product translated successfully!', 'success');
  } catch (e) {
    showAlert('Error', 'Translation failed.', 'error');
  } finally {
    isTranslating.value[product.id] = false;
  }
};

const uploadProductImage = async (event, product, imgIndex) => {
  const file = event.target.files[0];
  if (!file) return;
  const fd = new FormData();
  fd.append('file', file);
  try {
    const res = await api.post(`/${selectedProjectId.value}/upload-asset?asset_type=product`, fd);
    if (!product.images) product.images = [];
    product.images[imgIndex] = `${res.data.url}?t=${Date.now()}`;
  } catch (err) {
    showAlert('Error', t('products.alerts.uploadFailed') || 'Upload failed', 'error');
  } finally {
    event.target.value = '';
  }
};

const removeProductImage = (product, imgIndex) => {
  if (product.images) {
    product.images.splice(imgIndex, 1);
  }
};

const addExcludedLang = (event, product) => {
  const val = event.target.value.trim().toLowerCase();
  if (val && (!product.excluded_langs || !product.excluded_langs.includes(val))) {
    if (!product.excluded_langs) product.excluded_langs = [];
    product.excluded_langs.push(val);
  }
  event.target.value = '';
};

const removeExcludedLang = (product, index) => {
  if (product.excluded_langs) product.excluded_langs.splice(index, 1);
};

const enableCatalog = async () => {
  if (!checkLimit('catalogs')) {
    return triggerUpgrade("Product Catalogs are only available on the Pro plan.", 'pro');
  }
  if (!projectConfig.value) return;
  projectConfig.value.has_catalog = true;
  if (!projectConfig.value.products) projectConfig.value.products = [];
  await saveCatalog();
};

const addProduct = () => {
  if (!projectConfig.value.products) projectConfig.value.products = [];

  if (projectConfig.value.products.length >= 25) {
    return showAlert('Limit Reached', 'You can add a maximum of 25 products per website.', 'warning');
  }

  const langs = Object.keys(projectConfig.value.translations || { en: '' });
  const emptyTitle = {};
  const emptyDesc = {};
  const emptyCat = {};

  langs.forEach(l => {
    emptyTitle[l] = t('products.defaults.newProduct') || 'New Product';
    emptyDesc[l] = '';
    emptyCat[l] = t('products.defaults.general') || 'General';
  });

  projectConfig.value.products.push({
    id: 'prod_' + Date.now(),
    images: [],
    title: emptyTitle,
    description: emptyDesc,
    price: '0.00',
    category: emptyCat,
    excluded_langs: []
  });
};

const removeProduct = (index) => {
  projectConfig.value.products.splice(index, 1);
};

const saveCatalog = async () => {
  if (!selectedProjectId.value) return;
  isSaving.value = true;
  try {
    await api.patch(`/${selectedProjectId.value}`, { site_config: projectConfig.value });
    await api.post(`/${selectedProjectId.value}/deploy`);
    showAlert('Success', t('products.alerts.saveSuccess') || 'Saved successfully!', 'success');
  } catch (e) {
    showAlert('Error', t('products.alerts.saveError') || 'Error saving catalog.', 'error');
  } finally {
    isSaving.value = false;
  }
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  loadProjects();
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
</style>