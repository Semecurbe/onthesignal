#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 13:59:04 2024

@author: onthesignal
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 14}) 

# Paramètres du câble (valeurs typiques)
R = 0.108  # Résistance par unité de longueur en Ω/m
L = 0.46e-6  # Inductance par unité de longueur en H/m
C = 27e-12  # Capacité par unité de longueur en F/m
G = 0  # Conductance par unité de longueur, négligée ici en S/m

# Fréquences à analyser (de 1 kHz à 1 GHz)
frequences = np.logspace(1, 5, 1000)  # de 10^3 Hz à 10^9 Hz
omega = 2 * np.pi * frequences  # Pulsation angulaire

# Calcul de la constante de propagation complexe γ
gamma = np.sqrt((R + 1j * omega * L) * (G + 1j * omega * C))

# Extraction de la partie réelle pour l'atténuation α (en Np/m)
#att_1m = -np.abs(20*np.log10(np.exp(-gamma*1)))
#att_10m = np.abs(20*np.log10(np.exp(-gamma*10)))
#att_100m = np.abs(20*np.log10(np.exp(-gamma*100)))
#att_1000m = np.abs(20*np.log10(np.exp(-gamma*1000)))

att_1m = np.abs(np.exp(-gamma*1))
att_10m = np.abs(np.exp(-gamma*10))
att_100m = np.abs(np.exp(-gamma*100))
att_1000m = np.abs(np.exp(-gamma*1000))


# Tracé de l'atténuation en fonction de la fréquence
plt.figure(figsize=(10, 6))
plt.plot(frequences, att_1m, label="1 m", linewidth=3)
plt.plot(frequences, att_10m, label="10 m", linewidth=3)
plt.plot(frequences, att_100m, label="100 m", linewidth=3)
#plt.plot(frequences, att_1000m, label="1000 m")


plt.xscale('log')  # Échelle logarithmique pour l'axe des fréquences
#plt.yscale('log')  # Échelle logarithmique pour l'axe des atténuations
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Atténuation')
#plt.title('Fonction de transfert  câble bifilaire non torsadé ave')
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.legend(frameon=False)
plt.tight_layout()

plt.show()
