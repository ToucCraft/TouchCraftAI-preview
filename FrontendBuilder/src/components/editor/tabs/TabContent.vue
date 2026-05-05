<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">

    <button @click="isOpen = !isOpen" class="w-full p-4 flex justify-between items-center bg-slate-50 hover:bg-slate-100 transition-colors">
      <h3 class="font-bold text-[10px] text-gray-700 uppercase flex items-center">
        <i class="fas fa-pen mr-2 text-blue-500"></i> {{ t('editSite.tabs.content.title') }}
      </h3>

      <div class="flex items-center gap-2">
        <select v-show="isOpen" v-model="editingLang" @click.stop class="p-1 border rounded text-[9px] outline-none bg-white uppercase font-bold cursor-pointer hover:bg-slate-50 transition-colors">
          <option v-for="lang in availableEditorLanguages" :key="lang" :value="lang">{{ lang }}</option>
        </select>
        <i class="fas text-gray-400 ml-1" :class="isOpen ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
      </div>
    </button>

    <div v-show="isOpen" class="p-4 border-t border-slate-100 bg-white max-h-[500px] overflow-y-auto custom-scrollbar space-y-4">

      <div v-if="config.contact && config.translations && config.translations[editingLang]" class="p-3 bg-slate-50 rounded-lg border border-slate-100 shadow-sm mb-4">
        <h4 class="font-bold text-[10px] text-blue-600 uppercase mb-3 border-b border-blue-100 pb-1 flex items-center justify-between">
          <span><i class="fas fa-heading mr-1"></i> Header & Navigation</span>
          <div class="flex items-center gap-1">
            <input type="checkbox" v-model="config.contact.header_show_cta" id="showCtaToggle" class="w-3 h-3 cursor-pointer">
            <label for="showCtaToggle" class="text-[8px] font-bold text-gray-500 uppercase cursor-pointer">Show Button</label>
          </div>
        </h4>

        <div class="space-y-4">
          <div>
            <label class="text-[9px] font-bold text-gray-500 uppercase mb-2 block">Menu Links ({{ editingLang.toUpperCase() }})</label>
            <div class="grid grid-cols-2 gap-2">
              <div class="space-y-1">
                <span class="text-[8px] font-bold text-gray-400 uppercase block">Home</span>
                <input v-model="config.translations[editingLang]['Home']" placeholder="Home" class="w-full p-1.5 border rounded bg-white text-[10px] outline-none focus:border-blue-500">
              </div>

              <template v-for="block in config.blocks" :key="'nav-'+block.id">
                <div v-if="['FeaturesBlock', 'AboutBlock', 'FaqBlock', 'MapBlock', 'GalleryBlock'].includes(block.type)" class="space-y-1">
                  <span class="text-[8px] font-bold text-gray-400 uppercase block">{{ block.type.replace('Block', '') }}</span>
                  <input v-model="config.translations[editingLang][block.type.replace('Block', '')]" :placeholder="block.type.replace('Block', '')" class="w-full p-1.5 border rounded bg-white text-[10px] outline-none focus:border-blue-500">
                </div>
              </template>

              <div v-if="config.has_catalog" class="space-y-1">
                <span class="text-[8px] font-bold text-gray-400 uppercase block">Catalog</span>
                <input v-model="config.translations[editingLang]['Catalog']" placeholder="Catalog" class="w-full p-1.5 border rounded bg-white text-[10px] outline-none focus:border-blue-500">
              </div>

              <div class="space-y-1">
                <span class="text-[8px] font-bold text-gray-400 uppercase block">Privacy Policy</span>
                <input v-model="config.translations[editingLang]['Privacy']" placeholder="Privacy Policy" class="w-full p-1.5 border rounded bg-white text-[10px] outline-none focus:border-blue-500">
              </div>
            </div>
          </div>

          <div v-if="config.contact.header_show_cta !== false" class="pt-3 border-t border-slate-100">
            <label class="text-[9px] font-bold text-gray-500 uppercase mb-2 block">Header Button ({{ editingLang.toUpperCase() }})</label>
            <div class="space-y-3">
              <div>
                <label class="text-[8px] font-bold text-gray-400 uppercase mb-1 block">Button Text</label>
                <input v-model="config.translations[editingLang]['Contact Us']" @input="config.contact.header_cta_text = ''" placeholder="Contact Us" class="w-full p-2 border rounded bg-white text-xs outline-none focus:border-blue-500 transition-colors">
              </div>
              <div>
                <label class="text-[8px] font-bold text-gray-400 uppercase mb-1 block">Button Link</label>
                <div class="flex gap-2">
                  <select @change="config.contact.header_cta_url = $event.target.value" class="w-1/3 p-2 border rounded bg-slate-50 text-xs font-bold outline-none focus:border-blue-500 cursor-pointer text-gray-600">
                    <option value="" disabled selected>Link...</option>
                    <option value="https://">External URL</option>
                    <optgroup label="Sections">
                      <option v-for="b in config.blocks" :key="'opt-h-'+b.id" :value="'#' + b.type.replace('Block', '').toLowerCase()">
                        {{ b.type.replace('Block', '') }}
                      </option>
                    </optgroup>
                  </select>
                  <input v-model="config.contact.header_cta_url" placeholder="e.g. #contacts or https://..." class="w-2/3 p-2 border rounded bg-white text-xs outline-none focus:border-blue-500 transition-colors font-mono">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-for="(block, index) in config.blocks" :key="block.id" class="p-3 bg-slate-50 rounded-lg border border-slate-100 shadow-sm">
        <h4 class="font-bold text-[10px] text-blue-600 uppercase mb-3 border-b border-blue-100 pb-1">
          {{ index + 1 }}. {{ block.type.replace('Block','') }}
        </h4>

        <div class="space-y-3">
          <template v-for="key in ['title', 'subtitle', 'description', 'cta_text', 'cta_url', 'address', 'phone', 'email', 'submit_button_text']" :key="key">
            <div v-if="block.props[key] !== undefined">
              <label class="text-[9px] font-bold text-gray-500 uppercase mb-1 block">{{ t('editSite.props.' + key) || key }}</label>

              <template v-if="key === 'cta_url'">
                <div class="flex gap-2">
                  <select @change="block.props[key] = $event.target.value" class="w-1/3 p-2 border rounded bg-slate-50 text-xs font-bold outline-none focus:border-blue-500 cursor-pointer text-gray-600">
                    <option value="" disabled selected>Link...</option>
                    <option value="https://">External URL</option>
                    <optgroup label="Sections">
                      <option v-for="b in config.blocks" :key="'opt-'+b.id" :value="'#' + b.type.replace('Block', '').toLowerCase()">
                        {{ b.type.replace('Block', '') }}
                      </option>
                    </optgroup>
                  </select>
                  <input v-model="block.props[key]" placeholder="e.g. #contacts or https://..." class="w-2/3 p-2 border rounded bg-white text-xs outline-none focus:border-blue-500 transition-colors font-mono">
                </div>
              </template>

              <template v-else-if="['description', 'subtitle', 'address'].includes(key)">
                <textarea v-if="typeof block.props[key] === 'string'" v-model="block.props[key]" rows="2" class="w-full p-2 border rounded bg-white text-xs outline-none focus:border-blue-500 transition-colors"></textarea>
                <textarea v-else v-model="block.props[key][editingLang]" rows="2" class="w-full p-2 border rounded bg-white text-xs outline-none focus:border-blue-500 transition-colors"></textarea>
              </template>

              <template v-else>
                <input v-if="typeof block.props[key] === 'string'" v-model="block.props[key]" class="w-full p-2 border rounded bg-white text-xs outline-none focus:border-blue-500 transition-colors">
                <input v-else v-model="block.props[key][editingLang]" class="w-full p-2 border rounded bg-white text-xs outline-none focus:border-blue-500 transition-colors">
              </template>
            </div>
          </template>

          <div v-if="block.props.features && block.props.features.length" class="space-y-2 pt-2 border-t border-slate-200">
            <h5 class="text-[9px] font-bold text-gray-400 uppercase">{{ t('editSite.tabs.content.featureItems') }}</h5>
            <div v-for="(feat, fIdx) in block.props.features" :key="fIdx" class="bg-white p-2 rounded border border-slate-100 space-y-2">
              <div>
                <label class="text-[8px] font-bold text-gray-400 uppercase mb-0.5 block">{{ t('editSite.props.title') }}</label>
                <input v-if="typeof feat.title === 'string'" v-model="feat.title" class="w-full p-1.5 border rounded bg-slate-50 text-[10px] outline-none focus:border-blue-500">
                <input v-else v-model="feat.title[editingLang]" class="w-full p-1.5 border rounded bg-slate-50 text-[10px] outline-none focus:border-blue-500">
              </div>
              <div>
                <label class="text-[8px] font-bold text-gray-400 uppercase mb-0.5 block">{{ t('editSite.props.description') }}</label>
                <textarea v-if="typeof feat.description === 'string'" v-model="feat.description" rows="2" class="w-full p-1.5 border rounded bg-slate-50 text-[10px] outline-none focus:border-blue-500"></textarea>
                <textarea v-else v-model="feat.description[editingLang]" rows="2" class="w-full p-1.5 border rounded bg-slate-50 text-[10px] outline-none focus:border-blue-500"></textarea>
              </div>
            </div>
          </div>

          <div v-if="block.props.faqs && block.props.faqs.length" class="space-y-2 pt-2 border-t border-slate-200">
            <h5 class="text-[9px] font-bold text-gray-400 uppercase">{{ t('editSite.tabs.content.faqItems') }}</h5>
            <div v-for="(faq, fIdx) in block.props.faqs" :key="fIdx" class="bg-white p-2 rounded border border-slate-100 space-y-2">
              <div>
                <label class="text-[8px] font-bold text-gray-400 uppercase mb-0.5 block">{{ t('editSite.props.question') }}</label>
                <input v-if="typeof faq.question === 'string'" v-model="faq.question" class="w-full p-1.5 border rounded bg-slate-50 text-[10px] outline-none focus:border-blue-500">
                <input v-else v-model="faq.question[editingLang]" class="w-full p-1.5 border rounded bg-slate-50 text-[10px] outline-none focus:border-blue-500">
              </div>
              <div>
                <label class="text-[8px] font-bold text-gray-400 uppercase mb-0.5 block">{{ t('editSite.props.answer') }}</label>
                <textarea v-if="typeof faq.answer === 'string'" v-model="faq.answer" rows="2" class="w-full p-1.5 border rounded bg-slate-50 text-[10px] outline-none focus:border-blue-500"></textarea>
                <textarea v-else v-model="faq.answer[editingLang]" rows="2" class="w-full p-1.5 border rounded bg-slate-50 text-[10px] outline-none focus:border-blue-500"></textarea>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="p-3 bg-slate-50 rounded-lg border border-slate-100 shadow-sm mt-4">
        <h4 class="font-bold text-[10px] text-blue-600 uppercase mb-3 border-b border-blue-100 pb-1 flex items-center">
          <i class="fas fa-shield-alt mr-2"></i> {{ t('privacy.title') || 'Privacy Policy' }}
        </h4>
        <div class="space-y-3" v-if="config.translations && config.translations[editingLang]">
          <div>
            <label class="text-[9px] font-bold text-gray-500 uppercase mb-1 block">HTML Content</label>
            <textarea
                v-model="config.translations[editingLang].privacy_policy_text"
                rows="8"
                class="w-full p-2 border rounded bg-white text-[10px] outline-none focus:border-blue-500 transition-colors font-mono custom-scrollbar"
                placeholder="<p>Enter your privacy policy here...</p>"
            ></textarea>
          </div>
        </div>
      </div>

      <div v-if="config.contact && config.translations && config.translations[editingLang]" class="p-3 bg-slate-50 rounded-lg border border-slate-100 shadow-sm mt-4">
        <h4 class="font-bold text-[10px] text-blue-600 uppercase mb-3 border-b border-blue-100 pb-1 flex items-center">
          <i class="fas fa-shoe-prints mr-2"></i> Footer ({{ editingLang.toUpperCase() }})
        </h4>
        <div class="space-y-3">
          <div>
            <label class="text-[9px] font-bold text-gray-500 uppercase mb-1 block">Footer Description</label>
            <textarea v-model="config.translations[editingLang]['footer_desc']" @input="config.contact.footer_description = ''" rows="2" placeholder="A short description about your business..." class="w-full p-2 border rounded bg-white text-xs outline-none focus:border-blue-500 transition-colors custom-scrollbar"></textarea>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed, watch } from 'vue';

// Инжектим глобальные данные
const config = inject('siteConfig');
const t = inject('t');

// Локальное состояние таба
const isOpen = ref(false);
const editingLang = ref('en');

// Вычисляем доступные языки из конфига
const availableEditorLanguages = computed(() => {
  if (config.value && config.value.translations) {
    return Object.keys(config.value.translations);
  }
  return ['en'];
});

// Следим за сменой языка и инициализируем пустой объект, если его нет
watch(editingLang, (newLang) => {
  if (config.value) {
    if (!config.value.translations) {
      config.value.translations = {};
    }
    if (!config.value.translations[newLang]) {
      config.value.translations[newLang] = {};
    }
  }
}, { immediate: true });

</script>