import React from 'react';

export const SkillBadge = ({ name, category, source, isMissing = false, isRequired = true }) => {
  if (isMissing) {
    return (
      <span className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-mono font-medium bg-rose-950/40 text-rose-300 border border-rose-800/40">
        <span>{name}</span>
        {isRequired && <span className="text-[10px] text-rose-400 font-bold">*</span>}
      </span>
    );
  }

  return (
    <span className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs font-mono font-medium bg-slate-800/80 text-slate-200 border border-slate-700/60 hover:border-slate-600 transition-colors">
      <span className="w-1.5 h-1.5 rounded-full bg-brand-emerald"></span>
      <span>{name}</span>
      {source === 'github_language' && (
        <span className="text-[9px] uppercase px-1 rounded bg-slate-900 text-slate-400">GH</span>
      )}
    </span>
  );
};
