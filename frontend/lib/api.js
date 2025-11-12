import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080";

export async function fetchAvgSpeedByRoad() {
  const res = await axios.get(`${API_BASE}/analytics/avg_speed_by_road`);
  return res.data;
}

export async function fetchVehicleCountByType() {
  const res = await axios.get(`${API_BASE}/analytics/vehicle_count_by_type`);
  return res.data;
}

export async function fetchOccupancyTrend() {
  const res = await axios.get(`${API_BASE}/analytics/occupancy_trend`);
  return res.data;
}

export async function fetchHealth() {
  const res = await axios.get(`${API_BASE}/health`);
  return res.data;
}
