import CandidateCard from "./CandidateCard";

export default function ATSRanking({
  atsResults,
  onView,
}) {
  if (atsResults.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow p-10 text-center text-gray-500">
        Upload resumes and calculate ATS to see rankings.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
      {atsResults.map((candidate, index) => (
        <CandidateCard
          key={index}
          candidate={candidate}
          onView={onView}
        />
      ))}
    </div>
  );
}