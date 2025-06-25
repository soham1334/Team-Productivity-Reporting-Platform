import { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import Chatbot from "./chatbot";


type MetricEntry = {
  sprint: string;
  velocity: number;
  mttr: number;
};

export default function Dashboard() {
  const [teams, setTeams] = useState<string[]>([]);
  const [sprints, setSprints] = useState<string[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<string>("");
  const [selectedSprint, setSelectedSprint] = useState<string>("");
  const [filter, setFilter] = useState<"velocity" | "mttr">("velocity");
  const [chartData, setChartData] = useState<MetricEntry[]>([]);
  const [open, setOpen] = useState(false);

  // Fetch dropdowns
  useEffect(() => {
    const fetchDropdowns = async () => {
      try {
        console.log("SENDING TEMS AND SPRINT REQUEST")
        console.log("VITE_TEAM_API:", import.meta.env.VITE_TEAM_API);
        console.log("VITE_SPRINTS_API:", import.meta.env.VITE_SPRINTS_API);

        const [teamRes, sprintRes] = await Promise.all([
          axios.get(`${import.meta.env.VITE_TEAM_API}`),
          axios.get(`${import.meta.env.VITE_SPRINTS_API}`),
        ]);

        const teamList = teamRes.data.teams;
        const sprintList = sprintRes.data.sprints;

        setTeams(teamList);
        setSprints(sprintList);

        if (teamList.length > 0) setSelectedTeam(teamList[0]);
        if (sprintList.length > 0) setSelectedSprint(sprintList[3]);
      } catch {
        console.log("Failed to fetch dropdown data");
      }
    };

    fetchDropdowns();
  }, []);

  // Fetch metrics
  useEffect(() => {
    const fetchMetrics = async () => {
      if (!selectedTeam || !selectedSprint) return;

      try {
        const res = await axios.get(
          `${import.meta.env.VITE_METRICS_API}/${selectedTeam}/${selectedSprint}`
        );
        setChartData([res.data]);
      } catch {
        console.log("Failed to fetch metric data");
        alert("No Data");
      }
    };

    fetchMetrics();
  }, [selectedTeam, selectedSprint]);

  return (
    <div className="relative min-h-screen bg-gray-100 p-6 pb-20">
      <h1 className="text-3xl font-bold mb-6 text-center">Team Productivity Dashboard</h1>

      {/* Dropdown Filters */}
      <div className="flex flex-wrap justify-center gap-4 mb-6">
        <select
          value={selectedTeam}
          onChange={(e) => {
            setSelectedTeam(e.target.value);
            setSelectedSprint(sprints[0]); // reset sprint to first option
          }}
          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm"
        >
          {teams?.map((team) => (
            <option key={team} value={team}>
              {team}
            </option>
          ))}
        </select>

        <select
          value={selectedSprint}
          onChange={(e) => setSelectedSprint(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm"
        >
          {sprints?.map((sprint) => (
            <option key={sprint} value={sprint}>
              {sprint}
            </option>
          ))}
        </select>

        <Button
          onClick={() => setFilter("velocity")}
          variant={filter === "velocity" ? "default" : "outline"}
        >
          Sprint Velocity
        </Button>
        <Button
          onClick={() => setFilter("mttr")}
          variant={filter === "mttr" ? "default" : "outline"}
        >
          MTTR
        </Button>
      </div>

      {/* Chart */}
      <Card className="mx-auto max-w-4xl">
        <CardContent className="p-6">
          <h2 className="text-xl font-semibold mb-4">
            {filter === "velocity" ? "Sprint Velocity" : "Mean Time to Resolve (MTTR)"} for{" "}
            {selectedTeam} - {selectedSprint}
          </h2>

          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="sprint" />
              <YAxis domain={filter === "velocity" ? [0, 6] : [0, 10]} />
              <Tooltip />
              <Bar
                dataKey={filter}
                fill={filter === "velocity" ? "#6366f1" : "#f97316"}
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Chatbot Toggle Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <Button
          onClick={() => setOpen(!open)}
          className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg"
        >
          {open ? "Close Chatbot" : "Open Chatbot"}
        </Button>
      </div>

      {/* Chatbot */}
      {open && <Chatbot onClose={()=>(setOpen(false))}/>}
    </div>
  );
}
