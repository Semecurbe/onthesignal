import numpy as np
import matplotlib.pyplot as plt

# Paramètres de la figure de Lissajous
p = 2
q = 3
delta = 0  # Déphasage à 0 comme demandé

# Créer un tableau de temps
t = np.linspace(0, 2 * np.pi, 500)

# Calculer les coordonnées x et y
x = np.sin(p * t + delta)
y = np.sin(q * t)

# Créer la figure et l'axe
fig, ax = plt.subplots(figsize=(6, 6))

# Régler le fond de la figure en noir
fig.patch.set_facecolor('black')
# Régler le fond de l'axe en noir
ax.set_facecolor('black')

# Tracer la courbe en blanc
ax.plot(x, y, color='white', linewidth=25) # Épaisseur de ligne ajustée pour un logo

# Supprimer les axes et les ticks pour un look plus épuré de logo
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Assurer un rapport d'aspect égal pour éviter la déformation
ax.set_aspect('equal', adjustable='box')

# Ajuster les marges pour que la figure remplisse bien l'espace
plt.tight_layout()

# Afficher la figure
plt.show()
