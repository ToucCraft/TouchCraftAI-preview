<template>
  <section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-gray-900 text-white">
    <div class="absolute inset-0 z-0">
      <img v-if="props.props.image_url" :src="props.props.image_url" class="w-full h-full object-cover opacity-50" alt="Hero background" />
    </div>

    <div class="container mx-auto px-6 relative z-10 text-center" :class="[animationsEnabled ? 'animate-fade-in-up' : '']">
      <h1 class="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight break-words">{{ props.props.title }}</h1>
      <p class="text-xl md:text-2xl mb-10 text-gray-200 max-w-3xl mx-auto">{{ props.props.subtitle }}</p>

      <a :href="props.props.cta_url || '#contacts'"
         :target="props.props.cta_url && props.props.cta_url.startsWith('http') ? '_blank' : '_self'"
         @click="handleScroll"
         :style="{ backgroundColor: themeColor }"
         :class="[animationsEnabled ? 'hover:-translate-y-1 hover:shadow-2xl transition-all duration-300' : '']"
         class="px-10 py-4 rounded-full font-bold text-lg inline-block cursor-pointer">
        {{ props.props.cta_text }}
      </a>
    </div>
  </section>
</template>

<script setup>
const props = defineProps(['props', 'themeColor', 'animationsEnabled']);

const handleScroll = (e) => {
  const targetUrl = props.props.cta_url || '#contacts';
  if (targetUrl.startsWith('#')) {
    e.preventDefault();
    const targetElement = document.querySelector(targetUrl);
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
};
</script>