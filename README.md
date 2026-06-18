# My 2022 Logseq Note

> 发布状态：Logseq GitHub Pages 工作流已成功生成 `gh-pages` 分支，但仓库 GitHub Pages 目前尚未启用。待在 GitHub Settings -> Pages 中选择 `gh-pages / root` 后，预计可通过 `https://conanxin.github.io/My-2022-Logseq-Note/` 在线阅读。

这是 2022 年 5 月的一组 Logseq 阅读笔记与知识采集档案。

它不是一个代码应用，而是一份早期个人知识系统的快照：我当时把每天看到的文章、项目、书、视频、人物和概念收集到 Logseq 中，用标签、双链和每日记录串起来。今天重新整理它，是为了让这批旧笔记变得可读、可展示，也方便以后继续拆分成文章、专题或研究线索。

## 原始笔记目录

- `journals/`：每日记录，按日期保存 2022 年 5 月的阅读与摘录。
- `pages/`：主题页面，包含部分由 Logseq 自动生成或手动创建的页面。
- `assets/`：图片与视频素材，来自当时笔记中的引用。
- `logseq/`：Logseq 配置与页面元数据。

本次升级尽量不改动原始笔记，只新增说明文档、统计脚本和 GitHub Pages 发布工作流。

## 如何阅读

如果你只是想快速了解这批笔记，可以先看 [INDEX.md](INDEX.md)。它把笔记按 6 条主线重新整理：Web3、AI、思考工具、元宇宙、设计艺术、永久计算与太阳朋克。

如果你想了解这个仓库本身的价值和问题，可以看 [docs/PROJECT_ANALYSIS.md](docs/PROJECT_ANALYSIS.md)。如果你想看机器统计结果，可以看 [docs/GRAPH_STATS.md](docs/GRAPH_STATS.md)。

如果你熟悉 Logseq，也可以直接用 Logseq 打开这个仓库，将它作为一个 graph 阅读。

## 主要主题

- Web3 / 区块链 / DAO：以太坊、去中心化社会、DAO、NFT、稳定币和 Web3 应用架构。
- AI / 大语言模型 / 文明：GPT-3、DeepMind、常识推理、AI 与文明未来。
- Tools for Thought / 可编程笔记：Heptabase、Programmable Notes、Dynamicland、Engelbart、Alan Kay、Bret Victor。
- 元宇宙 / 游戏 / 虚拟世界：Metaverse、Fortnite、VR、Will Wright、GDC 和虚拟空间设计。
- 设计 / 艺术 / 未来想象：沉浸式艺术、可视化、未来展览、乌托邦黑客和数字艺术。
- 永久计算 / 太阳朋克 / 长期主义工具：Hundred Rabbits、Uxn、Low-Tech Magazine、IPFS、solarpunk。

## 如何继续整理

一个轻量路线是：

1. 先运行统计脚本，确认主题、标签和外链分布。
2. 按 [INDEX.md](INDEX.md) 的 6 条主线补充每篇专题页。
3. 从每条主线挑 1 到 2 个问题，整理成独立文章。
4. 保留原始 Logseq 笔记，只在 `docs/` 中写整理后的解释和索引。

最简单的本地统计命令：

```bash
python3 scripts/analyze_logseq_archive.py
```

在 Windows PowerShell 中，如果 `python3` alias 不可用，也可以使用：

```powershell
python .\scripts\analyze_logseq_archive.py
```

## 如何发布

仓库包含 GitHub Actions workflow：`.github/workflows/publish-logseq.yml`。它会在 push 到 `master` 或手动触发时，使用 `logseq/publish-spa` 将 Logseq graph 发布到 `gh-pages` 分支。

当前发布工作流已配置并成功生成 `gh-pages` 分支。GitHub Pages 仍需要在仓库设置中启用：Settings -> Pages -> Source 选择 `Deploy from a branch`，Branch 选择 `gh-pages / root`。

## 升级记录

本次升级报告见 [docs/UPGRADE_REPORT_L2022_1A.md](docs/UPGRADE_REPORT_L2022_1A.md)。

发布检查报告见 [docs/PUBLISH_REPORT_L2022_1B.md](docs/PUBLISH_REPORT_L2022_1B.md)。
