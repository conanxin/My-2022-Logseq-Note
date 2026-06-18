#!/usr/bin/env python3
"""Analyze the 2022 Logseq archive and write docs/GRAPH_STATS.md.

用途：
    只读扫描 journals/ 和 pages/ 中的 Markdown 笔记，统计标签、外链域名、
    Logseq 双链、主题词和基础文件数量，生成一个可重复运行的 Markdown 报告。

运行方法：
    python3 scripts/analyze_logseq_archive.py

脚本只使用 Python 标准库，不修改 journals/、pages/、assets/ 或 logseq/ 内容。
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
JOURNALS_DIR = ROOT / "journals"
PAGES_DIR = ROOT / "pages"
ASSETS_DIR = ROOT / "assets"
LOGSEQ_DIR = ROOT / "logseq"
OUTPUT_PATH = ROOT / "docs" / "GRAPH_STATS.md"

TAG_RE = re.compile(r"(?<![\w/])#([A-Za-z0-9_\-·\u4e00-\u9fff\u3040-\u30ff]+)")
URL_RE = re.compile(r"https?://[^\s\])>\"']+")
WIKILINK_RE = re.compile(r"\[\[([^\]\n]+)\]\]")
DATE_RE = re.compile(r"^(\d{4})_(\d{2})_(\d{2})\.md$")

TOPIC_TERMS = {
    "Web3": ["web3", "web 3", "web 3.0"],
    "区块链": ["区块链", "blockchain"],
    "DAO": ["dao", "daos"],
    "NFT": ["nft", "nfts"],
    "以太坊": ["以太坊", "ethereum"],
    "加密货币": ["加密货币", "crypto", "cryptocurrency", "cryptocurrencies"],
    "去中心化": ["去中心化", "decentralized", "decentralization"],
    "人工智能": ["人工智能", "ai"],
    "GPT-3": ["gpt-3", "gpt3"],
    "语言模型": ["语言模型", "language model", "large language model"],
    "DeepMind": ["deepmind"],
    "常识": ["常识", "common sense"],
    "文明": ["文明", "civilization"],
    "思考工具": ["思考工具", "tools for thought"],
    "可编程笔记": ["可编程笔记", "programmable notes", "programmatic notes"],
    "Heptabase": ["heptabase"],
    "Logseq": ["logseq"],
    "Dynamicland": ["dynamicland"],
    "Engelbart": ["engelbart", "恩格尔巴特"],
    "Ted Nelson": ["ted nelson", "泰德·尼尔森"],
    "Alan Kay": ["alan kay", "艾伦·凯"],
    "Bret Victor": ["bret victor", "布雷特·维克多"],
    "元宇宙": ["元宇宙", "metaverse"],
    "虚拟世界": ["虚拟世界", "virtual world", "virtual worlds"],
    "游戏": ["游戏", "game", "games", "gaming"],
    "VR": ["vr"],
    "设计": ["设计", "design"],
    "艺术": ["艺术", "art"],
    "可视化": ["可视化", "visualization"],
    "未来": ["未来", "future"],
    "太阳朋克": ["太阳朋克", "solarpunk"],
    "永久计算": ["永久计算", "permanent computing"],
    "离线优先": ["离线优先", "offline-first", "offline first"],
    "Hundred Rabbits": ["hundred rabbits", "100r"],
    "Uxn": ["uxn"],
    "IPFS": ["ipfs"],
    "互联网": ["互联网", "internet"],
    "创作者经济": ["创作者经济", "creator economy"],
    "小额支付": ["小额支付", "micropayments"],
    "社区": ["社区", "community", "communities"],
    "平台": ["平台", "platform", "platforms"],
}

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob("*.md"), key=lambda path: path.name.casefold())


def asset_files() -> list[Path]:
    if not ASSETS_DIR.exists():
        return []
    return sorted((path for path in ASSETS_DIR.iterdir() if path.is_file()), key=lambda path: path.name.casefold())


def format_date_from_filename(path: Path) -> str | None:
    match = DATE_RE.match(path.name)
    if not match:
        return None
    year, month, day = match.groups()
    return f"{year}-{month}-{day}"


def normalize_domain(url: str) -> str | None:
    parsed = urlparse(url)
    if not parsed.netloc:
        return None
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def count_topics(text: str) -> Counter[str]:
    lowered = text.lower()
    counts: Counter[str] = Counter()
    for display, variants in TOPIC_TERMS.items():
        total = 0
        for variant in variants:
            total += lowered.count(variant.lower())
        if total:
            counts[display] = total
    return counts


def sorted_counter(counter: Counter[str], limit: int = 30) -> list[tuple[str, int]]:
    return sorted(counter.items(), key=lambda item: (-item[1], item[0].casefold()))[:limit]


def table_rows(items: list[tuple[str, int]], label: str) -> str:
    if not items:
        return "| 排名 | " + label + " | 次数 |\n| --- | --- | --- |\n| - | 无 | 0 |\n"
    lines = [f"| {index} | {name} | {count} |" for index, (name, count) in enumerate(items, start=1)]
    return "| 排名 | " + label + " | 次数 |\n| --- | --- | --- |\n" + "\n".join(lines) + "\n"


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def main() -> None:
    journal_files = markdown_files(JOURNALS_DIR)
    page_files = markdown_files(PAGES_DIR)
    assets = asset_files()

    combined_text_parts: list[str] = []
    tags: Counter[str] = Counter()
    domains: Counter[str] = Counter()
    wikilinks: Counter[str] = Counter()
    topics: Counter[str] = Counter()

    for path in journal_files + page_files:
        text = read_text(path)
        combined_text_parts.append(text)
        tags.update("#" + tag for tag in TAG_RE.findall(text))
        wikilinks.update(link.strip() for link in WIKILINK_RE.findall(text) if link.strip())
        for url in URL_RE.findall(text):
            domain = normalize_domain(url)
            if domain:
                domains[domain] += 1
        topics.update(count_topics(text))

    dates = [date for path in journal_files if (date := format_date_from_filename(path))]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "unknown"

    workflow_dir = ROOT / ".github" / "workflows"
    publish_workflow = workflow_dir / "publish-logseq.yml"
    has_any_workflow = workflow_dir.exists() and any(workflow_dir.glob("*.yml"))
    has_pages_config = publish_workflow.exists()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = [
        "# Graph Stats",
        "",
        "本报告由 `scripts/analyze_logseq_archive.py` 生成。脚本只读扫描 `journals/` 与 `pages/`，并统计仓库当前的公开发布配置文件状态。",
        "",
        "## 基础统计",
        "",
        "| 指标 | 值 |",
        "| --- | --- |",
        f"| 日记文件数量 | {len(journal_files)} |",
        f"| 页面文件数量 | {len(page_files)} |",
        f"| Asset 数量 | {len(assets)} |",
        f"| 日期范围 | {date_range} |",
        f"| 是否存在 README.md | {yes_no((ROOT / 'README.md').exists())} |",
        f"| 是否存在 GitHub Actions workflow | {yes_no(has_any_workflow)} |",
        f"| 是否存在 GitHub Pages 发布配置文件 | {yes_no(has_pages_config)} |",
        f"| 是否存在 logseq/config.edn | {yes_no((LOGSEQ_DIR / 'config.edn').exists())} |",
        f"| 是否存在 logseq/pages-metadata.edn | {yes_no((LOGSEQ_DIR / 'pages-metadata.edn').exists())} |",
        "",
        "## 高频标签 Top 30",
        "",
        table_rows(sorted_counter(tags), "标签"),
        "## 高频外链域名 Top 30",
        "",
        table_rows(sorted_counter(domains), "域名"),
        "## 高频 Logseq 双链 Top 30",
        "",
        table_rows(sorted_counter(wikilinks), "双链"),
        "## 高频主题词 Top 30",
        "",
        table_rows(sorted_counter(topics), "主题词"),
        "## 日记文件",
        "",
        "\n".join(f"- `journals/{path.name}`" for path in journal_files) or "- 无",
        "",
        "## 页面文件",
        "",
        "\n".join(f"- `pages/{path.name}`" for path in page_files) or "- 无",
        "",
        "## Assets",
        "",
        "\n".join(f"- `assets/{path.name}`" for path in assets) or "- 无",
        "",
    ]
    OUTPUT_PATH.write_text("\n".join(report), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
