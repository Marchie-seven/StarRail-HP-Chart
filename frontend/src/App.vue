<script setup lang="ts">
import { Orbit } from '@lucide/vue'
import { useTemplateRef } from 'vue'
import StarfieldBackground from './components/StarfieldBackground.vue'
import { modeInfo } from './domain/modes'
import { MODES } from './types'

const main = useTemplateRef<HTMLElement>('main')
</script>

<template>
  <StarfieldBackground />
  <a class="skip-link" href="#main-content" @click.prevent="main?.focus()">跳至内容</a>
  <header class="site-header">
    <div class="site-header__inner container">
      <RouterLink class="branding" :to="{ name: 'home' }" aria-label="星轨档案首页">
        <span class="branding__mark"><Orbit :size="24" :stroke-width="1.7" /></span>
        <span class="branding__type"><strong>星轨档案</strong><small>STAR RAIL ARCHIVE</small></span>
      </RouterLink>
      <nav class="site-nav" aria-label="主导航">
        <RouterLink :to="{ name: 'home' }">首页</RouterLink>
        <RouterLink v-for="mode in MODES" :key="mode" :to="{ name: mode }">{{ modeInfo[mode].name }}</RouterLink>
      </nav>
      <span class="data-badge"><span aria-hidden="true"></span>演示数据</span>
    </div>
  </header>

  <main id="main-content" ref="main" class="container main-content" tabindex="-1">
    <RouterView v-slot="{ Component, route }">
      <component :is="Component" :key="route.name" />
    </RouterView>
  </main>

  <footer class="site-footer">
    <div class="container site-footer__inner">
      <span class="footer-brand"><Orbit :size="18" />星轨档案</span>
      <span>同人作品集 · 血量、期数与奖励均为演示数据</span>
    </div>
  </footer>
</template>
