import React from 'react';
import { Link } from 'react-router-dom';
import { ScoreGauge } from '../components/ScoreGauge';
import { StatCard } from '../components/StatCard';
import { SkillBadge } from '../components/SkillBadge';
import { StackCard } from '../components/StackCard';
import { ProjectCard } from '../components/ProjectCard';
import { RoadmapTimeline } from '../components/RoadmapTimeline';
import { Target, Layers, Map, FolderGit2, Sparkles, AlertCircle, ArrowRight, ShieldCheck } from 'lucide-react';

export const DashboardPage = ({ analysisData }) => {
  if (!analysisData) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-6">
        <div className="p-4 rounded-full bg-brand-indigo/10 border border-brand-indigo/20 text-brand-indigo w-16 h-16 mx-auto flex items-center justify-center">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-white">No Portfolio Analysis Found</h2>
        <p className="text-slate-400 text-sm max-w-md mx-auto">
          Please run a portfolio analysis first by providing your GitHub profile or technical skills.
        </p>
        <Link
          to="/analyze"
          className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl font-bold bg-brand-indigo text-white hover:bg-brand-indigo/90 transition-colors shadow-lg shadow-brand-indigo/20"
        >
          <span>Run Portfolio Analysis</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  const {
    overall_score = 0,
    score_breakdown = {},
    target_role = {},
    existing_skills = [],
    skill_gaps = {},
    recommended_stacks = [],
    recommended_projects = [],
    roadmap = {},
    ai_feedback = {}
  } = analysisData;

  const matchedSkills = skill_gaps.matched_skills || [];
  const missingSkills = (skill_gaps.missing_required_skills || []).concat(skill_gaps.missing_optional_skills || []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-dark-card via-slate-900 to-dark-card border border-dark-border rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center space-x-2 text-brand-indigo text-xs font-semibold uppercase tracking-wider mb-1">
            <Target className="w-4 h-4" />
            <span>Target Role Evaluation</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
            {target_role.name || 'Full Stack Developer'}
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">
            {target_role.description || 'Target role analysis and gap assessment.'}
          </p>
        </div>

        <Link
          to="/analyze"
          className="px-4 py-2.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors flex-shrink-0"
        >
          Re-Analyze Portfolio
        </Link>
      </div>

      {/* Top Metrics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Score Gauge Card */}
        <div className="bg-dark-card border border-dark-border rounded-2xl p-6 flex flex-col items-center justify-center">
          <ScoreGauge score={overall_score} label="Portfolio Strength Score" />
        </div>

        {/* Component Scores Grid */}
        <div className="lg:col-span-2 grid grid-cols-2 sm:grid-cols-3 gap-4">
          <StatCard
            title="Skill Diversity"
            value={`${score_breakdown.skill_diversity || 0}/100`}
            subtitle="25% Weight"
            color="indigo"
          />
          <StatCard
            title="Project Complexity"
            value={`${score_breakdown.project_complexity || 0}/100`}
            subtitle="25% Weight"
            color="purple"
          />
          <StatCard
            title="GitHub Activity"
            value={`${score_breakdown.github_activity || 0}/100`}
            subtitle="20% Weight"
            color="blue"
          />
          <StatCard
            title="Documentation"
            value={`${score_breakdown.documentation_quality || 0}/100`}
            subtitle="15% Weight"
            color="amber"
          />
          <StatCard
            title="Tech Relevance"
            value={`${score_breakdown.technology_relevance || 0}/100`}
            subtitle="15% Weight"
            color="emerald"
          />
          <StatCard
            title="Skill Match"
            value={`${skill_gaps.match_percentage || 0}%`}
            subtitle={`${missingSkills.length} Skill Gaps`}
            color="rose"
          />
        </div>
      </div>

      {/* AI Qualitative Feedback Banner */}
      {ai_feedback.executive_summary && (
        <div className="bg-gradient-to-r from-brand-indigo/10 via-brand-purple/10 to-transparent border border-brand-indigo/30 rounded-2xl p-6 space-y-3">
          <div className="flex items-center space-x-2 text-brand-purple font-bold text-sm">
            <Sparkles className="w-4 h-4" />
            <span>AI Executive Career Assessment</span>
          </div>
          <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-sans">
            {ai_feedback.executive_summary}
          </p>
          {ai_feedback.career_advice && (
            <p className="text-xs text-slate-300 border-t border-slate-800/80 pt-2 font-sans">
              <strong className="text-brand-indigo">Strategic Advice:</strong> {ai_feedback.career_advice}
            </p>
          )}
        </div>
      )}

      {/* Existing Skills vs Skill Gaps Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-dark-card border border-dark-border rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-brand-emerald"></span>
              <span>Matched Core Skills ({matchedSkills.length})</span>
            </h3>
          </div>
          <div className="flex flex-wrap gap-1.5 min-h-[80px]">
            {matchedSkills.map((sk) => (
              <SkillBadge key={sk.name} name={sk.name} category={sk.category} />
            ))}
          </div>
        </div>

        <div className="bg-dark-card border border-dark-border rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-brand-rose"></span>
              <span>Identified Skill Gaps ({missingSkills.length})</span>
            </h3>
          </div>
          <div className="flex flex-wrap gap-1.5 min-h-[80px]">
            {missingSkills.map((sk) => (
              <SkillBadge key={sk.name} name={sk.name} isMissing={true} isRequired={sk.is_required} />
            ))}
          </div>
        </div>
      </div>

      {/* Recommended Technology Stack Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Layers className="w-5 h-5 text-brand-indigo" />
            <span>Predicted Technology Stack</span>
          </h2>
          <Link to="/recommendations" className="text-xs font-semibold text-brand-indigo hover:underline flex items-center space-x-1">
            <span>View All Predictions</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {recommended_stacks.length > 0 && (
          <StackCard stack={recommended_stacks[0]} rank={1} />
        )}
      </div>

      {/* Recommended Projects Preview */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <FolderGit2 className="w-5 h-5 text-brand-purple" />
            <span>Recommended Skill Gap Projects</span>
          </h2>
          <Link to="/projects" className="text-xs font-semibold text-brand-purple hover:underline flex items-center space-x-1">
            <span>Explore All Projects</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recommended_projects.slice(0, 3).map((proj) => (
            <ProjectCard key={proj.id} project={proj} />
          ))}
        </div>
      </div>

      {/* Roadmap Preview */}
      <div className="bg-dark-card border border-dark-border rounded-2xl p-6 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center space-x-2">
              <Map className="w-5 h-5 text-brand-blue" />
              <span>Personalized Learning Roadmap</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Estimated Completion: {roadmap.estimated_weeks || 8} Weeks | {roadmap.phases?.length || 0} Phases
            </p>
          </div>
          <Link to="/roadmap" className="text-xs font-semibold text-brand-blue hover:underline flex items-center space-x-1">
            <span>Full Roadmap</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <RoadmapTimeline phases={roadmap.phases} />
      </div>
    </div>
  );
};
