<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
    <button @click="isOpen = !isOpen" class="w-full p-4 flex justify-between items-center bg-slate-50 hover:bg-slate-100 transition-colors">
      <h3 class="font-bold text-[10px] text-gray-700 uppercase flex items-center">
        <i class="fas fa-images mr-2 text-blue-500"></i> {{ t('editSite.tabs.assets.title') }}
      </h3>
      <i class="fas text-gray-400" :class="isOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
    </button>

    <div v-show="isOpen" class="p-4 border-t border-slate-100 bg-white space-y-4">

      <template v-for="type in ['hero', 'about']" :key="type">
        <div v-if="findBlockByCat(type)" class="space-y-2">
          <h3 class="font-bold text-[9px] text-gray-500 flex justify-between uppercase">
            {{type}} {{ t('editSite.tabs.assets.image') }}
            <span v-if="loadingStates[type]" class="text-blue-500 animate-pulse">{{ t('editSite.tabs.assets.processing') }}</span>
          </h3>
          <div class="h-24 bg-gray-100 rounded-lg overflow-hidden border relative">
            <img :src="findBlockByCat(type)?.props?.image_url || 'https://placehold.co/400x200?text=No+Image'" class="w-full h-full object-cover">
          </div>
          <div class="space-y-2">
            <input v-model="prompts[type]" type="text"
                   :placeholder="t('editSite.tabs.assets.promptPlaceholder') || 'Describe the image...'"
                   class="w-full p-2 border border-indigo-100 rounded bg-indigo-50/30 text-[10px] outline-none focus:border-indigo-400 focus:bg-white transition-colors placeholder-indigo-300"
                   :disabled="loadingStates[type]" @keyup.enter="generateAiAsset(type)">
            <div class="grid grid-cols-2 gap-2">
              <button @click="generateAiAsset(type)" :disabled="loadingStates[type]" class="bg-indigo-50 text-indigo-700 py-2 rounded text-[10px] font-bold border border-indigo-100 hover:bg-indigo-100 transition disabled:opacity-50">
                <i class="fas fa-magic mr-1"></i> AI Generate
              </button>
              <label class="bg-gray-50 text-gray-700 py-2 rounded text-[10px] font-bold border text-center cursor-pointer hover:bg-gray-100 transition flex items-center justify-center" :class="{'opacity-50 pointer-events-none': loadingStates[type]}">
                <i class="fas fa-upload mr-1"></i> Upload
                <input type="file" @change="(e) => uploadAsset(e, type)" class="hidden" :disabled="loadingStates[type]">
              </label>
            </div>
          </div>
        </div>
      </template>

      <div v-if="findBlockByCat('gallery')" class="space-y-2 pt-4 border-t border-slate-100 mt-2">
        <h3 class="font-bold text-[9px] text-gray-500 flex justify-between uppercase">
          Gallery Images (Max 6)
          <span v-if="loadingStates['gallery_upload']" class="text-blue-500 animate-pulse">Uploading...</span>
        </h3>
        <div class="grid grid-cols-2 gap-2">
          <div v-for="(img, idx) in findBlockByCat('gallery').props.images" :key="idx" class="relative group h-20 border rounded-lg overflow-hidden shadow-sm">
            <img :src="img" class="w-full h-full object-cover">
            <button @click="removeGalleryImage(idx)" class="absolute top-1 right-1 bg-red-500/90 hover:bg-red-600 text-white rounded-md w-5 h-5 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all text-[10px]">
              <i class="fas fa-trash"></i>
            </button>
          </div>
          <label v-if="(findBlockByCat('gallery').props.images?.length || 0) < 6" class="h-20 border-dashed border-2 border-slate-200 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:bg-slate-50 transition-colors" :class="{'opacity-50 pointer-events-none': loadingStates['gallery_upload']}">
            <i class="fas text-slate-400 mb-1" :class="loadingStates['gallery_upload'] ? 'fa-spinner fa-spin' : 'fa-plus'"></i>
            <span class="text-[8px] font-bold text-slate-500 uppercase">Upload</span>
            <input type="file" @change="(e) => uploadGalleryAsset(e)" class="hidden" accept="image/*" :disabled="loadingStates['gallery_upload']">
          </label>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue';
import api from '../../../api/client';
import { useSubscription } from '../../../composables/useSubscription';
import { useModal } from '../../../composables/useModal';

const config = inject('siteConfig');
const t = inject('t');
const projectId = inject('projectId');
const { checkLimit, triggerUpgrade } = useSubscription();
const { showAlert, showConfirm } = useModal();

const isOpen = ref(false);
const loadingStates = ref({});
const prompts = ref({ hero: '', about: '' });

const findBlockByCat = (cat) => config.value.blocks?.find(b => (b.category || '').toLowerCase() === cat || (b.type || '').toLowerCase().startsWith(cat));

const uploadAsset = async (e, type) => {
  const file = e.target.files[0];
  if(!file) return;
  loadingStates.value[type] = true;
  const fd = new FormData();
  fd.append('file', file);
  try {
    const res = await api.post(`/${projectId.value}/upload-asset?asset_type=${type}`, fd);
    const freshUrl = `${res.data.url}?t=${Date.now()}`;
    const block = findBlockByCat(type);
    if(block) block.props.image_url = freshUrl;
  } catch(e) {
    showAlert('Error', t('editSite.alerts.uploadFail') || 'File upload failed.', 'error');
  } finally {
    loadingStates.value[type] = false;
    e.target.value = '';
  }
};

const generateAiAsset = async (type) => {
  if (!checkLimit('ai_generations')) {
    return triggerUpgrade(t('editSite.upgrade.aiImage') || "AI requires Starter plan.", 'starter');
  }
  loadingStates.value[type] = true;
  try {
    const res = await api.post(`/${projectId.value}/generate-asset`, {
      asset_type: type, prompt: prompts.value[type]
    });
    const block = findBlockByCat(type);
    if(block) block.props.image_url = `${res.data.url}?t=${Date.now()}`;
    prompts.value[type] = '';
  } catch(e) {
    showAlert('Error', t('editSite.alerts.aiGenError') || 'AI Generation failed.', 'error');
  } finally {
    loadingStates.value[type] = false;
  }
};

const uploadGalleryAsset = async (e) => {
  const file = e.target.files[0];
  if(!file) return;
  loadingStates.value['gallery_upload'] = true;
  const fd = new FormData();
  fd.append('file', file);
  try {
    const res = await api.post(`/${projectId.value}/upload-asset?asset_type=raw_image`, fd);
    const block = findBlockByCat('gallery');
    if(block) {
      if (!block.props.images) block.props.images = [];
      block.props.images.push(`${res.data.url}?t=${Date.now()}`);
    }
  } catch(err) {
    showAlert('Error', 'Upload failed.', 'error');
  } finally {
    loadingStates.value['gallery_upload'] = false;
    e.target.value = '';
  }
};

const removeGalleryImage = async (idx) => {
  if (await showConfirm('Remove image?', 'Are you sure?', 'warning')) {
    const block = findBlockByCat('gallery');
    if(block && block.props.images) block.props.images.splice(idx, 1);
  }
};
</script>