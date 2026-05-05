<template>
  <section class="py-24" id="about" :style="{ backgroundColor: palette?.background }">
    <div class="container mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">
      <div>
        <h2 class="text-3xl md:text-4xl font-black mb-6 leading-tight break-words" :style="{ color: themeColor }">
          {{ props.props.title }}
        </h2>
        <p class="text-lg leading-relaxed mb-8" :style="{ color: palette?.text }">
          {{ props.props.description }}
        </p>
      </div>
      <div class="relative group">
        <img v-if="props.props.image_url" :src="props.props.image_url"
             :class="[animationsEnabled ? 'group-hover:scale-[1.02] group-hover:shadow-2xl group-hover:-rotate-1 transition-all duration-500' : '']"
             class="relative rounded-[2rem] shadow-xl w-full object-cover aspect-video" alt="About Us" />
        <div v-else class="relative rounded-[2rem] shadow-xl w-full aspect-video bg-slate-200 flex items-center justify-center">
          <i class="fas fa-image text-5xl text-slate-400"></i>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps(['props', 'themeColor', 'palette', 'animationsEnabled']);
</script>