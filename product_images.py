"""
Ảnh sản phẩm — URL theo từ khóa (loremflickr.com, ảnh thật trên Flickr).
Seed lưu URL vào Product.image; app.build_image_url() nhận URL https.
Tùy chọn tải về: python scripts/download_product_images.py
"""
import os

# (tên gốc, file local, URL ảnh)
def _lf(tags: str, lock: int) -> str:
    return f'https://loremflickr.com/600/600/{tags}/all?lock={lock}'


PRODUCT_IMAGE_ENTRIES = [
    ('Cà chua', 'ca-chua.jpg', _lf('tomato,vegetable', 101)),
    ('Rau muống', 'rau-muong.jpg', _lf('spinach,vegetable', 102)),
    ('Xoài cát', 'xoai-cat.jpg', _lf('mango,fruit', 103)),
    ('Bưởi da xanh', 'buoi-da-xanh.jpg', _lf('pomelo,citrus', 104)),
    ('Khoai lang mật', 'khoai-lang-mat.jpg', _lf('sweetpotato', 105)),
    ('Gạo ST25', 'gao-st25.jpg', _lf('rice,grain', 106)),
    ('Thơm', 'thom.jpg', _lf('pineapple,fruit', 107)),
    ('Giá đỗ', 'gia-do.jpg', _lf('beansprout', 108)),
    ('Ớt sừng', 'ot-sung.jpg', _lf('chili,pepper', 109)),
    ('Sả tươi', 'sa-tuoi.jpg', _lf('lemongrass,herb', 110)),
    ('Nấm bào ngư', 'nam-bao-ngu.jpg', _lf('mushroom,oyster', 111)),
    ('Bí đỏ hồ lô', 'bi-do-ho-lo.jpg', _lf('pumpkin,squash', 112)),
    ('Cam sành', 'cam-sanh.jpg', _lf('orange,citrus', 113)),
    ('Chuối già', 'chuoi-gia.jpg', _lf('banana,fruit', 114)),
    ('Dưa hấu', 'dua-hau.jpg', _lf('watermelon,fruit', 115)),
    ('Dưa lưới', 'dua-luoi.jpg', _lf('melon,cantaloupe', 116)),
    ('Cải ngọt', 'cai-ngot.jpg', _lf('bokchoy,vegetable', 117)),
    ('Cải thìa', 'cai-thia.jpg', _lf('bokchoy,greens', 118)),
    ('Rau dền', 'rau-den.jpg', _lf('amaranth,greens', 119)),
    ('Xà lách Mỹ', 'xa-lach-my.jpg', _lf('lettuce,vegetable', 120)),
    ('Cà rốt', 'ca-rot.jpg', _lf('carrot,vegetable', 121)),
    ('Khoai tây', 'khoai-tay.jpg', _lf('potato,vegetable', 122)),
    ('Củ cải trắng', 'cu-cai-trang.jpg', _lf('radish,daikon', 123)),
    ('Hành tây', 'hanh-tay.jpg', _lf('onion,vegetable', 124)),
    ('Tỏi', 'toi.jpg', _lf('garlic,vegetable', 125)),
    ('Gừng tươi', 'gung-tuoi.jpg', _lf('ginger,root', 126)),
    ('Tiêu xanh', 'tieu-xanh.jpg', _lf('peppercorn,spice', 127)),
    ('Đậu xanh', 'dau-xanh.jpg', _lf('mungbean,legume', 128)),
    ('Đậu đen', 'dau-den.jpg', _lf('blackbean,legume', 129)),
    ('Yến mạch', 'yen-mach.jpg', _lf('oats,cereal', 130)),
]

DEFAULT_IMAGE_URL = _lf('vegetables,farmersmarket', 199)

_BASES_SORTED = sorted([e[0] for e in PRODUCT_IMAGE_ENTRIES], key=len, reverse=True)
_NAME_TO_URL = {e[0]: e[2] for e in PRODUCT_IMAGE_ENTRIES}
_NAME_TO_FILE = {e[0]: e[1] for e in PRODUCT_IMAGE_ENTRIES}


def _match_base(product_name: str):
    name = (product_name or '').strip()
    for base in _BASES_SORTED:
        if name.startswith(base):
            return base
    for base in _BASES_SORTED:
        if base.lower() in name.lower():
            return base
    return None


def image_url_for_product_name(product_name: str) -> str:
    base = _match_base(product_name)
    return _NAME_TO_URL[base] if base else DEFAULT_IMAGE_URL


def image_path_for_product_name(product_name: str) -> str:
    """Giá trị lưu Product.image — file local hoặc URL."""
    base = _match_base(product_name)
    if not base:
        return DEFAULT_IMAGE_URL
    filename = _NAME_TO_FILE[base]
    local = os.path.join(os.path.dirname(__file__), 'static', 'products', filename)
    if os.path.isfile(local) and os.path.getsize(local) > 3000:
        return f'products/{filename}'
    return _NAME_TO_URL[base]


def all_download_targets():
    yield ('default.jpg', DEFAULT_IMAGE_URL)
    for _base, filename, url in PRODUCT_IMAGE_ENTRIES:
        yield (filename, url)
