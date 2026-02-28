"""
Ana Kullanıcı Arayüzü
DTMF Benzeri Metin Kodlama/Kod Çözme Uygulaması
"""

import os
import sys
from signal_encoder import SignalEncoder
from signal_decoder import SignalDecoder
from frequency_mapper import FrequencyMapper
import sounddevice as sd
import soundfile as sf
import numpy as np


class DTMFApplication:
    """
    Ana uygulama sınıfı - Kullanıcı etkileşimi ve menü yönetimi
    """
    
    def __init__(self):
        self.encoder = SignalEncoder(
            sample_rate=44100,
            tone_duration_ms=40,
            silence_duration_ms=10
        )
        self.decoder = SignalDecoder(
            sample_rate=44100,
            window_duration_ms=40,
            hop_duration_ms=25,
            power_threshold=0.1
        )
        self.frequency_mapper = FrequencyMapper()
        self.output_folder = "output"
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def clear_screen(self):
        """Ekranı temizler."""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self):
        """Uygulama başlığını yazdırır."""
        print("\n" + "="*70)
        print(" " * 10 + "DTMF BENZERİ METİN KODLAMA/KOD ÇÖZME SİSTEMİ")
        print(" " * 15 + "Türkçe Alfabe - Frekans Tabanlı İletişim")
        print("="*70 + "\n")
    
    def print_menu(self):
        """Ana menüyü yazdırır."""
        print("\n📋 ANA MENÜ")
        print("-" * 70)
        print("1. 📝 Metin → Ses Dosyası (Encoding)")
        print("2. 🔊 Ses Dosyası → Metin (Decoding)")
        print("3. 🎵 Ses Dosyasını Çal")
        print("4. 📊 Frekans Tablosunu Görüntüle")
        print("5. 🧪 Test - Tam Döngü (Encoding + Decoding)")
        print("6. ❌ Çıkış")
        print("-" * 70)
    
    def encode_text_interface(self):
        """Metin kodlama arayüzü."""
        self.clear_screen()
        self.print_header()
        
        print("📝 METİN → SES DOSYASI (ENCODING)\n")
        print(f"Desteklenen karakterler: {', '.join(self.frequency_mapper.TURKISH_ALPHABET[:29])}")
        print("(Boşluk karakteri de desteklenmektedir)\n")
        
        text = input("🔤 Kodlanacak metni girin: ").strip()
        
        if not text:
            print("\n⚠ Hata: Metin boş olamaz!")
            input("\nDevam etmek için Enter'a basın...")
            return
        
        filename = input("💾 Dosya adı (varsayılan: encoded_message): ").strip()
        if not filename:
            filename = "encoded_message"
        
        filepath = os.path.join(self.output_folder, filename)
        
        try:
            signal = self.encoder.encode_and_save(text, filepath)
            
            play_choice = input("\n▶️  Sesi şimdi çalmak ister misiniz? (E/H): ").strip().upper()
            if play_choice == 'E':
                self.play_audio(signal, self.encoder.sample_rate)
            
        except Exception as e:
            print(f"\n❌ Hata: {e}")
        
        input("\nDevam etmek için Enter'a basın...")
    
    def decode_file_interface(self):
        """Ses dosyası kod çözme arayüzü."""
        self.clear_screen()
        self.print_header()
        
        print("🔊 SES DOSYASI → METİN (DECODING)\n")
        
        wav_files = [f for f in os.listdir(self.output_folder) if f.endswith('.wav')]
        
        if wav_files:
            print(f"📁 '{self.output_folder}' klasöründeki WAV dosyaları:")
            for i, f in enumerate(wav_files, 1):
                print(f"  {i}. {f}")
            print()
        
        filename = input("📂 Analiz edilecek WAV dosyasının adı: ").strip()
        
        if not filename:
            print("\n⚠ Hata: Dosya adı boş olamaz!")
            input("\nDevam etmek için Enter'a basın...")
            return
        
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        if not os.path.exists(filename):
            filepath = os.path.join(self.output_folder, filename)
        else:
            filepath = filename
        
        if not os.path.exists(filepath):
            print(f"\n❌ Hata: '{filepath}' dosyası bulunamadı!")
            input("\nDevam etmek için Enter'a basın...")
            return
        
        try:
            decoded_text = self.decoder.decode_file(filepath)
            
            print(f"\n✅ BAŞARILI!")
            print(f"📄 Çözümlenen metin: \"{decoded_text}\"")
            
            save_choice = input("\n💾 Sonucu metin dosyasına kaydetmek ister misiniz? (E/H): ").strip().upper()
            if save_choice == 'E':
                output_file = os.path.join(self.output_folder, "decoded_text.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(decoded_text)
                print(f"✓ Kaydedildi: {output_file}")
            
        except Exception as e:
            print(f"\n❌ Hata: {e}")
        
        input("\nDevam etmek için Enter'a basın...")
    
    def play_audio(self, signal: np.ndarray = None, sample_rate: int = None, filename: str = None):
        """Ses sinyalini çalar."""
        try:
            if filename:
                signal, sample_rate = sf.read(filename)
                print(f"\n▶️  Çalınıyor: {filename}")
            elif signal is not None and sample_rate is not None:
                print(f"\n▶️  Ses çalınıyor...")
            else:
                print("\n❌ Hata: Çalınacak ses bulunamadı!")
                return
            
            sd.play(signal, sample_rate)
            sd.wait()
            print("✓ Çalma tamamlandı.")
            
        except Exception as e:
            print(f"\n❌ Ses çalma hatası: {e}")
    
    def play_audio_interface(self):
        """Ses dosyası çalma arayüzü."""
        self.clear_screen()
        self.print_header()
        
        print("🎵 SES DOSYASINI ÇAL\n")
        
        wav_files = [f for f in os.listdir(self.output_folder) if f.endswith('.wav')]
        
        if not wav_files:
            print("⚠ 'output' klasöründe WAV dosyası bulunamadı!")
            input("\nDevam etmek için Enter'a basın...")
            return
        
        print(f"📁 Mevcut WAV dosyaları:")
        for i, f in enumerate(wav_files, 1):
            print(f"  {i}. {f}")
        
        filename = input("\n🎵 Çalınacak dosya adı: ").strip()
        
        if not filename:
            print("\n⚠ Hata: Dosya adı boş olamaz!")
            input("\nDevam etmek için Enter'a basın...")
            return
        
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        filepath = os.path.join(self.output_folder, filename)
        
        if not os.path.exists(filepath):
            print(f"\n❌ Hata: '{filepath}' dosyası bulunamadı!")
            input("\nDevam etmek için Enter'a basın...")
            return
        
        self.play_audio(filename=filepath)
        input("\nDevam etmek için Enter'a basın...")
    
    def show_frequency_table(self):
        """Frekans tablosunu görüntüler."""
        self.clear_screen()
        self.print_header()
        self.frequency_mapper.print_frequency_table()
        input("Devam etmek için Enter'a basın...")
    
    def test_full_cycle(self):
        """Tam döngü testi yapar (encoding + decoding)."""
        self.clear_screen()
        self.print_header()
        
        print("🧪 TAM DÖNGÜ TESTİ (ENCODING + DECODING)\n")
        
        test_text = input("🔤 Test metni girin (varsayılan: 'MERHABA DÜNYA'): ").strip()
        if not test_text:
            test_text = "MERHABA DÜNYA"
        
        print(f"\n{'='*70}")
        print(f"📝 Orijinal Metin: \"{test_text}\"")
        print(f"{'='*70}")
        
        test_file = os.path.join(self.output_folder, "test_cycle.wav")
        
        try:
            print("\n[1/3] Encoding (Metin → Ses)...")
            signal = self.encoder.encode_and_save(test_text, test_file)
            
            play_choice = input("\n▶️  Üretilen sesi çalmak ister misiniz? (E/H): ").strip().upper()
            if play_choice == 'E':
                self.play_audio(signal, self.encoder.sample_rate)
            
            print("\n[2/3] Decoding (Ses → Metin)...")
            decoded_text = self.decoder.decode_file(test_file)
            
            print("\n[3/3] Sonuçlar Karşılaştırılıyor...")
            print(f"\n{'='*70}")
            print(f"📝 Orijinal : \"{test_text}\"")
            print(f"📄 Çözümlenen: \"{decoded_text}\"")
            print(f"{'='*70}")
            
            if test_text.upper() == decoded_text:
                print("\n✅ TEST BAŞARILI! Orijinal ve çözümlenen metin eşleşiyor.")
            else:
                print("\n⚠️  UYARI: Metinler tam olarak eşleşmiyor!")
                print(f"   Doğruluk oranı: {self._calculate_accuracy(test_text.upper(), decoded_text):.1f}%")
            
        except Exception as e:
            print(f"\n❌ Test Hatası: {e}")
        
        input("\nDevam etmek için Enter'a basın...")
    
    def _calculate_accuracy(self, original: str, decoded: str) -> float:
        """İki metin arasındaki benzerlik oranını hesaplar."""
        if not original:
            return 0.0
        
        matches = sum(1 for a, b in zip(original, decoded) if a == b)
        max_len = max(len(original), len(decoded))
        
        return (matches / max_len) * 100
    
    def run(self):
        """Ana uygulama döngüsü."""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = input("\n🔢 Seçiminiz (1-6): ").strip()
            
            if choice == '1':
                self.encode_text_interface()
            elif choice == '2':
                self.decode_file_interface()
            elif choice == '3':
                self.play_audio_interface()
            elif choice == '4':
                self.show_frequency_table()
            elif choice == '5':
                self.test_full_cycle()
            elif choice == '6':
                self.clear_screen()
                print("\n👋 Güle güle!\n")
                sys.exit(0)
            else:
                print("\n⚠ Geçersiz seçim! Lütfen 1-6 arası bir sayı girin.")
                input("\nDevam etmek için Enter'a basın...")


if __name__ == "__main__":
    try:
        app = DTMFApplication()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program sonlandırıldı.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        sys.exit(1)
