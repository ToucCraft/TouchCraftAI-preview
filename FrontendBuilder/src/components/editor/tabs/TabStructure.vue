<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
    <button @click="isOpen = !isOpen" class="w-full p-4 flex justify-between items-center bg-slate-50 hover:bg-slate-100 transition-colors">
      <h3 class="font-bold text-[10px] text-gray-700 uppercase flex items-center">
        <i class="fas fa-layer-group mr-2 text-blue-500"></i> {{ t('editSite.tabs.structure.title') }}
      </h3>
      <i class="fas text-gray-400" :class="isOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
    </button>

    <div v-show="isOpen" class="p-4 border-t border-slate-100 bg-white space-y-2">
      <div
          v-for="(block, index) in config.blocks"
          :key="block.id || index"
          draggable="true"
          @dragstart="dragStart(index, $event)"
          @dragover.prevent
          @dragenter.prevent="dragEnter(index)"
          @dragend="dragEnd"
          @drop="dropBlock(index)"
          class="flex items-center justify-between bg-slate-50 p-2 rounded border cursor-move transition-all duration-300 ease-in-out"
          :class="{
            'opacity-40 scale-95 border-dashed border-blue-400 bg-blue-50 shadow-inner': draggedIndex === index,
            'mt-8 border-t-2 border-t-blue-500 shadow-md': dragOverIndex === index && draggedIndex > index,
            'mb-8 border-b-2 border-b-blue-500 shadow-md': dragOverIndex === index && draggedIndex < index,
            'hover:bg-slate-100': draggedIndex === null
          }"
      >
        <div class="flex items-center pointer-events-none">
          <i class="fas fa-grip-vertical text-slate-300 mr-3"></i>
          <span class="text-[10px] bg-white border border-slate-200 px-1.5 py-0.5 rounded text-gray-500 mr-2 font-mono">{{index + 1}}</span>
          <span class="text-xs font-bold text-slate-700 uppercase">{{block.type.replace('Block','')}}</span>
        </div>
        <button @click.stop="removeBlock(index)" class="text-red-400 hover:text-red-600">
          <i class="fas fa-trash"></i>
        </button>
      </div>

      <div class="flex gap-2 mt-4 pt-2 border-t border-slate-100 relative">
        <select v-model="selectedNewBlock" class="flex-1 p-2 border rounded text-[10px] bg-slate-50 uppercase font-bold outline-none">
          <option value="hero">{{ t('editSite.blocks.hero') || 'Hero' }}</option>
          <option value="about">{{ t('editSite.blocks.about') || 'About' }}</option>
          <option value="map">{{ t('editSite.blocks.map') || 'Map' }}</option>
          <option value="contacts">{{ t('editSite.blocks.contacts') || 'Contacts' }}</option>
          <option value="features">Features</option>
          <option value="gallery">Gallery</option>
          <option value="faq">FAQ</option>
          <option value="form">Form</option>
        </select>
        <button @click="addBlock" class="bg-gray-800 text-white px-3 py-2 rounded text-[10px] font-bold hover:bg-black uppercase transition-all">
          {{ t('editSite.tabs.structure.addBtn') || 'Add' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
import { useSubscription } from '../../../composables/useSubscription';
import { useModal } from '../../../composables/useModal';

const config = inject('siteConfig');
const t = inject('t');
// Важно: чтобы работала проверка на SMTP для формы, передайте этот стейт из главного файла
const isSmtpConfigured = inject('isSmtpConfigured', false);

const { checkLimit, triggerUpgrade } = useSubscription();
const { showConfirm, showAlert } = useModal();

const isOpen = ref(false);
const draggedIndex = ref(null);
const dragOverIndex = ref(null);
const selectedNewBlock = ref('features');

const dragStart = (index, event) => {
  draggedIndex.value = index;
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move';
    event.dataTransfer.dropEffect = 'move';
  }
};

const dragEnter = (index) => {
  if (draggedIndex.value !== index) dragOverIndex.value = index;
};

const dropBlock = (dropIndex) => {
  if (draggedIndex.value !== null && draggedIndex.value !== dropIndex) {
    const movedBlock = config.value.blocks.splice(draggedIndex.value, 1)[0];
    config.value.blocks.splice(dropIndex, 0, movedBlock);
  }
  draggedIndex.value = null;
  dragOverIndex.value = null;
};

const dragEnd = () => {
  draggedIndex.value = null;
  dragOverIndex.value = null;
};

const removeBlock = async (index) => {
  if (await showConfirm('Remove block?', 'Delete this section?', 'warning')) {
    config.value.blocks.splice(index, 1);
  }
};

const addBlock = () => {
  if (selectedNewBlock.value === 'form') {
    if (!checkLimit('lead_forms')) return triggerUpgrade(t('editSite.upgrade.leadForms'), 'starter');
    if (!isSmtpConfigured.value) return showAlert('Warning', t('editSite.alerts.smtpWarning'), 'warning');
  }

  const defaultProps = {
    hero: { title: t('editSite.defaults.heroTitle'), subtitle: 'Subtitle', cta_text: 'Start', cta_url: '#contacts', image_url: "https://placehold.co/1200x800" },
    features: { title: 'Features', features: [{title: 'Fast', description: 'Speed', icon: "fas fa-bolt"}] },
    about: { title: 'About Us', description: 'Established 2024', image_url: "https://placehold.co/800x600" },
    faq: { title: 'FAQ', faqs: [{question: 'How?', answer: 'Easy'}] },
    form: {
      title: 'Get In Touch', submit_button_text: 'Send',
      fields: [
        { name: "name", label: "Your Name", type: "text", required: true, enabled: true },
        { name: "email", label: "Email", type: "email", required: true, enabled: true },
        { name: "message", label: "Message", type: "textarea", required: true, enabled: true }
      ]
    },
    gallery: { title: 'Gallery', images: ['https://placehold.co/800x600'] },
  };

  const typeMapping = { hero: 'HeroBlock', features: 'FeaturesBlock', about: 'AboutBlock', faq: 'FaqBlock', form: 'FormBlock', gallery: 'GalleryBlock' };

  if(!config.value.blocks) config.value.blocks = [];
  config.value.blocks.push({
    category: 'blocks',
    type: typeMapping[selectedNewBlock.value] || 'HeroBlock',
    id: selectedNewBlock.value + '-' + Date.now(),
    props: defaultProps[selectedNewBlock.value] || {}
  });
};
</script>