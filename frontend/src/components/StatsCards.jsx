import {
  Users,
  Trophy,
  BarChart3,
  AlertTriangle,
} from "lucide-react";

export default function StatsCards({ atsResults }) {
  const total = atsResults.length;

  const highest =
    total > 0
      ? Math.max(...atsResults.map((c) => c.ats_score))
      : 0;

  const average =
    total > 0
      ? Math.round(
          atsResults.reduce(
            (sum, c) => sum + c.ats_score,
            0
          ) / total
        )
      : 0;

  const review = atsResults.filter(
    (c) => c.ats_score < 60
  ).length;

  const cards = [
    {
      title: "Candidates",
      value: total,
      icon: Users,
      color: "bg-blue-100 text-blue-600",
    },
    {
      title: "Highest Score",
      value: highest + "%",
      icon: Trophy,
      color: "bg-green-100 text-green-600",
    },
    {
      title: "Average ATS",
      value: average + "%",
      icon: BarChart3,
      color: "bg-indigo-100 text-indigo-600",
    },
    {
      title: "Need Review",
      value: review,
      icon: AlertTriangle,
      color: "bg-red-100 text-red-600",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      {cards.map((card, index) => {
        const Icon = card.icon;

        return (
          <div
            key={index}
            className="bg-white rounded-xl shadow p-6"
          >
            <div className="flex justify-between items-center">

              <div>

                <p className="text-gray-500 text-sm">
                  {card.title}
                </p>

                <h2 className="text-3xl font-bold mt-2">
                  {card.value}
                </h2>

              </div>

              <div
                className={`p-4 rounded-xl ${card.color}`}
              >
                <Icon size={28} />
              </div>

            </div>
          </div>
        );
      })}
    </div>
  );
}