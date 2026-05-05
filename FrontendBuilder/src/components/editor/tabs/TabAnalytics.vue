<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden mt-3">
    <button @click="isOpen = !isOpen" class="w-full p-4 flex justify-between items-center bg-slate-50 hover:bg-slate-100 transition-colors">
      <h3 class="font-bold text-[10px] text-gray-700 uppercase flex items-center">
        <i class="fas fa-chart-line mr-2 text-blue-500"></i> Analytics & Cookies
      </h3>
      <i class="fas text-gray-400" :class="isOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
    </button>
    <div v-show="isOpen" class="p-4 border-t border-slate-100 bg-white space-y-4">
      <div>
        <label class="text-[9px] font-bold text-gray-500 uppercase mb-2 block">
          Google Analytics 4 (GA4) ID
        </label>
        <input
            v-model="config.analytics_id"
            placeholder="G-XXXXXXXXXX"
            class="w-full p-2 border rounded-lg text-xs outline-none focus:ring-1 focus:ring-blue-500 bg-slate-50 font-mono"
        >
      </div>
      <div class="flex items-center gap-2 pt-2 border-t border-slate-100">
        <input type="checkbox" v-model="config.cookie_banner" id="cookieBannerToggle" class="w-3.5 h-3.5 cursor-pointer text-blue-600 rounded border-gray-300">
        <label for="cookieBannerToggle" class="text-[10px] font-bold text-gray-600 cursor-pointer uppercase">
          Show Cookie Consent Banner
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';

const config = inject('siteConfig');
const isOpen = ref(false);
</script>