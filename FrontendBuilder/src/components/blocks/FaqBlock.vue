<template>
  <section class="py-24" id="faq" :style="{ backgroundColor: palette?.background }">
    <div class="container mx-auto px-6 max-w-4xl">
      <h2 class="text-3xl md:text-4xl font-black mb-6 leading-tight break-words" :style="{ color: themeColor }">{{ props.props.title }}</h2>

      <div class="border-t">
        <div v-for="(faq, i) in props.props.faqs" :key="i" class="border-b">
          <button
              @click="toggle(i)"
              :style="{ '--hover-color': themeColor || palette?.primary || '#3B82F6' }"
              class="w-full py-6 flex justify-between items-center text-left group focus:outline-none"
              :class="[animationsEnabled ? 'hover:text-[var(--hover-color)] transition-colors' : '']"
          >
            <span
                class="text-lg md:text-xl font-bold pr-8 break-words"
                :class="[animationsEnabled ? 'transition-colors duration-300' : '']"
                :style="{ color: activeIndex === i ? (themeColor || '#3B82F6') : '' }"
            >
              {{ faq.question }}
            </span>
            <i
                class="fas fa-chevron-down text-slate-400"
                :class="[animationsEnabled ? 'transition-transform duration-300' : '', activeIndex === i ? 'rotate-180' : '']"
            ></i>
          </button>

          <transition
              :name="animationsEnabled ? 'faq-slide' : ''"
              @enter="startTransition"
              @after-enter="endTransition"
              @before-leave="startTransition"
              @after-leave="endTransition"
          >
            <div v-if="activeIndex === i" class="overflow-hidden" :class="[animationsEnabled ? 'transition-all duration-300 ease-in-out' : '']">
              <div class="pb-8 text-slate-600 text-lg leading-relaxed max-w-3xl">
                {{ faq.answer }}
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps(['props', 'themeColor', 'palette', 'animationsEnabled']);
const activeIndex = ref(null);

const toggle = (index) => {
  activeIndex.value = activeIndex.value === index ? null : index;
};

const startTransition = (el) => {
  if (props.animationsEnabled) el.style.height = el.scrollHeight + 'px';
};
const endTransition = (el) => {
  if (props.animationsEnabled) el.style.height = '';
};
</script>

<style scoped>
.faq-slide-enter-active,
.faq-slide-leave-active {
  transition: all 0.3s ease-in-out;
}
.faq-slide-enter-from,
.faq-slide-leave-to {
  opacity: 0;
  height: 0 !important;
}
</style>