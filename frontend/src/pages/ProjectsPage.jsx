import React, { useState } from 'react';
import { ProjectCard } from '../components/ProjectCard';
import { FolderGit2, Filter } from 'lucide-react';

export const ProjectsPage = ({ analysisData }) => {
  const [filterDifficulty, setFilterDifficulty] = useState('All');

  if (!analysisData) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center text-slate-400 text-sm">
        Please complete a portfolio analysis first to view project recommendations.
      </div>
    );
  }

  const projects = analysisData.recommended_projects || [];

  const filteredProjects = projects.filter((p) => {
    if (filterDifficulty === 'All') return true;
    return p.difficulty?.toLowerCase() === filterDifficulty.toLowerCase();
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-dark-border pb-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center space-x-3">
            <FolderGit2 className="w-7 h-7 text-brand-purple" />
            <span>Recommended Portfolio Projects</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Curated real-world project specifications designed to cover identified skill gaps.
          </p>
        </div>

        {/* Filter buttons */}
        <div className="flex items-center space-x-2 bg-dark-card border border-slate-800 rounded-lg p-1">
          <Filter className="w-4 h-4 text-slate-400 ml-2" />
          {['All', 'Beginner', 'Intermediate', 'Advanced'].map((level) => (
            <button
              key={level}
              onClick={() => setFilterDifficulty(level)}
              className={`px-3 py-1 rounded-md text-xs font-semibold transition-colors ${
                filterDifficulty === level
                  ? 'bg-brand-purple text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProjects.map((proj) => (
          <ProjectCard key={proj.id} project={proj} />
        ))}
      </div>
    </div>
  );
};
