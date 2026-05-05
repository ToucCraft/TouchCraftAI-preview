<template>
  <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
  >
    <div v-if="isOpen" class="fixed inset-0 z-[200] flex items-center justify-center bg-gray-900/60 backdrop-blur-sm px-4">
      <div class="bg-white rounded-3xl p-8 max-w-sm w-full shadow-2xl relative text-center">
        <button @click="closeAlert(false)" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition">
          <i class="fas fa-times text-xl"></i>
        </button>

        <div :class="iconWrapperClass" class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">
          <i :class="iconClass"></i>
        </div>

        <h3 class="text-2xl font-black text-gray-800 mb-2">{{ title }}</h3>
        <p class="text-gray-500 mb-6 font-medium">{{ message }}</p>

        <div v-if="isConfirm" class="flex gap-3">
          <button @click="closeAlert(false)" class="flex-1 bg-gray-100 text-gray-600 py-3 rounded-xl font-bold text-lg hover:bg-gray-200 transition">
            {{ t('modal.cancel') || 'Cancel' }}
          </button>
          <button @click="closeAlert(true)" :class="buttonClass" class="flex-1 text-white py-3 rounded-xl font-bold text-lg transition shadow-lg">
            {{ t('modal.confirm') || 'Confirm' }}
          </button>
        </div>

        <button v-else @click="closeAlert(true)" :class="buttonClass" class="w-full text-white py-3 rounded-xl font-bold text-lg transition shadow-lg">
          {{ t('modal.ok') || 'OK' }}
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { useModal } from '../composables/useModal';

const { isOpen, title, message, type, isConfirm, closeAlert } = useModal();

// --- I18N LOGIC ---
const currentLang = ref(localStorage.getItem('app_lang') || 'en');
const translations = ref({});

const loadTranslations = async (lang) => {
  try {
    const response = await fetch(`/i18n/${lang}.json`);
    if (response.ok) {
      translations.value = await response.json();
    } else {
      if (lang !== 'en') await loadTranslations('en');
    }
  } catch (error) {
    console.error(error);
  }
};

const t = (key) => {
  const keys = key.split('.');
  let value = translations.value;
  for (const k of keys) {
    if (value && Object.prototype.hasOwnProperty.call(value, k)) {
      value = value[k];
    } else return key;
  }
  return value;
};

onMounted(() => {
  loadTranslations(currentLang.value);
});
// ------------------

// Стили для иконки в зависимости от типа
const iconWrapperClass = computed(() => {
  switch (type.value) {
    case 'success': return 'bg-green-50 text-green-500';
    case 'error': return 'bg-red-50 text-red-500';
    case 'warning': return 'bg-yellow-50 text-yellow-500';
    default: return 'bg-blue-50 text-blue-500'; // info
  }
});

const iconClass = computed(() => {
  switch (type.value) {
    case 'success': return 'fas fa-check-circle';
    case 'error': return 'fas fa-exclamation-circle';
    case 'warning': return 'fas fa-exclamation-triangle';
    default: return 'fas fa-info-circle'; // info
  }
});

// Стили для кнопки в зависимости от типа
const buttonClass = computed(() => {
  switch (type.value) {
    case 'success': return 'bg-green-500 hover:bg-green-600';
    case 'error': return 'bg-red-500 hover:bg-red-600';
    case 'warning': return 'bg-yellow-500 hover:bg-yellow-600';
    default: return 'bg-blue-600 hover:bg-blue-700'; // info
  }
});
</script>