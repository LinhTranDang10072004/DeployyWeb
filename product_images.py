"""
Ảnh sản phẩm — file SVG trong static/products/ (luôn hiển thị trên localhost & Render).
Chạy: python scripts/generate_product_images.py
"""
import os

# (tên gốc trong PRODUCT_TEMPLATES, file svg trong static/products/)
PRODUCT_IMAGE_ENTRIES = [
    ('Cà chua', 'ca-chua.svg'),
    ('Rau muống', 'rau-muong.svg'),
    ('Xoài cát', 'xoai-cat.svg'),
    ('Bưởi da xanh', 'buoi-da-xanh.svg'),
    ('Khoai lang mật', 'khoai-lang-mat.svg'),
    ('Gạo ST25', 'gao-st25.svg'),
    ('Thơm', 'thom.svg'),
    ('Giá đỗ', 'gia-do.svg'),
    ('Ớt sừng', 'ot-sung.svg'),
    ('Sả tươi', 'sa-tuoi.svg'),
    ('Nấm bào ngư', 'nam-bao-ngu.svg'),
    ('Bí đỏ hồ lô', 'bi-do-ho-lo.svg'),
    ('Cam sành', 'cam-sanh.svg'),
    ('Chuối già', 'chuoi-gia.svg'),
    ('Dưa hấu', 'dua-hau.svg'),
    ('Dưa lưới', 'dua-luoi.svg'),
    ('Cải ngọt', 'cai-ngot.svg'),
    ('Cải thìa', 'cai-thia.svg'),
    ('Rau dền', 'rau-den.svg'),
    ('Xà lách Mỹ', 'xa-lach-my.svg'),
    ('Cà rốt', 'ca-rot.svg'),
    ('Khoai tây', 'khoai-tay.svg'),
    ('Củ cải trắng', 'cu-cai-trang.svg'),
    ('Hành tây', 'hanh-tay.svg'),
    ('Tỏi', 'toi.svg'),
    ('Gừng tươi', 'gung-tuoi.svg'),
    ('Tiêu xanh', 'tieu-xanh.svg'),
    ('Đậu xanh', 'dau-xanh.svg'),
    ('Đậu đen', 'dau-den.svg'),
    ('Yến mạch', 'yen-mach.svg'),
]

DEFAULT_IMAGE_FILE = 'products/default.svg'

_BASES_SORTED = sorted([e[0] for e in PRODUCT_IMAGE_ENTRIES], key=len, reverse=True)
_NAME_TO_FILE = {e[0]: f'products/{e[1]}' for e in PRODUCT_IMAGE_ENTRIES}


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
    """Đường dẫn static, vd products/ca-chua.svg"""
    base = _match_base(product_name)
    if not base:
        return DEFAULT_IMAGE_FILE
    return _NAME_TO_FILE[base]


def image_url_for_product_name(product_name: str) -> str:
    return image_path_for_product_name(product_name)
