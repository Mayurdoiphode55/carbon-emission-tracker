"use client";

import { useState } from 'react';

export default function PredictionsPage() {
    const [form, setForm] = useState({
        vehicle_count: 250,
        speed: 45,
        weather: 'Clear',
    });
    const [result, setResult] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const params = new URLSearchParams({
                vehicle_count: form.vehicle_count.toString(),
                speed: form.speed.toString(),
                weather: form.weather
            });
            const res = await fetch(`http://localhost:8000/ml/predict?${params}`);
            const data = await res.json();
            setResult(data.predicted_co2_g_per_km);
        } catch (e) {
            console.error(e);
        }
        setLoading(false);
    };

    return (
        <div style={{ padding: '32px', minHeight: '100vh', backgroundColor: '#0f172a' }}>
            <div style={{ marginBottom: '24px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#fff', marginBottom: '8px' }}>
                    ML Predictions
                </h1>
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                    Test the machine learning model with custom parameters
                </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: '24px' }}>
                {/* Input Form */}
                <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', padding: '28px' }}>
                    <h2 style={{ color: '#fff', fontSize: '18px', fontWeight: '600', marginBottom: '24px' }}>
                        Input Parameters
                    </h2>
                    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        <div>
                            <label style={{ color: '#94a3b8', fontSize: '14px', display: 'block', marginBottom: '12px' }}>
                                Vehicle Count: <span style={{ color: '#fff', fontWeight: '600' }}>{form.vehicle_count}</span>
                            </label>
                            <input
                                type="range"
                                min="10"
                                max="500"
                                value={form.vehicle_count}
                                onChange={(e) => setForm({...form, vehicle_count: parseInt(e.target.value)})}
                                style={{ width: '100%', height: '6px', accentColor: '#10b981' }}
                            />
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '6px' }}>
                                <span style={{ fontSize: '12px', color: '#64748b' }}>10</span>
                                <span style={{ fontSize: '12px', color: '#64748b' }}>500</span>
                            </div>
                        </div>

                        <div>
                            <label style={{ color: '#94a3b8', fontSize: '14px', display: 'block', marginBottom: '12px' }}>
                                Average Speed: <span style={{ color: '#fff', fontWeight: '600' }}>{form.speed} km/h</span>
                            </label>
                            <input
                                type="range"
                                min="5"
                                max="120"
                                value={form.speed}
                                onChange={(e) => setForm({...form, speed: parseInt(e.target.value)})}
                                style={{ width: '100%', height: '6px', accentColor: '#3b82f6' }}
                            />
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '6px' }}>
                                <span style={{ fontSize: '12px', color: '#64748b' }}>5 km/h</span>
                                <span style={{ fontSize: '12px', color: '#64748b' }}>120 km/h</span>
                            </div>
                        </div>

                        <div>
                            <label style={{ color: '#94a3b8', fontSize: '14px', display: 'block', marginBottom: '12px' }}>
                                Weather Condition
                            </label>
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '8px' }}>
                                {['Clear', 'Cloudy', 'Rainy', 'Foggy'].map((w) => (
                                    <button
                                        key={w}
                                        type="button"
                                        onClick={() => setForm({...form, weather: w})}
                                        style={{
                                            padding: '12px',
                                            borderRadius: '8px',
                                            border: 'none',
                                            fontSize: '14px',
                                            fontWeight: '500',
                                            cursor: 'pointer',
                                            backgroundColor: form.weather === w ? '#10b981' : '#334155',
                                            color: form.weather === w ? '#fff' : '#94a3b8',
                                            transition: 'all 0.2s'
                                        }}
                                    >
                                        {w}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            style={{
                                marginTop: '8px',
                                padding: '14px',
                                backgroundColor: '#10b981',
                                color: '#fff',
                                border: 'none',
                                borderRadius: '8px',
                                fontSize: '16px',
                                fontWeight: '600',
                                cursor: loading ? 'not-allowed' : 'pointer',
                                opacity: loading ? 0.6 : 1
                            }}
                        >
                            {loading ? 'Predicting...' : 'Get Prediction'}
                        </button>
                    </form>
                </div>

                {/* Result Display */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div style={{ 
                        backgroundColor: '#1e293b', 
                        borderRadius: '12px', 
                        padding: '32px',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        minHeight: '320px'
                    }}>
                        <h3 style={{ color: '#fff', fontSize: '16px', fontWeight: '600', marginBottom: '20px' }}>
                            Predicted CO₂ Emission
                        </h3>
                        {result !== null ? (
                            <>
                                <div style={{ fontSize: '64px', fontWeight: 'bold', color: '#10b981', marginBottom: '8px' }}>
                                    {result.toFixed(1)}
                                </div>
                                <div style={{ fontSize: '18px', color: '#94a3b8', marginBottom: '24px' }}>
                                    g/km CO₂
                                </div>
                                <div style={{ 
                                    padding: '12px 20px', 
                                    borderRadius: '8px',
                                    backgroundColor: result < 150 ? '#10b98120' : result < 250 ? '#f59e0b20' : '#ef444420'
                                }}>
                                    <span style={{ 
                                        fontSize: '14px', 
                                        fontWeight: '500',
                                        color: result < 150 ? '#10b981' : result < 250 ? '#f59e0b' : '#ef4444'
                                    }}>
                                        {result < 150 ? '✓ Low Emission Level' : 
                                         result < 250 ? '⚠ Moderate Emission' : '⚠ High Emission Alert'}
                                    </span>
                                </div>
                            </>
                        ) : (
                            <p style={{ color: '#64748b', fontSize: '14px', textAlign: 'center' }}>
                                Configure parameters and click predict to see results
                            </p>
                        )}
                    </div>

                    {/* Model Info */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
                        <InfoCard label="Model Type" value="XGBoost" />
                        <InfoCard label="Latency" value="< 50ms" />
                        <InfoCard label="Accuracy" value="R² = 0.92" />
                        <InfoCard label="Version" value="v1.0" />
                    </div>
                </div>
            </div>
        </div>
    );
}

function InfoCard({ label, value }: { label: string; value: string }) {
    return (
        <div style={{ backgroundColor: '#1e293b', borderRadius: '8px', padding: '16px' }}>
            <div style={{ color: '#64748b', fontSize: '12px', marginBottom: '4px' }}>{label}</div>
            <div style={{ color: '#fff', fontSize: '15px', fontWeight: '600' }}>{value}</div>
        </div>
    );
}
