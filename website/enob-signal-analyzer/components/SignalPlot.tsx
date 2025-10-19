import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { SignalPoint } from '../types';

interface SignalPlotProps {
  data: SignalPoint[];
}

const SignalPlot: React.FC<SignalPlotProps> = ({ data }) => {
  return (
    <div className="w-full h-64 md:h-80 p-4 rounded-lg shadow-inner">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 0,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#4a5568" />
          <XAxis dataKey="index" stroke="#a0aec0" label={{ value: '', position: 'insideBottom', offset: -15, fill: '#a0aec0' }}/>
          <YAxis stroke="#a0aec0" label={{ value: 'Amplitude', angle: -90, position: 'insideLeft', fill: '#a0aec0' }} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1a202c', border: '1px solid #4a5568' }} 
            labelStyle={{ color: '#cbd5e0' }}
          />
          <Legend wrapperStyle={{ color: '#cbd5e0' }} />
          <Line type="monotone" dataKey="value" name="Signal" stroke="#4299e1" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SignalPlot;