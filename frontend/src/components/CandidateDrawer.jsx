import {
  X,
  User,
  Mail,
  Phone,
  GraduationCap,
  Briefcase,
  Award,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

export default function CandidateDrawer({ candidate, onClose }) {
  if (!candidate) return null;

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black/40 z-40"
        onClick={onClose}
      />

      {/* Drawer */}
      <div className="fixed top-0 right-0 h-screen w-full md:w-[480px] bg-white shadow-2xl z-50 overflow-y-auto">

        {/* Header */}
        <div className="sticky top-0 bg-white border-b p-6 flex justify-between items-center">

          <div>
            <h2 className="text-2xl font-bold">
              Candidate Profile
            </h2>

            <p className="text-gray-500">
              ATS Analysis Report
            </p>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100"
          >
            <X />
          </button>

        </div>

        <div className="p-6 space-y-8">

          {/* Candidate */}
          <div className="flex items-center gap-4">

            <div className="w-20 h-20 rounded-full bg-indigo-100 flex items-center justify-center">
              <User
                size={40}
                className="text-indigo-600"
              />
            </div>

            <div>
              <h2 className="text-2xl font-bold">
                {candidate.candidate}
              </h2>

              <p className="text-gray-500">
                Resume Candidate
              </p>
            </div>

          </div>

          {/* ATS Score */}
          <div>

            <div className="flex justify-between mb-2">

              <h3 className="font-semibold">
                ATS Score
              </h3>

              <span className="text-indigo-600 font-bold text-xl">
                {candidate.ats_score}%
              </span>

            </div>

            <div className="bg-gray-200 rounded-full h-4">

              <div
                className="bg-indigo-600 h-4 rounded-full"
                style={{
                  width: `${candidate.ats_score}%`,
                }}
              />

            </div>

          </div>

          {/* Contact */}

          <div>

            <h3 className="font-bold text-lg mb-4">
              Contact
            </h3>

            <div className="space-y-4">

              <div className="flex gap-3">

                <Mail className="text-indigo-600" />

                <span>
                  {candidate.email || "Not Available"}
                </span>

              </div>

              <div className="flex gap-3">

                <Phone className="text-indigo-600" />

                <span>
                  {candidate.phone || "Not Available"}
                </span>

              </div>

            </div>

          </div>

          {/* Education */}

          <div>

            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">

              <GraduationCap />

              Education

            </h3>

            <p className="text-gray-700">
              {candidate.education || "Not Available"}
            </p>

          </div>

          {/* Experience */}

          <div>

            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">

              <Briefcase />

              Experience

            </h3>

            <p className="text-gray-700">
              {candidate.experience || "Fresher"}
            </p>

          </div>

          {/* Matched Skills */}

          <div>

            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">

              <CheckCircle className="text-green-600" />

              Matched Skills

            </h3>

            <div className="flex flex-wrap gap-2">

              {candidate.matched_skills?.map((skill, index) => (
                <span
                  key={index}
                  className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
                >
                  {skill}
                </span>
              ))}

            </div>

          </div>

          {/* Missing Skills */}

          <div>

            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">

              <AlertCircle className="text-red-600" />

              Missing Skills

            </h3>

            <div className="flex flex-wrap gap-2">

              {candidate.missing_skills?.map((skill, index) => (
                <span
                  key={index}
                  className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm"
                >
                  {skill}
                </span>
              ))}

            </div>

          </div>

          {/* Projects */}

          <div>

            <h3 className="font-bold text-lg mb-4">
              Projects
            </h3>

            {candidate.projects?.length ? (
              <ul className="list-disc pl-5 space-y-2">

                {candidate.projects.map((project, index) => (
                  <li key={index}>
                    {project}
                  </li>
                ))}

              </ul>
            ) : (
              <p className="text-gray-500">
                No projects available
              </p>
            )}

          </div>

          {/* Certifications */}

          <div>

            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">

              <Award />

              Certifications

            </h3>

            {candidate.certifications?.length ? (
              <ul className="list-disc pl-5 space-y-2">

                {candidate.certifications.map((cert, index) => (
                  <li key={index}>
                    {cert}
                  </li>
                ))}

              </ul>
            ) : (
              <p className="text-gray-500">
                No certifications found
              </p>
            )}

          </div>

        </div>

      </div>
    </>
  );
}