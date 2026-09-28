import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Cpu, LayoutDashboard, BarChart3, Layers, FolderGit2, Map, LogIn, LogOut, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Navbar = () => {
  const location = useLocation();
  const { user, logout } = useAuth();

  const navLinks = [
    { path: '/analyze', label: 'Analyze', icon: Cpu },
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/skills', label: 'Skill Analysis', icon: BarChart3 },
    { path: '/recommendations', label: 'Tech Stack', icon: Layers },
    { path: '/projects', label: 'Projects', icon: FolderGit2 },
    { path: '/roadmap', label: 'Roadmap', icon: Map },
  ];

  return (
    <header className="sticky top-0 z-50 bg-dark-bg/90 backdrop-blur-md border-b border-dark-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-indigo via-brand-purple to-brand-blue flex items-center justify-center text-white shadow-lg shadow-brand-indigo/25 group-hover:scale-105 transition-transform">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <span className="font-bold text-lg tracking-tight text-white group-hover:text-brand-indigo transition-colors">
              TechStack<span className="text-brand-purple">Predictor</span>
            </span>
            <span className="block text-[10px] uppercase font-mono tracking-widest text-slate-400 -mt-1">
              AI Career Advisor
            </span>
          </div>
        </Link>

        {/* Navigation Items */}
        <nav className="hidden md:flex items-center space-x-1">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`px-3 py-2 rounded-lg text-sm font-medium flex items-center space-x-2 transition-all ${
                  isActive
                    ? 'bg-brand-indigo/15 text-brand-indigo border border-brand-indigo/30'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* User Status / Auth Button */}
        <div className="flex items-center space-x-3">
          {user ? (
            <div className="flex items-center space-x-3 bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5">
              <User className="w-4 h-4 text-brand-indigo" />
              <span className="text-xs font-medium text-slate-200">{user.username}</span>
              <button
                onClick={logout}
                className="text-slate-400 hover:text-rose-400 transition-colors p-1"
                title="Logout"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <Link
              to="/auth"
              className="px-4 py-2 rounded-lg text-sm font-medium bg-brand-indigo hover:bg-brand-indigo/90 text-white flex items-center space-x-2 shadow-md shadow-brand-indigo/20 transition-all"
            >
              <LogIn className="w-4 h-4" />
              <span>Sign In</span>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
};
