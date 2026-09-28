import React from 'react';
import { SkillRadarChart } from '../components/SkillRadarChart';
import { SkillBadge } from '../components/SkillBadge';
import { BarChart3, CheckCircle2, AlertCircle, Layers } from 'lucide-react';

export const SkillAnalysisPage = ({ analysisData }) => {
  if (!analysisData) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center text-slate-400 text-sm">
        Please complete a portfolio analysis first to view detailed skill distributions.
      </div>
    );
  }

  const existingSkills = analysisData.existing_skills || [];
  const skillGaps = analysisData.skill_gaps || {};
  const matchedSkills = skillGaps.matched_skills || [];
  const missingSkills = (skillGaps.missing_required_skills || []).concat(skillGaps.missing_optional_skills || []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="border-b border-dark-border pb-4">
        <h1 className="text-3xl font-bold text-white tracking-tight flex items-center space-x-3">
          <BarChart3 className="w-7 h-7 text-brand-indigo" />
          <span>Skill Distribution & Technical Gap Analysis</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Detailed breakdown of your extracted technologies, domain radar coverage, and target role skill requirements.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Domain Radar Chart Card */}
        <div className="bg-dark-card border border-dark-border rounded-2xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white border-b border-slate-800 pb-3">
            Domain Competency Radar
          </h3>
          <SkillRadarChart skills={existingSkills} />
        </div>

        {/* Category Breakdown Table */}
        <div className="bg-dark-card border border-dark-border rounded-2xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white border-b border-slate-800 pb-3">
            Extracted Skills Inventory ({existingSkills.length})
          </h3>

          <div className="max-h-72 overflow-y-auto space-y-2 pr-2">
            {existingSkills.map((sk, idx) => (
              <div key={idx} className="flex items-center justify-between p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs">
                <span className="font-semibold text-slate-200">{sk.name}</span>
                <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono text-[10px]">
                  {sk.category}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Strengths & Missing Table */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-dark-card border border-dark-border rounded-2xl p-6 space-y-4">
          <h3 className="text-base font-bold text-emerald-400 flex items-center space-x-2 border-b border-slate-800 pb-3">
            <CheckCircle2 className="w-5 h-5" />
            <span>Target Role Verified Strengths ({matchedSkills.length})</span>
          </h3>

          <div className="space-y-2">
            {matchedSkills.map((sk, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-emerald-950/20 border border-emerald-900/40 text-xs">
                <span className="font-bold text-emerald-300">{sk.name}</span>
                <span className="text-[11px] font-mono text-emerald-400/80">{sk.category}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-dark-card border border-dark-border rounded-2xl p-6 space-y-4">
          <h3 className="text-base font-bold text-rose-400 flex items-center space-x-2 border-b border-slate-800 pb-3">
            <AlertCircle className="w-5 h-5" />
            <span>Required Skill Gaps to Bridge ({missingSkills.length})</span>
          </h3>

          <div className="space-y-2">
            {missingSkills.map((sk, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-rose-950/20 border border-rose-900/40 text-xs">
                <span className="font-bold text-rose-300">{sk.name}</span>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800">
                  {sk.is_required ? 'Required' : 'Optional'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
