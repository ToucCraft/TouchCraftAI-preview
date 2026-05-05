<template>
  <div v-if="isI18nLoaded" class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 mb-8">
    <div class="flex items-center mb-6">
      <div class="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center text-green-600 mr-4">
        <i class="fas fa-life-ring text-xl"></i>
      </div>
      <div>
        <h2 class="text-xl font-black text-gray-800">{{ t('support.title', 'Support & Contact') }}</h2>
        <p class="text-sm text-gray-500">{{ t('support.subtitle', 'Found a bug or have a question? Let us know!') }}</p>
      </div>
    </div>

    <form @submit.prevent="submitForm" class="space-y-5">
      <div>
        <label class="block text-xs font-bold text-gray-600 uppercase mb-2">{{ t('support.labels.subject', 'Topic / Issue Type') }}</label>
        <select v-model="form.subject" required class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-green-500 focus:bg-white transition-all text-sm font-medium">
          <option value="Question">{{ t('support.topics.question', 'General Question') }}</option>
          <option value="Bug Report">{{ t('support.topics.bug', 'Bug Report') }}</option>
          <option value="Feature Request">{{ t('support.topics.feature', 'Feature Request') }}</option>
          <option value="Billing Issue">{{ t('support.topics.billing', 'Billing Issue') }}</option>
          <option value="Other">{{ t('support.topics.other', 'Other') }}</option>
        </select>
      </div>

      <div>
        <label class="block text-xs font-bold text-gray-600 uppercase mb-2">{{ t('support.labels.message', 'Your Message') }}</label>
        <textarea v-model="form.message" rows="5" :placeholder="t('support.placeholders.message', 'Please describe your issue in detail...')" required
                  class="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-green-500 focus:bg-white transition-all text-sm resize-none"></textarea>
      </div>

      <div>
        <label class="block text-xs font-bold text-gray-600 uppercase mb-2">{{ t('support.labels.attachments', 'Attachments (Optional)') }}</label>
        <div class="flex items-center justify-center w-full">
          <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-xl cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
            <div class="flex flex-col items-center justify-center pt-5 pb-6 text-gray-500">
              <i class="fas fa-cloud-upload-alt text-2xl mb-2"></i>
              <p class="text-sm"><span class="font-bold">{{ t('support.upload.click', 'Click to upload') }}</span> {{ t('support.upload.drag', 'or drag and drop') }}</p>
              <p class="text-xs text-gray-400 mt-1">{{ t('support.upload.formats', 'SVG, PNG, JPG or PDF (Max. 5MB)') }}</p>
            </div>
            <input type="file" class="hidden" multiple @change="handleFileUpload" accept="image/*,.pdf" />
          </label>
        </div>

        <div v-if="selectedFiles.length > 0" class="mt-3 space-y-2">
          <div v-for="(file, index) in selectedFiles" :key="index" class="flex items-center justify-between p-2 bg-gray-50 border border-gray-200 rounded-lg text-xs">
            <span class="truncate text-gray-600 font-medium"><i class="fas fa-file-alt mr-2 text-green-500"></i>{{ file.name }}</span>
            <button @click.prevent="removeFile(index)" class="text-red-400 hover:text-red-600 p-1"><i class="fas fa-times"></i></button>
          </div>
        </div>
      </div>

      <div class="pt-4 border-t border-gray-100 flex items-center justify-end">
        <button type="submit" :disabled="isLoading"
                class="bg-green-600 text-white px-6 py-3 rounded-xl font-bold text-sm hover:bg-green-700 transition shadow-md disabled:opacity-50 flex items-center">
          <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
          <i v-else class="fas fa-paper-plane mr-2"></i>
          {{ isLoading ? t('support.buttons.sending', 'Sending...') : t('support.buttons.send', 'Send Message') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/client';
import { useModal } from '../composables/useModal';

const { showAlert } = useModal();

// --- I18N LOGIC ---
const currentLang = ref(localStorage.getItem('app_lang') || 'en');
const translations = ref({});
const isI18nLoaded = ref(false);

const loadTranslations = async (lang) => {
  try {
    const response = await fetch(`/i18n/${lang}.json`);
    if (response.ok) {
      translations.value = await response.json();
    }
  } catch (error) {
    console.warn("Error loading translations", error);
  } finally {
    isI18nLoaded.value = true;
  }
};

const t = (key, fallback) => {
  const keys = key.split('.');
  let value = translations.value;
  for (const k of keys) {
    if (value && Object.prototype.hasOwnProperty.call(value, k)) {
      value = value[k];
    } else return fallback;
  }
  return value || fallback;
};

onMounted(() => {
  loadTranslations(currentLang.value);
});

const isLoading = ref(false);
const selectedFiles = ref([]);
const form = ref({
  subject: '',
  message: ''
});

const handleFileUpload = (event) => {
  const files = Array.from(event.target.files);
  if (selectedFiles.value.length + files.length > 5) {
    showAlert(
        t('support.alerts.fileLimitTitle', 'Warning'),
        t('support.alerts.fileLimitMsg', 'You can upload a maximum of 5 files.'),
        'warning'
    );
    return;
  }
  selectedFiles.value = [...selectedFiles.value, ...files];
  event.target.value = '';
};

const removeFile = (index) => {
  selectedFiles.value.splice(index, 1);
};

const submitForm = async () => {
  if (!form.value.subject || !form.value.message) return;

  isLoading.value = true;

  const formData = new FormData();
  formData.append('subject', form.value.subject);
  formData.append('message', form.value.message);

  selectedFiles.value.forEach(file => {
    formData.append('files', file);
  });

  try {
    await api.post('/user/support', formData);
    showAlert(
        t('support.alerts.successTitle', 'Success'),
        t('support.alerts.successMsg', 'Your message has been sent successfully!'),
        'success'
    );
    form.value.subject = '';
    form.value.message = '';
    selectedFiles.value = [];
  } catch (e) {
    console.error(e);
    showAlert(
        t('support.alerts.errorTitle', 'Error'),
        t('support.alerts.errorMsg', 'Failed to send message. Please try again later.'),
        'error'
    );
  } finally {
    isLoading.value = false;
  }
};
</script>