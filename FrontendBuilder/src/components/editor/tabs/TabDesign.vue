<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm transition-all" :class="{ 'overflow-hidden': !isFontDropdownOpen, 'relative z-[100]': isFontDropdownOpen }">
    <button @click="isOpen = !isOpen; isFontDropdownOpen = false" class="w-full p-4 flex justify-between items-center bg-slate-50 hover:bg-slate-100 transition-colors">
      <h3 class="font-bold text-[10px] text-gray-700 uppercase flex items-center">
        <i class="fas fa-paint-brush mr-2 text-blue-500"></i> {{ t('editSite.tabs.design.title') }}
      </h3>
      <i class="fas text-gray-400" :class="isOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
    </button>

    <div v-show="isOpen" class="p-4 border-t border-slate-100 bg-white">
      <div class="grid grid-cols-4 gap-3 mb-4" v-if="config.palette">
        <div v-for="(val, key) in config.palette" :key="key" class="flex flex-col items-center">
          <input type="color" v-model="config.palette[key]" class="w-8 h-8 cursor-pointer overflow-hidden border-none bg-transparent">
          <p class="text-[8px] text-center mt-2 uppercase text-gray-500 font-bold">{{key}}</p>
        </div>
      </div>

      <h3 class="font-bold text-[10px] text-gray-500 uppercase mb-2">{{ t('editSite.tabs.design.typography') }}</h3>
      <div class="relative w-full">
        <div @click="isFontDropdownOpen = !isFontDropdownOpen"
             class="w-full p-2 border border-slate-200 rounded-lg text-[13px] bg-white cursor-pointer flex justify-between items-center outline-none focus:ring-2 focus:ring-blue-500"
             :style="`font-family: '${config.font}', sans-serif;`">
          <span>{{ config.font }}</span>
          <i class="fas text-gray-400" :class="isFontDropdownOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
        </div>

        <div v-if="isFontDropdownOpen" class="absolute top-[105%] left-0 w-full bg-white border border-slate-200 rounded-lg shadow-2xl z-50 flex flex-col overflow-hidden">
          <div class="p-2 border-b border-slate-100 bg-slate-50">
            <input v-model="fontSearch" type="text" placeholder="Search fonts..." class="w-full p-1.5 text-xs border rounded outline-none focus:border-blue-500 bg-white">
          </div>

          <div class="max-h-60 overflow-y-auto custom-scrollbar" @scroll="handleFontScroll">
            <div v-for="font in visibleFonts" :key="font"
                 @click="selectFont(font)"
                 class="p-3 text-[14px] cursor-pointer hover:bg-blue-50 transition-colors border-b border-slate-50 last:border-0 flex items-center justify-between"
                 :class="{'bg-blue-50 text-blue-600': config.font === font}"
                 :style="`font-family: '${font}', sans-serif;`">
              {{ font }}
              <i v-if="config.font === font" class="fas fa-check text-blue-500 text-[10px]"></i>
            </div>
            <div v-if="visibleFonts.length < filteredFonts.length" class="p-3 text-center text-[10px] text-gray-400 font-bold uppercase tracking-wider">
              <i class="fas fa-spinner fa-spin mr-1"></i> Loading more...
            </div>
          </div>
        </div>
      </div>
      <h3 class="font-bold text-[10px] text-gray-500 uppercase mt-6 mb-2">{{ t('editSite.tabs.design.animations') || 'ANIMATIONS' }}</h3>
      <label class="flex items-center justify-between cursor-pointer p-3 border border-slate-200 rounded-lg bg-white hover:bg-slate-50 transition-colors">
        <span class="text-[13px] text-gray-700 font-medium">Enable Micro-Animations</span>
        <div class="relative">
          <input
              type="checkbox"
              :checked="config.animations_enabled !== false"
              @change="config.animations_enabled = $event.target.checked"
              class="sr-only peer"
          >
          <div class="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-500 transition-colors duration-300"></div>
        </div>
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, onMounted, computed, watch } from 'vue';

const config = inject('siteConfig');
const t = inject('t');

const isOpen = ref(false);
const isFontDropdownOpen = ref(false);
const fontSearch = ref('');
const allGoogleFonts = ref([]);
const fontPage = ref(1);
const fontsPerPage = 20;

const availableFonts = [
  'Inter', 'Roboto', 'Open Sans', 'Lato', 'Montserrat', 'Oswald', 'Raleway', 'Poppins' // Fallback список
];

onMounted(async () => {
  try {
    const res = await fetch('https://raw.githubusercontent.com/jonathantneal/google-fonts-complete/master/google-fonts.json');
    const data = await res.json();
    allGoogleFonts.value = Object.keys(data);
  } catch (e) {
    allGoogleFonts.value = availableFonts;
  }
});

const filteredFonts = computed(() => {
  if (!fontSearch.value) return allGoogleFonts.value;
  return allGoogleFonts.value.filter(f => f.toLowerCase().includes(fontSearch.value.toLowerCase()));
});

const visibleFonts = computed(() => filteredFonts.value.slice(0, fontPage.value * fontsPerPage));

const loadGoogleFont = (fontName) => {
  const fontFormatted = fontName.replace(/ /g, '+');
  const linkId = `gfont-lazy-${fontFormatted.toLowerCase()}`;
  if (!document.getElementById(linkId)) {
    const link = document.createElement('link');
    link.id = linkId;
    link.href = `https://fonts.googleapis.com/css2?family=${fontFormatted}:wght@400;600;900&display=swap`;
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }
};

watch(visibleFonts, (newFonts) => {
  newFonts.forEach(font => loadGoogleFont(font));
}, { immediate: true });

watch(fontSearch, () => { fontPage.value = 1; });

const handleFontScroll = (e) => {
  const { scrollTop, clientHeight, scrollHeight } = e.target;
  if (scrollTop + clientHeight >= scrollHeight - 10) {
    if (visibleFonts.value.length < filteredFonts.value.length) fontPage.value++;
  }
};

const selectFont = (font) => {
  config.value.font = font;
  isFontDropdownOpen.value = false;
  fontSearch.value = '';
};
</script>