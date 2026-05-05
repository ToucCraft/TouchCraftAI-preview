<template>
  <div class="bg-white rounded-xl border border-blue-200 shadow-sm overflow-hidden">
    <button @click="isOpen = !isOpen" class="w-full p-4 flex justify-between items-center bg-blue-50 hover:bg-blue-100 transition-colors">
      <h3 class="font-bold text-[10px] text-blue-700 uppercase flex items-center">
        <i class="fas fa-tasks mr-2 text-blue-500"></i> {{ t('editSite.tabs.form.title') || 'Form Settings' }}
      </h3>
      <i class="fas text-blue-400" :class="isOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
    </button>
    <div v-show="isOpen" class="p-4 border-t border-blue-100 bg-white space-y-3">
      <div v-for="field in formBlock.props.fields" :key="field.name" class="bg-slate-50 p-3 rounded-lg border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-2">
          <span class="text-[10px] font-black text-gray-500 uppercase">{{ field.name }}</span>
          <div class="flex items-center gap-2">
            <input type="checkbox" v-model="field.enabled" class="w-3 h-3">
            <span class="text-[9px] font-bold uppercase text-gray-500">{{ t('editSite.tabs.form.show') || 'Show' }}</span>
          </div>
        </div>
        <input v-model="field.label" class="w-full p-2 bg-white border rounded text-[11px] outline-none focus:border-blue-500" :placeholder="t('editSite.tabs.form.labelPlaceholder')">
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed } from 'vue';

const config = inject('siteConfig');
const t = inject('t');
const isOpen = ref(false);

const formBlock = computed(() => config.value.blocks?.find(b => b.type === 'FormBlock'));
</script>