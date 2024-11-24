#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:06:45 2024

@author: semecurbep
"""

import numpy as np
import matplotlib.pyplot as plt

# Fréquences audibles en Hz
frequencies = np.logspace(np.log10(20), np.log10(20000), num=500)

# Courbe typique de l'audition humaine, basée sur la courbe d'isosonie à 40 phon (simplifiée)
# Formule simplifiée pour une représentation visuelle
spl = 3.64 * (frequencies / 1000)**-0.8 - 6.5 * np.exp(-0.6 * (frequencies / 1000 - 3.3)**2) + 0.001 * (frequencies / 1000)**4

# Tracé de la courbe
plt.figure(figsize=(12, 6))
plt.plot(frequencies, spl, label='Courbe de l\'audition humaine', color='blue')
plt.xscale('log')
plt.gca().invert_yaxis()  # Pour que la sensibilité augmente vers le bas
plt.title('Courbe de sensibilité de l\'audition humaine (40 phon)')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('SPL (dB)')
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.axhline(0, color='gray', linewidth=0.7)
plt.legend()
plt.show()
