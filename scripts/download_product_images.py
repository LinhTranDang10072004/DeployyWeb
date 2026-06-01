#!/usr/bin/env python3
"""Tải ảnh thật từ Wikimedia Commons vào static/products/."""
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from product_images import all_download_targets, wiki_image_url  # noqa: E402

OUT_DIR = os.path.join(ROOT, 'static', 'products')


def download_wiki(wiki_filename: str, dest: str) -> bool:
    url = wiki_image_url(wiki_filename, width=500)
    time.sleep(2.5)
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'NongSanXanh/1.0 (student project; contact: local)'},
        )
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = resp.read()
        if len(data) < 2000:
            print(f'  [FAIL] {dest}: file too small ({len(data)} bytes)')
            return False
        with open(dest, 'wb') as f:
            f.write(data)
        return True
    except Exception as exc:
        print(f'  [FAIL] {dest}: {exc}')
        return False


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    ok, fail = 0, 0
    for filename, wiki_name in all_download_targets():
        dest = os.path.join(OUT_DIR, filename)
        if os.path.isfile(dest) and os.path.getsize(dest) > 5000:
            print(f'  [SKIP] {filename}')
            ok += 1
            continue
        print(f'  ... {filename} <- {wiki_name}')
        if download_wiki(wiki_name, dest):
            print(f'  [OK] {filename} ({os.path.getsize(dest) // 1024} KB)')
            ok += 1
        else:
            fail += 1
    print(f'\nDone: {ok} ok, {fail} fail')
    print('Chay: python scripts/fix_product_images.py')


if __name__ == '__main__':
    main()
