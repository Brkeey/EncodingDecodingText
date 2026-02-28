"""
DTMF Benzeri Metin Kodlama/Kod Çözme Sistemi
Türkçe Alfabesi için Frekans Tabanlı Sinyal İşleme
"""

import numpy as np
from typing import Tuple, Dict

class FrequencyMapper:
    """
    Türkçe alfabedeki her karakter için benzersiz frekans çiftleri atar.
    DTMF benzeri bir yapı kullanır (düşük ve yüksek frekans kombinasyonları).
    """
    
    def __init__(self):
        self.TURKISH_ALPHABET = [
            'A', 'B', 'C', 'Ç', 'D', 'E', 'F', 'G', 'Ğ', 'H',
            'I', 'İ', 'J', 'K', 'L', 'M', 'N', 'O', 'Ö', 'P',
            'R', 'S', 'Ş', 'T', 'U', 'Ü', 'V', 'Y', 'Z', ' '
        ]
        
        self.low_frequencies = [
            697, 770, 852, 941, 1020, 1100
        ]
        
        self.high_frequencies = [
            1209, 1336, 1477, 1633, 1800
        ]
        
        self.char_to_freq: Dict[str, Tuple[int, int]] = {}
        self.freq_to_char: Dict[Tuple[int, int], str] = {}
        
        self._generate_frequency_map()
    
    def _generate_frequency_map(self):
        """
        Her karakter için benzersiz (düşük_frekans, yüksek_frekans) çifti oluşturur.
        """
        index = 0
        for low_freq in self.low_frequencies:
            for high_freq in self.high_frequencies:
                if index < len(self.TURKISH_ALPHABET):
                    char = self.TURKISH_ALPHABET[index]
                    self.char_to_freq[char] = (low_freq, high_freq)
                    self.freq_to_char[(low_freq, high_freq)] = char
                    index += 1
    
    def get_frequencies(self, char: str) -> Tuple[int, int]:
        """Verilen karakter için frekans çiftini döndürür."""
        char_upper = char.upper()
        if char_upper not in self.char_to_freq:
            raise ValueError(f"Karakter '{char}' desteklenmiyor")
        return self.char_to_freq[char_upper]
    
    def get_character(self, low_freq: int, high_freq: int, tolerance: int = 50) -> str:
        """
        Verilen frekans çifti için karakteri döndürür.
        Tolerans değeri ile yaklaşık eşleşmelere izin verir.
        """
        for (stored_low, stored_high), char in self.freq_to_char.items():
            if (abs(stored_low - low_freq) <= tolerance and 
                abs(stored_high - high_freq) <= tolerance):
                return char
        return None
    
    def get_all_frequencies(self):
        """Tüm kullanılan frekansları döndürür (analiz için)."""
        all_freqs = set()
        for low_freq, high_freq in self.char_to_freq.values():
            all_freqs.add(low_freq)
            all_freqs.add(high_freq)
        return sorted(list(all_freqs))
    
    def print_frequency_table(self):
        """Frekans tablosunu yazdırır."""
        print("\n" + "="*60)
        print("TÜRKÇE ALFABE FREKANS TABLOSU")
        print("="*60)
        print(f"{'Karakter':<10} {'Düşük Frekans (Hz)':<20} {'Yüksek Frekans (Hz)':<20}")
        print("-"*60)
        for char in self.TURKISH_ALPHABET:
            low_freq, high_freq = self.char_to_freq[char]
            char_display = 'BOŞLUK' if char == ' ' else char
            print(f"{char_display:<10} {low_freq:<20} {high_freq:<20}")
        print("="*60 + "\n")


if __name__ == "__main__":
    mapper = FrequencyMapper()
    mapper.print_frequency_table()
    
    test_char = 'M'
    freq = mapper.get_frequencies(test_char)
    print(f"\n'{test_char}' karakteri için frekanslar: {freq}")
    
    retrieved_char = mapper.get_character(freq[0], freq[1])
    print(f"Frekans {freq} için karakter: '{retrieved_char}'")
