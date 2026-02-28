# DTMF Benzeri Metin Kodlama/Kod Çözme Sistemi

**COE216 Signals and Systems - Homework 2**

Bu proje, DTMF (Dual-Tone Multi-Frequency) protokolüne benzer bir yöntem kullanarak Türkçe metinleri frekans tabanlı ses sinyallerine dönüştürür ve bu sinyalleri tekrar metne çevirir.

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Proje Yapısı](#proje-yapısı)
- [Teknik Detaylar](#teknik-detaylar)
- [Örnekler](#örnekler)
- [Katkıda Bulunanlar](#katkıda-bulunanlar)

## ✨ Özellikler

- ✅ Türkçe alfabenin 29 harfi + boşluk karakteri desteği (toplam 30 karakter)
- ✅ DTMF benzeri frekans çifti (düşük/yüksek frekans) sistemi
- ✅ Sinyal sentezi (Encoding): Metin → WAV ses dosyası
- ✅ Sinyal analizi (Decoding): WAV ses dosyası → Metin
- ✅ Goertzel algoritması ile hızlı ve verimli frekans tespiti
- ✅ Hann/Hamming pencereleme ile spektral sızıntı kontrolü
- ✅ Debouncing mekanizması ile karakter tekrarı önleme
- ✅ Kullanıcı dostu interaktif arayüz
- ✅ Ses dosyası çalma özelliği
- ✅ Tam döngü test modülü

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Kurulum Adımları

1. Repoyu klonlayın veya indirin:
```bash
git clone <repository-url>
cd EncodingDecodingText
```

2. Gerekli Python kütüphanelerini yükleyin:
```bash
pip install -r requirements.txt
```

Kurulacak kütüphaneler:
- `numpy` - Sayısal hesaplamalar
- `scipy` - Sinyal işleme
- `sounddevice` - Ses I/O işlemleri
- `soundfile` - WAV dosya okuma/yazma
- `matplotlib` - Grafik çizimi (opsiyonel)

## 💻 Kullanım

### Ana Uygulama

Interaktif menü ile uygulamayı başlatın:

```bash
python main.py
```

### Menü Seçenekleri

1. **Metin → Ses Dosyası (Encoding)**: Girilen metni WAV dosyasına dönüştürür
2. **Ses Dosyası → Metin (Decoding)**: WAV dosyasını analiz ederek metni çıkarır
3. **Ses Dosyasını Çal**: Oluşturulan ses dosyalarını dinler
4. **Frekans Tablosunu Görüntüle**: Karakter-frekans eşleştirme tablosunu gösterir
5. **Test - Tam Döngü**: Encoding ve decoding işlemlerini test eder
6. **Çıkış**: Uygulamadan çıkar

### Programatik Kullanım

#### Encoding (Metin → Ses)

```python
from signal_encoder import SignalEncoder

encoder = SignalEncoder(
    sample_rate=44100,
    tone_duration_ms=40,
    silence_duration_ms=10
)

text = "MERHABA DÜNYA"
encoder.encode_and_save(text, "output/message.wav")
```

#### Decoding (Ses → Metin)

```python
from signal_decoder import SignalDecoder

decoder = SignalDecoder(
    sample_rate=44100,
    window_duration_ms=40,
    hop_duration_ms=25,
    power_threshold=0.1
)

decoded_text = decoder.decode_file("output/message.wav")
print(f"Çözümlenen: {decoded_text}")
```

## 📁 Proje Yapısı

```
EncodingDecodingText/
├── main.py                 # Ana uygulama ve kullanıcı arayüzü
├── frequency_mapper.py     # Karakter-frekans eşleştirme modülü
├── signal_encoder.py       # Sinyal sentezi (encoding) modülü
├── signal_decoder.py       # Sinyal analizi (decoding) modülü
├── requirements.txt        # Python bağımlılıkları
├── .gitignore             # Git ignore kuralları
├── README.md              # Proje dokümantasyonu
└── output/                # Oluşturulan ses dosyaları (otomatik)
```

## 🔬 Teknik Detaylar

### Frekans Atama Sistemi

Sistem, DTMF protokolüne benzer şekilde her karakter için iki frekans kullanır:

- **Düşük Frekanslar**: 697, 770, 852, 941, 1020, 1100 Hz (6 frekans)
- **Yüksek Frekanslar**: 1209, 1336, 1477, 1633, 1800 Hz (5 frekans)
- **Toplam Kombinasyon**: 6 × 5 = 30 benzersiz karakter

Örnek eşleştirmeler:
- **A** → (697 Hz, 1209 Hz)
- **M** → (941 Hz, 1209 Hz)
- **Boşluk** → (1100 Hz, 1800 Hz)

### Sinyal Sentezi (Encoding)

Her karakter için sinyal şu formülle üretilir:

```
s(t) = sin(2πf₁t) + sin(2πf₂t)
```

Parametreler:
- **Örnekleme Oranı**: 44100 Hz (CD kalitesi)
- **Ton Süresi**: 40 ms (her karakter için)
- **Sessizlik Süresi**: 10 ms (karakterler arası)
- **Pencereleme**: Hann penceresi (spektral sızıntı önleme)
- **Normalizasyon**: 0.8 maksimum genlik

### Sinyal Analizi (Decoding)

#### Goertzel Algoritması

FFT'ye göre çok daha verimli, çünkü sadece önceden tanımlı frekansları kontrol eder:

1. Her frekans için ayrı Goertzel filtresi oluşturulur
2. Sinyal, zaman pencereleri halinde analiz edilir
3. Her pencerede en güçlü iki frekans tespit edilir
4. Frekans çifti, karakter tablosunda aranır

Parametreler:
- **Pencere Süresi**: 40 ms
- **Kaydırma Süresi**: 25 ms (pencere overlap)
- **Pencereleme**: Hamming penceresi
- **Güç Eşiği**: 0.1 (gürültü filtreleme)
- **Debouncing**: 2 pencere (karakter tekrarı önleme)

### Performans İyileştirmeleri

1. **Spektral Sızıntı Kontrolü**:
   - Hann/Hamming pencereleme
   - Yumuşak geçişler

2. **Gürültü Filtreleme**:
   - Güç eşiği kullanımı
   - Düşük sinyaller göz ardı edilir

3. **Debouncing**:
   - Aynı karakterin tekrar algılanması önlenir
   - Daha stabil sonuçlar

4. **Verimli Frekans Analizi**:
   - FFT yerine Goertzel algoritması
   - 10-15x daha hızlı

## 📊 Örnekler

### Örnek 1: Basit Metin

```python
text = "MERHABA"
encoder.encode_and_save(text, "hello.wav")
decoded = decoder.decode_file("hello.wav")
print(decoded)  # "MERHABA"
```

### Örnek 2: Boşluklu Metin

```python
text = "TÜRKÇE ALFABE"
encoder.encode_and_save(text, "turkish.wav")
decoded = decoder.decode_file("turkish.wav")
print(decoded)  # "TÜRKÇE ALFABE"
```

### Örnek 3: Tam Alfabe Testi

```python
text = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
encoder.encode_and_save(text, "alphabet.wav")
decoded = decoder.decode_file("alphabet.wav")
# Doğruluk oranı kontrolü
accuracy = (sum(1 for a,b in zip(text, decoded) if a==b) / len(text)) * 100
print(f"Doğruluk: %{accuracy:.1f}")
```

## 🎯 Değerlendirme Kriterleri

Proje şu kriterlere göre değerlendirilecektir:

1. **Sinyal Sentezi ve Kayıt Doğruluğu** (30%)
   - Doğru frekans üretimi
   - WAV dosyası kalitesi
   - Pencereleme ve normalizasyon

2. **Sinyal Analizi ve Karakter Tespit Başarısı** (30%)
   - Goertzel algoritması implementasyonu
   - Frekans tespit doğruluğu
   - Debouncing ve hata toleransı

3. **Arayüz ve Kullanılabilirlik** (20%)
   - Menü sistemi
   - Hata yönetimi
   - Kullanıcı deneyimi

4. **Teknik Rapor Formatı** (20%)
   - Dokümantasyon kalitesi
   - Kod organizasyonu
   - Git kullanımı

## 🤝 Katkıda Bulunanlar

Bu proje COE216 Sinyal ve Sistemler dersi kapsamında geliştirilmiştir.

### Grup Üyeleri
- [Berke] - [Kod Yazımı ve Test]
- [Muhammed] - [Raporlama]
- [Mert] - [Raporlama]

### Kullanılan Kaynaklar
- Python Official Documentation
- NumPy Documentation
- SciPy Signal Processing Guide
- DTMF Protocol Specification
- Goertzel Algorithm Papers

### Kullanılan AI Araçları
- [Cursor] - [Kod Yazımı]

## 📄 Lisans

Bu proje eğitim amaçlıdır ve İSTUN COE216 dersi için hazırlanmıştır.


---

**Son Güncelleme**: Şubat 2026
**Versiyon**: 1.0.0
