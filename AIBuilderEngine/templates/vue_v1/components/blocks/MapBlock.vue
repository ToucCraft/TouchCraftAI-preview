<template>
  <section class="py-24" id="map" :style="{ backgroundColor: palette?.background }">
    <div class="container mx-auto px-6">
      <div class="grid md:grid-cols-2 gap-16 items-center">
        <div>
          <h2 class="text-4xl font-black mb-6 leading-tight" :style="{ color: themeColor }">
            {{ props.props.title || 'Find Us' }}
          </h2>
          <div class="flex items-start space-x-4 mb-8 group cursor-pointer">
            <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-white shadow-lg shrink-0"
                 :class="[animationsEnabled ? 'group-hover:scale-110 group-hover:rotate-6 transition-all duration-300' : '']"
                 :style="{ backgroundColor: themeColor || '#3B82F6' }">
              <i class="fas fa-location-dot"></i>
            </div>
            <div>
              <h4 class="font-bold text-xl text-slate-800 break-words" :style="{ color: themeColor }">
                {{ props.props.location_text || (t ? t('Map') : 'Our Location') }}
              </h4>
              <p class="text-slate-500 mt-1 leading-relaxed">{{ props.props.address }}</p>
            </div>
          </div>
        </div>

        <div class="h-[450px] bg-slate-200 rounded-[2rem] overflow-hidden shadow-2xl border-8"
             :class="[animationsEnabled ? 'hover:shadow-blue-500/20 transition-shadow duration-500' : '']"
             :style="{ borderColor: palette?.primary }">
          <iframe
              width="100%"
              height="100%"
              frameborder="0"
              style="border:0"
              :src="mapUrl"
              allowfullscreen>
          </iframe>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps(['props', 'themeColor', 'palette', 't', 'animationsEnabled']);

const mapUrl = computed(() => {
  const address = encodeURIComponent(props.props.address);
  const apiKey = 'AIzaSyCvEBglqS4fW2OY9Dy6dMTIuaOFm9YH6bA';
  return `https://www.google.com/maps/embed/v1/place?key=${apiKey}&q=${address}`;
});
</script>