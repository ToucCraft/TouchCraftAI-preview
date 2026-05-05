<template>
  <section class="py-16 md:py-24" id="contacts">
    <div class="container mx-auto px-4 md:px-6 text-center">
      <h2 class="text-3xl md:text-4xl font-black mb-12 md:mb-16">{{ props.props.title }}</h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 max-w-5xl mx-auto">
        <div class="p-8 md:p-10 rounded-[2rem] border shadow-sm bg-white"
             :class="[animationsEnabled ? 'hover:scale-105 hover:shadow-xl transition-all duration-300' : '']"
             :style="{ borderColor: themeColor + '40', backgroundColor: themeColor + '05' }">
          <i class="fas fa-phone text-3xl md:text-4xl mb-4 md:mb-6" :style="{ color: themeColor }"></i>
          <h4 class="font-bold text-lg md:text-xl mb-2">Phone</h4>
          <p class="text-sm md:text-base opacity-80">{{ props.props.phone }}</p>
        </div>

        <div class="p-8 md:p-10 rounded-[2rem] border shadow-sm bg-white"
             :class="[animationsEnabled ? 'hover:scale-105 hover:shadow-xl transition-all duration-300' : '']"
             :style="{ borderColor: themeColor + '40', backgroundColor: themeColor + '05' }">
          <i class="fas fa-envelope text-3xl md:text-4xl mb-4 md:mb-6" :style="{ color: themeColor }"></i>
          <h4 class="font-bold text-lg md:text-xl mb-2">Email</h4>
          <p class="text-sm md:text-base opacity-80 break-words">{{ props.props.email }}</p>
        </div>

        <div class="p-8 md:p-10 rounded-[2rem] border shadow-sm bg-white"
             :class="[animationsEnabled ? 'hover:scale-105 hover:shadow-xl transition-all duration-300' : '']"
             :style="{ borderColor: themeColor + '40', backgroundColor: themeColor + '05' }">
          <i class="fas fa-map-marker-alt text-3xl md:text-4xl mb-4 md:mb-6" :style="{ color: themeColor }"></i>
          <h4 class="font-bold text-lg md:text-xl mb-2">Address</h4>
          <p class="text-sm md:text-base opacity-80">{{ props.props.address }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps(['props', 'themeColor', 'palette', 'animationsEnabled']);
</script>