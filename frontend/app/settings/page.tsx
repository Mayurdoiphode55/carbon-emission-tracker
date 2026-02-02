"use client";

export default function SettingsPage() {
    return (
        <div style={{ padding: '32px', minHeight: '100vh', backgroundColor: '#0f172a' }}>
            <div style={{ marginBottom: '24px' }}>
                <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#fff', marginBottom: '8px' }}>
                    Settings
                </h1>
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                    System configuration and project information
                </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
                {/* Main Content */}
                <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', padding: '28px' }}>
                    <h2 style={{ color: '#fff', fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>
                        About This Project
                    </h2>
                    <p style={{ color: '#94a3b8', fontSize: '14px', lineHeight: '1.7', marginBottom: '24px' }}>
                        The AI-Powered Carbon Emission Tracker is a real-time system that monitors and predicts 
                        CO₂ emissions from transportation data. It uses machine learning to provide accurate predictions 
                        and helps identify emission patterns across different cities and weather conditions.
                    </p>

                    <h3 style={{ color: '#fff', fontSize: '16px', fontWeight: '600', marginBottom: '12px' }}>
                        Technology Stack
                    </h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '24px' }}>
                        <TechBox title="Frontend" tech="Next.js + React" />
                        <TechBox title="Backend" tech="FastAPI" />
                        <TechBox title="ML Model" tech="XGBoost" />
                        <TechBox title="Streaming" tech="Apache Kafka" />
                        <TechBox title="Database" tech="PostgreSQL" />
                        <TechBox title="Container" tech="Docker Compose" />
                    </div>

                    <h3 style={{ color: '#fff', fontSize: '16px', fontWeight: '600', marginBottom: '12px' }}>
                        Data Pipeline
                    </h3>
                    <div style={{ 
                        backgroundColor: '#334155', 
                        borderRadius: '8px', 
                        padding: '16px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        flexWrap: 'wrap'
                    }}>
                        <PipelineStep label="Traffic Data" />
                        <Arrow />
                        <PipelineStep label="Kafka Stream" />
                        <Arrow />
                        <PipelineStep label="ML Model" />
                        <Arrow />
                        <PipelineStep label="API" />
                        <Arrow />
                        <PipelineStep label="Dashboard" />
                    </div>
                </div>

                {/* Sidebar */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', padding: '20px' }}>
                        <h3 style={{ color: '#fff', fontSize: '14px', fontWeight: '600', marginBottom: '16px' }}>
                            API Endpoints
                        </h3>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                            <Endpoint method="GET" path="/health" color="#10b981" />
                            <Endpoint method="GET" path="/ml/predict" color="#10b981" />
                            <Endpoint method="WS" path="/ws" color="#8b5cf6" />
                        </div>
                    </div>

                    <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', padding: '20px' }}>
                        <h3 style={{ color: '#fff', fontSize: '14px', fontWeight: '600', marginBottom: '16px' }}>
                            Model Information
                        </h3>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13px' }}>
                            <Row label="Type" value="XGBoost Regressor" />
                            <Row label="Training Data" value="10k synthetic samples" />
                            <Row label="Input Features" value="6 parameters" />
                            <Row label="Target Output" value="CO₂ g/km" />
                        </div>
                    </div>

                    <div style={{ backgroundColor: '#1e293b', borderRadius: '12px', padding: '20px' }}>
                        <h3 style={{ color: '#fff', fontSize: '14px', fontWeight: '600', marginBottom: '16px' }}>
                            System Health
                        </h3>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                            <HealthBar label="Kafka Broker" percent={72} />
                            <HealthBar label="ML Service" percent={85} />
                            <HealthBar label="API Server" percent={68} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function TechBox({ title, tech }: { title: string; tech: string }) {
    return (
        <div style={{ backgroundColor: '#334155', borderRadius: '8px', padding: '14px' }}>
            <div style={{ color: '#10b981', fontSize: '11px', fontWeight: '600', marginBottom: '4px' }}>
                {title}
            </div>
            <div style={{ color: '#e2e8f0', fontSize: '13px' }}>{tech}</div>
        </div>
    );
}

function PipelineStep({ label }: { label: string }) {
    return (
        <span style={{ 
            padding: '6px 12px', 
            backgroundColor: '#10b98120',
            color: '#10b981',
            borderRadius: '6px',
            fontSize: '13px',
            fontWeight: '500',
            border: '1px solid #10b98140'
        }}>
            {label}
        </span>
    );
}

function Arrow() {
    return <span style={{ color: '#64748b', fontSize: '18px' }}>→</span>;
}

function Endpoint({ method, path, color }: { method: string; path: string; color: string }) {
    return (
        <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px',
            padding: '8px',
            backgroundColor: '#334155',
            borderRadius: '6px'
        }}>
            <span style={{ 
                fontSize: '11px', 
                fontWeight: '700',
                color: color,
                backgroundColor: `${color}20`,
                padding: '4px 8px',
                borderRadius: '4px'
            }}>
                {method}
            </span>
            <code style={{ color: '#e2e8f0', fontSize: '13px' }}>{path}</code>
        </div>
    );
}

function Row({ label, value }: { label: string; value: string }) {
    return (
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: '#64748b' }}>{label}</span>
            <span style={{ color: '#e2e8f0', fontWeight: '500' }}>{value}</span>
        </div>
    );
}

function HealthBar({ label, percent }: { label: string; percent: number }) {
    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                <span style={{ color: '#94a3b8' }}>{label}</span>
                <span style={{ color: '#10b981', fontWeight: '600' }}>{percent}%</span>
            </div>
            <div style={{ height: '6px', backgroundColor: '#334155', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ 
                    height: '100%', 
                    width: `${percent}%`, 
                    backgroundColor: '#10b981',
                    borderRadius: '3px'
                }}></div>
            </div>
        </div>
    );
}
