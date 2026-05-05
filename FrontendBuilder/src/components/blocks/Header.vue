<template>
  <header
      class="fixed top-0 w-full z-50 backdrop-blur-md border-b transition-all duration-300"
      :style="{
      backgroundColor: (palette?.background || '#ffffff') + 'CC',
      borderColor: isDarkBackground ? 'rgba(255,255,255,0.1)' : (themeColor + '30'),
      color: isDarkBackground ? '#ffffff' : '#1f2937'
    }"
  >
    <div class="container mx-auto px-4 lg:px-6 py-3 lg:py-4 flex justify-between items-center relative">

      <div class="flex items-center gap-3 cursor-pointer z-[60]" @click="handleNav({href: '#', page: 'home'})">

        <img v-if="(logoMode === 'logo' || logoMode === 'both') && logoUrl && !applyThemeColorToLogo"
             :src="logoUrl"
             class="h-8 max-w-[150px] object-contain"
             alt="Logo">

        <div v-if="(logoMode === 'logo' || logoMode === 'both') && logoUrl && applyThemeColorToLogo"
             class="h-8 w-8 lg:w-10"
             :style="{
               backgroundColor: isDarkBackground ? '#ffffff' : themeColor,
               maskImage: `url(${logoUrl})`, WebkitMaskImage: `url(${logoUrl})`,
               maskSize: 'contain', WebkitMaskSize: 'contain',
               maskRepeat: 'no-repeat', WebkitMaskRepeat: 'no-repeat',
               maskPosition: 'left center', WebkitMaskPosition: 'left center'
             }">
        </div>

        <div v-if="(!logoUrl) || logoMode === 'text' || logoMode === 'both'"
             class="text-lg lg:text-xl font-black tracking-tight"
             :style="{ color: isDarkBackground ? '#ffffff' : themeColor }">
          {{ businessName }}
        </div>
      </div>

      <nav class="hidden lg:flex space-x-4 xl:space-x-6 font-bold text-xs uppercase tracking-wider" :class="isDarkBackground ? 'opacity-90' : 'opacity-80'">
        <a v-for="item in navLinks" :key="item.label" :href="item.href" @click.prevent="handleNav(item)" class="hover:opacity-100 transition-opacity" :style="{ color: 'inherit' }">
          {{ item.label }}
        </a>
      </nav>

      <div class="hidden lg:flex items-center space-x-4">
        <div v-if="availableLanguages && availableLanguages.length > 1" class="relative group h-full flex items-center">
          <button class="flex items-center gap-2 px-3 py-1.5 border rounded-lg transition shadow-sm cursor-pointer"
                  :style="{
                    borderColor: isDarkBackground ? 'rgba(255,255,255,0.2)' : themeColor + '50',
                    backgroundColor: isDarkBackground ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.02)'
                  }">
            <img :src="getFlagUrl(currentLang)" class="w-4 h-[11px] object-cover rounded-[1px] shadow-sm">
            <span class="text-xs font-bold uppercase">{{ currentLang }}</span>
            <i class="fas fa-chevron-down text-[10px] ml-1" :style="{ color: themeColor }"></i>
          </button>
          <div class="absolute right-0 top-[100%] pt-2 w-full min-w-[90px] hidden group-hover:block z-50">
            <div class="rounded-lg shadow-xl overflow-hidden border"
                 :style="{ backgroundColor: palette?.background || '#ffffff', borderColor: isDarkBackground ? 'rgba(255,255,255,0.1)' : themeColor + '30' }">
              <button v-for="lang in availableLanguages" :key="lang" @click="$emit('changeLang', lang)"
                      class="w-full flex items-center justify-between px-3 py-2 transition-colors hover:bg-black/5 border-b last:border-0"
                      :style="{
                        color: isDarkBackground ? '#ffffff' : '#1f2937',
                        borderColor: isDarkBackground ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)'
                      }">
                <img :src="getFlagUrl(lang)" class="w-4 h-3 object-cover rounded-sm shadow-sm">
                <span class="text-[10px] font-black uppercase">{{ lang }}</span>
              </button>
            </div>
          </div>
        </div>

        <a v-if="contact?.header_show_cta !== false"
           :href="contact?.header_cta_url || '#contacts'"
           :target="contact?.header_cta_url && contact.header_cta_url.startsWith('http') ? '_blank' : '_self'"
           @click="handleCtaScroll"
           class="px-5 py-2 rounded-full font-bold text-xs shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all cursor-pointer whitespace-nowrap"
           :style="{ backgroundColor: themeColor, color: '#fff' }">
          {{ contact?.header_cta_text || (t ? t('Contact Us') : 'Contact Us') }}
        </a>
      </div>

      <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="lg:hidden p-2 focus:outline-none z-[60] relative" :class="isDarkBackground ? 'text-white' : 'text-slate-800'">
        <i class="fas text-xl" :class="isMobileMenuOpen ? 'fa-times' : 'fa-bars'"></i>
      </button>

      </div>
      <transition name="slide-down">
        <div v-if="isMobileMenuOpen" class="absolute top-full left-0 w-full shadow-2xl border-b p-6 flex flex-col gap-6 lg:hidden z-50" :style="{ backgroundColor: palette?.background || '#ffffff', borderColor: isDarkBackground ? 'rgba(255,255,255,0.1)' : themeColor + '30' }">
          <a v-for="item in navLinks" :key="item.href" :href="item.href" @click.prevent="handleNav(item)" class="font-black text-lg" :style="{ color: isDarkBackground ? '#ffffff' : '#1f2937' }">
            {{ item.label }}
          </a>
          <div class="h-px w-full bg-current opacity-10"></div>
          <div v-if="availableLanguages && availableLanguages.length > 1" class="flex flex-col gap-3">
            <span class="font-bold text-xs uppercase tracking-widest px-2" :style="{ color: isDarkBackground ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.4)' }">
              Language
            </span>
            <div class="flex overflow-x-auto gap-3 pb-2 px-2 no-scrollbar">
              <button v-for="lang in availableLanguages" :key="lang"
                      @click="$emit('changeLang', lang); isMobileMenuOpen = false"
                      class="flex flex-col items-center gap-2 min-w-[65px] p-3 border rounded-xl transition-all shrink-0"
                      :style="currentLang === lang ?
                        { borderColor: themeColor, backgroundColor: themeColor + '20', color: isDarkBackground ? '#ffffff' : '#000000' } :
                        { borderColor: isDarkBackground ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)', color: isDarkBackground ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.6)' }">
                <img :src="getFlagUrl(lang)" class="w-6 h-4 object-cover rounded-sm shadow-sm">
                <span class="text-[10px] font-black uppercase tracking-widest">{{ lang }}</span>
              </button>
            </div>
          </div>
        </div>
      </transition>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps([
  'businessName', 'themeColor', 'availableLanguages', 'currentLang',
  't', 'blocks', 'palette', 'hasCatalog',
  'logoUrl', 'logoMode', 'applyThemeColorToLogo', 'contact'
]);
const emit = defineEmits(['changeLang', 'navigate']);

const isMobileMenuOpen = ref(false);

const isDarkBackground = computed(() => {
  const color = props.palette?.background || '#ffffff';
  if (color.startsWith('#')) {
    const r = parseInt(color.slice(1, 3), 16);
    const g = parseInt(color.slice(3, 5), 16);
    const b = parseInt(color.slice(5, 7), 16);
    const yiq = (r * 299 + g * 587 + b * 114) / 1000;
    return yiq < 128;
  }
  return false;
});

const getFlagUrl = (lang) => {
  if (!lang) return '';
  const l = lang.toLowerCase();
  if (l === 'en') return 'https://flagcdn.com/w20/gb.png';
  if (l === 'uk') return 'https://flagcdn.com/w20/ua.png';
  if (l === 'ca') return 'https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.0.0/flags/4x3/es-ct.svg';
  return `https://flagcdn.com/w20/${l}.png`;
};

const navLinks = computed(() => {
  const links = [{ label: props.t ? props.t('Home') : 'Home', href: '#', page: 'home' }];

  if (props.hasCatalog) {
    links.push({ label: props.t ? props.t('Catalog') : 'Catalog', href: '#catalog', page: 'catalog' });
  }

  if (!props.blocks) return links;
  const typeMap = { 'FeaturesBlock': 'Features', 'AboutBlock': 'About', 'FaqBlock': 'FAQ', 'MapBlock': 'Map', 'GalleryBlock': 'Gallery' };
  props.blocks.forEach(block => {
    const labelKey = typeMap[block.type];
    if (labelKey) {
      const href = `#${labelKey.toLowerCase()}`;
      if (!links.find(l => l.href === href)) {
        links.push({ label: props.t ? props.t(labelKey) : labelKey, href, page: 'home' });
      }
    }
  });
  return links;
});

const handleNav = (item) => {
  isMobileMenuOpen.value = false;

  if (item.page === 'catalog') {
    emit('navigate', 'catalog');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } else if (item.href === '#') {
    emit('navigate', 'home');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } else {
    emit('navigate', 'home');
    setTimeout(() => {
      const el = document.querySelector(item.href);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }
};

const handleCtaScroll = (e) => {
  const targetUrl = props.contact?.header_cta_url || '#contacts';

  if (targetUrl.startsWith('#')) {
    e.preventDefault();
    emit('navigate', 'home');

    setTimeout(() => {
      const targetElement = document.querySelector(targetUrl);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  }
};
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;  /* IE и Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>