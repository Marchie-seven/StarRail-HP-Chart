<script setup lang="ts">
import { onBeforeUnmount, onMounted, useTemplateRef } from 'vue'

interface Star {
  x: number
  y: number
  radius: number
  opacity: number
  phase: number
  rate: number
  depth: number
  color: string
}

interface Meteor {
  x: number
  y: number
  length: number
  start: number
}

const canvas = useTemplateRef<HTMLCanvasElement>('canvas')
const colors = ['#fff5e7', '#d9d0ff', '#ffce9a', '#c8d9ff']
const frameInterval = 1000 / 30
let context: CanvasRenderingContext2D | null = null
let motion: MediaQueryList | undefined
let stars: Star[] = []
let meteor: Meteor | undefined
let nextMeteor = 5200
let width = 0
let height = 0
let time = 0
let lastFrame = 0
let frame: number | undefined
let scrollPosition = 0

function createStars(count: number): Star[] {
  return Array.from({ length: count }, () => {
    const size = Math.random() ** 2
    return {
      x: Math.random(),
      y: Math.random(),
      radius: 0.38 + size * 1.08,
      opacity: 0.26 + Math.random() * 0.45 + size * 0.18,
      phase: Math.random() * 2 * Math.PI,
      rate: 0.00045 + Math.random() * 0.0007,
      depth: 0.025 + Math.random() * 0.07,
      color: colors[Math.floor(Math.random() * colors.length)],
    }
  })
}

function drawMeteor(ctx: CanvasRenderingContext2D) {
  if (!meteor && time >= nextMeteor) {
    meteor = {
      x: width * (0.59 + Math.random() * 0.36),
      y: height * (0.04 + Math.random() * 0.23),
      length: Math.min(width * 0.33, 145),
      start: time,
    }
  }
  if (!meteor) return

  const progress = (time - meteor.start) / 1080
  if (progress >= 1) {
    meteor = undefined
    nextMeteor = time + 9000 + Math.random() * 9000
    return
  }

  const distance = Math.min(width * 0.58, height * 0.62, 540)
  const x = meteor.x - progress * distance
  const y = meteor.y + progress * distance * 0.6
  const tailX = x + meteor.length
  const tailY = y - meteor.length * 0.6
  const gradient = ctx.createLinearGradient(x, y, tailX, tailY)
  gradient.addColorStop(0, '#fff2d9')
  gradient.addColorStop(0.18, '#ffc78db3')
  gradient.addColorStop(0.62, '#a28ded37')
  gradient.addColorStop(1, '#a28ded00')

  ctx.globalAlpha = 0.85 * Math.sin(progress * Math.PI)
  ctx.strokeStyle = gradient
  ctx.lineWidth = 1.25
  ctx.lineCap = 'round'
  ctx.beginPath()
  ctx.moveTo(x, y)
  ctx.lineTo(tailX, tailY)
  ctx.stroke()
}

function draw(animated: boolean) {
  const ctx = context
  if (!ctx || !height) return

  ctx.clearRect(0, 0, width, height)
  for (const star of stars) {
    const shift = animated ? scrollPosition * star.depth : 0
    const y = ((star.y * height - shift) % height + height) % height
    const pulse = animated ? 0.73 + 0.27 * Math.sin(time * star.rate + star.phase) : 0.84
    ctx.globalAlpha = star.opacity * pulse
    ctx.fillStyle = star.color
    ctx.beginPath()
    ctx.arc(star.x * width, y, star.radius, 0, 2 * Math.PI)
    ctx.fill()
  }

  if (animated) drawMeteor(ctx)
  ctx.globalAlpha = 1
}

function tick(timestamp: number) {
  const delta = timestamp - lastFrame
  if (delta >= frameInterval) {
    time += Math.min(delta, 100)
    lastFrame = timestamp
    draw(true)
  }
  frame = requestAnimationFrame(tick)
}

function syncMotion() {
  if (!context) return

  if (frame !== undefined) cancelAnimationFrame(frame)
  frame = undefined

  if (document.hidden) return
  if (motion?.matches) {
    draw(false)
    return
  }

  lastFrame = performance.now()
  draw(true)
  frame = requestAnimationFrame(tick)
}

function syncScroll() {
  scrollPosition = window.scrollY
}

function fitCanvas() {
  const element = canvas.value
  if (!element || !context) return

  width = element.clientWidth
  height = element.clientHeight
  const ratio = Math.min(window.devicePixelRatio || 1, 1.5)
  element.width = Math.round(width * ratio)
  element.height = Math.round(height * ratio)
  context.setTransform(ratio, 0, 0, ratio, 0, 0)
  const count = width < 690 ? 55 : 145
  if (stars.length !== count) stars = createStars(count)

  syncScroll()
  syncMotion()
}

onMounted(() => {
  context = canvas.value?.getContext('2d') ?? null
  if (!context) return

  motion = window.matchMedia('(prefers-reduced-motion: reduce)')
  window.addEventListener('resize', fitCanvas)
  window.addEventListener('scroll', syncScroll, { passive: true })
  document.addEventListener('visibilitychange', syncMotion)
  motion.addEventListener('change', syncMotion)
  fitCanvas()
})

onBeforeUnmount(() => {
  if (frame !== undefined) cancelAnimationFrame(frame)
  window.removeEventListener('resize', fitCanvas)
  window.removeEventListener('scroll', syncScroll)
  document.removeEventListener('visibilitychange', syncMotion)
  motion?.removeEventListener('change', syncMotion)
})
</script>

<template>
  <div class="starfield" aria-hidden="true"><canvas ref="canvas" /></div>
</template>
