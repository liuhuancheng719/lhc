#!/usr/bin/env python3
"""Search the current Cantonese requirements catalog without a web server."""
import argparse
import json
from pathlib import Path

LIBRARY = Path(__file__).resolve().parents[1] / 'assets/library'


def search(query):
    records = json.loads((LIBRARY / 'catalog.json').read_text(encoding='utf-8'))
    words = query.casefold().split()
    results = []
    for record in records:
        text = ' '.join(record.get(k, '') for k in ('title', 'summary', 'code', 'category')).casefold()
        if not all(word in text for word in words):
            continue
        item = {key: record.get(key, '') for key in ('title', 'code', 'category', 'summary')}
        item['pdfs'] = []
        for pdf in record.get('pdfs', []):
            path = (LIBRARY / pdf['path']).resolve()
            path.relative_to(LIBRARY.resolve())
            item['pdfs'].append({'title': pdf['title'], 'path': str(path), 'exists': path.is_file()})
        results.append(item)
    return {'query': query, 'total': len(records), 'matched': len(results), 'results': results}


def main():
    parser = argparse.ArgumentParser(description='检索粤菜功能知识库，返回简介与本机 PDF 路径。')
    parser.add_argument('query', help='检索词；多个词用空格分隔并整体加引号；空字符串列出全部。')
    args = parser.parse_args()
    try:
        result = search(args.query)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'检索失败：{error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
