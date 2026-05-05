<template>
  <div v-if="isI18nLoaded" class="min-h-screen bg-[#020617] text-slate-300 font-sans selection:bg-blue-500/30 pb-32">

    <div class="fixed top-0 left-0 w-full z-50 pt-6 px-4">
      <header class="max-w-4xl mx-auto h-16 rounded-2xl border border-white/10 backdrop-blur-xl bg-[#0f172a]/60 shadow-[0_8px_30px_rgb(0,0,0,0.5)] flex items-center justify-between px-6 transition-all duration-300">
        <router-link to="/" class="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity">
          <i class="fas fa-arrow-left text-blue-400"></i>
          <span class="text-sm font-bold tracking-tight text-white">{{ t('privacy.backToHome') }}</span>
        </router-link>
        <span class="text-xl font-black tracking-tighter">
          <span class="text-[#00c2ff]">TouchCraft AI</span>
        </span>
      </header>
    </div>

    <main class="max-w-4xl mx-auto px-6 pt-40">
      <div class="mb-12 border-b border-slate-800 pb-8">
        <h1 class="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">{{ t('privacy.title') }}</h1>
        <p class="text-blue-400 font-medium tracking-wide text-sm">{{ t('privacy.lastUpdated') }}: {{ new Date().toLocaleDateString(currentLang === 'ru' ? 'ru-RU' : 'en-US', { month: 'long', day: 'numeric', year: 'numeric' }) }}</p>
      </div>

      <div class="space-y-10 leading-relaxed text-slate-400 text-sm md:text-base">

        <section>
          <p v-html="t('privacy.intro')"></p>
        </section>

        <section>
          <h2 class="text-2xl font-bold text-white mb-4">{{ t('privacy.sec1.title') }}</h2>
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 text-slate-300">
            <p><strong>{{ t('privacy.sec1.entity') }}</strong> TouchCraft</p>
            <p><strong>{{ t('privacy.sec1.email') }}</strong> <a href="mailto:ivan@touch-craft.com" class="text-blue-400 hover:underline">ivan@touch-craft.com</a></p>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-bold text-white mb-4">{{ t('privacy.sec2.title') }}</h2>
          <p>{{ t('privacy.sec2.desc') }}</p>
          <ul class="list-disc pl-6 mt-4 space-y-3">
            <li v-html="t('privacy.sec2.li1')"></li>
            <li v-html="t('privacy.sec2.li2')"></li>
          </ul>
        </section>

        <section>
          <h2 class="text-2xl font-bold text-white mb-4">{{ t('privacy.sec3.title') }}</h2>
          <div class="overflow-x-auto mt-4">
            <table class="w-full text-left border-collapse border border-slate-800">
              <thead>
              <tr class="bg-slate-900 border-b border-slate-800 text-white">
                <th class="p-4 font-bold">{{ t('privacy.sec3.th1') }}</th>
                <th class="p-4 font-bold">{{ t('privacy.sec3.th2') }}</th>
                <th class="p-4 font-bold">{{ t('privacy.sec3.th3') }}</th>
              </tr>
              </thead>
              <tbody>
              <tr class="border-b border-slate-800">
                <td class="p-4" v-html="t('privacy.sec3.r1c1')"></td>
                <td class="p-4">{{ t('privacy.sec3.r1c2') }}</td>
                <td class="p-4">{{ t('privacy.sec3.r1c3') }}</td>
              </tr>
              <tr class="border-b border-slate-800">
                <td class="p-4" v-html="t('privacy.sec3.r2c1')"></td>
                <td class="p-4">{{ t('privacy.sec3.r2c2') }}</td>
                <td class="p-4">{{ t('privacy.sec3.r2c3') }}</td>
              </tr>
              <tr class="border-b border-slate-800">
                <td class="p-4" v-html="t('privacy.sec3.r3c1')"></td>
                <td class="p-4">{{ t('privacy.sec3.r3c2') }}</td>
                <td class="p-4">{{ t('privacy.sec3.r3c3') }}</td>
              </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-bold text-white mb-4">{{ t('privacy.sec4.title') }}</h2>
          <p>{{ t('privacy.sec4.desc') }}</p>
          <ul class="list-disc pl-6 mt-4 space-y-2">
            <li v-html="t('privacy.sec4.li1')"></li>
            <li v-html="t('privacy.sec4.li2')"></li>
            <li v-html="t('privacy.sec4.li3')"></li>
          </ul>
        </section>

        <section>
          <h2 class="text-2xl font-bold text-white mb-4">{{ t('privacy.sec5.title') }}</h2>
          <p>{{ t('privacy.sec5.desc') }}</p>
        </section>

        <section>
          <h2 class="text-2xl font-bold text-white mb-4">{{ t('privacy.sec6.title') }}</h2>
          <p>{{ t('privacy.sec6.desc') }}</p>
          <ul class="list-disc pl-6 mt-4 space-y-2">
            <li v-html="t('privacy.sec6.li1')"></li>
            <li v-html="t('privacy.sec6.li2')"></li>
            <li v-html="t('privacy.sec6.li3')"></li>
            <li v-html="t('privacy.sec6.li4')"></li>
            <li v-html="t('privacy.sec6.li5')"></li>
            <li v-html="t('privacy.sec6.li6')"></li>
          </ul>
          <p class="mt-4">{{ t('privacy.sec6.contact') }} <a href="mailto:ivan@touch-craft.com" class="text-blue-400 hover:underline">ivan@touch-craft.com</a>.</p>
        </section>

        <section>
          <h2 class="text-2xl font-bold text-white mb-4">{{ t('privacy.sec7.title') }}</h2>
          <p v-html="t('privacy.sec7.desc')"></p>
          <p class="mt-2">
            {{ t('privacy.sec7.website') }} <a href="https://www.aepd.es" target="_blank" class="text-blue-400 hover:underline">www.aepd.es</a><br>
            {{ t('privacy.sec7.address') }} C/ Jorge Juan, 6, 28001 Madrid, Spain.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-bold text-white mb-4">{{ t('privacy.sec8.title') }}</h2>
          <p>{{ t('privacy.sec8.desc') }}</p>
        </section>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const currentLang = ref(localStorage.getItem('app_lang') || 'en');
const translations = ref({});
const isI18nLoaded = ref(false);

const loadTranslations = async (lang) => {
  try {
    const response = await fetch(`/i18n/${lang}.json`);
    if (response.ok) {
      translations.value = await response.json();
      document.documentElement.lang = lang;
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

onMounted(() => {
  loadTranslations(currentLang.value);
});
</script>