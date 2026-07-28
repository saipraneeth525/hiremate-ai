import { Upload, FileText, Users, BarChart3 } from "lucide-react";

export default function UploadCard({
  uploadJD,
  uploadResumes,
  calculateATS,
}) {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">

      <div className="flex items-center gap-3 mb-6">

        <div className="bg-indigo-100 p-3 rounded-lg">
          <Upload className="text-indigo-600" size={24} />
        </div>

        <div>
          <h2 className="text-2xl font-bold">
            Upload Center
          </h2>

          <p className="text-gray-500 text-sm">
            Upload Job Description & Candidate Resumes
          </p>
        </div>

      </div>

      {/* Job Description */}

      <div className="border-2 border-dashed border-gray-300 rounded-xl p-5 mb-5 hover:border-indigo-500 transition">

        <div className="flex items-center gap-3 mb-3">

          <FileText className="text-indigo-600" />

          <h3 className="font-semibold">
            Job Description
          </h3>

        </div>

        <input
          type="file"
          accept=".pdf,.doc,.docx,.txt"
          onChange={uploadJD}
          className="w-full text-sm"
        />

      </div>

      {/* Candidate Resumes */}

      <div className="border-2 border-dashed border-gray-300 rounded-xl p-5 mb-5 hover:border-green-500 transition">

        <div className="flex items-center gap-3 mb-3">

          <Users className="text-green-600" />

          <h3 className="font-semibold">
            Candidate Resumes
          </h3>

        </div>

        <input
          type="file"
          multiple
          accept=".pdf,.doc,.docx,.txt"
          onChange={uploadResumes}
          className="w-full text-sm"
        />

      </div>

      {/* Calculate Button */}

      <button
        onClick={calculateATS}
        className="w-full flex justify-center items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl transition"
      >
        <BarChart3 size={20} />
        Calculate ATS
      </button>

    </div>
  );
}