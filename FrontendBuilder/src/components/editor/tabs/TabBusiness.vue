<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
    <button @click="isOpen = !isOpen" class="w-full p-4 flex justify-between items-center bg-slate-50 hover:bg-slate-100 transition-colors">
      <h3 class="font-bold text-[10px] text-gray-700 uppercase flex items-center">
        <i class="fas fa-building mr-2 text-blue-500"></i> {{ t('editSite.tabs.business.title') || 'Business Details' }}
      </h3>
      <i class="fas text-gray-400" :class="isOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
    </button>
    <div v-show="isOpen" class="p-4 border-t border-slate-100 bg-white space-y-2">
      <input v-model="config.business_name" :placeholder="t('editSite.tabs.business.businessName') || 'Business Name'" class="w-full p-2 border rounded-lg text-xs outline-none focus:ring-1 focus:ring-blue-500 bg-slate-50">
      <input v-model="config.contact.legal_name" :placeholder="t('editSite.tabs.business.legalName') || 'Legal Name'" class="w-full p-2 border rounded-lg text-xs outline-none focus:ring-1 focus:ring-blue-500 bg-slate-50">
      <input v-model="config.contact.email" :placeholder="t('editSite.tabs.business.email') || 'Email'" class="w-full p-2 border rounded-lg text-xs outline-none focus:ring-1 focus:ring-blue-500 bg-slate-50">
      <input v-model="config.contact.phone" :placeholder="t('editSite.tabs.business.phone') || 'Phone'" class="w-full p-2 border rounded-lg text-xs outline-none focus:ring-1 focus:ring-blue-500 bg-slate-50">
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
const config = inject('siteConfig');
const t = inject('t');
const isOpen = ref(false);
</script>