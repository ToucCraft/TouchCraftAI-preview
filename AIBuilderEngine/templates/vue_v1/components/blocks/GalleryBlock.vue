<template>
  <section class="py-24" id="gallery" :style="{ backgroundColor: palette?.background }">
    <div class="container mx-auto px-6">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-black mb-4 leading-tight" :style="{ color: themeColor }">
          {{ props.props.title }}
        </h2>
        <p v-if="props.props.description" class="text-lg opacity-80 max-w-2xl mx-auto" :style="{ color: palette?.text }">
          {{ props.props.description }}
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <div v-for="(img, idx) in props.props.images" :key="idx"
             class="relative group rounded-3xl overflow-hidden shadow-lg aspect-[4/3] bg-slate-100 flex items-center justify-center">
          <img v-if="img" :src="img" class="w-full h-full object-cover" :class="[animationsEnabled ? 'transition-transform duration-500 group-hover:scale-110' : '']">
          <i v-else class="fas fa-image text-4xl text-slate-300"></i>

          <div v-if="animationsEnabled" class="absolute inset-0 bg-black/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps(['props', 'themeColor', 'palette', 't', 'animationsEnabled']);
</script>