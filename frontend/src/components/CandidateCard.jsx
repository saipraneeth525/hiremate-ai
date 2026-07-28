import { User, Star, Eye } from "lucide-react";

export default function CandidateCard({ candidate, onView }) {
  const score = candidate.ats_score;

  let badgeColor = "bg-red-100 text-red-700";
  let badgeText = "Needs Review";

  if (score >= 80) {
    badgeColor = "bg-green-100 text-green-700";
    badgeText = "Excellent";
  } else if (score >= 65) {
    badgeColor = "bg-blue-100 text-blue-700";
    badgeText = "Good Match";
  } else if (score >= 50) {
    badgeColor = "bg-yellow-100 text-yellow-700";
    badgeText = "Average";
  }

  return (
    <div className="bg-white border rounded-xl shadow-sm hover:shadow-xl transition duration-300 p-6">

      {/* Header */}
      <div className="flex justify-between items-start">

        <div className="flex gap-4">

          <div className="w-14 h-14 rounded-full bg-indigo-100 flex items-center justify-center">
            <User className="text-indigo-600" size={28} />
          </div>

          <div>

            <h2 className="font-bold text-lg">
              {candidate.candidate}
            </h2>

            <p className="text-gray-500 text-sm">
              Resume Candidate
            </p>

          </div>

        </div>

        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold ${badgeColor}`}
        >
          {badgeText}
        </span>

      </div>

      {/* ATS Score */}

      <div className="mt-6">

        <div className="flex justify-between mb-2">

          <span className="font-medium">
            ATS Score
          </span>

          <span className="font-bold text-indigo-600">
            {score}%
          </span>

        </div>

        <div className="w-full bg-gray-200 rounded-full h-3">

          <div
            className="bg-indigo-600 h-3 rounded-full transition-all duration-700"
            style={{ width: `${score}%` }}
          />

        </div>

      </div>

      {/* Skills */}

      <div className="mt-6">

        <h3 className="font-semibold mb-2">
          Matched Skills
        </h3>

        <div className="flex flex-wrap gap-2">

          {candidate.matched_skills?.slice(0, 6).map((skill, index) => (
            <span
              key={index}
              className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm"
            >
              {skill}
            </span>
          ))}

        </div>

      </div>

      {/* Missing Skills */}

      <div className="mt-6">

        <h3 className="font-semibold mb-2">
          Missing Skills
        </h3>

        <div className="flex flex-wrap gap-2">

          {candidate.missing_skills?.slice(0, 5).map((skill, index) => (
            <span
              key={index}
              className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm"
            >
              {skill}
            </span>
          ))}

        </div>

      </div>

      {/* Footer */}

      <div className="mt-8 flex justify-between items-center">

        <div className="flex items-center gap-2 text-yellow-500">

          <Star size={18} fill="currentColor" />

          <span className="font-semibold">
            {score}/100
          </span>

        </div>

        <button
          onClick={() => onView(candidate)}
          className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-lg transition"
        >
          <Eye size={18} />
          View Details
        </button>

      </div>

    </div>
  );
}