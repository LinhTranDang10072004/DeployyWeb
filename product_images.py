"""
Ảnh sản phẩm thật — tải từ Wikimedia Commons vào static/products/.
Chạy: python scripts/download_product_images.py
"""
import os
from urllib.parse import quote

# (tên gốc seed, file jpg local, tên file trên Wikimedia Commons)
PRODUCT_IMAGE_ENTRIES = [
    ('Cà chua', 'ca-chua.jpg', 'Tomato_je.jpg'),
    ('Rau muống', 'rau-muong.jpg', 'Ipomoea_aquatica.jpg'),
    ('Xoài cát', 'xoai-cat.jpg', 'Hapus_Mango.jpg'),
    ('Bưởi da xanh', 'buoi-da-xanh.jpg', 'Pomelo_fruit.jpg'),
    ('Khoai lang mật', 'khoai-lang-mat.jpg', 'Sweet_potato.jpg'),
    ('Gạo ST25', 'gao-st25.jpg', 'Rice_grains_(IRRI).jpg'),
    ('Thơm', 'thom.jpg', 'Pineapple_and_cross_section.jpg'),
    ('Giá đỗ', 'gia-do.jpg', 'Mung_bean_sprouts.jpg'),
    ('Ớt sừng', 'ot-sung.jpg', 'Red_Chili.jpg'),
    ('Sả tươi', 'sa-tuoi.jpg', 'Lemongrass.jpg'),
    ('Nấm bào ngư', 'nam-bao-ngu.jpg', 'Mushrooms.jpg'),
    ('Bí đỏ hồ lô', 'bi-do-ho-lo.jpg', 'Pumpkin.jpg'),
    ('Cam sành', 'cam-sanh.jpg', 'Orange-Whole-%26-Split.jpg'),
    ('Chuối già', 'chuoi-gia.jpg', 'Banana-Single.jpg'),
    ('Dưa hấu', 'dua-hau.jpg', 'Watermelon.jpg'),
    ('Dưa lưới', 'dua-luoi.jpg', 'Melon.jpg'),
    ('Cải ngọt', 'cai-ngot.jpg', 'Pak_choi.jpg'),
    ('Cải thìa', 'cai-thia.jpg', 'Pak_choi.jpg'),
    ('Rau dền', 'rau-den.jpg', 'Amaranthus_tricolor0.jpg'),
    ('Xà lách Mỹ', 'xa-lach-my.jpg', 'Iceberg_lettuce.jpg'),
    ('Cà rốt', 'ca-rot.jpg', 'Carrots.jpg'),
    ('Khoai tây', 'khoai-tay.jpg', 'Patates.jpg'),
    ('Củ cải trắng', 'cu-cai-trang.jpg', 'Daikon.JPG'),
    ('Hành tây', 'hanh-tay.jpg', 'Onion_on_White.JPG'),
    ('Tỏi', 'toi.jpg', 'Garlic.jpg'),
    ('Gừng tươi', 'gung-tuoi.jpg', 'Ginger_garden.jpg'),
    ('Tiêu xanh', 'tieu-xanh.jpg', 'Peppercorns.jpg'),
    ('Đậu xanh', 'dau-xanh.jpg', 'Mung_bean_sprouts.jpg'),
    ('Đậu đen', 'dau-den.jpg', 'Black_beans.jpg'),
    ('Yến mạch', 'yen-mach.jpg', 'Rolled_oats.jpg'),
]

DEFAULT_IMAGE_FILE = 'products/default.jpg'
DEFAULT_WIKI_FILE = 'Assorted_vegetables.jpg'

_BASES_SORTED = sorted([e[0] for e in PRODUCT_IMAGE_ENTRIES], key=len, reverse=True)
_NAME_TO_FILE = {e[0]: f'products/{e[1]}' for e in PRODUCT_IMAGE_ENTRIES}
_WIKI_FILES = {e[0]: e[2] for e in PRODUCT_IMAGE_ENTRIES}


def wiki_image_url(wiki_filename: str, width: int = 500) -> str:
    """URL ảnh thật (redirect Wikimedia, dùng khi chưa tải file local)."""
    return (
        'https://commons.wikimedia.org/wiki/Special:FilePath/'
        + quote(wiki_filename, safe='/%')
        + f'?width={width}'
    )


def _static_path(local_filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'static', 'products', local_filename)


def _match_base(product_name: str):
    name = (product_name or '').strip()
    for base in _BASES_SORTED:
        if name.startswith(base):
            return base
    for base in _BASES_SORTED:
        if base.lower() in name.lower():
            return base
    return None


def image_path_for_product_name(product_name: str) -> str:
    """Ưu tiên file JPG trong static/products/, không thì URL Wikimedia."""
    base = _match_base(product_name)
    if not base:
        local = _static_path('default.jpg')
        if os.path.isfile(local) and os.path.getsize(local) > 2000:
            return DEFAULT_IMAGE_FILE
        return wiki_image_url(DEFAULT_WIKI_FILE)

    rel = _NAME_TO_FILE[base]
    local = _static_path(rel.replace('products/', ''))
    if os.path.isfile(local) and os.path.getsize(local) > 2000:
        return rel
    return wiki_image_url(_WIKI_FILES[base])


def image_url_for_product_name(product_name: str) -> str:
    return image_path_for_product_name(product_name)


def all_download_targets():
    yield ('default.jpg', DEFAULT_WIKI_FILE)
    for _base, filename, wiki_name in PRODUCT_IMAGE_ENTRIES:
        yield (filename, wiki_name)
