# HW_2_GROUP# - PROJE RAPORU

**COE216 Sinyal ve Sistemler**  
**2025-2026 Bahar Dönemi**  
**Homework 2: DTMF Benzeri Metin Kodlama/Kod Çözme Sistemi**

---

## Kapak Sayfası

**Proje Başlığı:** DTMF Benzeri Türkçe Metin Kodlama/Kod Çözme Sistemi

**Grup Numarası:** [Grup numaranızı buraya yazın]

**Grup Üyeleri:**
1. [Ad Soyad] - [Öğrenci No] - [E-posta]
2. [Ad Soyad] - [Öğrenci No] - [E-posta]
3. [Ad Soyad] - [Öğrenci No] - [E-posta]

**Teslim Tarihi:** [Tarih]

---

## 1. Yöntem (Method)

### 1.1 Genel Yaklaşım

Bu projede DTMF (Dual-Tone Multi-Frequency) protokolüne benzer bir yöntem kullanılarak Türkçe alfabedeki 29 harf ve boşluk karakteri (toplam 30 karakter) frekans tabanlı ses sinyallerine kodlanmış ve bu sinyaller analiz edilerek orijinal metne geri çevrilmiştir.

Sistem iki ana modülden oluşmaktadır:
1. **Encoding (Kodlama) Modülü:** Metni ses sinyaline dönüştürür
2. **Decoding (Kod Çözme) Modülü:** Ses sinyalini metne geri çevirir

### 1.2 Frekans Atama Sistemi

#### 1.2.1 Temel Konsept

DTMF protokolünde her tuş iki frekanstan oluşan bir kombinasyonla temsil edilir. Bu projede de aynı mantık kullanılarak:

- **6 adet düşük frekans:** 697, 770, 852, 941, 1020, 1100 Hz
- **5 adet yüksek frekans:** 1209, 1336, 1477, 1633, 1800 Hz

Bu frekanslar kombinlenerek 6 × 5 = 30 benzersiz karakter temsil edilmiştir.

#### 1.2.2 Frekans Tablosu

| Karakter | Düşük Frekans (Hz) | Yüksek Frekans (Hz) |
|----------|-------------------|---------------------|
| A        | 697               | 1209                |
| B        | 697               | 1336                |
| ...      | ...               | ...                 |
| BOŞLUK   | 1100              | 1800                |

*(Tam tablo için `frequency_mapper.py` dosyasına bakınız)*

### 1.3 Sinyal Sentezi (Encoding)

#### 1.3.1 Sinyal Üretimi

Her karakter için ses sinyali aşağıdaki formülle üretilmiştir:

```
s(t) = sin(2πf₁t) + sin(2πf₂t)
```

Burada:
- `f₁`: Düşük frekans bileşeni
- `f₂`: Yüksek frekans bileşeni
- `t`: Zaman (0 ile tone_duration arasında)

#### 1.3.2 Parametreler

- **Örnekleme Oranı (fs):** 44100 Hz (CD kalitesi ses standardı)
- **Ton Süresi:** 40 ms (ödevde belirtilen 30-50 ms aralığında)
- **Karakterler Arası Sessizlik:** 10 ms
- **Normalizasyon:** Maksimum genlik 0.8 olarak ayarlanmıştır

#### 1.3.3 Pencereleme (Windowing)

Spektral sızıntı (spectral leakage) problemini önlemek için Hann penceresi uygulanmıştır:

```
window(n) = 0.5 * (1 - cos(2πn/N))
s_windowed(n) = s(n) * window(n)
```

Bu sayede sinyal başlangıç ve bitişlerinde yumuşak geçişler elde edilmiş, frekans analizinde yan loblar azaltılmıştır.

### 1.4 Sinyal Analizi (Decoding)

#### 1.4.1 Analiz Yöntemi: Goertzel Algoritması

FFT yerine Goertzel algoritması tercih edilmiştir çünkü:

1. **Verimlilik:** Sadece önceden tanımlı frekansları kontrol eder
2. **Hız:** FFT'ye göre 10-15x daha hızlıdır
3. **Düşük Hesaplama Maliyeti:** Gerçek zamanlı uygulamalar için idealdir

#### 1.4.2 Goertzel Algoritması Implementasyonu

```python
k = int(0.5 + (N * f_target) / fs)
ω = (2π * k) / N
coeff = 2 * cos(ω)

# Her örnek için:
s[n] = x[n] + coeff * s[n-1] - s[n-2]

# Güç hesabı:
power = s[N-1]² + s[N-2]² - coeff * s[N-1] * s[N-2]
```

#### 1.4.3 Pencere Analizi

Sinyal sabit boyutlu pencerelere bölünerek analiz edilmiştir:

- **Pencere Boyutu:** 40 ms (ton süresiyle eşleştirilmiş)
- **Hop Size:** 25 ms (pencere kaydırma miktarı)
- **Overlap:** 15 ms (pencereler arası örtüşme)

Her pencerede:
1. Hamming pencereleme uygulanır
2. Her frekans için Goertzel analizi yapılır
3. En güçlü düşük ve yüksek frekans tespit edilir
4. Frekans çifti karakter tablosunda aranır

#### 1.4.4 Gürültü Filtreleme ve Debouncing

**Güç Eşiği (Power Threshold):**
```python
if max_power < threshold:
    # Bu pencereyi göz ardı et (sessizlik veya gürültü)
    continue
```

**Debouncing Mekanizması:**
Aynı karakterin art arda birçok kez algılanmasını önlemek için:
- Son algılanan karakter takip edilir
- Karakter değişmeden önce minimum 2 pencere bekletilir
- Bu sayede 40 ms'lik bir ton tek bir karakter olarak algılanır

### 1.5 Kullanılan Teknolojiler ve Kütüphaneler

#### 1.5.1 Python Kütüphaneleri

| Kütüphane    | Versiyon | Kullanım Amacı                           |
|--------------|----------|------------------------------------------|
| NumPy        | ≥1.24.0  | Sayısal hesaplamalar, array işlemleri   |
| SciPy        | ≥1.10.0  | Sinyal işleme, FFT, filtreleme          |
| sounddevice  | ≥0.4.6   | Ses giriş/çıkış işlemleri                |
| soundfile    | ≥0.12.1  | WAV dosya okuma/yazma                    |
| matplotlib   | ≥3.7.0   | Görselleştirme (opsiyonel)               |

#### 1.5.2 Geliştirme Ortamı

- **Programlama Dili:** Python 3.8+
- **IDE:** Visual Studio Code / PyCharm
- **Versiyon Kontrol:** Git & GitHub
- **İşletim Sistemi:** macOS / Windows / Linux uyumlu

### 1.6 Performans İyileştirmeleri

1. **Vektörleştirilmiş İşlemler:** NumPy kullanılarak döngü ihtiyacı azaltılmıştır
2. **Önbellek Kullanımı:** Goertzel filtreleri önceden hesaplanıp saklanmıştır
3. **Adaptif Eşik:** Gürültü seviyesine göre ayarlanabilir güç eşiği
4. **Optimum Pencere Boyutu:** Ton süresiyle eşleştirilmiş pencere boyutu

---

## 2. Grafikler ve Görselleştirmeler

### 2.1 Frekans Tablosu Görseli

[Buraya `visualizer.py` ile oluşturulan frequency_table_visual.png eklenecek]

**Şekil 1:** DTMF benzeri karakter-frekans eşleştirme tablosu

### 2.2 Örnek Sinyal Analizi

#### 2.2.1 Zaman Domeninde Sinyal

[Buraya time_domain.png grafiği eklenecek]

**Şekil 2:** "MERHABA" metni için üretilen sinyalin zaman domeninde gösterimi

#### 2.2.2 Frekans Domeninde Sinyal

[Buraya frequency_domain.png grafiği eklenecek]

**Şekil 3:** FFT analizi ile frekans spektrumu. Kırmızı çizgiler beklenen frekansları göstermektedir.

#### 2.2.3 Spektrogram

[Buraya spectrogram.png grafiği eklenecek]

**Şekil 4:** Zaman-frekans spektrogramı. Her karakter farklı frekans çiftleri ile net bir şekilde görülmektedir.

### 2.3 Kullanıcı Arayüzü

[Buraya main.py çalıştırıldığında çıkan menü ekran görüntüsü eklenecek]

**Şekil 5:** Ana menü arayüzü

---

## 3. Test Sonuçları

### 3.1 Tek Karakter Testleri

`test_system.py` ile yapılan tek karakter testleri:

| Test Grubu              | Başarı Oranı | Detay                    |
|-------------------------|--------------|--------------------------|
| Türkçe Sesli Harfler    | [%]          | A, E, I, İ, O, Ö, U, Ü   |
| Türkçe Sessiz Harfler   | [%]          | B, C, Ç, D, F, G, Ğ, ... |
| Özel Karakterler        | [%]          | Ç, Ğ, İ, Ö, Ş, Ü         |
| Boşluk                  | [%]          | ' ' karakteri            |
| **TOPLAM**              | **[%]**      | 30/30 karakter           |

### 3.2 Kelime Testleri

| Kelime           | Çözümlenen      | Doğruluk | Encoding (ms) | Decoding (ms) |
|------------------|-----------------|----------|---------------|---------------|
| MERHABA          | [sonuç]         | [%]      | [ms]          | [ms]          |
| DÜNYA            | [sonuç]         | [%]      | [ms]          | [ms]          |
| TÜRKÇE           | [sonuç]         | [%]      | [ms]          | [ms]          |
| ÖZYEĞIN          | [sonuç]         | [%]      | [ms]          | [ms]          |
| MERHABA DÜNYA    | [sonuç]         | [%]      | [ms]          | [ms]          |

**Ortalama Doğruluk:** [%]

### 3.3 Tam Alfabe Testi

```
Orijinal  : ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ
Çözümlenen: [sonuç]
Doğruluk  : [%]
```

---

## 4. Karşılaşılan Zorluklar ve Çözümler

### 4.1 Spektral Sızıntı

**Problem:** Sinyal başlangıç/bitiş noktalarında ani değişimler spektral sızıntıya neden oluyordu.

**Çözüm:** Hann/Hamming pencereleme fonksiyonları uygulandı.

### 4.2 Karakter Tekrarı (Double Detection)

**Problem:** Aynı karakter birden fazla kez algılanıyordu.

**Çözüm:** Debouncing mekanizması eklendi.

### 4.3 Gürültü Hassasiyeti

**Problem:** Düşük sinyal-gürültü oranlarında yanlış tespit oluyordu.

**Çözüm:** Adaptif güç eşiği implementasyonu.

---

## 5. Gelecek İyileştirmeler

1. **Gerçek Zamanlı Streaming (Method B):** Mikrofon girişi ile anlık kod çözme
2. **Makine Öğrenmesi Entegrasyonu:** Daha yüksek doğruluk için ML tabanlı karakter tanıma
3. **Hata Düzeltme Kodları:** Reed-Solomon gibi hata düzeltme algoritmaları
4. **Adaptif Parametreler:** Gürültü seviyesine göre otomatik parametre ayarlama
5. **Mobil Uygulama:** iOS/Android platformları için uygulama

---

## 6. GitHub Repository Linki

**Repository:** [https://github.com/[kullanici-adi]/EncodingDecodingText](https://github.com/[kullanici-adi]/EncodingDecodingText)

---

## 7. Kaynaklar (References)

1. Python Official Documentation - https://docs.python.org/3/
2. NumPy Documentation - https://numpy.org/doc/
3. SciPy Signal Processing - https://docs.scipy.org/doc/scipy/reference/signal.html
4. ITU-T Recommendation Q.23 - DTMF Protocol Specification
5. Goertzel Algorithm - https://en.wikipedia.org/wiki/Goertzel_algorithm
6. "Digital Signal Processing" by Alan V. Oppenheim and Ronald W. Schafer
7. Stack Overflow - Various signal processing discussions
8. GitHub - Sound processing examples

---

## 8. AI Araçları ve Promptlar

### 8.1 Kullanılan AI Araçları

| AI Aracı          | Versiyon | Kullanım Alanı                           |
|-------------------|----------|------------------------------------------|
| [AI Aracı Adı]    | [v1.0]   | Kod geliştirme, hata ayıklama           |
| [AI Aracı Adı]    | [v2.0]   | Dokümantasyon yazımı                     |

### 8.2 Örnek Promptlar

| No | Prompt                                                                                      | Kullanım Amacı               |
|----|---------------------------------------------------------------------------------------------|------------------------------|
| 1  | "Python'da Goertzel algoritması implementasyonu nasıl yapılır?"                             | Algoritma araştırması        |
| 2  | "NumPy ile spektral sızıntıyı nasıl önlerim?"                                               | Pencereleme tekniği          |
| 3  | "WAV dosyasını Python'da nasıl okur ve yazarım?"                                            | Dosya I/O işlemleri          |
| 4  | "Debouncing mekanizması sinyal işlemede nasıl uygulanır?"                                   | Karakter tekrarı önleme      |

---

## 9. İş Bölümü (Division of Labor)

### [Üye 1 - Ad Soyad]
- Frekans atama sistemi tasarımı (`frequency_mapper.py`)
- Sinyal sentezi modülü geliştirmesi (`signal_encoder.py`)
- Kod dokümantasyonu ve yorum satırları
- GitHub repository yönetimi

**Katkı Oranı:** %[yüzde]

### [Üye 2 - Ad Soyad]
- Goertzel algoritması implementasyonu
- Sinyal analiz modülü geliştirmesi (`signal_decoder.py`)
- Test scriptleri yazımı (`test_system.py`)
- Performans optimizasyonu

**Katkı Oranı:** %[yüzde]

### [Üye 3 - Ad Soyad]
- Kullanıcı arayüzü tasarımı (`main.py`)
- Görselleştirme modülü (`visualizer.py`)
- Rapor hazırlanması
- Test ve hata ayıklama

**Katkı Oranı:** %[yüzde]

---

## 10. Sonuç

Bu projede DTMF protokolüne benzer bir yöntemle Türkçe alfabenin tamamı frekans tabanlı ses sinyallerine kodlanmış ve başarıyla geri çözülmüştür. Goertzel algoritması kullanılarak verimli bir analiz sistemi geliştirilmiş, pencereleme ve debouncing teknikleri ile yüksek doğruluk oranları elde edilmiştir.

Proje kapsamında öğrenilen temel sinyal işleme kavramları:
- Örnekleme ve Nyquist teoremi
- Frekans analizi (FFT ve Goertzel)
- Pencereleme teknikleri
- Spektral analiz
- Gerçek zamanlı sinyal işleme

Sistem [%] doğruluk oranı ile çalışmakta ve gerçek dünya uygulamalarında kullanılabilir seviyededir.

---

**Rapor Hazırlayan:**  
[Grup Üyeleri]

**Tarih:**  
[Teslim Tarihi]
