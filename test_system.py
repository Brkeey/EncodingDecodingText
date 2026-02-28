"""
Test Modülü
Sistem performansını test eder ve doğruluk oranlarını hesaplar.
"""

import time
import numpy as np
from signal_encoder import SignalEncoder
from signal_decoder import SignalDecoder
from frequency_mapper import FrequencyMapper


class SystemTester:
    """
    Encoding/Decoding sistemi için kapsamlı test suite.
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
        self.test_results = []
    
    def calculate_accuracy(self, original, decoded):
        """
        İki metin arasındaki doğruluk oranını hesaplar.
        """
        if not original or not decoded:
            return 0.0
        
        correct = sum(1 for a, b in zip(original, decoded) if a == b)
        max_len = max(len(original), len(decoded))
        
        return (correct / max_len) * 100
    
    def test_single_character(self, char):
        """
        Tek bir karakter için test yapar.
        """
        try:
            signal = self.encoder.encode_text(char)
            decoded = self.decoder.decode_signal(signal)
            
            success = (decoded == char)
            return {
                'char': char,
                'decoded': decoded,
                'success': success,
                'accuracy': 100.0 if success else 0.0
            }
        except Exception as e:
            return {
                'char': char,
                'decoded': '',
                'success': False,
                'accuracy': 0.0,
                'error': str(e)
            }
    
    def test_all_characters(self):
        """
        Tüm karakterleri tek tek test eder.
        """
        print("\n" + "="*70)
        print("TEK KARAKTER TESTLERİ")
        print("="*70)
        
        results = []
        for char in self.frequency_mapper.TURKISH_ALPHABET:
            result = self.test_single_character(char)
            results.append(result)
            
            char_display = 'BOŞLUK' if char == ' ' else char
            status = "✓" if result['success'] else "✗"
            decoded_display = 'BOŞLUK' if result.get('decoded') == ' ' else result.get('decoded', 'HATA')
            
            print(f"{status} {char_display:<8} → {decoded_display:<8}")
        
        success_count = sum(1 for r in results if r['success'])
        total = len(results)
        success_rate = (success_count / total) * 100
        
        print("="*70)
        print(f"SONUÇ: {success_count}/{total} karakter başarılı (%{success_rate:.1f})")
        print("="*70 + "\n")
        
        return results
    
    def test_word(self, word):
        """
        Bir kelime için test yapar.
        """
        try:
            start_time = time.time()
            signal = self.encoder.encode_text(word)
            encoding_time = time.time() - start_time
            
            start_time = time.time()
            decoded = self.decoder.decode_signal(signal)
            decoding_time = time.time() - start_time
            
            accuracy = self.calculate_accuracy(word, decoded)
            
            return {
                'original': word,
                'decoded': decoded,
                'accuracy': accuracy,
                'encoding_time': encoding_time,
                'decoding_time': decoding_time,
                'total_time': encoding_time + decoding_time
            }
        except Exception as e:
            return {
                'original': word,
                'decoded': '',
                'accuracy': 0.0,
                'error': str(e)
            }
    
    def test_word_list(self, words):
        """
        Kelime listesi için test yapar.
        """
        print("\n" + "="*70)
        print("KELİME TESTLERİ")
        print("="*70)
        
        results = []
        for word in words:
            result = self.test_word(word)
            results.append(result)
            
            status = "✓" if result['accuracy'] >= 90 else "⚠" if result['accuracy'] >= 70 else "✗"
            
            print(f"\n{status} Orijinal : {result['original']}")
            print(f"  Çözümlenen: {result['decoded']}")
            print(f"  Doğruluk  : %{result['accuracy']:.1f}")
            if 'encoding_time' in result:
                print(f"  Encoding  : {result['encoding_time']*1000:.1f} ms")
                print(f"  Decoding  : {result['decoding_time']*1000:.1f} ms")
        
        avg_accuracy = np.mean([r['accuracy'] for r in results])
        
        print("\n" + "="*70)
        print(f"ORTALAMA DOĞRULUK: %{avg_accuracy:.1f}")
        print("="*70 + "\n")
        
        return results
    
    def run_full_test_suite(self):
        """
        Tam test paketini çalıştırır.
        """
        print("\n" + "="*70)
        print("DTMF SİSTEM TEST PAKETİ BAŞLIYOR")
        print("="*70)
        
        print("\n[1/3] Tek Karakter Testleri...")
        char_results = self.test_all_characters()
        
        print("\n[2/3] Kelime Testleri...")
        test_words = [
            "MERHABA",
            "DÜNYA",
            "TÜRKÇE",
            "SİNYAL",
            "İŞLEME",
            "ÖZYEĞIN",
            "ÜNİVERSİTE",
            "MERHABA DÜNYA",
            "TÜRKÇE ALFABE"
        ]
        word_results = self.test_word_list(test_words)
        
        print("\n[3/3] Tam Alfabe Testi...")
        alphabet_text = ''.join(self.frequency_mapper.TURKISH_ALPHABET[:-1])
        alphabet_result = self.test_word(alphabet_text)
        
        print("\n" + "="*70)
        print("TAM ALFABE TEST SONUCU")
        print("="*70)
        print(f"Orijinal : {alphabet_result['original'][:40]}...")
        print(f"Çözümlenen: {alphabet_result['decoded'][:40]}...")
        print(f"Doğruluk  : %{alphabet_result['accuracy']:.1f}")
        print("="*70)
        
        print("\n" + "="*70)
        print("GENEL ÖZET")
        print("="*70)
        
        char_success = sum(1 for r in char_results if r['success'])
        char_total = len(char_results)
        print(f"Tek Karakter Başarı Oranı: {char_success}/{char_total} (%{(char_success/char_total)*100:.1f})")
        
        word_avg = np.mean([r['accuracy'] for r in word_results])
        print(f"Kelime Ortalama Doğruluk  : %{word_avg:.1f}")
        
        print(f"Tam Alfabe Doğruluk       : %{alphabet_result['accuracy']:.1f}")
        
        avg_encoding_time = np.mean([r.get('encoding_time', 0) for r in word_results if 'encoding_time' in r])
        avg_decoding_time = np.mean([r.get('decoding_time', 0) for r in word_results if 'decoding_time' in r])
        
        print(f"\nOrtalama Encoding Süresi  : {avg_encoding_time*1000:.1f} ms")
        print(f"Ortalama Decoding Süresi  : {avg_decoding_time*1000:.1f} ms")
        
        print("="*70 + "\n")
        
        return {
            'char_results': char_results,
            'word_results': word_results,
            'alphabet_result': alphabet_result
        }


if __name__ == "__main__":
    tester = SystemTester()
    results = tester.run_full_test_suite()
    
    print("\n✅ Test paketi tamamlandı!")
