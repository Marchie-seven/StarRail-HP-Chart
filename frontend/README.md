# 星轨档案 · 怪物血量统计

基于 Vue 3、Vite、TypeScript、ECharts 和 Vue Router 的纯前端作品集项目。内置四种玩法，各有 1.1、1.2、1.3 的上半与下半。日期、血量、阵容及奖励均为演示数据。

## 启动与构建

使用 Node.js 20.19+ 的 20.x，或 Node.js 22.12+。解压后在 `star-rail-hp-archive` 目录运行以下命令。

```bash
npm ci
npm run dev
```

打开 Vite 终端显示的地址，默认是 `http://localhost:5173`。在 Windows PowerShell 中，如果脚本执行策略拦截了 `npm.ps1`，可运行 `npm.cmd ci` 和 `npm.cmd run dev`。

```bash
npm run typecheck
npm run build
npm run preview
```

`npm run build` 先检查 TypeScript，再输出静态资源到 `dist/`。`npm run preview` 用于本地检查构建产物。应用使用哈希路由，可将 `dist/` 放到支持静态文件的站点目录。

## 浏览档案

- 首页展示四种玩法入口以及各模式最近开放一期的总血量、阵容规模和开放日期。
- 模式页的大小版本筛选同时作用于图表、明细和奖励。折线图支持总血量、单怪和单层三个口径，支持将上半和下半分线，或勾选多个怪物对比。
- 拖动图表底部滑块可缩放，拖动选中区域可平移。桌面也可在图表上按住 Ctrl 滚动缩放。点击数据点或表格中的期数可打开详情。
- 奖励面板默认展示筛选结果中最近开放的一期，可切换到其他期数。怪物或层级在某期缺席时，折线留空。
- 全站使用深色星空主题。小屏幕减少星点，页面不可见时暂停绘制，开启系统的减少动态效果选项时仅显示静态星点。

## 环境变量

复制 `.env.example` 为 `.env.local` 后可修改配置，修改后重启 Vite。

| 变量 | 默认值 | 用途 |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `/api` | API 前缀。Vite 开发代理将 `/api` 转发到 `http://127.0.0.1:8000`，并保留路径前缀。 |
| `VITE_USE_MOCK` | `true` | 默认读取本地 mock。FastAPI 就绪后设为 `false`，重启 Vite 即可联调。 |
| `VITE_MOCK_STATE` | 留空 | 设置 `empty` 或 `error` 可复现空数据或请求失败。默认 mock 延迟为 240 ms。 |

API 层负责把 FastAPI 的 snake_case JSON 转成组件使用的 camelCase。已有模式页用同一份分页明细生成图表、表格和奖励。另有 `getModeChart()` 供仅需趋势数据的调用方使用。生产部署使用同源 `/api` 时，由部署环境把该路径转发至 FastAPI。

## 目录结构

```text
star-rail-hp-archive/
├── .env.example           # 后端基址占位与 mock 状态
├── index.html
├── package.json
├── package-lock.json
├── vite.config.ts
├── tsconfig.json
└── src/
    ├── api/               # 请求、DTO 转换及 mock 适配
    ├── assets/            # 首页原创星轨插画
    ├── components/        # 折线图、明细表、奖励、状态和详情抽屉
    ├── domain/            # 版本排序、显示格式、玩法与图表口径
    ├── mock/              # 本地演示数据
    ├── views/             # 首页与四种玩法共用的模式页面
    ├── App.vue
    ├── main.ts
    ├── router.ts
    ├── styles.css
    └── types.ts           # Period、Monster、Reward、Mode
```

## 插画

`src/assets/orbit-hero.jpg` 由内置 ImageGen 生成并转为 JPEG。提示词如下。

> Use case: stylized-concept. Banner illustration for an original Chinese-language fan analytics archive about interstellar RPG encounters. Wide landscape crop. Deep warm espresso to near-black space, extremely dark and nearly empty leftmost 40 percent so website heading will be placed over it separately. On the right, a giant copper-gold ringed planet with its globe half eclipsed, bright slender rings sweeping diagonally from lower left toward upper right. Dusty burnt orange star clusters, tiny stars, elegant visible grain and fine etched orbital lines, antique astronomical print meets cinematic editorial science-fiction, quiet and refined. Right-side light and texture, very dark edges, strong chiaroscuro. Color palette black-brown, sepia, amber, old copper, muted ivory light. No lettering, logos, diagrams with labels, game characters, spaceships, emblems, pictograms, trademarks, or UI elements.
