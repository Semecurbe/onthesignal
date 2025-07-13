import numpy as np
import matplotlib.pyplot as plt

class Signal:
    """
    Représente un signal 1D.
    - Les propriétés dynamiques permettent de manipuler l'axe x.
    - Supporte les opérations arithmétiques.
    - La méthode fft() retourne un signal complexe.
    - La méthode afficher() gère l'affichage des signaux réels et complexes (gain/phase).
    - Inclut des méthodes pour les statistiques de base (min, max, moyenne).
    """

    def __init__(self, *args):
        # Le constructeur accepte maintenant les tableaux complexes nativement
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

    # --- Propriétés (x_start, periode_echantillonnage, x_end) ---
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
    def x_end(self): return self.x[-1] if len(self.x) > 0 else self._x_start
    @x_end.setter
    def x_end(self, val):
        if len(self.y) <= 1: self.x_start = val; return
        if val <= self._x_start: raise ValueError("'x_end' doit être supérieur à 'x_start'.")
        self.periode_echantillonnage = (val - self._x_start) / (len(self.y) - 1)

    # --- Surcharge des opérateurs arithmétiques ---
    def _apply_operation(self, other, op):
        if isinstance(other, Signal):
            x_commun_debut = max(self.x_start, other.x_start)
            x_commun_fin = min(self.x_end, other.x_end)
            if x_commun_debut >= x_commun_fin: return Signal(np.array([]), np.array([]))
            indices = np.where((self.x >= x_commun_debut) & (self.x <= x_commun_fin))
            x_final, y_self = self.x[indices], self.y[indices]
            y_other = np.interp(x_final, other.x, other.y)
            if op.__name__ == 'truediv':
                with np.errstate(divide='ignore', invalid='ignore'): result_y = op(y_self, y_other)
                result_y[np.isclose(y_other, 0)] = np.nan
                return Signal(x_final, result_y)
            return Signal(x_final, op(y_self, y_other))
        elif isinstance(other, (int, float, complex)):
            if op.__name__ == 'truediv' and other == 0: raise ZeroDivisionError("Division par un scalaire nul.")
            return Signal(self.x, op(self.y, other))
        return NotImplemented
    def __add__(self, other): return self._apply_operation(other, np.add)
    def __sub__(self, other): return self._apply_operation(other, np.subtract)
    def __mul__(self, other): return self._apply_operation(other, np.multiply)
    def __truediv__(self, other): return self._apply_operation(other, np.true_divide)
    def __radd__(self, other): return self.__add__(other)
    def __rmul__(self, other): return self.__mul__(other)
    def __rsub__(self, other):
        if isinstance(other, (int, float, complex)): return Signal(self.x, other - self.y)
        return NotImplemented
    def __rtruediv__(self, other):
        if isinstance(other, (int, float, complex)):
            with np.errstate(divide='ignore', invalid='ignore'): result_y = other / self.y
            result_y[np.isclose(self.y, 0)] = np.nan
            return Signal(self.x, result_y)
        return NotImplemented

    # --- Nouvelles méthodes pour les statistiques de base ---

    def min(self):
        """Calcule la valeur minimale du signal."""
        return np.min(self.y)

    def max(self):
        """Calcule la valeur maximale du signal."""
        return np.max(self.y)

    def mean(self):
        """Calcule la valeur moyenne du signal."""
        return np.mean(self.y)

    # --- Méthode pour la Transformée de Fourier ---
    def fft(self):
        """Calcule la FFT et retourne un nouveau Signal avec des valeurs y complexes."""
        N = len(self.y)
        if N == 0:
            return Signal(np.array([]), np.array([]))

        # 1. Calculer la FFT et l'axe des fréquences
        fft_values = np.fft.fft(self.y)
        freq_axis = np.fft.fftfreq(N, self.periode_echantillonnage)
        
        # 2. Ne garder que la partie positive du spectre
        positive_indices = np.where(freq_axis >= 0)
        
        return Signal(freq_axis[positive_indices], fft_values[positive_indices])

    # --- Méthode d'affichage ---
    def afficher(self, titre: str = "Signal", label_x: str = "X", label_y: str = "Y", **kwargs):
        """Affiche le signal. Gère automatiquement les signaux réels et complexes (gain/phase)."""
        
        # Cas 1 : Le signal est complexe (résultat d'une FFT)
        if np.iscomplexobj(self.y):
            # Créer 2 sous-graphiques (gain et phase)
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            fig.suptitle(titre, fontsize=16)

            # --- Graphique du Gain (Amplitude) ---
            N = len(self.y) * 2 # Approximer la taille du signal original
            gain = np.abs(self.y) / N * 2
            gain[0] /= 2 # La composante continue (0 Hz) ne doit pas être doublée
            
            ax1.plot(self.x, gain, 'o-', **kwargs)
            ax1.set_ylabel("Gain (Amplitude)")
            ax1.grid(True)

            # --- Graphique de la Phase ---
            phase = np.angle(self.y, deg=True) # Phase en degrés
            
            ax2.plot(self.x, phase, 'o-', color='r', **kwargs)
            ax2.set_xlabel(label_x)
            ax2.set_ylabel("Phase (degrés)")
            ax2.grid(True)

        # Cas 2 : Le signal est réel
        else:
            plt.figure(figsize=(12, 6))
            plt.plot(self.x, self.y, 'o-', label=repr(self), **kwargs)
            plt.title(titre)
            plt.xlabel(label_x)
            plt.ylabel(label_y)
            plt.grid(True)
            plt.legend()

    def __repr__(self) -> str:
        dtype = 'complex' if np.iscomplexobj(self.y) else 'real'
        return (f"Signal(pts={len(self.y)}, dtype={dtype}, "
                f"x=[{self.x_start:.2f}..{self.x_end:.2f}], p={self.periode_echantillonnage:.3f})")

# --- Exemple d'utilisation avec les nouvelles méthodes ---
if __name__ == "__main__":
    # Créer un signal temporel
    periode = 1.0 / 100  # 100 Hz
    temps = np.arange(0, 2, periode)
    y_signal = 0.7 * np.sin(2 * np.pi * 5 * temps) + 1.2 * np.sin(2 * np.pi * 12 * temps) + 5
    signal_temporel = Signal(temps, y_signal)
    
    print(f"Signal temporel : {signal_temporel}")
    
    # Utilisation des nouvelles méthodes de calcul
    print("-" * 30)
    print(f"Valeur minimale du signal : {signal_temporel.min():.4f}")
    print(f"Valeur maximale du signal : {signal_temporel.max():.4f}")
    print(f"Valeur moyenne du signal  : {signal_temporel.mean():.4f}")
    print("-" * 30)

    # Afficher le signal temporel
    signal_temporel.afficher(
        titre="Signal Temporel avec composante continue", 
        label_x="Temps (s)", 
        label_y="Amplitude"
    )

    # Calculer et afficher la FFT
    signal_frequentiel = signal_temporel.fft()
    print(f"Signal fréquentiel : {signal_frequentiel}")

    signal_frequentiel.afficher(
        titre="Spectre du Signal", 
        label_x="Fréquence (Hz)"
    )
    plt.xlim(0, 20)
    plt.show()