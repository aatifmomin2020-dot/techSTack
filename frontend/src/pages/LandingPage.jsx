import React from 'react';
import { Link } from 'react-router-dom';
import { Cpu, ArrowRight, Github, ShieldCheck, Layers, Map, Sparkles, FolderGit2, CheckCircle2, Award } from 'lucide-react';

export const LandingPage = () => {
  return (
    <div className="space-y-20 py-10">
      {/* Hero Section */}
      <section className="relative text-center space-y-6 max-w-4xl mx-auto px-4 pt-12">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-brand-indigo/15 border border-brand-indigo/30 text-brand-indigo text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Production AI/ML Developer Career & Portfolio Advisor</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight">
          Developer Portfolio <br />
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-brand-indigo via-brand-purple to-brand-blue">
            Tech Stack Predictor
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
          Analyze your GitHub profile, identify critical skill gaps for target roles, predict optimal technology stacks using TF-IDF Cosine Similarity, match portfolio projects, and generate a personalized learning roadmap.
        </p>

        <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            to="/analyze"
            className="w-full sm:w-auto px-8 py-4 rounded-xl font-bold bg-gradient-to-r from-brand-indigo to-brand-purple hover:from-brand-indigo/90 hover:to-brand-purple/90 text-white shadow-lg shadow-brand-indigo/25 flex items-center justify-center space-x-2 transition-all group"
          >
            <span>Analyze My Portfolio</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <a
            href="#features"
            className="w-full sm:w-auto px-8 py-4 rounded-xl font-semibold bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 flex items-center justify-center space-x-2 transition-colors"
          >
            <span>Explore Features</span>
          </a>
        </div>
      </section>

      {/* Analytics Preview Dashboard Grid */}
      <section id="features" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="text-center space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold text-white">
            End-to-End Developer Career Intelligence
          </h2>
          <p className="text-sm text-slate-400">
            Powered by GitHub REST API, TF-IDF Vector ML Engine, and Server-Side Gemini Reasoning
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-dark-card border border-dark-border rounded-2xl p-6 hover:border-slate-700 transition-all shadow-md">
            <div className="w-12 h-12 rounded-xl bg-brand-indigo/15 border border-brand-indigo/30 flex items-center justify-center text-brand-indigo mb-4">
              <Github className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">GitHub Skill Extraction</h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Extracts languages, topics, repository descriptions, and README content with canonical alias normalization (e.g. JS → JavaScript, Py → Python, Postgres → PostgreSQL).
            </p>
          </div>

          <div className="bg-dark-card border border-dark-border rounded-2xl p-6 hover:border-slate-700 transition-all shadow-md">
            <div className="w-12 h-12 rounded-xl bg-brand-purple/15 border border-brand-purple/30 flex items-center justify-center text-brand-purple mb-4">
              <Layers className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">ML Tech Stack Prediction</h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Calculates exact TF-IDF Cosine Similarity cosine(A, B) = (A · B) / (||A|| * ||B||) between your skill profile and enterprise production technology stacks.
            </p>
          </div>

          <div className="bg-dark-card border border-dark-border rounded-2xl p-6 hover:border-slate-700 transition-all shadow-md">
            <div className="w-12 h-12 rounded-xl bg-brand-blue/15 border border-brand-blue/30 flex items-center justify-center text-brand-blue mb-4">
              <Map className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Personalized Roadmap</h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Graph-based dependency topological sorting orders missing skills into phase-by-phase learning milestones with estimated effort hours and portfolio project recommendations.
            </p>
          </div>
        </div>
      </section>

      {/* Target Roles Showcase */}
      <section className="bg-slate-900/60 border-y border-dark-border py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <span className="text-xs font-mono uppercase tracking-widest text-brand-indigo">
            Supported Career Tracks
          </span>
          <h2 className="text-2xl font-bold text-white">Curated Industry Developer Roles</h2>
          
          <div className="flex flex-wrap justify-center gap-2">
            {[
              "Frontend Developer", "Backend Developer", "Full Stack Developer", "Python Developer",
              "Data Analyst", "Data Scientist", "Machine Learning Engineer", "AI Engineer",
              "DevOps Engineer", "Cloud Engineer"
            ].map((role) => (
              <span key={role} className="px-3 py-1.5 rounded-lg bg-dark-card border border-slate-800 text-slate-300 text-xs font-medium">
                {role}
              </span>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};
