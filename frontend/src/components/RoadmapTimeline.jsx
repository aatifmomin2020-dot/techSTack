import React from 'react';
import { Map, Clock, CheckCircle, ArrowRight, BookOpen, Rocket } from 'lucide-react';

export const RoadmapTimeline = ({ phases = [] }) => {
  if (!phases || phases.length === 0) {
    return (
      <div className="text-center py-10 text-slate-500 text-sm">
        No roadmap steps available yet. Please complete a portfolio analysis.
      </div>
    );
  }

  return (
    <div className="relative pl-6 md:pl-8 space-y-8 before:absolute before:left-3 md:before:left-4 before:top-3 before:bottom-3 before:w-0.5 before:bg-gradient-to-b before:from-brand-indigo before:via-brand-purple before:to-slate-800">
      {phases.map((phase, idx) => (
        <div key={idx} className="relative group">
          {/* Phase Node Indicator */}
          <div className="absolute -left-6 md:-left-8 top-1 w-6 h-6 rounded-full bg-slate-900 border-2 border-brand-indigo flex items-center justify-center text-white text-xs font-bold font-mono shadow-md group-hover:scale-110 group-hover:bg-brand-indigo transition-all">
            {phase.phase}
          </div>

          <div className="bg-dark-card border border-dark-border rounded-xl p-5 hover:border-slate-700 transition-all shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
              <div>
                <h4 className="text-base font-bold text-white flex items-center space-x-2">
                  <span>{phase.title}</span>
                  <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-brand-indigo/15 text-brand-indigo border border-brand-indigo/30">
                    {phase.priority} Priority
                  </span>
                </h4>
                <span className="text-xs text-slate-400 font-mono">Category: {phase.category}</span>
              </div>

              <div className="flex items-center space-x-3 text-xs text-slate-400">
                <span className="flex items-center space-x-1">
                  <Clock className="w-3.5 h-3.5 text-brand-amber" />
                  <span>Est. {phase.estimated_hours} Hours</span>
                </span>
                <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
                  {phase.difficulty_level}
                </span>
              </div>
            </div>

            <p className="text-xs text-slate-300 mt-3">{phase.reason}</p>

            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3 pt-3 border-t border-slate-800/60">
              {phase.prerequisites?.length > 0 && (
                <div className="text-xs text-slate-400">
                  <span className="font-semibold text-slate-300 block mb-1">Prerequisites:</span>
                  <div className="flex flex-wrap gap-1">
                    {phase.prerequisites.map((p) => (
                      <span key={p} className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300 font-mono text-[11px]">
                        {p}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {phase.recommended_project && (
                <div className="text-xs text-slate-400">
                  <span className="font-semibold text-brand-purple block mb-1 flex items-center">
                    <Rocket className="w-3 h-3 mr-1" /> Milestone Project:
                  </span>
                  <span className="text-slate-200 font-medium">{phase.recommended_project}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
