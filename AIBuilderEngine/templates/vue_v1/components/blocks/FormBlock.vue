<template>
  <section class="py-16 md:py-24" id="form" :style="{ backgroundColor: palette?.background }">
    <div class="container mx-auto px-4 md:px-6 max-w-2xl text-center">
      <h2 class="text-3xl md:text-4xl font-black mb-4 leading-tight" :style="{ color: palette?.primary }">
        {{ props.props?.title || safeT('Contact Us') }}
      </h2>
      <p class="text-base md:text-lg opacity-80 mb-10">
        {{ props.props?.subtitle || safeT('form_subtitle') || 'Please fill out the form below to get in touch.' }}
      </p>

      <form @submit.prevent="submitForm" class="text-left bg-white p-6 md:p-10 rounded-[2rem] shadow-xl border"
            :class="[animationsEnabled ? 'hover:shadow-2xl transition-shadow duration-500' : '']"
            :style="{ borderColor: themeColor + '30' }">

        <div class="opacity-0 absolute -z-50 h-0 w-0 overflow-hidden" aria-hidden="true">
          <label>{{ safeT('form_leave_empty') || 'Leave this field empty' }}</label>
          <input type="text" v-model="honeypot" tabindex="-1" autocomplete="off">
        </div>

        <div v-for="field in visibleFields" :key="field.name" class="mb-5">
          <label class="block text-sm font-bold mb-2 opacity-80">
            {{ field.label }} <span v-if="field.required" class="text-red-500">*</span>
          </label>

          <textarea
              v-if="field.type === 'textarea'"
              v-model="formData[field.name]"
              :required="field.required"
              class="w-full p-4 rounded-xl border outline-none bg-slate-50 focus:bg-white shadow-inner"
              :class="[animationsEnabled ? 'transition-all duration-300' : '']"
              :style="{ borderColor: focusedField === field.name ? themeColor : '#e2e8f0' }"
              @focus="focusedField = field.name"
              @blur="focusedField = null"
              rows="4"
          ></textarea>

          <input
              v-else
              :type="field.type === 'phone' ? 'tel' : field.type"
              v-model="formData[field.name]"
              :required="field.required"
              class="w-full p-4 rounded-xl border outline-none bg-slate-50 focus:bg-white shadow-inner"
              :class="[animationsEnabled ? 'transition-all duration-300' : '']"
              :style="{ borderColor: focusedField === field.name ? themeColor : '#e2e8f0' }"
              @focus="focusedField = field.name"
              @blur="focusedField = null"
          >
        </div>

        <div class="mb-2 p-4 rounded-xl border bg-slate-50 flex items-center justify-between"
             :class="[animationsEnabled ? 'transition-colors duration-300' : '']"
             :style="{ borderColor: captchaError ? '#ef4444' : themeColor + '30' }">
          <label class="text-sm font-bold opacity-80 flex-1">
            <i class="fas fa-shield-alt mr-2 text-slate-400" :class="[animationsEnabled && focusedField === 'captcha' ? 'animate-pulse' : '']"></i>
            {{ safeT('form_math_question') || 'How much is' }} {{ captchaNum1 }} + {{ captchaNum2 }}? <span class="text-red-500">*</span>
          </label>
          <input
              type="number"
              v-model="userCaptcha"
              required
              class="w-20 p-2 rounded-lg border outline-none text-center font-bold bg-white"
              :class="[animationsEnabled ? 'transition-colors duration-300' : '']"
              :style="{ borderColor: captchaError ? '#ef4444' : '#e2e8f0' }"
              @focus="focusedField = 'captcha'; captchaError = false"
              @blur="focusedField = null"
          >
        </div>

        <transition :name="animationsEnabled ? 'fade' : ''">
          <p v-if="captchaError" class="text-red-500 text-xs font-bold mb-4 mt-2 px-2">
            {{ safeT('form_math_error') || 'Incorrect answer, please try again.' }}
          </p>
        </transition>

        <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full py-4 mt-4 rounded-xl font-bold text-white shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
            :class="[animationsEnabled ? 'hover:shadow-lg hover:-translate-y-1 transition-all duration-300' : '']"
            :style="{ backgroundColor: themeColor }"
        >
          <i v-if="isSubmitting" class="fas fa-spinner fa-spin mr-2"></i>
          {{ isSubmitting ? (safeT('form_sending') || 'Sending...') : (props.props?.submit_button_text || safeT('form_submit') || 'Submit') }}
        </button>

        <transition :name="animationsEnabled ? 'fade' : ''">
          <div v-if="statusMessage" :class="`mt-6 p-4 rounded-xl text-center font-bold text-sm ${statusType === 'success' ? 'bg-green-50 text-green-600 border border-green-200' : 'bg-red-50 text-red-600 border border-red-200'}`">
            {{ statusMessage }}
          </div>
        </transition>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps(['props', 'themeColor', 'palette', 't', 'animationsEnabled']);

const safeT = (key) => props.t ? props.t(key) : key;

const formData = ref({});
const focusedField = ref(null);
const isSubmitting = ref(false);
const statusMessage = ref('');
const statusType = ref('');

const honeypot = ref('');
const captchaNum1 = ref(0);
const captchaNum2 = ref(0);
const userCaptcha = ref('');
const captchaError = ref(false);

const generateCaptcha = () => {
  captchaNum1.value = Math.floor(Math.random() * 10) + 1;
  captchaNum2.value = Math.floor(Math.random() * 10) + 1;
  userCaptcha.value = '';
};

onMounted(() => {
  generateCaptcha();
});

const visibleFields = computed(() => {
  if (!props.props?.fields) return [];
  return props.props.fields.filter(f => f.enabled);
});

const submitForm = async () => {
  if (honeypot.value !== '') {
    statusType.value = 'success';
    statusMessage.value = safeT('form_success') || 'Thank you! Your message has been sent successfully.';
    formData.value = {};
    return;
  }

  if (parseInt(userCaptcha.value) !== (captchaNum1.value + captchaNum2.value)) {
    captchaError.value = true;
    generateCaptcha();
    return;
  }

  isSubmitting.value = true;
  statusMessage.value = '';
  captchaError.value = false;

  try {
    const projectId = window.PROJECT_ID || 'default_id';
    const res = await fetch(`https://api-builder.touch-craft.com/api/v1/${projectId}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ form_data: formData.value })
    });

    if (!res.ok) throw new Error('Server error');

    statusType.value = 'success';
    statusMessage.value = safeT('form_success') || 'Thank you! Your message has been sent successfully.';
    formData.value = {};
    generateCaptcha();

    setTimeout(() => { statusMessage.value = ''; }, 5000);
  } catch (error) {
    statusType.value = 'error';
    statusMessage.value = safeT('form_error') || 'An error occurred while sending. Please try again later.';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>