import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';

import { LandingPage } from './pages/LandingPage';
import { AnalyzePage } from './pages/AnalyzePage';
import { DashboardPage } from './pages/DashboardPage';
import { SkillAnalysisPage } from './pages/SkillAnalysisPage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import { ProjectsPage } from './pages/ProjectsPage';
import { RoadmapPage } from './pages/RoadmapPage';
import { AuthPage } from './pages/AuthPage';

export function App() {
  const [analysisData, setAnalysisData] = useState(null);

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
  };

  return (
    <AuthProvider>
      <Router>
        <div className="flex flex-col min-h-screen bg-dark-bg text-slate-100 font-sans">
          <Navbar />
          
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route 
                path="/analyze" 
                element={<AnalyzePage onAnalysisComplete={handleAnalysisComplete} />} 
              />
              <Route 
                path="/dashboard" 
                element={<DashboardPage analysisData={analysisData} />} 
              />
              <Route 
                path="/skills" 
                element={<SkillAnalysisPage analysisData={analysisData} />} 
              />
              <Route 
                path="/recommendations" 
                element={<RecommendationsPage analysisData={analysisData} />} 
              />
              <Route 
                path="/projects" 
                element={<ProjectsPage analysisData={analysisData} />} 
              />
              <Route 
                path="/roadmap" 
                element={<RoadmapPage analysisData={analysisData} />} 
              />
              <Route path="/auth" element={<AuthPage />} />
            </Routes>
          </main>

          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
