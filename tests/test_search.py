import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1] / 'skills/yuecai-knowledge-search'

class SearchTests(unittest.TestCase):
    def test_installation_can_move_to_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / 'installed-skill'
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns('__pycache__'))
            spec = importlib.util.spec_from_file_location('installed_search', installed / 'scripts/search.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            all_rows = module.search('')
            self.assertGreater(all_rows['matched'], 0)
            self.assertEqual(all_rows['total'], all_rows['matched'])
            for row in all_rows['results']:
                self.assertTrue(row['summary'])
                for pdf in row['pdfs']:
                    self.assertTrue(pdf['exists'])
                    self.assertTrue(Path(pdf['path']).is_relative_to(installed.resolve()))
            self.assertEqual(module.search('canyin-17014')['matched'], 1)
            self.assertEqual(module.search('口头约定')['matched'], 1)
            self.assertEqual(module.search('合并前数量 区间')['matched'], 1)
            self.assertEqual(module.search('不存在的需求ZZZ')['matched'], 0)

    def test_page_and_skill_share_the_same_records(self):
        import re
        root = SKILL / 'assets/library'
        catalog = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
        page = (root / '打开目录.html').read_text(encoding='utf-8')
        embedded = json.loads(re.search(r'<script id="data"[^>]*>(.*?)</script>', page, re.S).group(1))
        self.assertEqual(catalog, embedded)
        referenced = {p['path'] for row in catalog for p in row['pdfs']}
        actual = {'PDF/' + p.name for p in (root / 'PDF').glob('*.pdf')}
        self.assertEqual(referenced, actual)

if __name__ == '__main__':
    unittest.main()
