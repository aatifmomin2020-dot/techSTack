import React from 'react';
import { FolderGit2, CheckCircle2, Award, Zap } from 'lucide-react';
import { SkillBadge } from './SkillBadge';

export const ProjectCard = ({ project }) => {
  const getDifficultyColor = (diff) => {
    switch (diff?.toLowerCase()) {
      case 'beginner':
        return 'text-emerald-400 bg-emerald-950/40 border-emerald-800/40';
      case 'intermediate':
        return 'text-indigo-400 bg-indigo-950/40 border-indigo-800/40';
      case 'advanced':
        return 'text-amber-400 bg-amber-950/40 border-amber-800/40';
      default:
        return 'text-slate-400 bg-slate-900 border-slate-800';
    }
  };

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-5 hover:border-slate-700 transition-all shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-2">
            <FolderGit2 className="w-5 h-5 text-brand-purple" />
            <h4 className="font-bold text-slate-100 text-base">{project.name}</h4>
          </div>
          <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${getDifficultyColor(project.difficulty)}`}>
            {project.difficulty}
          </span>
        </div>

        <p className="text-xs text-slate-400 mt-2 line-clamp-2">{project.description}</p>

        <div className="mt-4 pt-3 border-t border-slate-800">
          <span className="text-[10px] uppercase font-semibold text-slate-400 block mb-2">
            Skills Implemented
          </span>
          <div className="flex flex-wrap gap-1.5">
            {project.required_skills?.map((sk) => {
              const isCoveredGap = project.covered_missing_skills?.includes(sk);
              return (
                <SkillBadge key={sk} name={sk} isMissing={isCoveredGap} />
              );
            })}
          </div>
        </div>
      </div>

      {project.explanation && (
        <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center text-xs text-brand-emerald">
          <Zap className="w-3.5 h-3.5 mr-1.5 flex-shrink-0" />
          <span className="font-medium">{project.explanation}</span>
        </div>
      )}
    </div>
  );
};
