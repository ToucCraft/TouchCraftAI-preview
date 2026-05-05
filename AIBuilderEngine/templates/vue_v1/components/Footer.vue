<template>
  <footer
      class="border-t pt-16 pb-8 transition-colors duration-300"
      :style="{
      backgroundColor: palette?.background,
      color: palette?.text
    }"
  >
    <div class="container mx-auto px-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
        <div class="col-span-1 md:col-span-2">

          <div class="flex items-center gap-3 mb-4">
            <img v-if="(logoMode === 'logo' || logoMode === 'both') && logoUrl && !applyThemeColorToLogo"
                 :src="logoUrl"
                 class="h-10 max-w-[200px] object-contain"
                 alt="Logo">

            <div v-if="(logoMode === 'logo' || logoMode === 'both') && logoUrl && applyThemeColorToLogo"
                 class="h-10 w-10 md:w-12"
                 :style="{
                   backgroundColor: themeColor,
                   maskImage: `url(${logoUrl})`, WebkitMaskImage: `url(${logoUrl})`,
                   maskSize: 'contain', WebkitMaskSize: 'contain',
                   maskRepeat: 'no-repeat', WebkitMaskRepeat: 'no-repeat',
                   maskPosition: 'left center', WebkitMaskPosition: 'left center'
                 }">
            </div>

            <div v-if="(!logoUrl) || logoMode === 'text' || logoMode === 'both'"
                 class="text-xl font-black tracking-tight break-words"
                 :style="{ color: themeColor }">
              {{ businessName }}
            </div>
          </div>
          <p class="max-w-sm mb-8 leading-relaxed opacity-70">
            {{ t ? t('footer_desc') : 'We deliver exceptional digital experiences tailored for your business needs.' }}
          </p>

          <div v-if="contact" class="space-y-3 text-sm font-medium opacity-90">
            <div v-if="contact.email" class="flex items-center">
              <i class="fas fa-envelope w-5" :style="{ color: themeColor }"></i>
              <a :href="'mailto:' + contact.email" class="hover:opacity-70 transition-opacity break-all">{{ contact.email }}</a>
            </div>
            <div v-if="contact.phone" class="flex items-center">
              <i class="fas fa-phone w-5" :style="{ color: themeColor }"></i>
              <a :href="'tel:' + contact.phone" class="hover:opacity-70 transition-opacity">{{ contact.phone }}</a>
            </div>
            <div v-if="contact.address" class="flex items-center">
              <i class="fas fa-map-marker-alt w-5" :style="{ color: themeColor }"></i>
              {{ contact.address }}
            </div>
            <div v-if="contact.tax_id" class="flex items-center">
              <i class="fas fa-file-invoice w-5" :style="{ color: themeColor }"></i>
              NIF/VAT: {{ contact.tax_id }}
            </div>
          </div>
        </div>

        <div>
          <h4 class="font-bold mb-6 uppercase tracking-widest text-xs" :style="{ color: palette?.text }">
            {{ t ? t('quick_links') : 'Quick Links' }}
          </h4>
          <ul class="space-y-3 text-sm font-medium opacity-70">
            <li><a href="#" @click.prevent="$emit('navigate', 'home')" class="hover:opacity-100 transition-opacity">{{ t ? t('Home') : 'Home' }}</a></li>
            <li><a href="#about" @click.prevent="$emit('navigate', 'home')" class="hover:opacity-100 transition-opacity">{{ t ? t('About') : 'About Us' }}</a></li>
            <li><a href="#features" @click.prevent="$emit('navigate', 'home')" class="hover:opacity-100 transition-opacity">{{ t ? t('Features') : 'Features' }}</a></li>
            <li><a href="#" @click.prevent="$emit('navigate', 'privacy')" class="hover:opacity-100 transition-opacity">{{ t ? t('Privacy Policy') : 'Privacy Policy' }}</a></li>
          </ul>
        </div>

        <div v-if="hasSocials">
          <h4 class="font-bold mb-6 uppercase tracking-widest text-xs" :style="{ color: palette?.text }">
            {{ t ? t('follow_us') : 'Follow Us' }}
          </h4>
          <div class="flex flex-wrap gap-4">
            <a
                v-for="(url, network) in contact.socials"
                :key="network"
                :href="url"
                target="_blank"
                class="hover:-translate-y-1 transition-all transform flex items-center justify-center w-10 h-10 rounded-full border shadow-sm"
                :style="{
                  backgroundColor: isDarkBackground ? 'rgba(255,255,255,0.05)' : '#ffffff',
                  borderColor: isDarkBackground ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'
                }"
                :title="network"
            >
              <i :class="['fab', 'fa-' + network, 'text-lg']" :style="{ color: themeColor }"></i>
            </a>
          </div>
        </div>
      </div>

      <div
          class="border-t pt-8 flex flex-col md:flex-row justify-between items-center text-sm font-medium opacity-50"
          :style="{ borderColor: isDarkBackground ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)' }"
      >
        <p>© {{ new Date().getFullYear() }} {{ businessName }}. {{ t ? t('all_rights_reserved') : 'All rights reserved.' }}</p>
        <p class="mt-2 md:mt-0 text-[10px] uppercase tracking-widest font-bold">Powered by TouchCraft</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';

// ДОБАВЛЕНЫ НОВЫЕ ПРОПСЫ ДЛЯ ЛОГОТИПА
const props = defineProps([
  'businessName', 'themeColor', 't', 'contact', 'palette',
  'logoUrl', 'logoMode', 'applyThemeColorToLogo'
]);
defineEmits(['navigate']);

const isDarkBackground = computed(() => {
  const color = props.palette?.background || '#ffffff';
  if (color.startsWith('#')) {
    const r = parseInt(color.slice(1, 3), 16);
    const g = parseInt(color.slice(3, 5), 16);
    const b = parseInt(color.slice(5, 7), 16);
    const yiq = (r * 299 + g * 587 + b * 114) / 1000;
    return yiq < 128;
  }
  return false;
});

const hasSocials = computed(() => {
  return props.contact && props.contact.socials && Object.keys(props.contact.socials).length > 0;
});
</script>