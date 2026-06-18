#!/bin/bash
echo "📦 Gerekli paketler kuruluyor..."
pip install -r requirements.txt

echo ""
echo "🚀 Uygulama başlatılıyor..."
echo "👉 Tarayıcıda aç: http://localhost:5000"
echo ""
python app.py
