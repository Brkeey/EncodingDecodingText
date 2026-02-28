"""
Sinyal Sentezi (Encoding) Modülü
Metin karakterlerini DTMF benzeri ses sinyallerine dönüştürür.
"""

import numpy as np
import soundfile as sf
from typing import List
from frequency_mapper import FrequencyMapper


class SignalEncoder:
    """
    Metin karakterlerini frekans tabanlı ses sinyallerine kodlar.
    """
    
    def __init__(self, 
                 sample_rate: int = 44100,
                 tone_duration_ms: int = 40,
                 silence_duration_ms: int = 10):
        """
        Args:
            sample_rate: Örnekleme frekansı (Hz)
            tone_duration_ms: Her karakter sesi süresi (milisaniye)
            silence_duration_ms: Karakterler arası sessizlik süresi (milisaniye)
        """
        self.sample_rate = sample_rate
        self.tone_duration_ms = tone_duration_ms
        self.silence_duration_ms = silence_duration_ms
        self.frequency_mapper = FrequencyMapper()
        
        self.tone_samples = int(sample_rate * tone_duration_ms / 1000)
        self.silence_samples = int(sample_rate * silence_duration_ms / 1000)
    
    def generate_tone(self, freq1: int, freq2: int) -> np.ndarray:
        """
        İki frekanstan oluşan sinüzoidal sinyal üretir.
        s(t) = sin(2πf₁t) + sin(2πf₂t)
        
        Args:
            freq1: Düşük frekans (Hz)
            freq2: Yüksek frekans (Hz)
            
        Returns:
            Sinyal dizisi (numpy array)
        """
        t = np.linspace(0, self.tone_duration_ms / 1000, 
                       self.tone_samples, endpoint=False)
        
        signal = (np.sin(2 * np.pi * freq1 * t) + 
                 np.sin(2 * np.pi * freq2 * t))
        
        signal = self._apply_windowing(signal)
        
        signal = signal / np.max(np.abs(signal)) * 0.8
        
        return signal
    
    def _apply_windowing(self, signal: np.ndarray) -> np.ndarray:
        """
        Hann pencereleme uygulayarak spektral sızıntıyı azaltır.
        """
        window = np.hanning(len(signal))
        return signal * window
    
    def encode_text(self, text: str) -> np.ndarray:
        """
        Metni ses sinyaline kodlar.
        
        Args:
            text: Kodlanacak metin
            
        Returns:
            Kodlanmış ses sinyali (numpy array)
        """
        if not text:
            raise ValueError("Metin boş olamaz")
        
        audio_segments = []
        
        for char in text.upper():
            try:
                freq1, freq2 = self.frequency_mapper.get_frequencies(char)
                tone = self.generate_tone(freq1, freq2)
                audio_segments.append(tone)
                
                silence = np.zeros(self.silence_samples)
                audio_segments.append(silence)
                
            except ValueError as e:
                print(f"Uyarı: {e} - Karakter atlandı")
                continue
        
        full_signal = np.concatenate(audio_segments)
        
        return full_signal
    
    def save_to_wav(self, signal: np.ndarray, filename: str):
        """
        Ses sinyalini WAV dosyasına kaydeder.
        
        Args:
            signal: Kaydedilecek sinyal
            filename: Dosya adı (.wav uzantısı otomatik eklenir)
        """
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        sf.write(filename, signal, self.sample_rate)
        print(f"✓ Ses dosyası kaydedildi: {filename}")
        print(f"  - Süre: {len(signal) / self.sample_rate:.2f} saniye")
        print(f"  - Örnekleme oranı: {self.sample_rate} Hz")
        print(f"  - Örnekleme sayısı: {len(signal)}")
    
    def encode_and_save(self, text: str, filename: str) -> np.ndarray:
        """
        Metni kodlayıp WAV dosyasına kaydeder.
        
        Args:
            text: Kodlanacak metin
            filename: Çıktı dosya adı
            
        Returns:
            Kodlanmış sinyal
        """
        print(f"\n{'='*60}")
        print(f"METİN KODLAMA BAŞLADI")
        print(f"{'='*60}")
        print(f"Metin: \"{text}\"")
        print(f"Karakter sayısı: {len(text)}")
        print(f"Ton süresi: {self.tone_duration_ms} ms")
        print(f"Sessizlik süresi: {self.silence_duration_ms} ms")
        
        signal = self.encode_text(text)
        self.save_to_wav(signal, filename)
        
        print(f"{'='*60}\n")
        
        return signal


if __name__ == "__main__":
    encoder = SignalEncoder(
        sample_rate=44100,
        tone_duration_ms=40,
        silence_duration_ms=10
    )
    
    test_text = "MERHABA DÜNYA"
    encoder.encode_and_save(test_text, "test_output.wav")
    
    print("\n✓ Test başarılı! 'test_output.wav' dosyası oluşturuldu.")
