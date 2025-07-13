from bokeh.plotting import figure, show
import numpy as np

# Préparer les données
# 200 points entre 0 et 4*pi
x = np.linspace(0, 4 * np.pi, 200)
y = np.sin(x)

# Créer une nouvelle figure avec un titre et des libellés d'axes
p = figure(title="Exemple de courbe Sinus", x_axis_label='x', y_axis_label='sin(x)')

# Ajouter un glyphe de ligne avec les données
p.line(x, y, legend_label="sin(x)", line_width=2, color="blue")

# Afficher le résultat
show(p)