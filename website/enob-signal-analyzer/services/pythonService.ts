
export const enobCalculationScript = `
import numpy as np
from scipy.signal import blackmanharris
import json

def calculate_enob(signal):
    try:
        # Ensure signal is a numpy array
        signal = np.array(signal)
        
        # Number of samples
        N = len(signal)
        
        if N < 16: # Need a minimum number of points for FFT
            return {"error": "Signal is too short for analysis."}

        # Apply a window function to reduce spectral leakage
        window = blackmanharris(N)
        windowed_signal = signal * window
        
        # Compute the FFT
        fft_result = np.fft.fft(windowed_signal)
        fft_freq = np.fft.fftfreq(N)
        
        # We only care about the positive frequencies (and ignore DC component)
        positive_freq_indices = np.where(fft_freq > 0)
        fft_mag = np.abs(fft_result[positive_freq_indices])

        if len(fft_mag) == 0:
            return {"error": "Could not analyze signal spectrum."}
        
        # Find the fundamental frequency (the peak)
        signal_bin = np.argmax(fft_mag)
        
        # Estimate signal power
        # Consider a small bin width around the fundamental to capture main lobe energy
        start_bin = max(0, signal_bin - 2)
        end_bin = min(len(fft_mag), signal_bin + 3)
        signal_power_bins = fft_mag[start_bin:end_bin]**2
        signal_power = np.sum(signal_power_bins)
        
        # Estimate total power
        total_power = np.sum(fft_mag**2)
        
        # Estimate noise + distortion power
        noise_and_distortion_power = total_power - signal_power
        
        if noise_and_distortion_power <= 1e-12: # Handle near-ideal case
            sinad_db = 120.0
        else:
            # Calculate SINAD
            sinad_ratio = signal_power / noise_and_distortion_power
            sinad_db = 10 * np.log10(sinad_ratio)
            
        # Calculate ENOB
        enob = (sinad_db - 1.76) / 6.02
        
        return {
            "enob": enob,
            "sinad_db": sinad_db
        }
    except Exception as e:
        return {"error": str(e)}

# This part will be executed by pyodide
# We assume 'signal_data' is set in the global namespace from JS
result = calculate_enob(signal_data)

# Convert dict to a PyProxy that can be read in JS as a JSON string
json.dumps(result)
`;
