#!/usr/bin/env python3
"""Cập nhật ảnh sản phẩm trong DB (không xóa dữ liệu)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app import app  # noqa: E402
from seed import assign_product_images  # noqa: E402

if __name__ == '__main__':
    with app.app_context():
        assign_product_images()
