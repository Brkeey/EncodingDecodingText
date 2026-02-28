#!/bin/bash
# Proje Demo ve Test Scripti

echo "=========================================="
echo "DTMF Metin Kodlama/Kod Çözme Sistemi"
echo "COE216 - Homework 2"
echo "=========================================="
echo ""

# Renkli çıktı için
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Python kontrolü
echo -e "${BLUE}[1/5] Python versiyonu kontrol ediliyor...${NC}"
python3 --version
echo ""

# Gerekli kütüphaneler
echo -e "${BLUE}[2/5] Gerekli kütüphaneler kontrol ediliyor...${NC}"
echo "Kurulması gerekenler: numpy, scipy, sounddevice, soundfile, matplotlib"
echo ""
echo "Kurulum için çalıştırın:"
echo "  pip install -r requirements.txt"
echo ""

# Frekans tablosu gösterimi
echo -e "${BLUE}[3/5] Frekans tablosu görüntüleniyor...${NC}"
python3 frequency_mapper.py
echo ""

# Kısa test
echo -e "${BLUE}[4/5] Basit encoding test yapılıyor...${NC}"
python3 -c "
from signal_encoder import SignalEncoder
import os

if not os.path.exists('output'):
    os.makedirs('output')

encoder = SignalEncoder()
text = 'MERHABA'
print(f'Test metni: {text}')
signal = encoder.encode_and_save(text, 'output/demo_test.wav')
print(f'✓ WAV dosyası oluşturuldu: output/demo_test.wav')
"
echo ""

# Ana menü
echo -e "${BLUE}[5/5] Kullanım talimatları${NC}"
echo "=========================================="
echo ""
echo -e "${GREEN}✓ Proje kurulumu tamamlandı!${NC}"
echo ""
echo "Şimdi ne yapabilirsiniz?"
echo ""
echo "1. Ana uygulamayı başlatın:"
echo "   ${YELLOW}python main.py${NC}"
echo ""
echo "2. Tam test paketini çalıştırın:"
echo "   ${YELLOW}python test_system.py${NC}"
echo ""
echo "3. Grafikler oluşturun:"
echo "   ${YELLOW}python visualizer.py${NC}"
echo ""
echo "4. Dokümantasyonu okuyun:"
echo "   - README.md (detaylı bilgi)"
echo "   - QUICKSTART.md (hızlı başlangıç)"
echo "   - REPORT_TEMPLATE.md (rapor şablonu)"
echo ""
echo "=========================================="
echo ""
