
import { useState, useEffect } from 'react';

type PyodideStatus = 'loading' | 'ready' | 'error';

// Pyodide is loaded into the global window object from the script tag in index.html
declare global {
  interface Window {
    loadPyodide: (config?: { indexURL: string }) => Promise<any>;
  }
}

export const usePyodide = () => {
  const [pyodide, setPyodide] = useState<any | null>(null);
  const [status, setStatus] = useState<PyodideStatus>('loading');

  useEffect(() => {
    const loadPyodideInstance = async () => {
      try {
        console.log('Loading Pyodide...');
        const pyodideInstance = await window.loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/"
        });
        console.log('Pyodide loaded. Loading packages...');
        await pyodideInstance.loadPackage(['numpy', 'scipy']);
        console.log('Packages loaded.');
        setPyodide(pyodideInstance);
        setStatus('ready');
      } catch (error) {
        console.error('Failed to load Pyodide or packages:', error);
        setStatus('error');
      }
    };

    loadPyodideInstance();
  }, []);

  return { pyodide, status };
};
