import React, { useState, useEffect, useCallback } from 'react';
import { usePyodide } from './hooks/usePyodide';
import SignalPlot from './components/SignalPlot';
import Spinner from './components/Spinner';
import { enobCalculationScript } from './services/pythonService';
import { SignalPoint } from './types';

const App: React.FC = () => {
  const { pyodide, status: pyodideStatus } = usePyodide();
  const [signalData, setSignalData] = useState<SignalPoint[]>([]);
  const [enob, setEnob] = useState<number | null>(null);
  const [sinad, setSinad] = useState<number | null>(null);
  const [isCalculating, setIsCalculating] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const generateSignal = useCallback(() => {
    const numSamples = 1024;
    const frequency = 5; // A non-integer frequency to avoid perfect binning
    const amplitude = 1.0;
    const noiseLevel = 0.05;
    const data: SignalPoint[] = [];

    for (let i = 0; i < numSamples; i++) {
      const time = i / numSamples;
      const pureSignal = amplitude * Math.sin(2 * Math.PI * frequency * time);
      const noise = (Math.random() - 0.5) * 2 * noiseLevel;
      data.push({ index: i, value: pureSignal + noise });
    }
    setSignalData(data);
    setEnob(null); // Reset results when new signal is generated
    setSinad(null);
    setErrorMessage(null);
  }, []);

  useEffect(() => {
    generateSignal();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const calculateEnob = async () => {
    if (pyodideStatus !== 'ready' || !pyodide || signalData.length === 0) {
      setErrorMessage("Pyodide is not ready or no signal data available.");
      return;
    }

    setIsCalculating(true);
    setErrorMessage(null);
    setEnob(null);
    setSinad(null);

    try {
      const signalValues = signalData.map(p => p.value);
      pyodide.globals.set('signal_data', signalValues);
      
      const resultJson = await pyodide.runPythonAsync(enobCalculationScript);
      const result = JSON.parse(resultJson);

      if (result.error) {
        throw new Error(result.error);
      }

      setEnob(result.enob);
      setSinad(result.sinad_db);
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "An unknown error occurred during calculation.";
      console.error("Calculation Error:", error);
      setErrorMessage(message);
    } finally {
      setIsCalculating(false);
    }
  };
  
  const renderLoadingScreen = () => (
    <div className="flex flex-col items-center justify-center min-h-screen text-gray-300">
      <Spinner className="w-16 h-16 text-blue-500" />
      <h1 className="text-2xl font-bold mt-4">Initializing Python Environment</h1>
      <p className="mt-2 text-lg">Loading Pyodide, NumPy, and SciPy. This may take a moment...</p>
    </div>
  );

  if (pyodideStatus === 'loading') {
    return renderLoadingScreen();
  }

  if (pyodideStatus === 'error') {
    return <div className="flex items-center justify-center min-h-screen text-red-400 text-xl">Failed to load Pyodide. Please check the browser console.</div>;
  }

  return (
    <div className="min-h-screen p-4 sm:p-6 md:p-8">
      <main className="max-w-4xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-teal-300">
            ENOB Signal Analyzer
          </h1>
          <p className="mt-2 text-lg text-gray-400">
            Measure the Effective Number of Bits of a signal using Python.
          </p>
        </header>

        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl shadow-2xl p-6">
          <div className="mb-6">
             <SignalPlot data={signalData} />
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <button
                onClick={calculateEnob}
                disabled={isCalculating}
                className="flex items-center justify-center px-6 py-3 font-semibold text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700 disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors duration-300"
              >
                {isCalculating ? <><Spinner className="w-5 h-5 mr-2" /> Calculating...</> : 'Calculate ENOB'}
              </button>
               <button
                onClick={generateSignal}
                disabled={isCalculating}
                className="px-6 py-3 font-semibold text-gray-300 bg-gray-700 rounded-lg shadow-md hover:bg-gray-600 disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors duration-300"
              >
                New Signal
              </button>
            </div>
            
            <div className="flex items-baseline gap-4 text-right">
                <div className="flex flex-col">
                    <span className="text-sm text-gray-400">SINAD</span>
                    <span className="text-2xl font-bold text-teal-300">
                        {sinad !== null ? `${sinad.toFixed(2)} dB` : '-'}
                    </span>
                </div>
                <div className="flex flex-col">
                    <span className="text-sm text-gray-400">ENOB</span>
                    <span className="text-4xl font-extrabold text-blue-400">
                        {enob !== null ? enob.toFixed(2) : '-'}
                    </span>
                    <span className="text-sm text-gray-400">bits</span>
                </div>
            </div>
          </div>
          
          {errorMessage && (
            <div className="mt-4 p-3 bg-red-900/50 border border-red-500 text-red-300 rounded-lg text-center">
              <strong>Error:</strong> {errorMessage}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;