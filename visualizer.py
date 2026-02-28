"""
Görselleştirme ve Analiz Araçları
Sinyal ve frekans spektrumlarını görselleştirir.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as scipy_signal
import soundfile as sf
from frequency_mapper import FrequencyMapper


class SignalVisualizer:
    """
    Ses sinyallerini ve frekans spektrumlarını görselleştirir.
    """
    
    def __init__(self):
        self.frequency_mapper = FrequencyMapper()
    
    def plot_signal_time_domain(self, signal, sample_rate, title="Zaman Domeninde Sinyal"):
        """
        Sinyali zaman domeninde çizer.
        """
        time = np.arange(len(signal)) / sample_rate
        
        plt.figure(figsize=(14, 5))
        plt.plot(time, signal, linewidth=0.5)
        plt.xlabel('Zaman (saniye)')
        plt.ylabel('Genlik')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt.gcf()
    
    def plot_signal_frequency_domain(self, signal, sample_rate, 
                                     title="Frekans Domeninde Sinyal"):
        """
        Sinyalin frekans spektrumunu çizer (FFT kullanarak).
        """
        n = len(signal)
        freq = np.fft.rfftfreq(n, d=1/sample_rate)
        fft = np.abs(np.fft.rfft(signal))
        
        fft_db = 20 * np.log10(fft + 1e-10)
        
        plt.figure(figsize=(14, 5))
        plt.plot(freq, fft_db, linewidth=1)
        plt.xlabel('Frekans (Hz)')
        plt.ylabel('Güç (dB)')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 3000)
        
        all_freqs = self.frequency_mapper.get_all_frequencies()
        for f in all_freqs:
            plt.axvline(x=f, color='r', linestyle='--', alpha=0.3, linewidth=0.8)
        
        plt.tight_layout()
        return plt.gcf()
    
    def plot_spectrogram(self, signal, sample_rate, title="Spektrogram"):
        """
        Sinyalin spektrogramını çizer (zaman-frekans analizi).
        """
        plt.figure(figsize=(14, 6))
        
        f, t, Sxx = scipy_signal.spectrogram(
            signal, 
            sample_rate,
            window='hamming',
            nperseg=1024,
            noverlap=512
        )
        
        plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), 
                      shading='gouraud', cmap='viridis')
        plt.ylabel('Frekans (Hz)')
        plt.xlabel('Zaman (saniye)')
        plt.title(title)
        plt.colorbar(label='Güç (dB)')
        plt.ylim(0, 2500)
        
        all_freqs = self.frequency_mapper.get_all_frequencies()
        for f in all_freqs:
            plt.axhline(y=f, color='r', linestyle='--', alpha=0.3, linewidth=0.5)
        
        plt.tight_layout()
        return plt.gcf()
    
    def analyze_wav_file(self, filename, save_plots=True):
        """
        WAV dosyasını analiz eder ve grafikleri oluşturur.
        """
        signal, sample_rate = sf.read(filename)
        
        if signal.ndim > 1:
            signal = np.mean(signal, axis=1)
        
        print(f"\n{'='*70}")
        print(f"SİNYAL ANALİZ RAPORU: {filename}")
        print(f"{'='*70}")
        print(f"Örnekleme Oranı: {sample_rate} Hz")
        print(f"Sinyal Uzunluğu: {len(signal)} örnek")
        print(f"Süre: {len(signal)/sample_rate:.3f} saniye")
        print(f"Maksimum Genlik: {np.max(np.abs(signal)):.4f}")
        print(f"RMS: {np.sqrt(np.mean(signal**2)):.4f}")
        print(f"{'='*70}\n")
        
        fig1 = self.plot_signal_time_domain(signal, sample_rate)
        if save_plots:
            fig1.savefig(f"{filename[:-4]}_time_domain.png", dpi=150)
            print(f"✓ Zaman domeninde grafik kaydedildi: {filename[:-4]}_time_domain.png")
        
        fig2 = self.plot_signal_frequency_domain(signal, sample_rate)
        if save_plots:
            fig2.savefig(f"{filename[:-4]}_frequency_domain.png", dpi=150)
            print(f"✓ Frekans domeninde grafik kaydedildi: {filename[:-4]}_frequency_domain.png")
        
        fig3 = self.plot_spectrogram(signal, sample_rate)
        if save_plots:
            fig3.savefig(f"{filename[:-4]}_spectrogram.png", dpi=150)
            print(f"✓ Spektrogram kaydedildi: {filename[:-4]}_spectrogram.png")
        
        if not save_plots:
            plt.show()
        else:
            plt.close('all')
    
    def plot_frequency_table_visual(self):
        """
        Frekans tablosunu görsel olarak çizer.
        """
        low_freqs = self.frequency_mapper.low_frequencies
        high_freqs = self.frequency_mapper.high_frequencies
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for i, char in enumerate(self.frequency_mapper.TURKISH_ALPHABET):
            low_f, high_f = self.frequency_mapper.get_frequencies(char)
            
            low_idx = low_freqs.index(low_f)
            high_idx = high_freqs.index(high_f)
            
            char_display = 'BOŞ' if char == ' ' else char
            ax.text(high_idx, len(low_freqs)-1-low_idx, char_display,
                   ha='center', va='center', fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        ax.set_xticks(range(len(high_freqs)))
        ax.set_xticklabels([f"{f} Hz" for f in high_freqs], rotation=45)
        ax.set_yticks(range(len(low_freqs)))
        ax.set_yticklabels([f"{f} Hz" for f in reversed(low_freqs)])
        
        ax.set_xlabel('Yüksek Frekanslar', fontsize=12, fontweight='bold')
        ax.set_ylabel('Düşük Frekanslar', fontsize=12, fontweight='bold')
        ax.set_title('DTMF Benzeri Türkçe Alfabe Frekans Tablosu', 
                    fontsize=14, fontweight='bold', pad=20)
        
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-0.5, len(high_freqs)-0.5)
        ax.set_ylim(-0.5, len(low_freqs)-0.5)
        
        plt.tight_layout()
        return fig


if __name__ == "__main__":
    visualizer = SignalVisualizer()
    
    print("📊 Görselleştirme Araçları Test Ediliyor...\n")
    
    fig = visualizer.plot_frequency_table_visual()
    fig.savefig("output/frequency_table_visual.png", dpi=150, bbox_inches='tight')
    print("✓ Frekans tablosu görseli oluşturuldu: output/frequency_table_visual.png")
    plt.close()
    
    import os
    wav_files = [f for f in os.listdir("output") if f.endswith('.wav')]
    
    if wav_files:
        print(f"\n📁 '{wav_files[0]}' dosyası analiz ediliyor...\n")
        visualizer.analyze_wav_file(f"output/{wav_files[0]}")
    else:
        print("\n⚠ Test için WAV dosyası bulunamadı.")
        print("Önce main.py'yi çalıştırarak bir ses dosyası oluşturun.")
