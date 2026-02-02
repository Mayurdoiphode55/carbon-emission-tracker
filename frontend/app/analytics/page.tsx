"use client";

import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, ScatterChart, Scatter } from 'recharts';

interface DataPoint {
    location: string;
    vehicle_count: number;
    avg_speed: number;
    predicted_co2: number;
    weather?: string;
    vehicle_type?: string;
}

const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function AnalyticsPage() {
    const [data, setData] = useState<DataPoint[]>([]);

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws');
        ws.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                const point: DataPoint = {
                    location: msg.original_data?.location || 'Unknown',
                    vehicle_count: msg.original_data?.vehicle_count || 0,
                    avg_speed: msg.original_data?.avg_speed || 0,
                    predicted_co2: msg.predicted_co2 || 0,
                    weather: msg.original_data?.weather || 'Clear',
                    vehicle_type: msg.original_data?.vehicle_type || 'Car'
                };
                setData(prev => [...prev, point].slice(-100));
            } catch (e) { console.error(e); }
        };
        return () => ws.close();
    }, []);

    // City Statistics
    const cityData = Object.entries(
        data.reduce((acc, d) => {
            if (!acc[d.location]) acc[d.location] = { total: 0, count: 0 };
            acc[d.location].total += d.predicted_co2;
            acc[d.location].count++;
            return acc;
        }, {} as Record<string, { total: number; count: number }>)
    ).map(([name, stats]) => ({
        name,
        avgCo2: Math.round(stats.total / stats.count),
        count: stats.count
    }));

    // Vehicle Type Distribution
    const vehicleData = Object.entries(
        data.reduce((acc, d) => {
            const type = d.vehicle_type || 'Car';
            acc[type] = (acc[type] || 0) + 1;
            return acc;
        }, {} as Record<string, number>)
    ).map(([name, value]) => ({ name, value }));

    // Weather Impact
    const weatherData = Object.entries(
        data.reduce((acc, d) => {
            const weather = d.weather || 'Clear';
            if (!acc[weather]) acc[weather] = { total: 0, count: 0 };
            acc[weather].total += d.predicted_co2;
            acc[weather].count++;
            return acc;
        }, {} as Record<string, { total: number; count: number }>)
    ).map(([name, stats]) => ({
        name,
        avgCo2: Math.round(stats.total / stats.count)
    }));

    // Speed vs Emission Correlation
    const speedEmissionData = data.map(d => ({
        speed: d.avg_speed,
        emission: d.predicted_co2
    }));

    const avg = data.length ? (data.reduce((a, d) => a + d.predicted_co2, 0) / data.length) : 0;
    const max = data.length ? Math.max(...data.map(d => d.predicted_co2)) : 0;
    const min = data.length ? Math.min(...data.map(d => d.predicted_co2)) : 0;
    const avgSpeed = data.length ? (data.reduce((a, d) => a + d.avg_speed, 0) / data.length) : 0;

    return (
        <div style={{ padding: '32px', minHeight: '100vh', backgroundColor: '#0f172a' }}>
            <div style={{ marginBottom: '24px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#fff', marginBottom: '8px' }}>
                    Analytics
                </h1>
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                    Deep insights into emission patterns and trends
                </p>
            </div>

            {/* Summary Stats */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(4, 1fr)',
                gap: '16px',
                marginBottom: '24px'
            }}>
                <MiniCard label="Avg Emission" value={avg.toFixed(1)} unit="g/km" color="#10b981" />
                <MiniCard label="Peak Emission" value={max.toFixed(1)} unit="g/km" color="#ef4444" />
                <MiniCard label="Min Emission" value={min.toFixed(1)} unit="g/km" color="#3b82f6" />
                <MiniCard label="Avg Speed" value={avgSpeed.toFixed(1)} unit="km/h" color="#f59e0b" />
            </div>

            {/* Charts Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
                {/* City Emissions */}
                <ChartCard title="Emissions by City" subtitle="Average CO₂ levels per location">
                    <ResponsiveContainer width="100%" height={240}>
                        <BarChart data={cityData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey="name" stroke="#64748b" style={{ fontSize: '12px' }} />
                            <YAxis stroke="#64748b" style={{ fontSize: '12px' }} />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#1e293b',
                                    border: 'none',
                                    borderRadius: '8px'
                                }}
                            />
                            <Bar dataKey="avgCo2" fill="#10b981" radius={[6, 6, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </ChartCard>

                {/* Vehicle Type Distribution */}
                <ChartCard title="Vehicle Type Distribution" subtitle="Traffic composition breakdown">
                    <ResponsiveContainer width="100%" height={240}>
                        <PieChart>
                            <Pie
                                data={vehicleData}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={90}
                                paddingAngle={5}
                                dataKey="value"
                                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                            >
                                {vehicleData.map((_, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </ChartCard>

                {/* Weather Impact */}
                <ChartCard title="Weather Impact Analysis" subtitle="How weather affects emissions">
                    <ResponsiveContainer width="100%" height={240}>
                        <BarChart data={weatherData} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis type="number" stroke="#64748b" style={{ fontSize: '12px' }} />
                            <YAxis dataKey="name" type="category" stroke="#64748b" width={70} style={{ fontSize: '12px' }} />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#1e293b',
                                    border: 'none',
                                    borderRadius: '8px'
                                }}
                            />
                            <Bar dataKey="avgCo2" fill="#8b5cf6" radius={[0, 6, 6, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </ChartCard>

                {/* Speed vs Emission Correlation */}
                <ChartCard title="Speed vs Emission Correlation" subtitle="Relationship between traffic speed and CO₂">
                    <ResponsiveContainer width="100%" height={240}>
                        <ScatterChart>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis
                                dataKey="speed"
                                name="Speed"
                                unit=" km/h"
                                stroke="#64748b"
                                style={{ fontSize: '12px' }}
                            />
                            <YAxis
                                dataKey="emission"
                                name="Emission"
                                unit=" g/km"
                                stroke="#64748b"
                                style={{ fontSize: '12px' }}
                            />
                            <Tooltip
                                cursor={{ strokeDasharray: '3 3' }}
                                contentStyle={{
                                    backgroundColor: '#1e293b',
                                    border: 'none',
                                    borderRadius: '8px'
                                }}
                            />
                            <Scatter
                                data={speedEmissionData}
                                fill="#f59e0b"
                                opacity={0.6}
                            />
                        </ScatterChart>
                    </ResponsiveContainer>
                </ChartCard>
            </div>
        </div>
    );
}

function MiniCard({ label, value, unit, color }: {
    label: string;
    value: string;
    unit: string;
    color: string;
}) {
    return (
        <div style={{
            backgroundColor: '#1e293b',
            borderRadius: '12px',
            padding: '20px',
            border: `1px solid ${color}40`
        }}>
            <div style={{ color: '#94a3b8', fontSize: '13px', marginBottom: '8px' }}>{label}</div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
                <span style={{ fontSize: '28px', fontWeight: 'bold', color: '#fff' }}>{value}</span>
                <span style={{ fontSize: '13px', color: '#64748b' }}>{unit}</span>
            </div>
        </div>
    );
}

function ChartCard({ title, subtitle, children }: {
    title: string;
    subtitle: string;
    children: React.ReactNode;
}) {
    return (
        <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', padding: '24px' }}>
            <div style={{ marginBottom: '16px' }}>
                <h3 style={{ fontSize: '16px', fontWeight: '600', color: '#fff', marginBottom: '4px' }}>
                    {title}
                </h3>
                <p style={{ fontSize: '13px', color: '#64748b' }}>{subtitle}</p>
            </div>
            {children}
        </div>
    );
}
