import { MODES, type Half, type Mode, type Monster, type Period, type Reward } from '../types'

const boundaries = [
  '2025-01-08', '2025-01-29', '2025-02-19', '2025-03-12',
  '2025-04-02', '2025-04-23', '2025-05-14',
]
const growth = [0, 42_800, 87_600, 62_400, 126_000, 158_400]

type MockMonster = Omit<Monster, 'hp'> & { baseHp: number }

const rosters: Record<Mode, MockMonster[]> = {
  fiction: [
    { id: 'silverguard', name: '银鬃尉官', baseHp: 360_000, weakness: ['物理', '冰', '量子'], floor: '第 4 层', room: '节点一', note: '架盾后会反击攻击者。' },
    { id: 'automaton-direwolf', name: '自动机兵·齿狼', baseHp: 257_000, weakness: ['冰', '雷', '虚数'], floor: '第 4 层', room: '节点二', note: '锁定单体目标后发动连击。' },
    { id: 'blaze-out-of-space', name: '外宇宙之炎', baseHp: 209_000, weakness: ['物理', '冰', '量子'], floor: '第 3 层', room: '节点二', note: '群体攻击可施加灼烧。' },
  ],
  forgotten: [
    { id: 'cocolia', name: '可可利亚', baseHp: 735_000, weakness: ['火', '雷', '量子'], floor: '第 12 层', room: '节点一', note: '召唤冰棱协同攻击。' },
    { id: 'deer', name: '丰饶玄鹿', baseHp: 704_000, weakness: ['火', '冰', '量子'], floor: '第 12 层', room: '节点二', note: '召唤枝梢强化自身。' },
    { id: 'guardian-shadow', name: '守护者之影', baseHp: 405_000, weakness: ['物理', '风', '量子'], floor: '第 11 层', room: '节点一', note: '违反禁令会触发惩戒。' },
  ],
  apocalypse: [
    { id: 'kafka', name: '卡芙卡', baseHp: 1_195_000, weakness: ['物理', '风', '虚数'], floor: '难度 IV', room: '节点一', note: '可支配角色，使其攻击队友。' },
    { id: 'doomsday-beast', name: '末日兽', baseHp: 1_316_000, weakness: ['火', '冰', '风'], floor: '难度 IV', room: '节点二', note: '击破部位后核心进入易伤状态。' },
    { id: 'storm-out-of-space', name: '外宇宙之冰', baseHp: 527_000, weakness: ['火', '风', '量子'], floor: '难度 III', room: '节点一', note: '部分攻击可施加冻结。' },
  ],
  arbitration: [
    { id: 'sam', name: '星核猎手·萨姆', baseHp: 1_805_000, weakness: ['雷', '量子', '虚数'], floor: '试炼三', room: '节点一', note: '进入强化状态后为战场附加燃烧效果。' },
    { id: 'svarog', name: '史瓦罗', baseHp: 1_568_000, weakness: ['火', '雷', '风'], floor: '试炼三', room: '节点二', note: '机械臂可限制角色行动。' },
    { id: 'argent-knight', name: '银枝', baseHp: 1_092_000, weakness: ['物理', '火', '冰'], floor: '试炼二', room: '节点二', note: '召唤饰物提供额外效果。' },
  ],
}

const rewards: Record<Mode, Reward[]> = {
  fiction: [
    { name: '星琼', icon: 'stellar-jade', amount: 800, condition: '累计取得 12/12 星' },
    { name: '信用点', icon: 'credits', amount: 120_000, condition: '完成全部 4 层关卡' },
  ],
  forgotten: [
    { name: '星琼', icon: 'stellar-jade', amount: 800, condition: '累计取得 36/36 星' },
    { name: '流光余晖', icon: 'medal', amount: 200, condition: '通关第 12 层' },
  ],
  apocalypse: [
    { name: '星琼', icon: 'stellar-jade', amount: 800, condition: '累计取得 12/12 星' },
    { name: '信用点', icon: 'credits', amount: 120_000, condition: '完成难度 IV 的两个节点' },
  ],
  arbitration: [
    { name: '自塑尘脂', icon: 'resin', amount: 1, condition: '完成第三试炼的全部节点' },
    { name: '命运的足迹', icon: 'tracks', amount: 1, condition: '达成任意两个试炼目标' },
    { name: '信用点', icon: 'credits', amount: 180_000, condition: '完成第一试炼' },
  ],
}

export const mockPeriods: Period[] = MODES.flatMap((mode, modeIndex) =>
  growth.map((increase, index) => {
    const version = '1.' + (Math.floor(index / 2) + 1)
    const half: Half = index % 2 === 0 ? '上半' : '下半'
    const monsters = rosters[mode].map(({ baseHp, ...monster }, monsterIndex) => ({
      ...monster,
      hp: baseHp + increase * (modeIndex + 1) / 4 + (index % 2) * monsterIndex * 2_300,
    }))

    return {
      id: mode + '-' + version + (half === '上半' ? '-first' : '-second'),
      mode,
      majorVersion: 1,
      version,
      half,
      startTime: boundaries[index] + 'T04:00:00+08:00',
      endTime: boundaries[index + 1] + 'T04:00:00+08:00',
      monsters,
      rewards: rewards[mode],
      totalHp: monsters.reduce((total, monster) => total + monster.hp, 0),
    }
  }),
)
