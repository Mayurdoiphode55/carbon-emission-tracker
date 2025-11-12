"use client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function AvgSpeedBar({ data }) {
  return (
    <div className="p-4 bg-white rounded-2xl shadow-sm h-72">
      <h4 className="text-sm font-medium mb-2">Average Speed by Road</h4>
      <ResponsiveContainer width="100%" height={300} minWidth={300} minHeight={200}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="road" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="avg_speed" fill="#60a5fa" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
