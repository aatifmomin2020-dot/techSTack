import React from 'react';
import { StackCard } from '../components/StackCard';
import { Layers, Sparkles } from 'lucide-react';

export const RecommendationsPage = ({ analysisData }) => {
  if (!analysisData) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center text-slate-400 text-sm">
        Please complete a portfolio analysis first to view technology stack predictions.
      </div>
    );
  }

  const recommendedStacks = analysisData.recommended_stacks || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="border-b border-dark-border pb-4">
        <h1 className="text-3xl font-bold text-white tracking-tight flex items-center space-x-3">
          <Layers className="w-7 h-7 text-brand-indigo" />
          <span>Predicted Technology Stacks</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          ML TF-IDF Cosine Similarity predictions ranking candidate tech stacks for your target career path.
        </p>
      </div>

      <div className="space-y-6">
        {recommendedStacks.map((stack, idx) => (
          <StackCard key={stack.id || idx} stack={stack} rank={idx + 1} />
        ))}
      </div>
    </div>
  );
};
