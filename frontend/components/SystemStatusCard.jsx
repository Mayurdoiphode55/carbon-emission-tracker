"use client";
import { useEffect, useState } from "react";
import { fetchHealth } from "../lib/api";

export default function SystemStatusCard() {
  const [status, setStatus] = useState({ ok: false, info: null });

  async function check() {
    try {
      const data = await fetchHealth();
      setStatus({ ok: true, info: data });
    } catch {
      setStatus({ ok: false, info: null });
    }
  }

  useEffect(() => {
    check();
    const timer = setInterval(check, 10000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="p-4 bg-white rounded-2xl shadow-sm w-full max-w-sm">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-medium">System status</h3>
          <p className="text-xs text-gray-500">Backend health</p>
        </div>
        <div
          className={`px-3 py-1 rounded-full text-xs font-semibold ${
            status.ok ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
          }`}
        >
          {status.ok ? "OK" : "DOWN"}
        </div>
      </div>
      <p className="text-xs text-gray-600 mt-2">
        Info: {status.info ? JSON.stringify(status.info) : "No data"}
      </p>
    </div>
  );
}
