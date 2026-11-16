<script setup>
import { withBase } from 'vitepress'

defineProps({
  src: { type: String, required: true },
  width: { type: Number, required: true },
  height: { type: Number, required: true },
  alt: { type: String, required: true },
  title: { type: String, required: true },
})
</script>

<template>
  <figure class="tutorial-figure">
    <a :href="withBase(src)" target="_blank" rel="noopener">
      <img :src="withBase(src)" :width="width" :height="height" :alt="alt" loading="lazy" />
    </a>
    <figcaption><strong>{{ title }}</strong> <slot /></figcaption>
  </figure>
</template>
