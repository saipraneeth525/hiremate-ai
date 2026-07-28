import UploadCard from "./UploadCard";
import ATSRanking from "./ATSRanking";
import ChatPanel from "./ChatPanel";
import StatsCards from "./StatsCards";

export default function DashboardContent({
  uploadJD,
  uploadResumes,
  calculateATS,
  atsResults,
  sendMessage,
  onView,
}) {
  return (
    <div className="p-6 space-y-8">

      {/* Statistics */}
      <StatsCards atsResults={atsResults} />

      {/* Upload + Ranking */}
      <div className="grid grid-cols-12 gap-6">

        <div className="col-span-12 lg:col-span-4">
          <UploadCard
            uploadJD={uploadJD}
            uploadResumes={uploadResumes}
            calculateATS={calculateATS}
          />
        </div>

        <div className="col-span-12 lg:col-span-8">
          <ATSRanking
            atsResults={atsResults}
            onView={onView}
          />
        </div>

      </div>

      {/* AI Chat */}
      <ChatPanel
        sendMessage={sendMessage}
      />

    </div>
  );
}