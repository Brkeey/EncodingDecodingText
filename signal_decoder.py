"""
Sinyal Analizi (Decoding) Modülü
DTMF benzeri ses sinyallerini metin karakterlerine geri çözer.
Goertzel algoritması kullanarak frekans tespiti yapar.
"""

import numpy as np
import soundfile as sf
from typing import List, Tuple, Optional
from frequency_mapper import FrequencyMapper


class GoertzelAnalyzer:
    """
    Goertzel algoritması kullanarak belirli frekansların varlığını tespit eder.
    FFT'ye göre çok daha hızlı ve verimli çalışır.
    """
    
    def __init__(self, sample_rate: int, target_freq: float, block_size: int):
        """
        Args:
            sample_rate: Örnekleme frekansı (Hz)
            target_freq: Aranacak hedef frekans (Hz)
            block_size: Analiz bloğu büyüklüğü (örnek sayısı)
        """
        self.sample_rate = sample_rate
        self.target_freq = target_freq
        self.block_size = block_size
        
        k = int(0.5 + (block_size * target_freq) / sample_rate)
        omega = (2.0 * np.pi * k) / block_size
        self.coeff = 2.0 * np.cos(omega)
    
    def analyze(self, samples: np.ndarray) -> float:
        """
        Goertzel algoritması ile belirli frekansta güç seviyesini hesaplar.
        
        Args:
            samples: Analiz edilecek örnekler
            
        Returns:
            Hedef frekanstaki güç seviyesi
        """
        s_prev = 0.0
        s_prev2 = 0.0
        
        for sample in samples:
            s = sample + self.coeff * s_prev - s_prev2
            s_prev2 = s_prev
            s_prev = s
        
        power = s_prev2 * s_prev2 + s_prev * s_prev - self.coeff * s_prev * s_prev2
        
        return power


class SignalDecoder:
    """
    Ses sinyallerini analiz ederek orijinal metni geri çözer.
    """
    
    def __init__(self, 
                 sample_rate: int = 44100,
                 window_duration_ms: int = 40,
                 hop_duration_ms: int = 25,
                 power_threshold: float = 0.1):
        """
        Args:
            sample_rate: Örnekleme frekansı (Hz)
            window_duration_ms: Analiz penceresi süresi (milisaniye)
            hop_duration_ms: Pencere kaydırma süresi (milisaniye)
            power_threshold: Minimum güç eşik değeri (sinyal/gürültü ayrımı)
        """
        self.sample_rate = sample_rate
        self.window_duration_ms = window_duration_ms
        self.hop_duration_ms = hop_duration_ms
        self.power_threshold = power_threshold
        
        self.window_samples = int(sample_rate * window_duration_ms / 1000)
        self.hop_samples = int(sample_rate * hop_duration_ms / 1000)
        
        self.frequency_mapper = FrequencyMapper()
        self.all_frequencies = self.frequency_mapper.get_all_frequencies()
        
        self.goertzel_filters = {
            freq: GoertzelAnalyzer(sample_rate, freq, self.window_samples)
            for freq in self.all_frequencies
        }
    
    def _apply_window(self, samples: np.ndarray) -> np.ndarray:
        """Hamming pencereleme uygular."""
        window = np.hamming(len(samples))
        return samples * window
    
    def _detect_frequencies(self, window: np.ndarray) -> Tuple[Optional[int], Optional[int]]:
        """
        Pencerede en güçlü iki frekansı tespit eder.
        
        Returns:
            (düşük_frekans, yüksek_frekans) veya (None, None)
        """
        windowed_samples = self._apply_window(window)
        
        freq_powers = {}
        for freq, analyzer in self.goertzel_filters.items():
            power = analyzer.analyze(windowed_samples)
            freq_powers[freq] = power
        
        max_power = max(freq_powers.values())
        if max_power < self.power_threshold:
            return None, None
        
        sorted_freqs = sorted(freq_powers.items(), key=lambda x: x[1], reverse=True)
        
        low_freqs = self.frequency_mapper.low_frequencies
        high_freqs = self.frequency_mapper.high_frequencies
        
        detected_low = None
        detected_high = None
        
        for freq, power in sorted_freqs:
            if freq in low_freqs and detected_low is None:
                detected_low = freq
            elif freq in high_freqs and detected_high is None:
                detected_high = freq
            
            if detected_low is not None and detected_high is not None:
                break
        
        return detected_low, detected_high
    
    def decode_signal(self, signal: np.ndarray, debounce_windows: int = 2) -> str:
        """
        Ses sinyalini analiz ederek metni geri çözer.
        
        Args:
            signal: Analiz edilecek sinyal
            debounce_windows: Aynı karakterin tekrar algılanmasını önlemek için bekleme süresi
            
        Returns:
            Çözümlenmiş metin
        """
        decoded_chars = []
        last_char = None
        debounce_counter = 0
        
        num_windows = (len(signal) - self.window_samples) // self.hop_samples + 1
        
        for i in range(num_windows):
            start = i * self.hop_samples
            end = start + self.window_samples
            
            if end > len(signal):
                break
            
            window = signal[start:end]
            
            low_freq, high_freq = self._detect_frequencies(window)
            
            if low_freq is not None and high_freq is not None:
                char = self.frequency_mapper.get_character(low_freq, high_freq)
                
                if char is not None:
                    if char == last_char:
                        debounce_counter += 1
                    else:
                        if debounce_counter >= debounce_windows or last_char is None:
                            if char != last_char:
                                decoded_chars.append(char)
                                last_char = char
                                debounce_counter = 0
            else:
                if debounce_counter > 0:
                    debounce_counter -= 1
                if debounce_counter == 0:
                    last_char = None
        
        return ''.join(decoded_chars)
    
    def decode_file(self, filename: str) -> str:
        """
        WAV dosyasını okuyup içindeki metni çözer.
        
        Args:
            filename: Analiz edilecek WAV dosyası
            
        Returns:
            Çözümlenmiş metin
        """
        print(f"\n{'='*60}")
        print(f"SES DOSYASI ANALİZİ BAŞLADI")
        print(f"{'='*60}")
        print(f"Dosya: {filename}")
        
        signal, file_sample_rate = sf.read(filename)
        
        if file_sample_rate != self.sample_rate:
            print(f"⚠ Uyarı: Dosya örnekleme oranı ({file_sample_rate} Hz) "
                  f"beklenen değerden ({self.sample_rate} Hz) farklı!")
        
        if signal.ndim > 1:
            signal = np.mean(signal, axis=1)
        
        print(f"Sinyal süresi: {len(signal) / file_sample_rate:.2f} saniye")
        print(f"Örnek sayısı: {len(signal)}")
        print(f"Analiz penceresi: {self.window_duration_ms} ms")
        print(f"Pencere kaydırma: {self.hop_duration_ms} ms")
        
        decoded_text = self.decode_signal(signal)
        
        print(f"\n{'='*60}")
        print(f"SONUÇ: \"{decoded_text}\"")
        print(f"{'='*60}\n")
        
        return decoded_text


if __name__ == "__main__":
    decoder = SignalDecoder(
        sample_rate=44100,
        window_duration_ms=40,
        hop_duration_ms=25,
        power_threshold=0.1
    )
    
    try:
        decoded_text = decoder.decode_file("test_output.wav")
        print(f"✓ Çözümlenen metin: {decoded_text}")
    except FileNotFoundError:
        print("⚠ Test dosyası bulunamadı. Önce signal_encoder.py'yi çalıştırın.")
