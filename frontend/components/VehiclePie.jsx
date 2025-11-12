"use client";
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#60a5fa", "#facc15", "#34d399", "#f87171", "#a78bfa"];

export default function VehiclePie({ data }) {
  return (
    <div className="p-4 bg-white rounded-2xl shadow-sm h-72">
      <h4 className="text-sm font-medium mb-2">Vehicle Count by Type</h4>
      <ResponsiveContainer width="100%" height={300} minWidth={300} minHeight={200}>
        <PieChart>
          <Pie
            data={data}
            dataKey="count"
            nameKey="type"
            outerRadius={80}
            label
          >
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
