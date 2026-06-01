#!/usr/bin/env bash
# Render build: cài package + tạo nongsan.db (bắt buộc có sản phẩm)
set -e
pip install -r requirements.txt

if [ -f nongsan_demo.db ]; then
  echo "[BUILD] Copy nongsan_demo.db -> nongsan.db"
  cp nongsan_demo.db nongsan.db
else
  echo "[BUILD] Chay seed.py --reset --fixed"
  python seed.py --reset --fixed
fi

python -c "from app import app; from models import Product; 
with app.app_context():
    n = Product.query.count()
    print(f'[BUILD] San pham trong DB: {n}')
    assert n >= 300, 'Seed that bai — chua du 300 san pham'"
