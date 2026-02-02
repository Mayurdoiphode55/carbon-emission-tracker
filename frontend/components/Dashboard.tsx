"use client";

import { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

interface DataPoint {
    timestamp: string;
    location: string;
    vehicle_count: number;
    avg_speed: number;
    predicted_co2: number;
}

export default function Dashboard() {
    const [data, setData] = useState<DataPoint[]>([]);
    const [current, setCurrent] = useState<DataPoint | null>(null);
    const [connected, setConnected] = useState(false);
    const [total, setTotal] = useState(0);

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws');

        ws.onopen = () => setConnected(true);
        ws.onclose = () => setConnected(false);

        ws.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);
                const point: DataPoint = {
                    timestamp: new Date().toLocaleTimeString(),
                    location: msg.original_data?.location || 'Unknown',
                    vehicle_count: msg.original_data?.vehicle_count || 0,
                    avg_speed: msg.original_data?.avg_speed || 0,
                    predicted_co2: msg.predicted_co2 || 0,
                };
                setCurrent(point);
                setTotal(prev => prev + point.predicted_co2);
                setData(prev => [...prev, point].slice(-50));
            } catch (e) {
                console.error(e);
            }
        };

        return () => ws.close();
    }, []);

    const cityData = Object.entries(
        data.reduce((acc, d) => {
            if (!acc[d.location]) acc[d.location] = { total: 0, count: 0 };
            acc[d.location].total += d.predicted_co2;
            acc[d.location].count++;
            return acc;
        }, {} as Record<string, { total: number; count: number }>)
    ).map(([city, stats]) => ({ city, avg: Math.round(stats.total / stats.count) }));

    return (
        <div style={{ padding: '32px', minHeight: '100vh', backgroundColor: '#0f172a' }}>
            {/* Header */}
            <div style={{ marginBottom: '24px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#fff', marginBottom: '8px' }}>
                    Dashboard
                </h1>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        backgroundColor: connected ? '#10b981' : '#ef4444'
                    }}></div>
                    <span style={{ color: '#94a3b8', fontSize: '14px' }}>
                        {connected ? 'Live Stream Active' : 'Disconnected'}
                    </span>
                </div>
            </div>

            {/* Stats Grid */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(4, 1fr)',
                gap: '16px',
                marginBottom: '24px'
            }}>
                <StatCard
                    label="Current CO₂"
                    value={current ? current.predicted_co2.toFixed(1) : '--'}
                    unit="g/km"
                    color="#10b981"
                />
                <StatCard
                    label="Active Vehicles"
                    value={current ? current.vehicle_count.toString() : '--'}
                    unit="vehicles"
                    color="#3b82f6"
                />
                <StatCard
                    label="Avg Traffic Speed"
                    value={current ? current.avg_speed.toString() : '--'}
                    unit="km/h"
                    color="#f59e0b"
                />
                <StatCard
                    label="Total Emissions"
                    value={total > 1000 ? (total / 1000).toFixed(1) + 'k' : total.toFixed(0)}
                    unit="g CO₂"
                    color="#8b5cf6"
                />
            </div>

            {/* Main Chart */}
            <div style={{
                backgroundColor: '#1e293b',
                borderRadius: '12px',
                padding: '24px',
                marginBottom: '24px'
            }}>
                <div style={{ marginBottom: '16px' }}>
                    <h2 style={{ fontSize: '18px', fontWeight: '600', color: '#fff', marginBottom: '4px' }}>
                        Live Emission Trend
                    </h2>
                    <p style={{ fontSize: '14px', color: '#64748b' }}>
                        Real-time CO₂ predictions over time
                    </p>
                </div>
                <ResponsiveContainer width="100%" height={320}>
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorCo2" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="timestamp" stroke="#64748b" style={{ fontSize: '12px' }} />
                        <YAxis stroke="#64748b" style={{ fontSize: '12px' }} />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: '#1e293b',
                                border: '1px solid #334155',
                                borderRadius: '8px'
                            }}
                        />
                        <Area
                            type="monotone"
                            dataKey="predicted_co2"
                            stroke="#10b981"
                            fill="url(#colorCo2)"
                            strokeWidth={2}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            {/* Bottom Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
                {/* City Chart */}
                <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', padding: '24px' }}>
                    <h3 style={{ fontSize: '16px', fontWeight: '600', color: '#fff', marginBottom: '16px' }}>
                        Emissions by City
                    </h3>
                    <ResponsiveContainer width="100%" height={200}>
                        <BarChart data={cityData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey="city" stroke="#64748b" style={{ fontSize: '11px' }} />
                            <YAxis stroke="#64748b" style={{ fontSize: '11px' }} />
                            <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
                            <Bar dataKey="avg" fill="#10b981" radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Recent Events */}
                <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', padding: '24px' }}>
                    <h3 style={{ fontSize: '16px', fontWeight: '600', color: '#fff', marginBottom: '16px' }}>
                        Recent Events
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {data.slice(-5).reverse().map((d, i) => (
                            <div
                                key={i}
                                style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    padding: '12px',
                                    backgroundColor: '#334155',
                                    borderRadius: '8px'
                                }}
                            >
                                <span style={{ color: '#e2e8f0', fontSize: '14px' }}>{d.location}</span>
                                <span style={{ color: '#10b981', fontSize: '14px', fontWeight: '600' }}>
                                    {d.predicted_co2.toFixed(1)} g/km
                                </span>
                            </div>
                        ))}
                        {data.length === 0 && (
                            <p style={{ color: '#64748b', fontSize: '14px', textAlign: 'center', padding: '40px 0' }}>
                                Waiting for data...
                            </p>
                        )}
                    </div>
                </div>

                {/* System Status */}
                <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', padding: '24px' }}>
                    <h3 style={{ fontSize: '16px', fontWeight: '600', color: '#fff', marginBottom: '16px' }}>
                        System Status
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                        <StatusRow name="Kafka Broker" status="Healthy" online={true} />
                        <StatusRow name="ML Inference Engine" status="Active" online={true} />
                        <StatusRow name="PostgreSQL Database" status="Connected" online={true} />
                        <StatusRow name="WebSocket Stream" status={connected ? "Live" : "Offline"} online={connected} />
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ label, value, unit, color }: {
    label: string;
    value: string;
    unit: string;
    color: string;
}) {
    return (
        <div style={{
            backgroundColor: '#1e293b',
            borderRadius: '12px',
            padding: '24px',
            border: `1px solid ${color}40`
        }}>
            <div style={{ color: '#94a3b8', fontSize: '14px', marginBottom: '8px' }}>{label}</div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
                <span style={{ fontSize: '36px', fontWeight: 'bold', color: '#fff' }}>{value}</span>
                <span style={{ fontSize: '14px', color: '#64748b' }}>{unit}</span>
            </div>
        </div>
    );
}

function StatusRow({ name, status, online }: { name: string; status: string; online: boolean }) {
    return (
        <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '12px',
            backgroundColor: '#334155',
            borderRadius: '8px'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <div style={{
                    width: '8px',
                    height: '8px',
                    borderRadius: '50%',
                    backgroundColor: online ? '#10b981' : '#ef4444'
                }}></div>
                <span style={{ color: '#e2e8f0', fontSize: '14px' }}>{name}</span>
            </div>
            <span style={{
                fontSize: '12px',
                fontWeight: '600',
                color: online ? '#10b981' : '#ef4444',
                backgroundColor: online ? '#10b98120' : '#ef444420',
                padding: '4px 8px',
                borderRadius: '4px'
            }}>
                {status}
            </span>
        </div>
    );
}
