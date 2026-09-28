import React from 'react';

export const ScoreGauge = ({ score = 0, size = 180, strokeWidth = 14, label = "Portfolio Score" }) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let colorClass = "text-emerald-500";
  let strokeColor = "#10b981";
  let ratingText = "Exceptional";

  if (score < 50) {
    colorClass = "text-rose-500";
    strokeColor = "#f43f5e";
    ratingText = "Needs Growth";
  } else if (score < 70) {
    colorClass = "text-amber-500";
    strokeColor = "#f59e0b";
    ratingText = "Developing";
  } else if (score < 85) {
    colorClass = "text-indigo-400";
    strokeColor = "#6366f1";
    ratingText = "Strong Fit";
  }

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#1e293b"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-4xl font-extrabold font-mono tracking-tight text-white">
            {score}
          </span>
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mt-0.5">
            out of 100
          </span>
        </div>
      </div>

      <div className="mt-3 text-center">
        <span className={`inline-block px-3 py-0.5 rounded-full text-xs font-semibold bg-slate-900 border border-slate-800 ${colorClass}`}>
          {ratingText}
        </span>
        <span className="block text-xs font-medium text-slate-400 mt-1">{label}</span>
      </div>
    </div>
  );
};
