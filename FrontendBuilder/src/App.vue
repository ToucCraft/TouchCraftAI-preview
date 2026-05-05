<template>
  <div v-if="isLoading && route.path !== '/' && route.path !== '/preview-render'" class="h-screen w-full flex items-center justify-center bg-gray-900">
    <div class="loader ease-linear rounded-full border-4 border-t-4 border-gray-700 h-12 w-12"></div>
  </div>

  <div v-else-if="route.meta.hideLayout" class="w-full min-h-screen" :class="route.path === '/' ? 'bg-[#020617]' : 'bg-white'">
    <router-view />
  </div>

  <div v-else-if="isI18nLoaded" class="flex flex-col h-screen overflow-hidden bg-gray-100 font-sans text-left">
    <header class="bg-gray-900 text-white z-50 shadow-lg border-b border-gray-800">
      <div class="p-4 flex justify-between items-center relative z-50 bg-gray-900">
        <div class="flex items-center gap-4">
          <button @click="isDesktopCollapsed = !isDesktopCollapsed" class="hidden lg:flex items-center justify-center w-8 h-8 rounded-lg bg-gray-800 border border-gray-700 hover:bg-gray-700 hover:border-blue-500 transition-all text-gray-400 hover:text-white">
            <i class="fas" :class="isDesktopCollapsed ? 'fa-indent' : 'fa-outdent'"></i>
          </button>
          <router-link to="/dashboard" class="flex items-center cursor-pointer select-none hover:opacity-80 transition-opacity">
            <span class="text-xl font-black tracking-tighter">
              <span class="text-[#00c2ff]">TouchCraft AI</span>
            </span>
          </router-link>
        </div>

        <div class="flex items-center gap-4">

          <div class="hidden lg:block relative group">
            <button class="flex items-center gap-2 px-3 py-1.5 border border-[#00c2ff] rounded-lg bg-[#1f2937] text-white hover:bg-[#374151] transition shadow-sm">
              <img :src="currentLang === 'en' ? 'https://flagcdn.com/w20/gb.png' :
           currentLang === 'uk' ? 'https://flagcdn.com/w20/ua.png' :
           currentLang === 'ca' ? 'https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.0.0/flags/4x3/es-ct.svg' :
           `https://flagcdn.com/w20/${currentLang}.png`"
                   class="w-4 h-[11px] object-cover rounded-[1px] shadow-sm border border-white/10" alt="flag">
              <span class="text-xs font-bold uppercase text-white">{{ currentLang }}</span>
              <i class="fas fa-chevron-down text-[10px] ml-1 text-[#00c2ff]"></i>
            </button>

            <div class="absolute right-0 top-full pt-2 w-full min-w-[90px] z-50 opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto transition-all transform origin-top-right scale-95 group-hover:scale-100">
              <div class="bg-[#1f2937] rounded-lg shadow-xl overflow-hidden border border-gray-700">
                <button @click="changeLanguage('en')" class="w-full flex items-center justify-between px-3 py-2 hover:bg-[#374151] transition" :class="currentLang === 'en' ? 'bg-[#374151]' : ''">
                  <img src="https://flagcdn.com/w20/gb.png" class="w-4 h-3 object-cover rounded-sm shadow-sm" alt="EN">
                  <span class="text-[10px] font-black text-white">EN</span>
                </button>
                <button @click="changeLanguage('ru')" class="w-full flex items-center justify-between px-3 py-2 hover:bg-[#374151] transition border-t border-gray-700/50" :class="currentLang === 'ru' ? 'bg-[#374151]' : ''">
                  <img src="https://flagcdn.com/w20/ru.png" class="w-4 h-3 object-cover rounded-sm shadow-sm" alt="RU">
                  <span class="text-[10px] font-black text-white">RU</span>
                </button>
                <button @click="changeLanguage('es')" class="w-full flex items-center justify-between px-3 py-2 hover:bg-[#374151] transition border-t border-gray-700/50" :class="currentLang === 'es' ? 'bg-[#374151]' : ''">
                  <img src="https://flagcdn.com/w20/es.png" class="w-4 h-3 object-cover rounded-sm shadow-sm" alt="ES">
                  <span class="text-[10px] font-black text-white">ES</span>
                </button>
                <button @click="changeLanguage('uk')" class="w-full flex items-center justify-between px-3 py-2 hover:bg-[#374151] transition border-t border-gray-700/50" :class="currentLang === 'uk' ? 'bg-[#374151]' : ''">
                  <img src="https://flagcdn.com/w20/ua.png" class="w-4 h-3 object-cover rounded-sm shadow-sm" alt="UK">
                  <span class="text-[10px] font-black text-white">UA</span>
                </button>
                <button @click="changeLanguage('ee')" class="w-full flex items-center justify-between px-3 py-2 hover:bg-[#374151] transition border-t border-gray-700/50" :class="currentLang === 'ee' ? 'bg-[#374151]' : ''">
                  <img src="https://flagcdn.com/w20/ee.png" class="w-4 h-3 object-cover rounded-sm shadow-sm" alt="EE">
                  <span class="text-[10px] font-black text-white">EE</span>
                </button>
                <button @click="changeLanguage('de')" class="w-full flex items-center justify-between px-3 py-2 hover:bg-[#374151] transition border-t border-gray-700/50" :class="currentLang === 'de' ? 'bg-[#374151]' : ''">
                  <img src="https://flagcdn.com/w20/de.png" class="w-4 h-3 object-cover rounded-sm shadow-sm" alt="DE">
                  <span class="text-[10px] font-black text-white">DE</span>
                </button>
                <button @click="changeLanguage('fr')" class="w-full flex items-center justify-between px-3 py-2 hover:bg-[#374151] transition border-t border-gray-700/50" :class="currentLang === 'fr' ? 'bg-[#374151]' : ''">
                  <img src="https://flagcdn.com/w20/fr.png" class="w-4 h-3 object-cover rounded-sm shadow-sm" alt="FR">
                  <span class="text-[10px] font-black text-white">FR</span>
                </button>
                <button @click="changeLanguage('it')" class="w-full flex items-center justify-between px-3 py-2 hover:bg-[#374151] transition border-t border-gray-700/50" :class="currentLang === 'it' ? 'bg-[#374151]' : ''">
                  <img src="https://flagcdn.com/w20/it.png" class="w-4 h-3 object-cover rounded-sm shadow-sm" alt="IT">
                  <span class="text-[10px] font-black text-white">IT</span>
                </button>
                <button @click="changeLanguage('ca')" class="w-full flex items-center justify-between px-3 py-2 hover:bg-[#374151] transition border-t border-gray-700/50" :class="currentLang === 'ca' ? 'bg-[#374151]' : ''">
                  <img src="https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.0.0/flags/4x3/es-ct.svg" class="w-4 h-3 object-cover rounded-sm shadow-sm" alt="CA">
                  <span class="text-[10px] font-black text-white">CA</span>
                </button>
              </div>
            </div>
          </div>

          <div v-if="isAuthenticated" class="hidden sm:flex items-center gap-2 px-3 py-1 bg-gray-800 rounded-full border border-gray-700">
            <img :src="user?.picture" class="w-6 h-6 rounded-full border border-gray-600" alt="Profile">
            <span class="text-xs font-medium text-gray-300">{{ user?.nickname || 'User' }}</span>
          </div>

          <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="lg:hidden text-gray-300 p-2 outline-none">
            <i class="fas" :class="isMobileMenuOpen ? 'fa-times' : 'fa-bars'"></i>
          </button>
        </div>
      </div>

      <transition
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="-translate-y-full opacity-0"
          enter-to-class="translate-y-0 opacity-100"
          leave-active-class="transition duration-200 ease-in"
          leave-from-class="translate-y-0 opacity-100"
          leave-to-class="-translate-y-full opacity-0"
      >
        <nav v-if="isMobileMenuOpen" class="absolute w-full bg-gray-800 border-b border-gray-700 p-4 space-y-2 z-40 shadow-xl lg:hidden">

          <div class="mt-auto p-4 border-t border-gray-800">
            <div class="text-xs font-bold text-gray-500 uppercase tracking-widest mb-4 px-2">
              {{ t('nav.language') }}
            </div>

            <div class="flex overflow-x-auto gap-3 pb-2 px-2 no-scrollbar">
              <button
                  v-for="lang in ['en', 'ru', 'es', 'uk', 'ee', 'de', 'fr', 'it', 'ca']"
                  :key="lang"
                  @click="changeLanguage(lang)"
                  class="flex flex-col items-center gap-2 min-w-[65px] p-3 rounded-xl border transition-all shrink-0"
                  :class="currentLang === lang
          ? 'bg-blue-600/20 border-blue-500 text-white shadow-[0_0_15px_rgba(37,99,235,0.2)]'
          : 'bg-gray-800 border-gray-700 text-gray-400 hover:border-gray-600'"
              >
                <img :src="getFlagUrl(lang)" class="w-6 h-4 object-cover rounded-sm shadow-sm" />
                <span class="text-[10px] font-black uppercase">{{ lang }}</span>
              </button>
            </div>
          </div>

          <router-link to="/dashboard" class="block p-4 rounded-xl flex items-center transition"
                       :class="route.path === '/dashboard' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300'">
            <i class="fas fa-th-large mr-3"></i> {{ t('app.nav.mySites') }}
          </router-link>

          <router-link to="/create" class="block p-4 rounded-xl flex items-center transition"
                       :class="route.path.startsWith('/create') ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300'">
            <i class="fas fa-plus-circle mr-3"></i> {{ t('app.nav.createNew') }}
          </router-link>

          <router-link to="/domains" class="block p-4 rounded-xl flex items-center transition"
                       :class="route.path === '/domains' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300'">
            <i class="fas fa-globe mr-3"></i> {{ t('app.nav.domains') }}
          </router-link>

          <router-link to="/leads" class="block p-4 rounded-xl flex items-center transition"
                       :class="route.path === '/leads' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300'">
            <i class="fas fa-inbox mr-3"></i> {{ t('app.nav.leads') }}
          </router-link>

          <router-link to="/products" class="block p-4 rounded-xl flex items-center transition"
                       :class="route.path === '/products' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300'">
            <i class="fas fa-box-open mr-3"></i> {{ t('app.nav.products') }}
          </router-link>

          <router-link to="/seo" class="block p-4 rounded-xl flex items-center transition"
                       :class="route.path === '/seo' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300'">
            <i class="fas fa-search mr-3"></i> SEO
          </router-link>

          <router-link to="/usage" class="block p-4 rounded-xl flex items-center transition"
                       :class="route.path === '/usage' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300'">
            <i class="fas fa-chart-pie mr-3"></i> {{ t('app.nav.usage') }}
          </router-link>

          <router-link to="/settings" class="block p-4 rounded-xl flex items-center transition"
                       :class="route.path === '/settings' ? 'bg-blue-600 text-white' : 'hover:bg-gray-700 text-gray-300'">
            <i class="fas fa-cog mr-3"></i> {{ t('app.nav.settings') }}
          </router-link>

          <button @click="handleLogout" class="w-full text-left p-4 rounded-xl flex items-center text-red-400 hover:bg-red-500/10 transition">
            <i class="fas fa-sign-out-alt mr-3"></i> {{ t('app.nav.logout') }}
          </button>
        </nav>
      </transition>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <aside :class="isDesktopCollapsed ? 'w-16' : 'w-64'" class="hidden lg:flex flex-col bg-gray-900 text-gray-300 shadow-2xl z-20 transition-all duration-300 border-r border-gray-800">
        <nav class="flex-1 p-2 space-y-3 mt-4">
          <router-link to="/dashboard" class="flex items-center p-3 rounded-xl transition-all group" exact-active-class="bg-blue-600 text-white shadow-lg">
            <i class="fas fa-th-large text-lg" :class="!isDesktopCollapsed ? 'mr-4' : 'mx-auto'"></i>
            <span v-if="!isDesktopCollapsed" class="font-medium truncate">{{ t('app.nav.mySites') }}</span>
          </router-link>
          <router-link to="/create" class="flex items-center p-3 rounded-xl transition-all group" :class="route.path.startsWith('/create') ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-gray-800'">
            <i class="fas fa-plus-circle text-lg" :class="!isDesktopCollapsed ? 'mr-4' : 'mx-auto'"></i>
            <span v-if="!isDesktopCollapsed" class="font-medium truncate">{{ t('app.nav.createNew') }}</span>
          </router-link>
          <router-link to="/domains" class="flex items-center p-3 rounded-xl transition-all group" :class="route.path === '/domains' ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-gray-800'">
            <i class="fas fa-globe text-lg" :class="!isDesktopCollapsed ? 'mr-4' : 'mx-auto'"></i>
            <span v-if="!isDesktopCollapsed" class="font-medium truncate">{{ t('app.nav.domains') }}</span>
          </router-link>
          <router-link to="/leads" class="flex items-center p-3 rounded-xl transition-all group" :class="route.path === '/leads' ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-gray-800'">
            <i class="fas fa-inbox text-lg" :class="!isDesktopCollapsed ? 'mr-4' : 'mx-auto'"></i>
            <span v-if="!isDesktopCollapsed" class="font-medium truncate">{{ t('app.nav.leads') }}</span>
          </router-link>
          <router-link to="/products" class="flex items-center p-3 rounded-xl transition-all group" :class="route.path === '/products' ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-gray-800'">
            <i class="fas fa-box-open text-lg" :class="!isDesktopCollapsed ? 'mr-4' : 'mx-auto'"></i>
            <span v-if="!isDesktopCollapsed" class="font-medium truncate">{{ t('app.nav.products') }}</span>
          </router-link>
          <router-link to="/seo" class="flex items-center p-3 rounded-xl transition-all group" :class="route.path === '/seo' ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-gray-800'">
            <i class="fas fa-search text-lg" :class="!isDesktopCollapsed ? 'mr-4' : 'mx-auto'"></i>
            <span v-if="!isDesktopCollapsed" class="font-medium truncate">{{ t('app.nav.seo') }}</span>
          </router-link>
          <router-link to="/usage" class="flex items-center p-3 rounded-xl transition-all group" :class="route.path === '/usage' ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-gray-800'">
            <i class="fas fa-chart-pie text-lg" :class="!isDesktopCollapsed ? 'mr-4' : 'mx-auto'"></i>
            <span v-if="!isDesktopCollapsed" class="font-medium truncate">{{ t('app.nav.usage') }}</span>
          </router-link>
          <router-link to="/settings" class="flex items-center p-3 rounded-xl transition-all group" :class="route.path === '/settings' ? 'bg-blue-600 text-white shadow-lg' : 'hover:bg-gray-800'">
            <i class="fas fa-cog text-lg" :class="!isDesktopCollapsed ? 'mr-4' : 'mx-auto'"></i>
            <span v-if="!isDesktopCollapsed" class="font-medium truncate">{{ t('app.nav.settings') }}</span>
          </router-link>
        </nav>
        <div class="p-3 border-t border-gray-800">
          <button @click="handleLogout" class="flex items-center w-full p-3 rounded-xl text-gray-400 hover:bg-red-500/10 hover:text-red-400 transition-all">
            <i class="fas fa-sign-out-alt text-lg" :class="!isDesktopCollapsed ? 'mr-4' : 'mx-auto'"></i>
            <span v-if="!isDesktopCollapsed" class="font-medium">{{ t('app.nav.logout') }}</span>
          </button>
        </div>
      </aside>

      <main class="flex-1 overflow-auto relative h-full bg-gray-50 scroll-smooth">
        <router-view />
      </main>
    </div>
  </div>
  <Modal />
  <UpgradeModal />
  <CookieBanner />
</template>

<script setup>
import { ref, watch, onMounted, defineAsyncComponent } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';
import { useRouter, useRoute } from 'vue-router';

import api, { setAuthToken, setTokenFetcher } from './api/client';

import { useSubscription } from './composables/useSubscription';

const Modal = defineAsyncComponent(() => import('./components/Modal.vue'));
const CookieBanner = defineAsyncComponent(() => import('./components/CookieBanner.vue'));
const UpgradeModal = defineAsyncComponent(() => import('./components/UpgradeModal.vue'));

const router = useRouter();
const route = useRoute();
const { updateUserData } = useSubscription();

// --- Auth0 Настройки ---
const {
  isAuthenticated,
  getAccessTokenSilently,
  logout: auth0Logout,
  user,
  isLoading
} = useAuth0();

const isMobileMenuOpen = ref(false);
const isDesktopCollapsed = ref(false);

// --- I18N (Интернационализация) ---
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

const getFlagUrl = (lang) => {
  const flags = {
    en: 'https://flagcdn.com/w20/gb.png',
    uk: 'https://flagcdn.com/w20/ua.png',
    ca: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Flag_of_Catalonia.svg/40px-Flag_of_Catalonia.svg.png'
  };
  return flags[lang] || `https://flagcdn.com/w20/${lang.toLowerCase()}.png`;
};

const changeLanguage = (lang) => {
  if (lang !== currentLang.value) {
    localStorage.setItem('app_lang', lang);
    window.location.reload();
  }
};


const handleLogout = () => {
  auth0Logout({
    logoutParams: {
      returnTo: window.location.origin
    }
  });
};

watch(isAuthenticated, async (newVal) => {
  if (newVal) {
    try {
      const token = await getAccessTokenSilently();
      setAuthToken(token);

      const res = await api.get('/user/me');
      updateUserData(res.data);

      if (window.location.pathname === '/') {
        router.push('/dashboard');
      }
    } catch (e) {
      console.error("Auth sync error", e);
    }
  }
});

onMounted(async () => {
  setTokenFetcher(getAccessTokenSilently);

  await loadTranslations(currentLang.value);

  if (isAuthenticated.value && window.location.pathname === '/') {
    router.push('/dashboard');
  }
});

watch(() => route.path, () => {
  isMobileMenuOpen.value = false;
});
</script>