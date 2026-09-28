import React from 'react';
import { Layers, CheckCircle2, ArrowUpRight, Sparkles } from 'lucide-react';
import { SkillBadge } from './SkillBadge';

export const StackCard = ({ stack, rank = 1 }) => {
  const isTop = rank === 1;

  return (
    <div className={`relative bg-dark-card border rounded-xl p-6 transition-all shadow-md ${
      isTop ? 'border-brand-indigo/60 ring-1 ring-brand-indigo/30 bg-gradient-to-b from-dark-card to-slate-900/80' : 'border-dark-border hover:border-slate-700'
    }`}>
      {isTop && (
        <div className="absolute -top-3 right-4 px-3 py-0.5 rounded-full bg-gradient-to-r from-brand-indigo to-brand-purple text-white text-[11px] font-semibold flex items-center space-x-1 shadow-md">
          <Sparkles className="w-3 h-3" />
          <span>Top Match</span>
        </div>
      )}

      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center space-x-2">
            <Layers className="w-5 h-5 text-brand-indigo" />
            <h3 className="text-lg font-bold text-white">{stack.name}</h3>
          </div>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">{stack.description}</p>
        </div>

        <div className="text-right">
          <div className="text-2xl font-black font-mono text-brand-indigo">
            {stack.match_score}%
          </div>
          <span className="text-[10px] text-slate-500 font-mono block">
            TF-IDF Cosine: {stack.cosine_similarity}
          </span>
        </div>
      </div>

      <div className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-slate-800/80">
        <div>
          <span className="text-[11px] uppercase font-semibold text-slate-400 block mb-2">
            Current Skill Synergy ({stack.existing_skills?.length || 0})
          </span>
          <div className="flex flex-wrap gap-1.5">
            {stack.existing_skills?.map((sk) => (
              <SkillBadge key={sk} name={sk} />
            ))}
          </div>
        </div>

        <div>
          <span className="text-[11px] uppercase font-semibold text-rose-400 block mb-2">
            Missing Skills Covered ({stack.missing_skills_covered?.length || 0})
          </span>
          <div className="flex flex-wrap gap-1.5">
            {stack.missing_skills_covered?.map((sk) => (
              <SkillBadge key={sk} name={sk} isMissing={true} />
            ))}
          </div>
        </div>
      </div>

      {stack.reason && (
        <div className="mt-4 p-3 rounded-lg bg-slate-900/90 border border-slate-800 text-xs text-slate-300">
          <span className="font-semibold text-brand-indigo mr-1">ML Analysis:</span>
          {stack.reason}
        </div>
      )}
    </div>
  );
};
