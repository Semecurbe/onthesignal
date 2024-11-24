#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:19:21 2024

@author: semecurbep
"""

import numpy as np
import matplotlib.pyplot as plt

# Définir la fréquence fondamentale et les harmoniques
fundamental_freq = 440  # Fréquence de la fondamentale (La 440 Hz)
harmonics_count = 10  # Nombre d'harmoniques à tracer

# Calculer les fréquences et intensités relatives (simplifiées)
harmonic_frequencies = [fundamental_freq * (n + 1) for n in range(harmonics_count)]
harmonic_intensities = [1 / (n + 1) for n in range(harmonics_count)]  # Intensité décroissante simplifiée

# Tracer le spectre
plt.figure(figsize=(14, 6))
plt.stem(harmonic_frequencies, harmonic_intensities, basefmt=" ", linefmt="b-", markerfmt="bo")
plt.title('Spectre simplifié d\'un La 440 Hz avec harmoniques')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Amplitude relative')
plt.xticks(np.arange(0, harmonic_frequencies[-1] + 500, 440))
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.show()
