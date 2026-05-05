<template>
  <transition name="sidebar">
    <div v-show="isOpen" class="sidebar-container w-96 shrink-0 bg-slate-50 border-r border-gray-200 overflow-y-auto hide-scrollbar p-4 flex flex-col shadow-xl z-20 relative">

      <div class="mb-4 flex items-center justify-between shrink-0">
        <h2 class="text-lg font-black text-gray-800 tracking-tight">{{ t('editSite.sidebar.title') }}</h2>
        <button @click="$emit('save')" class="bg-blue-50 text-blue-600 px-3 py-1.5 rounded-lg text-[10px] font-bold border border-blue-200 hover:bg-blue-100 transition shadow-sm">
          <i class="fas fa-save mr-1"></i> {{ t('editSite.sidebar.saveBtn') }}
        </button>
      </div>

      <div class="flex-1 flex flex-col pb-6 relative">

        <TabAiChat v-model:isOpen="isChatOpen" />

        <transition name="fade-tabs">
          <div v-show="!isChatOpen" class="space-y-3 mt-3">
            <TabContent />
            <TabDesign />
            <TabAnalytics />
            <TabBusiness />
            <TabSocials v-if="config.contact" />
            <TabAssets v-if="hasAssetsBlocks" />
            <TabFavicon />
            <TabStructure />
            <TabForm v-if="formBlock" />
          </div>
        </transition>

      </div>

      <transition name="fade-tabs">
        <button v-show="!isChatOpen" @click="$emit('deploy')" :disabled="isProcessing" class="w-full shrink-0 bg-green-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-green-700 transition shadow-lg mt-2">
          <i class="fas" :class="isProcessing ? 'fa-cog fa-spin' : 'fa-rocket'"></i>
          {{ isProcessing ? t('editSite.publish.building') : t('editSite.publish.publishBtn') }}
        </button>
      </transition>

    </div>
  </transition>
</template>

<script setup>
import { ref, inject, computed } from 'vue';

import TabAiChat from './tabs/TabAiChat.vue';
import TabContent from './tabs/TabContent.vue';
import TabDesign from './tabs/TabDesign.vue';
import TabAnalytics from './tabs/TabAnalytics.vue';
import TabBusiness from './tabs/TabBusiness.vue';
import TabSocials from './tabs/TabSocials.vue';
import TabAssets from './tabs/TabAssets.vue';
import TabFavicon from './tabs/TabFavicon.vue';
import TabStructure from './tabs/TabStructure.vue';
import TabForm from './tabs/TabForm.vue';

defineProps({
  isOpen: { type: Boolean, required: true },
  isProcessing: { type: Boolean, default: false }
});

defineEmits(['save', 'deploy']);

const config = inject('siteConfig');
const t = inject('t');

// Состояние чата (изначально закрыт)
const isChatOpen = ref(false);

const formBlock = computed(() => config.value.blocks?.find(b => b.type === 'FormBlock'));
const findBlockByCat = (cat) => config.value.blocks?.find(b =>
    (b.category || '').toLowerCase() === cat || (b.type || '').toLowerCase().startsWith(cat)
);
const hasAssetsBlocks = computed(() => {
  return findBlockByCat('hero') || findBlockByCat('about') || findBlockByCat('gallery');
});
</script>

<style scoped>
.sidebar-container {
  width: 24rem;
  transform-origin: left;
}

/* Анимация панели */
.sidebar-enter-active,
.sidebar-leave-active {
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
  margin-left 0.5s cubic-bezier(0.4, 0, 0.2, 1),
  opacity 0.4s ease;
}
.sidebar-enter-from,
.sidebar-leave-to {
  opacity: 0;
  transform: translateX(-100%);
  margin-left: -24rem;
}

/* Анимация исчезновения табов */
.fade-tabs-enter-active,
.fade-tabs-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-tabs-enter-from,
.fade-tabs-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>