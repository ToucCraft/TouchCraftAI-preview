<template>
  <div class="w-full bg-white flex flex-col min-h-screen font-sans relative"
       :style="`color: ${flatConfig.palette?.text}; background: ${flatConfig.palette?.background}; font-family: '${flatConfig.font || 'Inter'}', sans-serif;`">

    <HeaderBlock
        v-if="flatConfig.business_name"
        :businessName="flatConfig.business_name"
        :themeColor="flatConfig.palette?.primary"
        :palette="flatConfig.palette"
        :hasCatalog="flatConfig.has_catalog"
        :logoUrl="flatConfig.logo_url"
        :logoMode="flatConfig.logo_mode"
        :applyThemeColorToLogo="flatConfig.apply_theme_color_to_logo"
        :blocks="flatConfig.blocks"
        :availableLanguages="availableLanguages"
        :currentLang="currentLang"
        :contact="flatConfig.contact"  @changeLang="changeLang"
        @navigate="navigate"
        :t="t"
    />

    <main v-if="currentPage === 'home'" class="flex-grow flex flex-col">
      <template v-for="(block, index) in flatConfig.blocks" :key="block.id || index">
        <div class="relative w-full">
          <component
              :is="getComponent(block.type)"
              :props="block.props"
              :themeColor="flatConfig.palette?.primary"
              :palette="flatConfig.palette"
              :t="t"
          />

          <div v-if="index < flatConfig.blocks.length - 1 && block.type !== 'HeroBlock'" class="absolute bottom-0 left-0 w-full pointer-events-none">
            <div class="container mx-auto px-6">
              <div class="border-b-2" :style="{ borderColor: flatConfig.palette?.secondary || '#10B981', opacity: 0.90 }"></div>
            </div>
          </div>
        </div>
      </template>
    </main>

    <main v-else-if="currentPage === 'catalog'" class="flex-grow pt-32 pb-24 flex flex-col items-center justify-center">
      <div class="container mx-auto px-6 text-center">
        <i class="fas fa-shopping-bag text-6xl mb-6 opacity-20" :style="{ color: flatConfig.palette?.primary }"></i>
        <h1 class="text-4xl md:text-5xl font-black mb-4" :style="{ color: flatConfig.palette?.primary }">{{ t('Catalog') || 'Product Catalog' }}</h1>
      </div>
    </main>

    <main v-else-if="currentPage === 'privacy'" class="flex-grow pt-32 pb-24 flex flex-col items-center">
      <div class="container mx-auto px-6 max-w-4xl">
        <h1 class="text-4xl md:text-5xl font-black mb-8 text-center" :style="{ color: flatConfig.palette?.primary }">
          {{ t('Privacy Policy') !== 'Privacy Policy' ? t('Privacy Policy') : 'Privacy Policy' }}
        </h1>

        <div v-if="t('privacy_policy_text') && t('privacy_policy_text') !== 'privacy_policy_text'"
             class="prose max-w-none text-left"
             v-html="t('privacy_policy_text')">
        </div>

        <div v-else class="text-center mt-10">
          <i class="fas fa-shield-alt text-6xl mb-6 opacity-20" :style="{ color: flatConfig.palette?.primary }"></i>
          <p class="opacity-70">
            Privacy Policy
          </p>
        </div>
      </div>
    </main>

    <FooterBlock
        v-if="flatConfig.business_name"
        :businessName="flatConfig.business_name"
        :themeColor="flatConfig.palette?.primary"
        :contact="flatConfig.contact"
        :t="t"
        @navigate="navigate"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

import HeaderBlock from './blocks/Header.vue';
import FooterBlock from './blocks/Footer.vue';
import HeroBlock from './blocks/HeroBlock.vue';
import FeaturesBlock from './blocks/FeaturesBlock.vue';
import AboutBlock from './blocks/AboutBlock.vue';
import FaqBlock from './blocks/FaqBlock.vue';
import MapBlock from './blocks/MapBlock.vue';
import ContactBlock from './blocks/ContactBlock.vue';
import FormBlock from './blocks/FormBlock.vue';
import GalleryBlock from './blocks/GalleryBlock.vue';

const props = defineProps({
  config: { type: Object, required: true }
});

const componentsMap = { HeroBlock, FeaturesBlock, AboutBlock, FaqBlock, MapBlock, ContactBlock, FormBlock, GalleryBlock };
const getComponent = (type) => componentsMap[type] || null;

const currentLang = ref('en');
const currentPage = ref('home');

const availableLanguages = computed(() => {
  if (props.config && props.config.translations) {
    return Object.keys(props.config.translations);
  }
  return ['en'];
});

watch(() => availableLanguages.value, (langs) => {
  if (langs.length > 0 && !langs.includes(currentLang.value)) {
    currentLang.value = langs[0];
  }
}, { immediate: true });

const changeLang = (lang) => { currentLang.value = lang; };
const navigate = (page) => {
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const t = (key) => {
  if (props.config?.translations) {
    return props.config.translations[currentLang.value]?.[key] || key;
  }
  return key;
};

const flattenForLang = (data, targetLang) => {
  if (!data) return data;
  if (typeof data !== 'object') return data;
  if (Array.isArray(data)) return data.map(item => flattenForLang(item, targetLang));

  const keys = Object.keys(data);
  const isTranslationObj = keys.length > 0 && keys.every(k => /^[a-z]{2,3}(-[a-z0-9]{2,4})?$/i.test(k));

  if (isTranslationObj) return data[targetLang] || data['en'] || Object.values(data)[0];

  const result = {};
  for (let key in data) result[key] = flattenForLang(data[key], targetLang);
  return result;
};

const flatConfig = computed(() => {
  if (!props.config) return {};
  return flattenForLang(props.config, currentLang.value);
});

watch(() => flatConfig.value?.font, (newFont) => {
  if (newFont) {
    const fontFormatted = newFont.replace(/ /g, '+');
    const linkId = `google-font-${fontFormatted}`;
    if (!document.getElementById(linkId)) {
      const link = document.createElement('link');
      link.id = linkId;
      link.href = `https://fonts.googleapis.com/css2?family=${fontFormatted}:wght@400;600;900&display=swap`;
      link.rel = 'stylesheet';
      document.head.appendChild(link);
    }
  }
}, { immediate: true, deep: true });
</script>