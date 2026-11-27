import { BookOpen, Castle, Eclipse, Scale } from '@lucide/vue'
import type { Component } from 'vue'
import type { Mode } from '../types'

export const modeInfo = {
  fiction: {
    name: '虚构叙事',
    description: '查看叙事关卡的敌方阵容与血量变化。',
    icon: BookOpen,
    color: '#f3bd8b',
    tint: '#d9955e28',
  },
  forgotten: {
    name: '忘却之庭',
    description: '追踪混沌回忆各层怪物的血量变化。',
    icon: Castle,
    color: '#d7b8fa',
    tint: '#ae85dc35',
  },
  apocalypse: {
    name: '末日幻影',
    description: '对比首领节点的血量、弱点与机制。',
    icon: Eclipse,
    color: '#abe0cf',
    tint: '#81cbb12b',
  },
  arbitration: {
    name: '异想仲裁',
    description: '查阅仲裁试炼的敌方阵容与专属奖励。',
    icon: Scale,
    color: '#ffad9a',
    tint: '#e38c7c2d',
  },
} satisfies Record<Mode, { name: string; description: string; icon: Component; color: string; tint: string }>
