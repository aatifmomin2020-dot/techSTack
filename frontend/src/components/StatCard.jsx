import React from 'react';

export const StatCard = ({ title, value, subtitle, icon: Icon, trend, color = "indigo" }) => {
  const colorMap = {
    indigo: "text-brand-indigo bg-brand-indigo/10 border-brand-indigo/20",
    purple: "text-brand-purple bg-brand-purple/10 border-brand-purple/20",
    blue: "text-brand-blue bg-brand-blue/10 border-brand-blue/20",
    emerald: "text-brand-emerald bg-brand-emerald/10 border-brand-emerald/20",
    amber: "text-brand-amber bg-brand-amber/10 border-brand-amber/20",
    rose: "text-brand-rose bg-brand-rose/10 border-brand-rose/20",
  };

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-5 hover:border-slate-700 transition-all shadow-sm">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium uppercase tracking-wider text-slate-400">{title}</span>
        {Icon && (
          <div className={`p-2.5 rounded-lg border ${colorMap[color] || colorMap.indigo}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>

      <div className="mt-3 flex items-baseline justify-between">
        <span className="text-2xl font-bold font-mono text-white">{value}</span>
        {trend && (
          <span className="text-xs font-semibold text-brand-emerald">
            {trend}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="mt-1 text-xs text-slate-400 font-sans">{subtitle}</p>
      )}
    </div>
  );
};
