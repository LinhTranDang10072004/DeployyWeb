#!/usr/bin/env python3
"""Sinh ảnh SVG local cho từng loại nông sản (luôn hiển thị, không cần internet)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from product_images import PRODUCT_IMAGE_ENTRIES, DEFAULT_IMAGE_FILE  # noqa: E402

OUT = os.path.join(ROOT, 'static', 'products')

# Màu nền theo danh mục + emoji
CATEGORY_STYLE = {
    'Rau lá': ('#dcfce7', '#166534', '🥬'),
    'Rau củ': ('#fef3c7', '#92400e', '🥕'),
    'Trái cây': ('#ffedd5', '#c2410c', '🍎'),
    'Ngũ cốc': ('#fef9c3', '#854d0e', '🌾'),
    'Gia vị': ('#fee2e2', '#991b1b', '🌶️'),
    'Nấm': ('#f3e8ff', '#6b21a8', '🍄'),
    'Rau mầm': ('#d1fae5', '#065f46', '🌱'),
    'Khác': ('#f0fdf4', '#15803d', '🌿'),
}

# emoji riêng cho từng sản phẩm (ưu tiên hơn danh mục)
PRODUCT_EMOJI = {
    'Cà chua': '🍅', 'Rau muống': '🥬', 'Xoài cát': '🥭', 'Bưởi da xanh': '🍊',
    'Khoai lang mật': '🍠', 'Gạo ST25': '🍚', 'Thơm': '🍍', 'Giá đỗ': '🌱',
    'Ớt sừng': '🌶️', 'Sả tươi': '🌿', 'Nấm bào ngư': '🍄', 'Bí đỏ hồ lô': '🎃',
    'Cam sành': '🍊', 'Chuối già': '🍌', 'Dưa hấu': '🍉', 'Dưa lưới': '🍈',
    'Cải ngọt': '🥬', 'Cải thìa': '🥬', 'Rau dền': '🥬', 'Xà lách Mỹ': '🥗',
    'Cà rốt': '🥕', 'Khoai tây': '🥔', 'Củ cải trắng': '🥕', 'Hành tây': '🧅',
    'Tỏi': '🧄', 'Gừng tươi': '🫚', 'Tiêu xanh': '🫚', 'Đậu xanh': '🫘',
    'Đậu đen': '🫘', 'Yến mạch': '🌾',
}

# map tên -> category từ seed PRODUCT_TEMPLATES (rút gọn)
NAME_CATEGORY = {
    'Cà chua': 'Rau củ', 'Rau muống': 'Rau lá', 'Xoài cát': 'Trái cây',
    'Bưởi da xanh': 'Trái cây', 'Khoai lang mật': 'Rau củ', 'Gạo ST25': 'Ngũ cốc',
    'Thơm': 'Trái cây', 'Giá đỗ': 'Rau mầm', 'Ớt sừng': 'Gia vị', 'Sả tươi': 'Gia vị',
    'Nấm bào ngư': 'Nấm', 'Bí đỏ hồ lô': 'Rau củ', 'Cam sành': 'Trái cây',
    'Chuối già': 'Trái cây', 'Dưa hấu': 'Trái cây', 'Dưa lưới': 'Trái cây',
    'Cải ngọt': 'Rau lá', 'Cải thìa': 'Rau lá', 'Rau dền': 'Rau lá',
    'Xà lách Mỹ': 'Rau lá', 'Cà rốt': 'Rau củ', 'Khoai tây': 'Rau củ',
    'Củ cải trắng': 'Rau củ', 'Hành tây': 'Gia vị', 'Tỏi': 'Gia vị',
    'Gừng tươi': 'Gia vị', 'Tiêu xanh': 'Gia vị', 'Đậu xanh': 'Ngũ cốc',
    'Đậu đen': 'Ngũ cốc', 'Yến mạch': 'Ngũ cốc',
}


def svg_content(name: str, bg: str, fg: str, emoji: str) -> str:
    safe = name.replace('&', '&amp;').replace('<', '&lt;')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg}"/>
      <stop offset="100%" style="stop-color:#ffffff"/>
    </linearGradient>
  </defs>
  <rect width="600" height="600" fill="url(#g)"/>
  <text x="300" y="240" text-anchor="middle" font-size="120">{emoji}</text>
  <text x="300" y="340" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif"
        font-size="36" font-weight="700" fill="{fg}">{safe}</text>
  <text x="300" y="390" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif"
        font-size="22" fill="{fg}" opacity="0.75">Nông Sản Xanh</text>
</svg>
'''


def write_svg(path: str, name: str, cat: str):
    bg, fg, cat_emoji = CATEGORY_STYLE.get(cat, CATEGORY_STYLE['Khác'])
    emoji = PRODUCT_EMOJI.get(name, cat_emoji)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg_content(name, bg, fg, emoji))


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, filename in PRODUCT_IMAGE_ENTRIES:
        svg_name = filename if filename.endswith('.svg') else os.path.splitext(filename)[0] + '.svg'
        cat = NAME_CATEGORY.get(name, 'Khác')
        write_svg(os.path.join(OUT, svg_name), name, cat)
        print(f'  [OK] {svg_name}')
    write_svg(os.path.join(OUT, 'default.svg'), 'Nông sản', 'Khác')
    print(f'  [OK] default.svg')
    print(f'\nDone -> {OUT}')


if __name__ == '__main__':
    main()
