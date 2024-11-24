#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:26:03 2024

@author: semecurbep
"""

import numpy as np
import matplotlib.pyplot as plt

# Définir les fréquences fondamentales pour un exemple de voix masculine et féminine
fundamental_freq_male = 110  # Fréquence typique d'une voix masculine (Hz)
fundamental_freq_female = 220  # Fréquence typique d'une voix féminine (Hz)

# Définir les harmoniques pour chaque voix
harmonics_count = 15  # Nombre d'harmoniques à inclure
harmonic_frequencies_male = [fundamental_freq_male * (n + 1) for n in range(harmonics_count)]
harmonic_frequencies_female = [fundamental_freq_female * (n + 1) for n in range(harmonics_count)]

# Amplitudes décroissantes des harmoniques (simplifiées)
harmonic_intensities = [1 / (n + 1) for n in range(harmonics_count)]

# Tracer le spectre audio simplifié pour les deux voix
plt.figure(figsize=(14, 6))
plt.stem(harmonic_frequencies_male, harmonic_intensities, basefmt=" ", linefmt="b-", markerfmt="bo", label='Voix masculine')
plt.stem(harmonic_frequencies_female, harmonic_intensities, basefmt=" ", linefmt="r-", markerfmt="ro", label='Voix féminine')
plt.title('Spectre audio simplifié de la voix humaine')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Amplitude relative')
plt.xlim(0, 5000)  # Limite de fréquence pour visualiser jusqu'à 5 kHz
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.legend()
plt.show()
