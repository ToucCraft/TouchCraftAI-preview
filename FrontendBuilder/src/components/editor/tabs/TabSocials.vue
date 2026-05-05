<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
    <button @click="isOpen = !isOpen" class="w-full p-4 flex justify-between items-center bg-slate-50 hover:bg-slate-100 transition-colors">
      <h3 class="font-bold text-[10px] text-gray-700 uppercase flex items-center">
        <i class="fas fa-hashtag mr-2 text-blue-500"></i> {{ t('editSite.tabs.socials.title') || 'Social Media' }}
      </h3>
      <i class="fas text-gray-400" :class="isOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
    </button>
    <div v-show="isOpen" class="p-4 border-t border-slate-100 bg-white">
      <div class="grid grid-cols-2 gap-2">
        <div v-for="network in availableSocials" :key="network" class="flex items-center gap-2 bg-slate-50 border border-gray-200 rounded-lg px-2 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
          <i :class="`fab fa-${network} text-gray-400 text-[10px]`"></i>
          <input v-model="config.contact.socials[network]" :placeholder="network" class="w-full p-1.5 bg-transparent text-xs outline-none capitalize placeholder-gray-400">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
const config = inject('siteConfig');
const t = inject('t');
const isOpen = ref(false);
const availableSocials = ['instagram', 'x-twitter', 'facebook', 'linkedin', 'youtube', 'tiktok', 'telegram', 'whatsapp'];
</script>