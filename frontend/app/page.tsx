"use client";
import { useEffect, useState } from "react";
import AvgSpeedBar from "../components/AvgSpeedBar";
import VehiclePie from "../components/VehiclePie";
import OccupancyLine from "../components/OccupancyLine";
import SystemStatusCard from "../components/SystemStatusCard";
import {
  fetchAvgSpeedByRoad,
  fetchVehicleCountByType,
  fetchOccupancyTrend,
} from "../lib/api";

export default function Dashboard() {
  const [avgSpeed, setAvgSpeed] = useState([]);
  const [vehicleCount, setVehicleCount] = useState([]);
  const [occupancy, setOccupancy] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadData() {
    setLoading(true);
    try {
      const [a, v, o] = await Promise.all([
        fetchAvgSpeedByRoad(),
        fetchVehicleCountByType(),
        fetchOccupancyTrend(),
      ]);
      setAvgSpeed(a || []);
      setVehicleCount(v || []);
      setOccupancy(o || []);
      setError(null);
    } catch {
      setError("Failed to fetch analytics");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  return (
    <main className="min-h-screen p-6 bg-gray-50">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <h1 className="text-2xl font-semibold">
            Carbon Emission Tracker — Dashboard
          </h1>
          <SystemStatusCard />
        </div>

        {loading && <p className="text-gray-500 text-sm">Loading data...</p>}
        {error && <p className="text-red-600 text-sm">{error}</p>}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <AvgSpeedBar data={avgSpeed} />
          <VehiclePie data={vehicleCount} />
          <OccupancyLine data={occupancy} />
        </div>

        <p className="text-xs text-gray-500">
          Data fetched live from FastAPI on http://localhost:8080.
        </p>
      </div>
    </main>
  );
}
