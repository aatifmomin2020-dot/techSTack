import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Github, Cpu, Target, Plus, X, Search, Loader2, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';
import { fetchRoles, fetchSkills, fetchGithubProfile, runPortfolioAnalysis } from '../services/api';

export const AnalyzePage = ({ onAnalysisComplete }) => {
  const navigate = useNavigate();

  const [githubUsername, setGithubUsername] = useState('');
  const [targetRoleId, setTargetRoleId] = useState(3); // Default Full Stack Dev
  const [yearsExperience, setYearsExperience] = useState(2);
  
  const [roles, setRoles] = useState([]);
  const [availableSkills, setAvailableSkills] = useState([]);
  const [selectedSkills, setSelectedSkills] = useState(['Python', 'JavaScript', 'React', 'FastAPI']);
  const [customSkillInput, setCustomSkillInput] = useState('');

  const [isFetchingGithub, setIsFetchingGithub] = useState(false);
  const [githubPreview, setGithubPreview] = useState(null);
  const [githubError, setGithubError] = useState('');

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState('');

  useEffect(() => {
    const loadMetadata = async () => {
      try {
        const [rolesData, skillsData] = await Promise.all([fetchRoles(), fetchSkills()]);
        setRoles(rolesData || []);
        setAvailableSkills(skillsData || []);
      } catch (err) {
        console.error('Error loading metadata:', err);
      }
    };
    loadMetadata();
  }, []);

  const handleFetchGithub = async () => {
    if (!githubUsername || !githubUsername.trim()) return;
    setIsFetchingGithub(true);
    setGithubError('');
    setGithubPreview(null);

    try {
      const data = await fetchGithubProfile(githubUsername.trim());
      setGithubPreview(data);
      
      // Auto-populate detected languages into selected skills
      if (data.languages_summary) {
        const detected = Object.keys(data.languages_summary);
        setSelectedSkills(prev => Array.from(new Set([...prev, ...detected])));
      }
    } catch (err) {
      setGithubError(err.response?.data?.detail || 'GitHub username not found or API rate limit reached.');
    } finally {
      setIsFetchingGithub(false);
    }
  };

  const handleAddSkill = (skillName) => {
    if (!skillName) return;
    const clean = skillName.trim();
    if (clean && !selectedSkills.includes(clean)) {
      setSelectedSkills([...selectedSkills, clean]);
    }
    setCustomSkillInput('');
  };

  const handleRemoveSkill = (skillName) => {
    setSelectedSkills(selectedSkills.filter(s => s !== skillName));
  };

  const handleSubmitAnalysis = async (e) => {
    e.preventDefault();
    setIsAnalyzing(true);
    setAnalysisError('');

    try {
      const payload = {
        github_username: githubUsername.trim() || null,
        target_role_id: parseInt(targetRoleId),
        current_skills: selectedSkills,
        years_experience: parseInt(yearsExperience)
      };

      const result = await runPortfolioAnalysis(payload);
      if (onAnalysisComplete) {
        onAnalysisComplete(result);
      }
      navigate('/dashboard');
    } catch (err) {
      setAnalysisError(err.response?.data?.detail || 'Error executing portfolio analysis. Please check your inputs.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-white tracking-tight">
          Portfolio & Skill Analysis Configuration
        </h1>
        <p className="text-sm text-slate-400">
          Enter your GitHub username or manually specify your technical stack to initiate ML stack prediction.
        </p>
      </div>

      <form onSubmit={handleSubmitAnalysis} className="space-y-6">
        {/* GitHub Integration Card */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-6 space-y-4">
          <div className="flex items-center space-x-2 text-brand-indigo font-bold text-base border-b border-slate-800 pb-3">
            <Github className="w-5 h-5" />
            <span>GitHub Profile Integration</span>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold uppercase text-slate-300">
              GitHub Username (Optional)
            </label>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <input
                  type="text"
                  placeholder="e.g. torvalds or your username"
                  value={githubUsername}
                  onChange={(e) => setGithubUsername(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-brand-indigo font-mono placeholder:text-slate-600"
                />
              </div>
              <button
                type="button"
                onClick={handleFetchGithub}
                disabled={isFetchingGithub || !githubUsername.trim()}
                className="px-4 py-2.5 rounded-lg text-sm font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center space-x-2 disabled:opacity-50 transition-colors"
              >
                {isFetchingGithub ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                <span>Fetch Profile</span>
              </button>
            </div>
            <p className="text-[11px] text-slate-500">
              If GitHub data is unavailable, manual skill input below will be used for full ML prediction.
            </p>
          </div>

          {githubError && (
            <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-800/40 text-rose-300 text-xs flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{githubError}</span>
            </div>
          )}

          {githubPreview && (
            <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between text-xs text-slate-300">
              <div className="flex items-center space-x-3">
                {githubPreview.avatar_url && (
                  <img src={githubPreview.avatar_url} alt="Avatar" className="w-10 h-10 rounded-full border border-slate-700" />
                )}
                <div>
                  <span className="font-bold text-white block">{githubPreview.name || githubPreview.username}</span>
                  <span className="text-slate-400 font-mono text-[11px]">{githubPreview.public_repos} Repositories | {githubPreview.followers} Followers</span>
                </div>
              </div>
              <span className="px-2.5 py-1 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[11px] font-semibold flex items-center space-x-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Fetched</span>
              </span>
            </div>
          )}
        </div>

        {/* Target Role & Experience */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-6 space-y-4">
          <div className="flex items-center space-x-2 text-brand-purple font-bold text-base border-b border-slate-800 pb-3">
            <Target className="w-5 h-5" />
            <span>Target Career Role</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase text-slate-300">
                Target Role
              </label>
              <select
                value={targetRoleId}
                onChange={(e) => setTargetRoleId(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-brand-purple"
              >
                {roles.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.name} ({r.category})
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase text-slate-300">
                Experience Level (Years)
              </label>
              <input
                type="number"
                min="0"
                max="25"
                value={yearsExperience}
                onChange={(e) => setYearsExperience(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-brand-purple font-mono"
              />
            </div>
          </div>
        </div>

        {/* Skill Multi-Select */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center space-x-2 text-brand-blue font-bold text-base">
              <Cpu className="w-5 h-5" />
              <span>Current Technical Skills ({selectedSkills.length})</span>
            </div>
          </div>

          {/* Active Skills Badges */}
          <div className="flex flex-wrap gap-2 min-h-[48px] p-3 rounded-lg bg-slate-900 border border-slate-800">
            {selectedSkills.map((sk) => (
              <span key={sk} className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-md text-xs font-mono font-semibold bg-brand-indigo/20 text-brand-indigo border border-brand-indigo/30">
                <span>{sk}</span>
                <button
                  type="button"
                  onClick={() => handleRemoveSkill(sk)}
                  className="hover:text-rose-400 transition-colors"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </span>
            ))}
          </div>

          {/* Quick Add Buttons from catalog */}
          <div className="space-y-2 pt-2">
            <span className="text-[11px] uppercase font-semibold text-slate-400 block">
              Quick Select Popular Technologies
            </span>
            <div className="flex flex-wrap gap-1.5">
              {availableSkills.slice(0, 20).map((s) => (
                <button
                  key={s.id}
                  type="button"
                  onClick={() => handleAddSkill(s.name)}
                  className={`text-xs px-2.5 py-1 rounded-md border font-mono transition-colors ${
                    selectedSkills.includes(s.name)
                      ? 'bg-slate-800 text-slate-500 border-slate-800 cursor-default'
                      : 'bg-slate-900 hover:bg-slate-800 text-slate-300 border-slate-700'
                  }`}
                >
                  + {s.name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {analysisError && (
          <div className="p-4 rounded-xl bg-rose-950/50 border border-rose-800/50 text-rose-300 text-xs flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{analysisError}</span>
          </div>
        )}

        {/* Action Button */}
        <button
          type="submit"
          disabled={isAnalyzing}
          className="w-full py-4 rounded-xl font-bold text-base bg-gradient-to-r from-brand-indigo via-brand-purple to-brand-blue hover:from-brand-indigo/90 hover:to-brand-blue/90 text-white shadow-lg shadow-brand-indigo/25 flex items-center justify-center space-x-2 transition-all disabled:opacity-50"
        >
          {isAnalyzing ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Analyzing Portfolio & Vectorizing Skills...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              <span>Analyze Portfolio & Predict Tech Stack</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};
