import React from 'react';
import { Cpu, Github, ShieldCheck, Terminal } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="border-t border-dark-border bg-dark-bg/60 mt-16 py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between text-slate-400 text-xs">
        <div className="flex items-center space-x-3 mb-4 md:mb-0">
          <Cpu className="w-4 h-4 text-brand-indigo" />
          <span className="font-semibold text-slate-200">Developer Portfolio Tech Stack Predictor</span>
          <span className="text-slate-600">|</span>
          <span>Production AI/ML Career Intelligence</span>
        </div>

        <div className="flex items-center space-x-6 text-slate-400">
          <span className="flex items-center space-x-1">
            <ShieldCheck className="w-3.5 h-3.5 text-brand-emerald" />
            <span>Deterministic + TF-IDF Vector ML Engine</span>
          </span>
          <span className="flex items-center space-x-1">
            <Terminal className="w-3.5 h-3.5 text-brand-blue" />
            <span>FastAPI & React 18</span>
          </span>
        </div>
      </div>
    </footer>
  );
};
