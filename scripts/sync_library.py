#!/usr/bin/env python3
"""Update the distributable skill from a reviewed local knowledge library."""
import argparse
import json
from pathlib import Path
import re
import shutil

parser = argparse.ArgumentParser(description='将已核对的知识库同步到项目内的 Skill。')
parser.add_argument('--source', type=Path, required=True, help='包含打开目录.html和PDF目录的资料包路径')
args = parser.parse_args()
source = args.source.resolve()
target = Path(__file__).resolve().parents[1] / 'skills/yuecai-knowledge-search/assets/library'
page = (source / '打开目录.html').read_text(encoding='utf-8')
records = json.loads(re.search(r'<script id="data"[^>]*>(.*?)</script>', page, re.S).group(1))
paths = {pdf['path'] for record in records for pdf in record['pdfs']}
for relative in paths:
    path = (source / relative).resolve()
    path.relative_to(source)
    if not path.is_file():
        raise FileNotFoundError(path)
for name in ['打开目录.html', 'progressive-reveal.css', 'progressive-reveal.js',
             '粤菜需求_问题总结.xlsx', '文档导出清单.json', '使用说明.txt', *sorted(paths)]:
    destination = target / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / name, destination)
(target / 'catalog.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
for stale in (target / 'PDF').glob('*.pdf'):
    if str(stale.relative_to(target)) not in paths:
        stale.unlink()
print(f'同步完成：{len(records)} 条记录，{len(paths)} 份 PDF。')
