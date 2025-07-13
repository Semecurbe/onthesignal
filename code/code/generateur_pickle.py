import pickle
import numpy as np

#
# IMPORTANT : La définition de cette classe Signal doit être identique
# à celle utilisée dans l'application web qui chargera le fichier.
#
class Signal:
    """
    Représente un signal 1D.
    """
    def __init__(self, *args, label: str = None):
        # L'attribut 'label' est maintenant une partie standard de la classe.
        self.label = label
        if len(args) == 1:
            self.y = np.asarray(args[0])
            if self.y.ndim != 1: raise TypeError("L'argument y doit être un tableau 1D.")
            self._x_start = 0.0
            self._periode_echantillonnage = 1.0
        elif len(args) == 2:
            x, y = np.asarray(args[0]), np.asarray(args[1])
            if x.ndim != 1 or y.ndim != 1: raise TypeError("Les arguments x et y doivent être des tableaux 1D.")
            if x.shape != y.shape: raise ValueError("Les tableaux NumPy 'x' et 'y' doivent avoir la même taille.")
            self.y = y
            self._x_start = x[0] if len(x) > 0 else 0.0
            self._periode_echantillonnage = (x[1] - x[0]) if len(x) > 1 else 1.0
        else:
            raise ValueError(f"Le constructeur attend 1 ou 2 arguments, mais {len(args)} ont été fournis.")
        
        self._reconstruire_axe_x()

    def _reconstruire_axe_x(self):
        indices = np.arange(len(self.y))
        self.x = self._x_start + (indices * self._periode_echantillonnage)

    @property
    def x_start(self): return self._x_start
    @x_start.setter
    def x_start(self, val): self._x_start = float(val); self._reconstruire_axe_x()

    @property
    def periode_echantillonnage(self): return self._periode_echantillonnage
    @periode_echantillonnage.setter
    def periode_echantillonnage(self, val):
        if val <= 0: raise ValueError("La période d'échantillonnage doit être positive.")
        self._periode_echantillonnage = float(val); self._reconstruire_axe_x()

    @property
    def x_end(self): return self.x[-1] if len(self.y) > 0 else self._x_start
    @x_end.setter
    def x_end(self, val):
        if len(self.y) <= 1: self.x_start = val; return
        if val <= self._x_start: raise ValueError("'x_end' doit être supérieur à 'x_start'.")
        self.periode_echantillonnage = (val - self._x_start) / (len(self.y) - 1)
    
    def _apply_operation(self, other, op):
        new_label = None
        if isinstance(other, Signal):
            x_commun_debut = max(self.x_start, other.x_start)
            x_commun_fin = min(self.x_end, other.x_end)
            if x_commun_debut >= x_commun_fin: return Signal(np.array([]), np.array([]))
            indices = np.where((self.x >= x_commun_debut) & (self.x <= x_commun_fin))
            x_final, y_self = self.x[indices], self.y[indices]
            y_other = np.interp(x_final, other.x, other.y)
            return Signal(x_final, op(y_self, y_other), label=new_label)
        elif isinstance(other, (int, float, complex)):
            return Signal(self.x, op(self.y, other), label=new_label)
        return NotImplemented
    def __add__(self, other): return self._apply_operation(other, np.add)
    def __sub__(self, other): return self._apply_operation(other, np.subtract)

    def min(self): return np.min(self.y) if len(self.y) > 0 else np.nan
    def max(self): return np.max(self.y) if len(self.y) > 0 else np.nan
    def mean(self): return np.mean(self.y) if len(self.y) > 0 else np.nan

    def __repr__(self) -> str:
        return self.label if self.label else f"Signal(pts={len(self.y)})"

# --- Création des données à sauvegarder ---

# 1. Créer quelques signaux avec des labels
periode = 1.0 / 500  # 500 Hz
temps = np.arange(0, 2, periode) # 2 secondes de signal

s1 = Signal(temps, 2.5 * np.sin(2 * np.pi * 2 * temps), label="Basse Fréquence")
s2 = Signal(temps, 0.8 * np.cos(2 * np.pi * 20 * temps), label="Haute Fréquence")
s3 = s1 + s2
s3.label = "Signal Combiné"

# 2. Mettre les signaux dans une liste
donnees_a_sauvegarder = [s1, s2, s3]

# 3. Définir le nom du fichier
nom_fichier = 'signaux.pkl'

# 4. Sauvegarder la liste dans le fichier pickle
with open(nom_fichier, 'wb') as f:
    pickle.dump(donnees_a_sauvegarder, f)

print(f"Fichier '{nom_fichier}' créé avec succès, contenant {len(donnees_a_sauvegarder)} signaux.")

