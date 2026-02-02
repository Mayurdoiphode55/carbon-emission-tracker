"use client";

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
    const pathname = usePathname();
    const [isOpen, setIsOpen] = useState(false);
    
    const links = [
        { name: 'Dashboard', path: '/', icon: '📊' },
        { name: 'Analytics', path: '/analytics', icon: '📈' },
        { name: 'Predictions', path: '/predictions', icon: '🤖' },
        { name: 'Settings', path: '/settings', icon: '⚙️' },
    ];

    return (
        <div style={{ 
            position: 'fixed', 
            left: 0, 
            top: 0, 
            height: '100%', 
            width: isOpen ? '240px' : '70px',
            backgroundColor: '#1e293b', 
            borderRight: '1px solid #334155',
            transition: 'width 0.3s ease',
            zIndex: 1000
        }}>
            <div style={{ 
                padding: '20px',
                borderBottom: '1px solid #334155',
                display: 'flex',
                alignItems: 'center',
                gap: '12px'
            }}>
                <div style={{ 
                    width: '36px', 
                    height: '36px', 
                    backgroundColor: '#10b981', 
                    borderRadius: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '18px',
                    fontWeight: 'bold',
                    color: '#fff',
                    flexShrink: 0
                }}>
                    C
                </div>
                {isOpen && (
                    <div>
                        <div style={{ color: '#fff', fontSize: '14px', fontWeight: '600', whiteSpace: 'nowrap' }}>Carbon AI</div>
                        <div style={{ color: '#64748b', fontSize: '11px' }}>Tracker</div>
                    </div>
                )}
            </div>

            <button
                onClick={() => setIsOpen(!isOpen)}
                style={{
                    width: '100%',
                    padding: '10px',
                    backgroundColor: '#334155',
                    border: 'none',
                    color: '#94a3b8',
                    cursor: 'pointer',
                    fontSize: '16px',
                }}
            >
                {isOpen ? '◀' : '▶'}
            </button>
            
            <div style={{ padding: '16px 8px' }}>
                {links.map((link) => (
                    <Link
                        key={link.path}
                        href={link.path}
                        style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '12px',
                            padding: '12px',
                            marginBottom: '8px',
                            borderRadius: '8px',
                            backgroundColor: pathname === link.path ? '#10b981' : 'transparent',
                            color: pathname === link.path ? '#fff' : '#94a3b8',
                            textDecoration: 'none',
                            justifyContent: isOpen ? 'flex-start' : 'center'
                        }}
                    >
                        <span style={{ fontSize: '20px', flexShrink: 0 }}>{link.icon}</span>
                        {isOpen && <span style={{ fontSize: '14px', fontWeight: '500', whiteSpace: 'nowrap' }}>{link.name}</span>}
                    </Link>
                ))}
            </div>
        </div>
    );
}
