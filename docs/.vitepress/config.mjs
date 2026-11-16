import { defineConfig } from 'vitepress'

const githubPages = process.env.VITEPRESS_DEPLOY_TARGET === 'github-pages'

export default defineConfig({
  base: githubPages ? '/wind-data-analysis-guide/' : '/',
  outDir: githubPages ? '.vitepress/dist-github-pages' : '.vitepress/dist',
  lang: 'zh-CN',
  title: '风电数据分析教程',
  description: '风机运行工况、SCADA 数据质量、变桨状态监测、现场测风、功率曲线与风场运行后评估',
  appearance: false,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '运行工况', link: '/operations' },
    ],
    sidebar: [
      { text: '运行工况与变桨故障', link: '/operations' },
      { text: 'SCADA 数据质量与筛选', link: '/scada' },
      { text: '变桨状态监测', link: '/pitch' },
      { text: '风速对照与拟合', link: '/wind-speed' },
      { text: '功率曲线建模与验证', link: '/power' },
      { text: '风频与 Weibull 拟合', link: '/wind-frequency' },
      { text: '风场运行后评估', link: '/assessment' },
    ],
    outline: { label: '本页目录', level: [2, 3] },
    docFooter: { prev: '上一篇', next: '下一篇' },
    sidebarMenuLabel: '章节',
    returnToTopLabel: '返回顶部',
    darkModeSwitchLabel: '外观',
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索教程', buttonAriaLabel: '搜索教程' },
          modal: {
            displayDetails: '显示结果详情',
            resetButtonTitle: '清空搜索',
            backButtonTitle: '关闭搜索',
            noResultsText: '没有找到相关内容',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },
  },
})
