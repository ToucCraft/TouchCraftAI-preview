<template>
  <section class="py-24" id="features" :style="{ backgroundColor: palette?.background }">
    <div class="container mx-auto px-6">
      <h2 class="text-3xl md:text-4xl font-black mb-4 leading-tight break-words" :style="{ color: palette?.primary }">{{ props.props.title }}</h2>
      <div class="grid md:grid-cols-3 gap-12">
        <div v-for="(feature, i) in props.props.features" :key="i"
             class="p-8 rounded-2xl border bg-white"
             :class="[animationsEnabled ? 'hover:shadow-2xl hover:-translate-y-2 transition-all duration-300' : '']"
             :style="{ borderColor: palette?.secondary }">
          <div :style="{ color: themeColor }" class="text-4xl mb-4" :class="[animationsEnabled ? 'transform hover:scale-110 transition-transform duration-300' : '']">
            <i :class="feature.icon || 'fas fa-star'"></i>
          </div>
          <h3 class="text-xl md:text-2xl font-bold mb-4 break-words">{{ feature.title }}</h3>
          <p class="text-lg leading-relaxed mb-8" :style="{ color: palette?.text }">{{ feature.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps(['props', 'themeColor', 'palette', 'animationsEnabled']);
</script>