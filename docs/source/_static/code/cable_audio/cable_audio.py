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

ph_1m = np.angle(np.exp(-gamma*1))
ph_10m = np.angle(np.exp(-gamma*10))
ph_100m = np.angle(np.exp(-gamma*100))
ph_1000m = np.angle(np.exp(-gamma*1000))

gd_1m = -np.gradient(ph_1m, omega)
gd_10m = -np.gradient(ph_10m, omega)
gd_100m = -np.gradient(ph_100m, omega)
gd_1000m = -np.gradient(ph_1000m, omega)



# Tracé de l'atténuation en fonction de la fréquence
# axs.figure(figsize=(10, 6)
fig, axs = plt.subplots(2, 1, layout='constrained')


axs[0].plot(frequences, att_1m, label="1 m", linewidth=3)
axs[0].plot(frequences, att_10m, label="10 m", linewidth=3)
axs[0].plot(frequences, att_100m, label="100 m", linewidth=3)
#plt.plot(frequences, att_1000m, label="1000 m")

axs[1].plot(frequences, gd_1m*1e6, label="1 m", linewidth=3)
axs[1].plot(frequences, gd_10m*1e6, label="10 m", linewidth=3)
axs[1].plot(frequences, gd_100m*1e6, label="100 m", linewidth=3)

axs[0].set_xscale('log')  # Échelle logarithmique pour l'axe des fréquences
#plt.yscale('log')  # Échelle logarithmique pour l'axe des atténuations
axs[0].set_xlabel('Fréquence (Hz)')
axs[0].set_ylabel('Atténuation')
#plt.title('Fonction de transfert  câble bifilaire non torsadé ave')
axs[0].grid(True, which="both", linestyle='--', linewidth=0.5)
axs[0].legend(frameon=False)
#axs[0].tight_layout()

axs[1].set_xscale('log')  # Échelle logarithmique pour l'axe des fréquences
#plt.yscale('log')  # Échelle logarithmique pour l'axe des atténuations
axs[1].set_xlabel('Fréquence (Hz)')
axs[1].set_ylabel('Temps de groupe (μs)')
#plt.title('Fonction de transfert  câble bifilaire non torsadé ave')
axs[1].grid(True, which="both", linestyle='--', linewidth=0.5)
axs[1].legend(frameon=False)


plt.show()
