# 风电数据分析教程

面向计算机团队的风电数据分析入门教程。用公开运行记录和现场测风案例，说明风机运行工况、SCADA 数据筛选、变桨偏离筛查、两路测风对照、同期功率估算和风场后评估的基本做法。

- **在线教程**：https://luyh-101.github.io/wind-data-analysis-guide/
- **源码仓库**：https://github.com/luyh-101/wind-data-analysis-guide
- **当前结构**：首页 + 七个核心章节，使用 VitePress 构建
- **当前范围**：以公开案例和方法演示为主，不包含项目私有数据、厂商内部参数或完整项目工作说明

## 教程内容

| 顺序 | 章节 | 文件 |
| --- | --- | --- |
| 1 | 风机运行工况与变桨故障排查 | `docs/operations.md` |
| 2 | SCADA 数据质量与工况筛选 | `docs/scada.md` |
| 3 | 变桨状态监测与异常筛查 | `docs/pitch.md` |
| 4 | 两路实测风速对照 | `docs/wind-speed.md` |
| 5 | 两路实测风频比较 | `docs/wind-frequency.md` |
| 6 | 用风速估算同期功率 | `docs/power.md` |
| 7 | 风场运行后评估 | `docs/assessment.md` |

首页是 `docs/index.md`。教程重点是读懂运行记录、把同一时段的量对齐、区分“风速差（m/s）”和“风频差（百分点）”，以及把功率曲线用于同期电量对照。

## 本地预览

### 环境

- Node.js 22.13 或更高版本
- pnpm 11.25.0（`package.json` 已声明版本；未安装时可用 `start-preview.cmd` 自动调用）
- Windows 下可直接使用项目根目录的 `start-preview.cmd`

### 直接打开

1. 克隆仓库，或从 GitHub 下载 ZIP 后解压。
2. 在 VS Code 中打开包含 `package.json`、`pnpm-lock.yaml` 和 `docs` 的目录。
3. 在项目根目录打开 PowerShell，运行：

```powershell
.\start-preview.cmd
```

脚本会检查 Node.js 版本，安装锁定依赖并启动 VitePress。打开终端中 `Local` 后面的地址，通常是 http://127.0.0.1:5173/ 。结束预览按 `Ctrl+C`。

### 手动启动

```powershell
pnpm install --frozen-lockfile
pnpm run dev
```

macOS 或 Linux 使用同样的 pnpm 命令即可。

## 构建与部署

### 根路径构建

```powershell
pnpm run build
pnpm run preview
```

产物在 `docs/.vitepress/dist/`。

### GitHub Pages 子路径构建

```powershell
$env:VITEPRESS_DEPLOY_TARGET = 'github-pages'
pnpm run build
pnpm run preview
```

启动后访问 `http://127.0.0.1:4173/wind-data-analysis-guide/`。子路径版产物在 `docs/.vitepress/dist-github-pages/`。

### 自动部署

仓库通过 `.github/workflows/deploy-pages.yml` 部署到 GitHub Pages：

- 推送到 `main` 后自动构建和部署；
- 使用 pnpm 锁文件安装依赖；
- Pages 的 Source 设为 **GitHub Actions**；
- 正式地址：https://luyh-101.github.io/wind-data-analysis-guide/

## 目录说明

```text
docs/
  index.md                 首页
  operations.md            运行工况
  scada.md                 SCADA 数据质量与筛选
  pitch.md                 变桨状态监测
  wind-speed.md            两路实测风速对照
  wind-frequency.md        两路实测风频比较
  power.md                 同期功率估算
  assessment.md            风场运行后评估
  .vitepress/              配置、主题和组件
  public/data/             公开案例数据和复算脚本
  public/figures/          教程图表
scripts/
  plot-tutorial-figures.py 生成实测与示意图表
  draw-tutorial-diagrams.py 生成流程示意图
.github/workflows/         GitHub Pages 部署
```

## 修改正文和图表

普通正文直接编辑 `docs/*.md`，保存后浏览器会刷新预览。

页面中的读图组件是 `docs/.vitepress/theme/components/TeachingFigure.vue`。它负责统一图片、图注、点击查看原图和 `base` 路径，示例：

```md
<TeachingFigure
  src="/figures/example.png"
  :width="1020"
  :height="580"
  title="图题"
  alt="图片替代说明"
>
  图注正文。
</TeachingFigure>
```

新增图片放入 `docs/public/figures/`，用 `/figures/文件名` 引用。手写 HTML 的下载或原图链接时，需要从 `vitepress` 导入 `withBase`，并用 `:href="withBase('/figures/文件名')"`，否则 GitHub Pages 子路径下会失效。

实测图表由 `scripts/plot-tutorial-figures.py` 生成，流程示意图由 `scripts/draw-tutorial-diagrams.py` 生成。运行前安装 Python 依赖：

```powershell
python -m pip install pandas matplotlib pyarrow
python scripts/plot-tutorial-figures.py
python scripts/draw-tutorial-diagrams.py
```

图表生成脚本读取 `docs/public/data/` 中的公开节选；修改数据或图形后应重新生成图片并检查站点。图中数值只对应案例时段，不应直接当成其他机组或长期项目的结论。

## 案例数据与来源

`docs/public/data/` 保留四组公开案例的节选、说明和复算脚本：

- [案例数据说明](docs/public/data/case-data-notes.txt)
- Aventa AV-7：`aventa-linked-scatter.csv`、`aventa-case-input.parquet`
- ENGIE La Haute Borne：`engie-r80711-2014-02-03.csv`、`engie-case-input.zip`
- Kelmarsh：`kelmarsh-blade-pitch.csv`
- AWAKEN King Plains：`awaken-a1-wt041-2023-08-24.csv`、`awaken-a1-lidar-80m-10min.csv`、`awaken-wt041-scada-1min.csv`
- 复算脚本：`reproduce-scada-cases.py`

主要来源和许可：

- **Aventa AV-7**：Barber、Hammer、Marykovskiy，Zenodo，CC BY 4.0，https://doi.org/10.5281/zenodo.16738078
- **ENGIE La Haute Borne**：ENGIE Renewables / OpenOA 示例归档，Etalab Open Licence 2.0
- **Kelmarsh**：Charlie Plumley（Cubico），Zenodo，CC BY 4.0，https://doi.org/10.5281/zenodo.8252025
- **AWAKEN King Plains**：Nicola Bodini，Zenodo，CC BY 4.0，https://doi.org/10.5281/zenodo.15623845

完整的字段映射、筛选条件、时段和许可说明见 [案例数据说明](docs/public/data/case-data-notes.txt)。网站上的实测图使用这些节选绘制，转载或再利用时请保留数据来源和许可署名。

首页照片由美国鱼类及野生动物管理局拍摄，原图标注为公有领域，站内使用缩小后的 WebP：https://commons.wikimedia.org/wiki/File:Wind_turbines_%2854091153454%29.jpg

## 维护约定

- 页面标题、侧边栏和导航以当前七个章节为准；不要重新引入已删除的专题页。
- 章节顺序为：运行工况 → SCADA → 变桨 → 两路风速 → 两路风频 → 同期功率 → 风场后评估。
- 新增实测数字时，要同时写出数据来源、时间窗口、样本数和筛选条件。
- 合成示意图必须在可见标题或图注中标注“示意”，不能与实测图混用。
- 修改图表后重新运行构建，检查图片、站内锚点和 GitHub Pages 子路径。
- `CaseWalkthrough.vue` 和 `lesson-cases.data.js` 是旧版交互组件的保留文件，当前页面不再引用；新增页面请使用 `TeachingFigure.vue`。
