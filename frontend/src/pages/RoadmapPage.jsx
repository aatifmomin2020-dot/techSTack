import React from 'react';
import { RoadmapTimeline } from '../components/RoadmapTimeline';
import { Map, Clock, Rocket, Sparkles } from 'lucide-react';

export const RoadmapPage = ({ analysisData }) => {
  if (!analysisData) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center text-slate-400 text-sm">
        Please complete a portfolio analysis first to view your learning roadmap.
      </div>
    );
  }

  const roadmap = analysisData.roadmap || {};
  const phases = roadmap.phases || [];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="border-b border-dark-border pb-4">
        <h1 className="text-3xl font-bold text-white tracking-tight flex items-center space-x-3">
          <Map className="w-7 h-7 text-brand-blue" />
          <span>Personalized Learning Roadmap</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Sequenced multi-phase learning path ordered by prerequisite graphs and role importance.
        </p>
      </div>

      <div className="bg-gradient-to-r from-dark-card via-slate-900 to-dark-card border border-dark-border rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-3 rounded-xl bg-brand-blue/15 text-brand-blue border border-brand-blue/30">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs uppercase font-mono tracking-wider text-slate-400 block">
              Estimated Total Learning Effort
            </span>
            <span className="text-xl font-bold text-white font-mono">
              {roadmap.estimated_weeks || 8} Weeks ({phases.reduce((acc, p) => acc + (p.estimated_hours || 0), 0)} Total Hours)
            </span>
          </div>
        </div>

        <span className="px-3 py-1 rounded-full bg-brand-indigo/15 text-brand-indigo border border-brand-indigo/30 text-xs font-semibold">
          {roadmap.target_role || 'Full Stack Developer'} Track
        </span>
      </div>

      <div className="bg-dark-card border border-dark-border rounded-2xl p-6 sm:p-8">
        <RoadmapTimeline phases={phases} />
      </div>
    </div>
  );
};
