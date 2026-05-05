<template>
  <div v-if="isI18nLoaded" class="custom-font isolation-isolate min-h-screen bg-[#020617] text-white overflow-hidden relative selection:bg-blue-500/30">

    <div class="absolute top-[-10%] left-1/2 -translate-x-1/2 w-[600px] h-[500px] bg-blue-600/20 blur-[120px] rounded-full pointer-events-none transform-gpu"></div>
    <div class="absolute top-[30%] left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-cyan-600/10 blur-[150px] rounded-full pointer-events-none z-0 transform-gpu"></div>

    <div class="fixed top-0 left-0 w-full z-50 pt-6 px-4">
      <header class="max-w-7xl mx-auto h-16 rounded-2xl border border-white/10 backdrop-blur-xl bg-[#0f172a]/60 shadow-[0_8px_30px_rgb(0,0,0,0.5)] flex items-center justify-between px-6 transition-all duration-300 relative reveal-scale active" style="transition-delay: 0.1s;">

        <div class="flex items-center cursor-pointer select-none" @click="scrollTo('top')">
          <span class="text-xl font-black tracking-tighter">
            <span class="text-[#00c2ff]">TouchCraft AI</span>
          </span>
        </div>

        <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
          <a href="#how-it-works" @click.prevent="scrollTo('how-it-works')" class="hover:text-white transition-colors">{{ t('nav.howItWorks') }}</a>
          <a href="#features" @click.prevent="scrollTo('features')" class="hover:text-white transition-colors">{{ t('nav.features') }}</a>
          <a href="#blocks" @click.prevent="scrollTo('blocks')" class="hover:text-white transition-colors">{{ t('nav.blocks') }}</a>
          <a href="#pricing" @click.prevent="scrollTo('pricing')" class="hover:text-white transition-colors">{{ t('nav.pricing') }}</a>
          <a href="#about" @click.prevent="scrollTo('about')" class="hover:text-white transition-colors">{{ t('nav.aboutUs') }}</a>
          <a href="#contact" @click.prevent="scrollTo('contact')" class="text-sm font-medium text-slate-300 hover:text-white transition-colors">{{ t('nav.contact') }}</a>
        </nav>

        <div class="hidden md:flex items-center gap-4">
          <div class="relative group">
            <button class="flex items-center justify-center w-11 h-8 border border-white/10 hover:border-blue-500/50 rounded-lg bg-white/5 hover:bg-white/10 transition-all shadow-sm">
              <img :src="getFlagUrl(currentLang)" class="w-5 h-3.5 object-cover rounded-[2px]" alt="flag">
            </button>

            <div class="absolute right-0 top-full pt-2 w-32 z-50 opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto transition-all transform origin-top-right scale-95 group-hover:scale-100">
              <div class="bg-[#0f172a] border border-white/10 rounded-xl shadow-2xl overflow-hidden backdrop-blur-xl">
                <div class="max-h-[280px] overflow-y-auto custom-scrollbar">
                  <button v-for="lang in ['en', 'ru', 'es', 'uk', 'ee', 'de', 'fr', 'it', 'ca']"
                          :key="lang"
                          @click="changeLanguage(lang)"
                          class="w-full flex items-center justify-between px-4 py-2.5 hover:bg-blue-500/10 transition text-white border-b border-white/5 last:border-0">
                    <img :src="getFlagUrl(lang)" class="w-4 h-3 object-cover rounded-sm shadow-sm">
                    <span class="text-[10px] font-black uppercase tracking-wider">{{ lang }}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <button @click="handleLogin"  class="px-5 py-2 bg-blue-500 hover:bg-blue-400 text-white text-sm font-bold rounded-xl transition-all shadow-[0_0_15px_rgba(59,130,246,0.5)]">
            {{ t('nav.getStarted') }}
          </button>
        </div>

        <button @click="isMobileMenuOpen = !isMobileMenuOpen" class="md:hidden text-slate-300 hover:text-white p-2 z-50">
          <i class="fas text-xl" :class="isMobileMenuOpen ? 'fa-times' : 'fa-bars'"></i>
        </button>

        <transition name="slide-down">
          <div v-if="isMobileMenuOpen" class="absolute top-[calc(100%+10px)] left-0 w-full bg-[#0b1120]/95 backdrop-blur-2xl border border-slate-700/50 rounded-2xl p-6 flex flex-col gap-5 md:hidden shadow-[0_20px_50px_rgba(0,0,0,0.5)] z-40">
            <a href="#how-it-works" @click.prevent="scrollTo('how-it-works')" class="text-white font-bold text-lg border-b border-slate-800 pb-2">{{ t('nav.howItWorks') }}</a>
            <a href="#features" @click.prevent="scrollTo('features')" class="text-white font-bold text-lg border-b border-slate-800 pb-2">{{ t('nav.features') }}</a>
            <a href="#blocks" @click.prevent="scrollTo('blocks')" class="text-white font-bold text-lg border-b border-slate-800 pb-2">{{ t('nav.blocks') }}</a>
            <a href="#pricing" @click.prevent="scrollTo('pricing')" class="text-white font-bold text-lg border-b border-slate-800 pb-2">{{ t('nav.pricing') }}</a>
            <a href="#about" @click.prevent="scrollTo('about')" class="text-white font-bold text-lg border-b border-slate-800 pb-2">{{ t('nav.aboutUs') }}</a>
            <a href="#contact" @click.prevent="scrollTo('contact')" class="text-white font-bold text-lg border-b border-slate-800 pb-2">{{ t('nav.contact') }}</a>

            <div class="flex flex-col gap-3 border-b border-slate-800 pb-6">
              <span class="text-white font-bold text-lg px-2">{{ t('nav.language') }}</span>

              <div class="flex overflow-x-auto gap-3 pb-2 px-2 custom-scrollbar no-scrollbar">
                <button v-for="lang in ['en', 'ru', 'es', 'uk', 'ee', 'de', 'fr', 'it', 'ca']"
                        :key="lang"
                        @click="changeLanguage(lang)"
                        class="flex flex-col items-center gap-2 min-w-[65px] p-3 border rounded-xl transition-all shrink-0"
                        :class="currentLang === lang ? 'border-[#00c2ff] bg-blue-500/20 text-white shadow-[0_0_15px_rgba(0,194,255,0.2)]' : 'border-slate-700 bg-[#0f172a] text-slate-300'">
                  <img :src="getFlagUrl(lang)" class="w-6 h-4 object-cover rounded-sm shadow-sm">
                  <span class="text-[10px] font-black uppercase tracking-widest">{{ lang }}</span>
                </button>
              </div>
            </div>

            <button @click="handleLogin" class="px-5 py-2 mt-2 bg-blue-500 hover:bg-blue-400 text-white text-sm font-bold rounded-xl transition-all shadow-[0_0_15px_rgba(59,130,246,0.5)]">
              {{ t('nav.getStarted') }}
            </button>
          </div>
        </transition>

      </header>
    </div>

    <section id="top" class="relative z-10 pt-40 pb-20 px-6 max-w-7xl mx-auto text-center flex flex-col items-center">
      <div class="reveal-scale inline-flex items-center gap-2 px-4 py-2 rounded-full border border-blue-500/30 bg-blue-500/10 backdrop-blur-md mb-8 shadow-2xl">
        <i class="fas fa-bolt text-blue-400 text-xs"></i>
        <span class="text-xs font-medium text-blue-100 tracking-wide">{{ t('hero.badge') }}</span>
      </div>

      <h1 class="reveal text-5xl md:text-7xl font-extrabold tracking-tight mb-6 leading-[1.1]" style="transition-delay: 0.1s;">
        {{ t('hero.titleLine1') }} <br class="hidden md:block" />
        <span class="px-2 inline-block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400">{{ t('hero.titleLine2') }}</span>
      </h1>

      <p class="reveal text-lg md:text-xl text-slate-400 mb-10 max-w-3xl mx-auto leading-relaxed" style="transition-delay: 0.2s;">
        {{ t('hero.description') }}
      </p>

      <div class="reveal flex flex-col sm:flex-row items-center justify-center w-full sm:w-auto gap-4 mb-20 px-4 sm:px-0" style="transition-delay: 0.3s;">
        <button @click="handleLogin" class="w-full sm:w-auto px-8 py-4 rounded-xl bg-white text-[#020617] font-bold hover:scale-105 transition-transform flex items-center justify-center shadow-[0_0_30px_rgba(255,255,255,0.2)]">
          {{ t('hero.startFree') }}
        </button>
        <button @click="router.push('/presentation')" class="w-full sm:w-auto px-8 py-4 rounded-xl bg-slate-800/50 border border-slate-700 text-white font-bold hover:bg-slate-700 transition-colors flex items-center justify-center backdrop-blur-md cursor-pointer">
          <i class="fas fa-play mr-2"></i> {{ t('hero.watchDemo') }}
        </button>
      </div>

      <div class="reveal-scale relative w-full max-w-5xl mx-auto group perspective-1000" style="transition-delay: 0.4s;">
        <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 via-cyan-500 to-teal-500 rounded-3xl blur-2xl opacity-30 group-hover:opacity-50 transition duration-500"></div>

        <div class="relative bg-[#0b1120] border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col transform-gpu transition-transform duration-500 hover:scale-[1.01] will-change-transform">
          <div class="h-12 border-b border-slate-800 bg-slate-900/50 flex items-center px-4 gap-2 z-20 relative">
            <div class="flex gap-1.5">
              <div class="w-3 h-3 rounded-full bg-slate-700"></div>
              <div class="w-3 h-3 rounded-full bg-slate-700"></div>
              <div class="w-3 h-3 rounded-full bg-slate-700"></div>
            </div>
            <div class="flex-1 flex justify-center">
              <div class="px-4 py-1 rounded bg-black/40 border border-slate-800 text-[10px] text-slate-500 flex items-center gap-2">
                <i class="fas fa-lock text-[8px]"></i> builder.touch-craft.com
              </div>
            </div>
          </div>
          <div class="relative w-full z-10 bg-[#0b1120]">
            <img src="/pre-hero-landing.jpg" alt="TouchCraft Interface" decoding="async" class="w-full h-auto object-cover opacity-50 group-hover:opacity-90 transition-opacity duration-500 transform-gpu">
            <div class="hidden md:block absolute inset-0 bg-blue-600/30 mix-blend-overlay pointer-events-none transition-opacity duration-500 group-hover:opacity-0 transform-gpu"></div>
            <div class="absolute inset-0 bg-[#020617]/20 pointer-events-none transition-opacity duration-500 group-hover:opacity-10 transform-gpu"></div>
            <div class="absolute inset-0 bg-gradient-to-t from-[#0b1120] via-transparent to-transparent opacity-80 pointer-events-none transform-gpu"></div>
          </div>
        </div>
      </div>
    </section>

    <section id="how-it-works" class="relative z-10 py-32 px-6 max-w-7xl mx-auto border-t border-slate-800/50">
      <div class="reveal text-center max-w-3xl mx-auto mb-20 relative z-10">
        <h2 class="text-sm font-bold tracking-widest text-cyan-400 uppercase mb-4">{{ t('workflow.subtitle') }}</h2>
        <h3 class="text-4xl md:text-5xl font-extrabold text-white mb-6 tracking-tight">{{ t('workflow.title') }}</h3>
      </div>

      <div class="grid md:grid-cols-3 gap-12 relative z-10">
        <div class="reveal-scale text-center" style="transition-delay: 0.1s;">
          <div class="w-20 h-20 mx-auto rounded-3xl bg-slate-800/50 border border-slate-700 flex items-center justify-center mb-6 shadow-xl text-3xl text-blue-400">1</div>
          <h4 class="text-xl font-bold mb-3">{{ t('workflow.step1Title') }}</h4>
          <p class="text-slate-400 text-sm leading-relaxed">{{ t('workflow.step1Desc') }}</p>
        </div>
        <div class="reveal-scale text-center relative" style="transition-delay: 0.2s;">
          <div class="hidden md:block absolute top-10 -left-[15%] w-[30%] h-px bg-gradient-to-r from-slate-700 to-blue-500/50 border-dashed"></div>
          <div class="w-20 h-20 mx-auto rounded-3xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center mb-6 shadow-xl text-3xl text-cyan-400">2</div>
          <h4 class="text-xl font-bold mb-3">{{ t('workflow.step2Title') }}</h4>
          <p class="text-slate-400 text-sm leading-relaxed">{{ t('workflow.step2Desc') }}</p>
          <div class="hidden md:block absolute top-10 -right-[15%] w-[30%] h-px bg-gradient-to-r from-blue-500/50 to-slate-700 border-dashed"></div>
        </div>
        <div class="reveal-scale text-center" style="transition-delay: 0.3s;">
          <div class="w-20 h-20 mx-auto rounded-3xl bg-slate-800/50 border border-slate-700 flex items-center justify-center mb-6 shadow-xl text-3xl text-teal-400">3</div>
          <h4 class="text-xl font-bold mb-3">{{ t('workflow.step3Title') }}</h4>
          <p class="text-slate-400 text-sm leading-relaxed">{{ t('workflow.step3Desc') }}</p>
        </div>
      </div>
    </section>

    <section id="features" class="relative z-10 py-32 px-6 max-w-7xl mx-auto border-t border-slate-800/50">
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-blue-600/5 blur-[120px] rounded-full pointer-events-none z-0"></div>

      <div class="reveal text-center max-w-3xl mx-auto mb-20 relative z-10">
        <h2 class="text-sm font-bold tracking-widest text-cyan-400 uppercase mb-4">{{ t('features.subtitle') }}</h2>
        <h3 class="text-4xl md:text-5xl font-extrabold text-white mb-6 tracking-tight">{{ t('features.title') }}</h3>
        <p class="text-lg text-slate-400 leading-relaxed">{{ t('features.description') }}</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 relative z-10">
        <div class="reveal group relative p-8 rounded-3xl bg-[#0b1120] md:bg-[#0b1120]/80 backdrop-blur-none md:backdrop-blur-sm border border-slate-800 hover:border-blue-500/50 transition-colors duration-500 overflow-hidden" style="transition-delay: 0.1s;">
          <div class="absolute inset-0 bg-gradient-to-br from-blue-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(59,130,246,0.1)] group-hover:scale-110 transition-transform duration-500">
              <i class="fas fa-magic text-2xl text-cyan-400"></i>
            </div>
            <h4 class="text-xl font-bold text-white mb-3">{{ t('features.item1Title') }}</h4>
            <p class="text-sm text-slate-400 leading-relaxed">{{ t('features.item1Desc') }}</p>
          </div>
        </div>
        <div class="reveal group relative p-8 rounded-3xl bg-[#0b1120] md:bg-[#0b1120]/80 backdrop-blur-none md:backdrop-blur-sm border border-slate-800 hover:border-blue-500/50 transition-colors duration-500 overflow-hidden" style="transition-delay: 0.2s;">
          <div class="absolute inset-0 bg-gradient-to-br from-cyan-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(6,182,212,0.1)] group-hover:scale-110 transition-transform duration-500">
              <i class="fas fa-rocket text-2xl text-cyan-400"></i>
            </div>
            <h4 class="text-xl font-bold text-white mb-3">{{ t('features.item2Title') }}</h4>
            <p class="text-sm text-slate-400 leading-relaxed">{{ t('features.item2Desc') }}</p>
          </div>
        </div>
        <div class="reveal group relative p-8 rounded-3xl bg-[#0b1120] md:bg-[#0b1120]/80 backdrop-blur-none md:backdrop-blur-sm border border-slate-800 hover:border-blue-500/50 transition-colors duration-500 overflow-hidden" style="transition-delay: 0.3s;">
          <div class="absolute inset-0 bg-gradient-to-br from-teal-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(20,184,166,0.1)] group-hover:scale-110 transition-transform duration-500">
              <i class="fas fa-globe text-2xl text-teal-400"></i>
            </div>
            <h4 class="text-xl font-bold text-white mb-3">{{ t('features.item3Title') }}</h4>
            <p class="text-sm text-slate-400 leading-relaxed">{{ t('features.item3Desc') }}</p>
          </div>
        </div>
        <div class="reveal group relative p-8 rounded-3xl bg-[#0b1120] md:bg-[#0b1120]/80 backdrop-blur-none md:backdrop-blur-sm border border-slate-800 hover:border-blue-500/50 transition-colors duration-500 overflow-hidden" style="transition-delay: 0.4s;">
          <div class="absolute inset-0 bg-gradient-to-br from-blue-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(59,130,246,0.1)] group-hover:scale-110 transition-transform duration-500">
              <i class="fas fa-inbox text-2xl text-blue-400"></i>
            </div>
            <h4 class="text-xl font-bold text-white mb-3">{{ t('features.item4Title') }}</h4>
            <p class="text-sm text-slate-400 leading-relaxed">{{ t('features.item4Desc') }}</p>
          </div>
        </div>
        <div class="reveal group relative p-8 rounded-3xl bg-[#0b1120] md:bg-[#0b1120]/80 backdrop-blur-none md:backdrop-blur-sm border border-slate-800 hover:border-blue-500/50 transition-colors duration-500 overflow-hidden" style="transition-delay: 0.5s;">
          <div class="absolute inset-0 bg-gradient-to-br from-purple-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(168,85,247,0.1)] group-hover:scale-110 transition-transform duration-500">
              <i class="fas fa-store text-2xl text-purple-400"></i>
            </div>
            <h4 class="text-xl font-bold text-white mb-3">{{ t('features.item5Title') }}</h4>
            <p class="text-sm text-slate-400 leading-relaxed">{{ t('features.item5Desc') }}</p>
          </div>
        </div>
        <div class="reveal group relative p-8 rounded-3xl bg-[#0b1120] md:bg-[#0b1120]/80 backdrop-blur-none md:backdrop-blur-sm border border-slate-800 hover:border-blue-500/50 transition-colors duration-500 overflow-hidden" style="transition-delay: 0.6s;">
          <div class="absolute inset-0 bg-gradient-to-br from-pink-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-pink-500/10 border border-pink-500/20 flex items-center justify-center mb-6 shadow-[0_0_15px_rgba(236,72,153,0.1)] group-hover:scale-110 transition-transform duration-500">
              <i class="fas fa-edit text-2xl text-pink-400"></i>
            </div>
            <h4 class="text-xl font-bold text-white mb-3">{{ t('features.item6Title') }}</h4>
            <p class="text-sm text-slate-400 leading-relaxed">{{ t('features.item6Desc') }}</p>
          </div>
        </div>
      </div>
    </section>

    <section id="blocks" class="relative z-10 py-32 px-6 max-w-7xl mx-auto border-t border-slate-800/50">
      <div class="reveal flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
        <div class="max-w-2xl">
          <h2 class="text-sm font-bold tracking-widest text-blue-400 uppercase mb-4">{{ t('blocks.subtitle') }}</h2>
          <h3 class="text-4xl font-extrabold text-white tracking-tight">{{ t('blocks.title') }}</h3>
        </div>
        <p class="text-slate-400 text-sm md:text-right max-w-sm">{{ t('blocks.description') }}</p>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div class="reveal-scale bg-slate-800/30 border border-slate-700/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition-colors cursor-default" style="transition-delay: 0.1s;">
          <i class="fas fa-image text-3xl text-blue-400 mb-3"></i>
          <p class="font-bold text-sm text-slate-200">{{ t('blocks.hero') }}</p>
        </div>
        <div class="reveal-scale bg-slate-800/30 border border-slate-700/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition-colors cursor-default" style="transition-delay: 0.2s;">
          <i class="fas fa-star text-3xl text-cyan-400 mb-3"></i>
          <p class="font-bold text-sm text-slate-200">{{ t('blocks.features') }}</p>
        </div>
        <div class="reveal-scale bg-slate-800/30 border border-slate-700/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition-colors cursor-default" style="transition-delay: 0.3s;">
          <i class="fas fa-users text-3xl text-teal-400 mb-3"></i>
          <p class="font-bold text-sm text-slate-200">{{ t('blocks.aboutUs') }}</p>
        </div>
        <div class="reveal-scale bg-slate-800/30 border border-slate-700/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition-colors cursor-default" style="transition-delay: 0.4s;">
          <i class="fas fa-question-circle text-3xl text-purple-400 mb-3"></i>
          <p class="font-bold text-sm text-slate-200">{{ t('blocks.faq') }}</p>
        </div>
        <div class="reveal-scale bg-slate-800/30 border border-slate-700/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition-colors cursor-default" style="transition-delay: 0.5s;">
          <i class="fas fa-map-marked-alt text-3xl text-pink-400 mb-3"></i>
          <p class="font-bold text-sm text-slate-200">{{ t('blocks.maps') }}</p>
        </div>
        <div class="reveal-scale bg-slate-800/30 border border-slate-700/50 rounded-2xl p-6 text-center hover:bg-slate-800 transition-colors cursor-default" style="transition-delay: 0.6s;">
          <i class="fas fa-envelope-open-text text-3xl text-orange-400 mb-3"></i>
          <p class="font-bold text-sm text-slate-200">{{ t('blocks.leadForms') }}</p>
        </div>
      </div>
    </section>

    <section id="about" class="relative z-10 py-32 border-t border-slate-800/50 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-b from-[#0b1120] to-[#020617] -z-10"></div>

      <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-16 items-center relative z-10">
        <div class="reveal-left">
          <h2 class="text-sm font-bold tracking-widest text-teal-400 uppercase mb-4">{{ t('about.subtitle') }}</h2>
          <h3 class="text-4xl md:text-5xl font-extrabold text-white mb-6 tracking-tight">{{ t('about.title') }}</h3>
          <p class="text-lg text-slate-400 leading-relaxed mb-6">{{ t('about.para1') }}</p>
          <p class="text-lg text-slate-400 leading-relaxed mb-8">{{ t('about.para2') }}</p>
          <div class="flex items-center gap-6">
            <div class="text-center">
              <div class="text-3xl font-black text-white">10x</div>
              <div class="text-xs text-slate-500 uppercase tracking-widest mt-1">{{ t('about.stat1') }}</div>
            </div>
            <div class="w-px h-10 bg-slate-700"></div>
            <div class="text-center">
              <div class="text-3xl font-black text-white">100%</div>
              <div class="text-xs text-slate-500 uppercase tracking-widest mt-1">{{ t('about.stat2') }}</div>
            </div>
          </div>
        </div>

        <div class="reveal-right relative h-[400px] flex items-center justify-center">
          <div class="absolute w-64 h-64 bg-gradient-to-tr from-blue-600 to-cyan-400 rounded-3xl rotate-12 blur-sm opacity-50 animate-pulse"></div>
          <div class="absolute w-60 h-60 bg-gradient-to-tr from-slate-900 to-slate-800 border border-slate-700 rounded-3xl -rotate-6 shadow-2xl flex items-center justify-center backdrop-blur-xl">
            <i class="fas fa-cube text-7xl text-cyan-400 drop-shadow-[0_0_15px_rgba(6,182,212,0.8)]"></i>
          </div>
        </div>
      </div>
    </section>

    <section id="pricing" class="relative z-10 py-32 px-6 max-w-7xl mx-auto border-t border-slate-800/50">
      <div class="absolute top-0 right-0 w-[600px] h-[600px] bg-teal-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

      <div class="reveal text-center max-w-3xl mx-auto mb-20 relative z-10">
        <h2 class="text-sm font-bold tracking-widest text-blue-400 uppercase mb-4">{{ t('pricing.subtitle') }}</h2>
        <h3 class="text-4xl md:text-5xl font-extrabold text-white mb-6 tracking-tight">{{ t('pricing.title') }}</h3>
        <p class="text-lg text-slate-400 leading-relaxed">{{ t('pricing.description') }}</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative z-10 items-center">
        <div class="reveal-left group relative p-8 rounded-3xl bg-[#0b1120] md:bg-[#0b1120]/80 backdrop-blur-none md:backdrop-blur-sm border border-slate-800 hover:border-blue-500/50 transition-colors duration-500 overflow-hidden">
          <div class="mb-8">
            <h4 class="text-xl font-bold text-white mb-2">{{ t('pricing.free.name') }}</h4>
            <p class="text-sm text-slate-400 h-10">{{ t('pricing.free.desc') }}</p>
          </div>
          <div class="mb-8">
            <span class="text-5xl font-extrabold text-white">€0</span>
            <span class="text-slate-400">{{ t('pricing.perMonthFirst') }}</span>
          </div>
          <ul class="space-y-4 mb-8 text-sm text-slate-300">
            <li class="flex items-center"><i class="fas fa-check text-slate-600 mr-3"></i> {{ t('pricing.free.feature1') }}</li>
            <li class="flex items-center"><i class="fas fa-check text-slate-600 mr-3"></i> {{ t('pricing.free.feature2') }}</li>
            <li class="flex items-center"><i class="fas fa-check text-slate-600 mr-3"></i> {{ t('pricing.free.feature3') }}</li>
            <li class="flex items-center"><i class="fas fa-times text-slate-700 mr-3"></i> {{ t('pricing.free.feature4') }}</li>
            <li class="flex items-center"><i class="fas fa-times text-slate-700 mr-3"></i> {{ t('pricing.free.feature5') }}</li>
          </ul>
          <router-link to="/dashboard" class="block w-full py-3 rounded-xl border border-slate-700 text-center font-bold text-white hover:bg-slate-800 transition-colors">
            {{ t('pricing.startFreeTrial') }}
          </router-link>
        </div>

        <div class="reveal-scale p-8 rounded-3xl bg-gradient-to-b from-[#0f172a] to-[#0b1120] border-2 border-blue-500 shadow-[0_0_40px_rgba(59,130,246,0.15)] relative transform md:-translate-y-4 transition-transform duration-300 hover:scale-105 z-10">
          <div class="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-blue-500 text-white text-xs font-bold uppercase tracking-wider rounded-full shadow-lg">
            {{ t('pricing.mostPopular') }}
          </div>
          <div class="mb-8">
            <h4 class="text-xl font-bold text-white mb-2 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">{{ t('pricing.starter.name') }}</h4>
            <p class="text-sm text-slate-400 h-10">{{ t('pricing.starter.desc') }}</p>
          </div>
          <div class="mb-8">
            <span class="text-5xl font-extrabold text-white">€15</span>
            <span class="text-slate-400">{{ t('pricing.perMonth') }}</span>
          </div>
          <ul class="space-y-4 mb-8 text-sm text-slate-200">
            <li class="flex items-center"><i class="fas fa-check text-blue-400 mr-3"></i> {{ t('pricing.starter.feature1') }}</li>
            <li class="flex items-center"><i class="fas fa-check text-blue-400 mr-3"></i> {{ t('pricing.starter.feature2') }}</li>
            <li class="flex items-center"><i class="fas fa-check text-blue-400 mr-3"></i> {{ t('pricing.starter.feature3') }}</li>
            <li class="flex items-center"><i class="fas fa-check text-blue-400 mr-3"></i> {{ t('pricing.starter.feature4') }}</li>
            <li class="flex items-center"><i class="fas fa-times text-slate-600 mr-3 text-sm"></i> {{ t('pricing.starter.feature5') }}</li>
          </ul>
          <button @click="selectPlan('starter')" class="block w-full py-3 rounded-xl border border-slate-700 text-center font-bold text-white bg-blue-600 hover:bg-blue-500 transition-colors">
            {{ t('billing.starter.title') }}
          </button>
        </div>

        <div class="reveal-right group relative p-8 rounded-3xl bg-[#0b1120] md:bg-[#0b1120]/80 backdrop-blur-none md:backdrop-blur-sm border border-slate-800 hover:border-blue-500/50 transition-colors duration-500 overflow-hidden">
          <div class="mb-8">
            <h4 class="text-xl font-bold text-white mb-2">{{ t('pricing.pro.name') }}</h4>
            <p class="text-sm text-slate-400 h-10">{{ t('pricing.pro.desc') }}</p>
          </div>
          <div class="mb-8">
            <span class="text-5xl font-extrabold text-white">€25</span>
            <span class="text-slate-400">{{ t('pricing.perMonth') }}</span>
          </div>
          <ul class="space-y-4 mb-8 text-sm text-slate-300">
            <li class="flex items-center"><i class="fas fa-check text-teal-400 mr-3"></i> {{ t('pricing.pro.feature1') }}</li>
            <li class="flex items-center"><i class="fas fa-check text-teal-400 mr-3"></i> <span class="font-bold text-white">{{ t('pricing.pro.feature2') }}</span></li>
            <li class="flex items-center"><i class="fas fa-check text-teal-400 mr-3"></i> {{ t('pricing.pro.feature3') }}</li>
            <li class="flex items-center"><i class="fas fa-check text-teal-400 mr-3"></i> {{ t('pricing.pro.feature4') }}</li>
            <li class="flex items-center"><i class="fas fa-check text-teal-400 mr-3"></i> {{ t('pricing.pro.feature5') }}</li>
          </ul>
          <button @click="selectPlan('pro')" class="block w-full py-3 rounded-xl border border-slate-700 text-center font-bold text-white hover:bg-slate-800 transition-colors">
            {{ t('billing.pro.title') }}
          </button>
        </div>
      </div>
    </section>

    <section id="contact" class="relative z-10 py-32 px-6 max-w-4xl mx-auto border-t border-slate-800/50">
      <div class="reveal text-center mb-16">
        <h2 class="text-sm font-bold tracking-widest text-cyan-400 uppercase mb-4">{{ t('contact.subtitle') }}</h2>
        <h3 class="text-4xl font-extrabold text-white mb-4 tracking-tight">{{ t('contact.title') }}</h3>
        <p class="text-slate-400">{{ t('contact.description') }}</p>
      </div>

      <div class="reveal-scale bg-[#0b1120] border border-slate-800 p-8 rounded-3xl shadow-2xl relative">
        <form @submit.prevent="submitContactForm">

          <div class="opacity-0 absolute -z-50 h-0 w-0 overflow-hidden" aria-hidden="true">
            <label>Leave this field empty</label>
            <input type="text" v-model="contactForm.honeypot" tabindex="-1" autocomplete="off">
          </div>

          <div class="grid md:grid-cols-2 gap-6 mb-6">
            <div>
              <label class="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">{{ t('contact.nameLabel') }}</label>
              <input v-model="contactForm.name" type="text" required :placeholder="t('contact.namePlaceholder')" class="w-full bg-[#020617] border border-slate-700 rounded-xl p-4 text-white outline-none focus:border-cyan-400 transition-colors">
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">{{ t('contact.emailLabel') }}</label>
              <input v-model="contactForm.email" type="email" required :placeholder="t('contact.emailPlaceholder')" class="w-full bg-[#020617] border border-slate-700 rounded-xl p-4 text-white outline-none focus:border-cyan-400 transition-colors">
            </div>
          </div>
          <div class="mb-6">
            <label class="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">{{ t('contact.messageLabel') }}</label>
            <textarea v-model="contactForm.message" required rows="4" :placeholder="t('contact.messagePlaceholder')" class="w-full bg-[#020617] border border-slate-700 rounded-xl p-4 text-white outline-none focus:border-cyan-400 transition-colors"></textarea>
          </div>

          <div class="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-[#020617] border border-slate-700 rounded-xl p-4 transition-colors" :class="{'border-red-500/50': captchaError}">
            <label class="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center">
              <i class="fas fa-shield-alt mr-2 text-slate-500"></i>
              {{ t('contact.captchaQ') }} {{ captcha.num1 }} + {{ captcha.num2 }}? <span class="text-red-500 ml-1">*</span>
            </label>
            <input v-model="captcha.userAnswer" type="number" required class="w-full sm:w-24 bg-[#0b1120] border border-slate-600 rounded-lg p-2 text-white text-center outline-none focus:border-cyan-400" @focus="captchaError = false">
          </div>
          <transition name="fade">
            <p v-if="captchaError" class="text-red-400 text-xs font-bold mb-4 -mt-4 text-right">{{ t('contact.captchaError') }}</p>
          </transition>

          <button type="submit" :disabled="isSubmitting" class="w-full py-4 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-xl shadow-[0_0_15px_rgba(6,182,212,0.4)] transition-all disabled:opacity-50 disabled:cursor-not-allowed">
            <i v-if="isSubmitting" class="fas fa-spinner fa-spin mr-2"></i>
            {{ isSubmitting ? t('contact.sending') : t('contact.sendBtn') }}
          </button>

          <transition name="fade">
            <div v-if="formStatus === 'success'" class="mt-6 p-4 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-center font-bold text-sm">
              <i class="fas fa-check-circle mr-2"></i> {{ t('contact.successMsg') }}
            </div>
            <div v-else-if="formStatus === 'error'" class="mt-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-center font-bold text-sm">
              <i class="fas fa-exclamation-circle mr-2"></i> {{ t('contact.errorMsg') }}
            </div>
          </transition>
        </form>
      </div>
    </section>

    <footer class="reveal border-t border-slate-800/50 bg-[#020617] pt-16 pb-8 relative z-10">
      <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-4 gap-12 mb-12">
        <div class="col-span-2">
          <span class="text-[#00c2ff]">TouchCraft AI</span>
          <p class="text-slate-400 text-sm max-w-xs leading-relaxed mt-2">
            {{ t('footer.description') }}
          </p>
        </div>
        <div>
          <h5 class="text-white font-bold mb-4">{{ t('footer.product') }}</h5>
          <ul class="space-y-2 text-sm text-slate-400">
            <li><a href="#features" @click.prevent="scrollTo('features')" class="hover:text-blue-400 transition-colors">{{ t('nav.features') }}</a></li>
            <li><a href="#pricing" @click.prevent="scrollTo('pricing')" class="hover:text-blue-400 transition-colors">{{ t('nav.pricing') }}</a></li>
            <li><a href="#blocks" @click.prevent="scrollTo('blocks')" class="hover:text-blue-400 transition-colors">{{ t('nav.blocks') }}</a></li>
          </ul>
        </div>
        <div>
          <h5 class="text-white font-bold mb-4">{{ t('footer.company') }}</h5>
          <ul class="space-y-2 text-sm text-slate-400">
            <li><a href="#about" @click.prevent="scrollTo('about')" class="hover:text-blue-400 transition-colors">{{ t('nav.aboutUs') }}</a></li>
            <li><a href="#contact" @click.prevent="scrollTo('contact')" class="hover:text-blue-400 transition-colors">{{ t('nav.contact') }}</a></li>
            <li><a href="/privacy" class="hover:text-blue-400 transition-colors">{{ t('footer.privacy') }}</a></li>
          </ul>
        </div>
      </div>
      <div class="max-w-7xl mx-auto px-6 pt-8 border-t border-slate-800/50 flex flex-col md:flex-row items-center justify-between">
        <p class="text-slate-500 text-xs">{{ t('footer.copyright') }}</p>
        <div class="flex space-x-4 mt-4 md:mt-0">
          <a href="https://www.instagram.com/touchcraft.io?igsh=MWdvMDF5MTFneGFzMw%3D%3D&utm_source=qr" class="text-slate-500 hover:text-white transition-colors"><i class="fab fa-instagram"></i></a>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import api from '../api/client';
import { useAuth0 } from '@auth0/auth0-vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const currentLang = ref(localStorage.getItem('app_lang') || 'en');
const translations = ref({});
const isI18nLoaded = ref(false);

const loadTranslations = async (lang) => {
  try {
    const response = await fetch(`/i18n/${lang}.json`);
    if (response.ok) {
      translations.value = await response.json();
      localStorage.setItem('app_lang', lang);
      document.documentElement.lang = lang;
      isI18nLoaded.value = true;
    } else {
      console.warn(`Translation file for ${lang} not found, falling back to English`);
      if (lang !== 'en') await loadTranslations('en');
    }
  } catch (error) {
    console.error("Error loading translations:", error);
    isI18nLoaded.value = true;
  }
};

const t = (key) => {
  const keys = key.split('.');
  let value = translations.value;
  for (const k of keys) {
    if (value && Object.prototype.hasOwnProperty.call(value, k)) {
      value = value[k];
    } else {
      return key;
    }
  }
  return value;
};

const setLanguage = async (lang) => {
  if (currentLang.value !== lang) {
    currentLang.value = lang;
    await loadTranslations(lang);
  }
};

const { loginWithRedirect, isAuthenticated } = useAuth0();

const handleLogin = () => {
  loginWithRedirect({
    appState: { target: '/dashboard' }
  });
};

const selectPlan = (plan) => {
  const targetPath = `/settings?tab=billing&plan=${plan}`;

  if (!isAuthenticated.value) {
    loginWithRedirect({
      appState: { target: targetPath }
    });
  } else {
    router.push(targetPath);
  }
};

const isMobileMenuOpen = ref(false);

const scrollTo = (id) => {
  isMobileMenuOpen.value = false;
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
};

const getFlagUrl = (lang) => {
  if (lang === 'en') return 'https://flagcdn.com/w20/gb.png';
  if (lang === 'uk') return 'https://flagcdn.com/w20/ua.png';
  if (lang === 'ca') return 'https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.0.0/flags/4x3/es-ct.svg';
  return `https://flagcdn.com/w20/${lang}.png`;
};

const changeLanguage = async (lang) => {
  if (currentLang.value !== lang) {
    currentLang.value = lang;
    await loadTranslations(lang);
    isMobileMenuOpen.value = false;
  }
};

const contactForm = ref({ name: '', email: '', message: '', honeypot: '' });
const isSubmitting = ref(false);
const formStatus = ref(null);

const captcha = ref({ num1: 0, num2: 0, userAnswer: '' });
const captchaError = ref(false);

const generateCaptcha = () => {
  captcha.value.num1 = Math.floor(Math.random() * 10) + 1;
  captcha.value.num2 = Math.floor(Math.random() * 10) + 1;
  captcha.value.userAnswer = '';
};

onMounted(async () => {
  await loadTranslations(currentLang.value);
  generateCaptcha();

  await nextTick();

  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
  revealElements.forEach(el => observer.observe(el));
});

const submitContactForm = async () => {
  if (contactForm.value.honeypot !== '') {
    formStatus.value = 'success';
    contactForm.value = { name: '', email: '', message: '', honeypot: '' };
    return;
  }

  if (parseInt(captcha.value.userAnswer) !== (captcha.value.num1 + captcha.value.num2)) {
    captchaError.value = true;
    generateCaptcha();
    return;
  }

  isSubmitting.value = true;
  formStatus.value = null;
  captchaError.value = false;

  try {
    await api.post(`/contact`, {
      name: contactForm.value.name,
      email: contactForm.value.email,
      message: contactForm.value.message,
      honeypot: contactForm.value.honeypot
    });

    formStatus.value = 'success';
    contactForm.value = { name: '', email: '', message: '', honeypot: '' };
    generateCaptcha();
    setTimeout(() => { formStatus.value = null; }, 5000);

  } catch (error) {
    console.error(error);
    formStatus.value = 'error';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

.custom-font {
  font-family: 'Manrope', ui-sans-serif, system-ui, -apple-system, sans-serif;
}

.perspective-1000 {
  perspective: 1000px;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease-out;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(0, 194, 255, 0.3);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 194, 255, 0.5);
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s cubic-bezier(0.5, 0, 0, 1), transform 0.8s cubic-bezier(0.5, 0, 0, 1);
}
.reveal.active {
  opacity: 1;
  transform: translateY(0);
}

.reveal-left {
  opacity: 0;
  transform: translateX(-40px);
  transition: opacity 0.8s cubic-bezier(0.5, 0, 0, 1), transform 0.8s cubic-bezier(0.5, 0, 0, 1);
}
.reveal-left.active {
  opacity: 1;
  transform: translateX(0);
}

.reveal-right {
  opacity: 0;
  transform: translateX(40px);
  transition: opacity 0.8s cubic-bezier(0.5, 0, 0, 1), transform 0.8s cubic-bezier(0.5, 0, 0, 1);
}
.reveal-right.active {
  opacity: 1;
  transform: translateX(0);
}

.reveal-scale {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
  transition: opacity 0.8s cubic-bezier(0.5, 0, 0, 1), transform 0.8s cubic-bezier(0.5, 0, 0, 1);
}
.reveal-scale.active {
  opacity: 1;
  transform: scale(1) translateY(0);
}
</style>
