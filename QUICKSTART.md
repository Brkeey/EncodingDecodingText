# Hızlı Başlangıç Kılavuzu

Bu kılavuz projeyi hızlıca çalıştırmanız için adım adım talimatlar içerir.

## 📦 Kurulum (5 dakika)

### 1. Projeyi İndirin

```bash
git clone <repository-url>
cd EncodingDecodingText
```

### 2. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

veya tek tek:

```bash
pip install numpy scipy sounddevice soundfile matplotlib
```

## 🚀 İlk Çalıştırma

### Basit Test

1. Frekans tablosunu görüntüleyin:
```bash
python frequency_mapper.py
```

2. Test mesajı oluşturun ve çözün:
```bash
python test_system.py
```

### Ana Uygulamayı Başlatın

```bash
python main.py
```

## 📝 Örnek Kullanım Senaryoları

### Senaryo 1: Metin Kodlama

1. `python main.py` çalıştırın
2. Menüden `1` seçin (Metin → Ses)
3. Metninizi girin: `MERHABA DÜNYA`
4. Dosya adı girin veya Enter'a basın
5. Ses dosyası `output/` klasöründe oluşturulur

### Senaryo 2: Ses Dosyası Çözümleme

1. `python main.py` çalıştırın
2. Menüden `2` seçin (Ses → Metin)
3. Dosya adını girin
4. Çözümlenen metin ekranda görüntülenir

### Senaryo 3: Tam Test

1. `python main.py` çalıştırın
2. Menüden `5` seçin (Tam Döngü Test)
3. Test metnini girin veya Enter'a basın
4. Encoding ve decoding otomatik yapılır
5. Sonuçlar karşılaştırılır

## 🎨 Görselleştirme

Sinyal ve spektrum grafiklerini oluşturmak için:

```bash
python visualizer.py
```

Bu komut şunları oluşturur:
- Frekans tablosu görseli
- Zaman domeninde sinyal grafiği
- Frekans spektrumu
- Spektrogram

Grafikler `output/` klasörüne PNG formatında kaydedilir.

## 🧪 Testler

### Kapsamlı Test Paketi

```bash
python test_system.py
```

Test paketi şunları içerir:
- Tek karakter testleri (30 karakter)
- Kelime testleri
- Tam alfabe testi
- Performans metrikleri

### Hızlı Test (Tek Modül)

```python
from signal_encoder import SignalEncoder

encoder = SignalEncoder()
encoder.encode_and_save("TEST", "output/test.wav")
```

## 📊 Sonuç Dosyaları

Uygulamayı çalıştırdıktan sonra:

```
EncodingDecodingText/
└── output/
    ├── encoded_message.wav          # Kodlanmış ses dosyaları
    ├── decoded_text.txt             # Çözümlenen metinler
    ├── frequency_table_visual.png   # Frekans tablosu görseli
    ├── *_time_domain.png            # Zaman domeninde grafikler
    ├── *_frequency_domain.png       # Frekans spektrumları
    └── *_spectrogram.png            # Spektrogramlar
```

## 🔧 Parametre Ayarlama

Varsayılan parametreleri değiştirmek için kod içinde:

```python
encoder = SignalEncoder(
    sample_rate=44100,        # Örnekleme oranı
    tone_duration_ms=40,      # Ton süresi (30-50 ms arası)
    silence_duration_ms=10    # Sessizlik süresi
)

decoder = SignalDecoder(
    sample_rate=44100,
    window_duration_ms=40,    # Analiz penceresi
    hop_duration_ms=25,       # Pencere kaydırma
    power_threshold=0.1       # Gürültü eşiği
)
```

## ❓ Sık Karşılaşılan Sorunlar

### Problem: Ses çıkmıyor

**Çözüm:** Sistem ses ayarlarınızı kontrol edin. `sounddevice` kütüphanesi kurulu mu?

```bash
pip install --upgrade sounddevice
```

### Problem: WAV dosyası oluşturuluyor ama analiz çalışmıyor

**Çözüm:** 
1. Dosya yolunu kontrol edin
2. `power_threshold` değerini düşürün (örn. 0.05)
3. Sinyalde yeterli güç olduğundan emin olun

### Problem: Karakterler yanlış algılanıyor

**Çözüm:**
1. `tone_duration_ms` ve `window_duration_ms` değerlerini eşitleyin
2. Gürültülü ortamda mı çalıştırıyorsunuz? `power_threshold` değerini artırın
3. Debouncing parametresini ayarlayın

### Problem: Kütüphane kurulum hatası

**Çözüm:**
```bash
# Virtual environment oluşturun
python -m venv venv

# Aktifleştirin
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Tekrar yükleyin
pip install -r requirements.txt
```

## 📚 Daha Fazla Bilgi

- **Detaylı Dokümantasyon:** `README.md`
- **Rapor Şablonu:** `REPORT_TEMPLATE.md`
- **Kod Dokümantasyonu:** Her Python dosyasında detaylı docstring'ler

## 💡 İpuçları

1. **İlk kez mi kullanıyorsunuz?** Menüdeki 5. seçenekle (Tam Döngü Test) başlayın.

2. **Ödev raporu mu hazırlıyorsunuz?** 
   - `test_system.py` ile test sonuçları alın
   - `visualizer.py` ile grafikler oluşturun
   - `REPORT_TEMPLATE.md` dosyasını kullanın

3. **Performansı artırmak için:**
   - `tone_duration_ms` değerini azaltın (minimum 30 ms)
   - Goertzel yerine FFT denemek için `signal_decoder.py` dosyasını modifiye edin

4. **Hata ayıklama için:**
   - Her modülü tek başına test edin
   - Print statement'larını aktif edin
   - Grafikleri inceleyin

## 🎯 Sonraki Adımlar

1. ✅ Kurulumu tamamlayın
2. ✅ Test paketini çalıştırın
3. ✅ Kendi metinlerinizi deneyin
4. ✅ Grafikleri oluşturun
5. ✅ Parametreleri optimize edin
6. ✅ Raporu doldurun

---

**Başarılar!** 🚀

Sorularınız için: [İletişim bilgisi]
