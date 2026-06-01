#!/usr/bin/env python3
"""Tải ảnh sản phẩm từ Unsplash vào static/products/."""
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from product_images import all_download_targets  # noqa: E402

OUT_DIR = os.path.join(ROOT, 'static', 'products')


def download(url: str, dest: str) -> bool:
    import time
    time.sleep(2)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NongSanXanh/1.0 (edu project)'})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(dest, 'wb') as f:
            f.write(data)
        return True
    except Exception as exc:
        print(f'  [FAIL] {dest}: {exc}')
        return False


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    ok, fail = 0, 0
    for filename, url in all_download_targets():
        dest = os.path.join(OUT_DIR, filename)
        if os.path.isfile(dest) and os.path.getsize(dest) > 5000:
            print(f'  [SKIP] {filename} (da co)')
            ok += 1
            continue
        print(f'  ... {filename}')
        if download(url, dest):
            print(f'  [OK] {filename} ({os.path.getsize(dest) // 1024} KB)')
            ok += 1
        else:
            fail += 1
    print(f'\nDone: {ok} ok, {fail} fail -> {OUT_DIR}')


if __name__ == '__main__':
    main()
