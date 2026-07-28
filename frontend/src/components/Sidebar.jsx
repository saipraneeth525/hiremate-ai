import {
  LayoutDashboard,
  Users,
  MessageSquare,
  Settings,
} from "lucide-react";

export default function Sidebar() {
  return (
    <div className="w-64 h-screen bg-slate-900 text-white flex flex-col">

      <div className="text-2xl font-bold p-6 border-b border-slate-700">
        HireMate AI
      </div>

      <nav className="flex-1 mt-6">

        <button className="w-full flex items-center gap-3 px-6 py-4 hover:bg-slate-800">
          <LayoutDashboard size={20} />
          Dashboard
        </button>

        <button className="w-full flex items-center gap-3 px-6 py-4 hover:bg-slate-800">
          <Users size={20} />
          Candidates
        </button>

        <button className="w-full flex items-center gap-3 px-6 py-4 hover:bg-slate-800">
          <MessageSquare size={20} />
          Recruiter Chat
        </button>

        <button className="w-full flex items-center gap-3 px-6 py-4 hover:bg-slate-800">
          <Settings size={20} />
          Settings
        </button>

      </nav>
    </div>
  );
}