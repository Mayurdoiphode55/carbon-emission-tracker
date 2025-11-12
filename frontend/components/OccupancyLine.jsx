"use client";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function OccupancyLine({ data }) {
  const formatted = data.map((d) => ({
    ...d,
    label: new Date(d.timestamp).toLocaleTimeString(),
  }));

  return (
    <div className="p-4 bg-white rounded-2xl shadow-sm h-72">
      <h4 className="text-sm font-medium mb-2">Occupancy Trend</h4>
      <ResponsiveContainer width="100%" height={300} minWidth={300} minHeight={200}>
        <LineChart data={formatted}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="occupancy" stroke="#34d399" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
