# 风电数据分析教程

用 VS Code 编辑 Markdown，用 VitePress 预览和构建。下面以 Windows 为例。

## 1. 打开项目

1. 在资源管理器中右键点击 `wind-data-analysis-guide.zip`，选择「全部解压缩」。
2. 在 VS Code 选择「文件 → 打开文件夹」，打开解压后包含 `package.json`、`pnpm-lock.yaml` 和 `docs` 的 `wind-data-analysis-guide` 文件夹。
3. 在 VS Code 选择「终端 → 新建终端」。运行 `node --version` 检查版本。项目需要 Node.js 22.13 或更高版本。初次安装 Node.js 时保留 npm 和 npx，安装后重新打开 VS Code。 [Node.js 下载](https://nodejs.org/en/download)

## 2. 启动本地预览

在项目根目录的 PowerShell 终端运行：

```powershell
.\start-preview.cmd
```

首次运行需要联网安装锁定的依赖。已有 pnpm 时，脚本用 pnpm 安装。未安装 pnpm 时，脚本通过 npx 调用项目指定的版本，无需全局安装。依赖就绪后，脚本直接启动 VitePress。

打开终端中 `Local` 后的网址，通常是 [http://127.0.0.1:5173/](http://127.0.0.1:5173/)。保持终端运行，结束预览时按 `Ctrl+C`。macOS 或 Linux 可在项目目录运行 `pnpm install --frozen-lockfile` 和 `pnpm run dev`。 [VitePress 快速开始](https://vitepress.dev/zh/guide/getting-started)

## 3. 修改正文和图片

在 VS Code 左侧打开对应文件，修改后按 `Ctrl+S` 保存，再回到浏览器检查效果。

| 要修改的内容 | 文件 |
| --- | --- |
| 首页 | `docs/index.md` |
| 风机运行工况与变桨故障 | `docs/operations.md` |
| SCADA 数据质量与工况筛选 | `docs/scada.md` |
| 变桨状态监测 | `docs/pitch.md` |
| 现场测风对照与拟合 | `docs/wind-speed.md` |
| 功率曲线建模与验证 | `docs/power.md` |
| 风频与 Weibull 拟合 | `docs/wind-frequency.md` |
| 风场运行后评估 | `docs/assessment.md` |
| 运行分析专题 | `docs/practice.md` |
| 方法选择与公开案例 | `docs/research.md` |
| 案例图和 CSV | `docs/public/figures/`、`docs/public/data/` |
| 站点标题和导航 | `docs/.vitepress/config.mjs` |
| 全站字号、行距和正文栏宽 | `docs/.vitepress/theme/style.css` |
| 时间轴、覆盖图和实测对照 | `docs/.vitepress/theme/components/` |

审阅时可把浏览器和 VS Code 并排放。按 `Ctrl+P` 输入上表中的文件名快速打开章节，按 `Ctrl+Shift+F` 查找全站用词，修改后按 `Ctrl+S` 回浏览器核对。要统一调整排版，改样式文件开头的 `--tutorial-*` 变量。首页的标题、介绍、按钮和卡片文字在 `docs/index.md` 顶部的 `---` 之间。

新增图表时，把图片放进 `docs/public/figures/`，正文用 `![图表说明](/figures/your-chart.png)` 引用。预览会随文件保存更新。 [VitePress 静态资源说明](https://vitepress.dev/zh/guide/asset-handling)

普通 Markdown 链接和图片使用站内路径。如果手写 HTML 链接用于下载或打开原图，在页面的 `<script setup>` 中从 `vitepress` 导入 `withBase`，并用 `:href="withBase('/figures/your-chart.png')"` 生成地址。

案例图解的说明文字在 `CaseWalkthrough.vue`。图中的实测数值由 `lesson-cases.data.js` 读取站内公开 CSV 并计算。

首页照片由美国鱼类及野生动物管理局拍摄，原图标注为公有领域。站内使用缩小后的 WebP。 [原图与许可](https://commons.wikimedia.org/wiki/File:Wind_turbines_%2854091153454%29.jpg)

## 4. 构建根路径版

内容定稿且已安装依赖后，在 VS Code 新开一个终端运行：

```powershell
npm.cmd run build
npm.cmd run preview
```

构建完成后，打开预览命令打印的地址，检查首页、章节跳转、图片和 CSV 下载。这里预览的是本次构建生成的版本。 [VitePress 构建与部署](https://vitepress.dev/zh/guide/deploy)

发布文件在 `docs/.vitepress/dist/`。上传时选这个文件夹，或者把它里面的文件和子文件夹一起压缩，确保 ZIP 打开后的第一层就有 `index.html`。随交付提供的 `wind-data-analysis-site.zip` 是已构建的版本。在上码发布或更新原项目后，先用电脑无痕窗口和手机流量核对正式网址，再发给成员。 [上码发布与更新指南](https://www.upma.cn/docs)

## 5. GitHub Pages 自动部署

在 GitHub 仓库中，打开 **Settings → Pages**，将 **Build and deployment → Source** 设为 **GitHub Actions**。推送到 `main` 后，工作流按 `package.json` 指定的 pnpm 版本和锁文件安装依赖，构建并部署到 [GitHub Pages 站点](https://luyh-101.github.io/wind-data-analysis-guide/)。如果空仓库暂时无法选择来源，首次推送后再设置，并在 **Actions** 中运行工作流。 [GitHub Pages 工作流说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

要在本机验证同样的子路径，在新开的 PowerShell 终端运行以下命令。

```powershell
$env:VITEPRESS_DEPLOY_TARGET = 'github-pages'
npm.cmd run build
npm.cmd run preview
```

用预览端口访问 `/wind-data-analysis-guide/`，例如 [http://127.0.0.1:4173/wind-data-analysis-guide/](http://127.0.0.1:4173/wind-data-analysis-guide/)。子路径版产物在 `docs/.vitepress/dist-github-pages/`。结束预览后关闭这个终端，或运行 `Remove-Item Env:VITEPRESS_DEPLOY_TARGET`，使当前终端恢复根路径构建。

## 6. 分享源码

源码 ZIP 包含根目录的 README、项目配置、锁文件、启动脚本和部署工作流，以及 `docs` 中的章节、主题配置和公开资源。依赖、缓存和两种构建产物按 `.gitignore` 排除。提交前核对文件清单，`docs/public/` 中的文件会随网站一起公开。解压后在 VS Code 打开包含本 README 和 `package.json` 的目录。
