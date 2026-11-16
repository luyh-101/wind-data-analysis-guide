<script setup>
import { data } from './lesson-cases.data.js'

defineProps({ example: { type: String, required: true } })
const fmt = (value, digits = 2) => value.toFixed(digits).replace('-', '−')
const delta = data.pairing.nacelle - data.pairing.lidar
const coverageGroups = [
  { key: 'both', label: '两条都能估算' },
  { key: 'nacelle', label: '仅机舱曲线' },
  { key: 'lidar', label: '仅雷达曲线' },
  { key: 'neither', label: '两条都不能估算' }
]
</script>

<template>
  <figure v-if="example === 'pairing'" class="lesson-figure" aria-labelledby="pairing-caption">
    <figcaption id="pairing-caption" class="lesson-title">同一个 10 分钟窗口，两种时间标记</figcaption>
    <p class="lesson-note">AWAKEN，2023-08-24 UTC。配对键为统一后的窗口起点。</p>
    <div class="lesson-timeline" aria-hidden="true">
      <div class="lesson-axis"><span>00:00</span><span>00:05</span><span>00:10</span></div>
      <div class="lesson-ticks">
        <span v-for="minute in data.pairing.minutes" :key="minute"></span>
      </div>
      <div class="lesson-window">
        <span class="lesson-window-center"></span>
      </div>
    </div>
    <dl class="lesson-grid">
      <div><dt>WT041 机舱</dt><dd>00:00–00:09，共 10 条分钟记录</dd><dd class="lesson-value">{{ fmt(data.pairing.nacelle) }} m/s</dd></div>
      <div><dt>A1 雷达</dt><dd>00:05 是整段窗口的中点标记</dd><dd class="lesson-value">{{ fmt(data.pairing.lidar) }} m/s</dd></div>
    </dl>
    <p class="lesson-result">雷达记录的时间减去 5 分钟后，和机舱汇总记录用同一个起点 00:00 配对。机舱均值减去雷达读数，差值为 <strong>{{ fmt(delta) }} m/s</strong>。</p>
  </figure>

  <figure v-else-if="example === 'coverage'" class="lesson-figure" aria-labelledby="coverage-caption">
    <figcaption id="coverage-caption" class="lesson-title">两条曲线各能估算多少验证窗口</figcaption>
    <p class="lesson-note">{{ data.coverage.total }} 个留出窗口按两条曲线各自能否插值分为四组。</p>
    <div class="lesson-coverage-track" aria-hidden="true">
      <span v-for="group in coverageGroups" :key="group.key" :class="'lesson-segment-' + group.key"
        :style="{ flexGrow: data.coverage[group.key] }"></span>
    </div>
    <dl class="lesson-coverage-key">
      <div v-for="group in coverageGroups" :key="group.key">
        <dt><span class="lesson-swatch" :class="'lesson-segment-' + group.key" aria-hidden="true"></span>{{ group.label }}</dt>
        <dd>{{ data.coverage[group.key] }} 个</dd>
      </div>
    </dl>
    <p class="lesson-result">两条曲线都能估算的窗口约占 <strong>{{ fmt(data.coverage.both / data.coverage.total * 100, 0) }}%</strong>。</p>
  </figure>
</template>
