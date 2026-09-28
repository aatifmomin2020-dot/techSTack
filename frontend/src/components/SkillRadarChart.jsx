import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

export const SkillRadarChart = ({ skills = [] }) => {
  const categoryCounts = {
    'Programming Language': 0,
    'Frontend': 0,
    'Backend': 0,
    'Database': 0,
    'Cloud': 0,
    'DevOps': 0,
    'AI/ML': 0,
    'Data Science': 0,
    'Testing': 0
  };

  skills.forEach((s) => {
    const cat = s.category || 'Programming Language';
    if (categoryCounts[cat] !== undefined) {
      categoryCounts[cat] += 1;
    } else {
      categoryCounts['Programming Language'] += 1;
    }
  });

  const data = Object.keys(categoryCounts).map((cat) => ({
    subject: cat,
    A: Math.min(categoryCounts[cat] * 20 + 20, 100),
    fullMark: 100,
  }));

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
          <PolarGrid stroke="#334155" />
          <PolarAngleAxis dataKey="subject" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" />
          <Radar name="Category Coverage" dataKey="A" stroke="#6366f1" fill="#6366f1" fillOpacity={0.4} />
          <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569', color: '#f8fafc', fontSize: '12px' }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
