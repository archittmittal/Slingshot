import { useState, useEffect, useRef } from 'react'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { Zap, Users, Wind, MapPin, AlertTriangle, CheckCircle, Info, RefreshCw } from 'lucide-react'
import './OperatePage.css'

const API = 'http://localhost:8000'

const BUILDING_COLORS = ['#6366f1', '#10b981', '#f59e0b', '#3b82f6', '#ec4899', '#8b5cf6', '#14b8a6', '#f97316']

function AlertBadge({ severity }) {
    const map = { critical: 'badge-danger', warning: 'badge-warning', info: 'badge-primary' }
    return <span className={`badge ${map[severity] || 'badge-primary'}`}>{severity}</span>
}

function SeverityIcon({ severity }) {
    if (severity === 'critical') return <AlertTriangle size={16} color="var(--danger)" />
    if (severity === 'warning') return <AlertTriangle size={16} color="var(--warning)" />
    return <Info size={16} color="var(--info)" />
}

const CustomTooltip = ({ active, payload, label }) => {
    if (!active || !payload?.length) return null
    return (
        <div className="chart-tooltip">
            <div className="ct-label">{label}</div>
            {payload.map((p, i) => (
                <div key={i} className="ct-row" style={{ color: p.color }}>
                    <span>{p.name}:</span> <strong>{p.value}</strong>
                </div>
            ))}
        </div>
    )
}

export default function OperatePage() {
    const [metrics, setMetrics] = useState(null)
    const [history, setHistory] = useState([])
    const [loading, setLoading] = useState(true)
    const [lastUpdate, setLastUpdate] = useState(null)
    const wsRef = useRef(null)

    useEffect(() => {
        // Load history once
        fetch(`${API}/api/operate/history`).then(r => r.json()).then(d => setHistory(d.history || []))

        // Initial metrics
        fetchMetrics()

        // WebSocket for live updates
        const ws = new WebSocket('ws://localhost:8000/ws/campus')
        ws.onmessage = e => {
            const data = JSON.parse(e.data)
            setMetrics(data)
            setLastUpdate(new Date().toLocaleTimeString())
            setLoading(false)
        }
        ws.onerror = () => fetchMetrics()
        wsRef.current = ws
        return () => ws.close()
    }, [])

    async function fetchMetrics() {
        try {
            const r = await fetch(`${API}/api/operate/metrics`)
            const d = await r.json()
            setMetrics(d)
            setLastUpdate(new Date().toLocaleTimeString())
            setLoading(false)
        } catch (e) {
            setLoading(false)
        }
    }

    if (loading) return (
        <div className="operate-loading">
            <div className="spinner" style={{ width: 40, height: 40 }} />
            <p>Connecting to campus sensors...</p>
        </div>
    )

    const kpis = metrics?.kpis || {}
    const buildings = metrics?.buildings || []
    const alerts = metrics?.alerts || []
    const maxOcc = Math.max(...buildings.map(b => b.occupancy), 1)

    return (
        <div className="operate-page fade-in">
            <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                    <h1><span className="gradient-text" style={{ backgroundImage: 'linear-gradient(135deg,#10b981,#3b82f6)' }}>OPERATE</span> — Campus OS</h1>
                    <p>Real-time campus intelligence • Updated {lastUpdate || '—'}</p>
                </div>
                <button className="btn btn-ghost" onClick={fetchMetrics}><RefreshCw size={14} /> Refresh</button>
            </div>

            {/* KPI Cards */}
            <div className="kpi-grid">
                <div className="kpi-card">
                    <div className="kpi-icon" style={{ background: 'rgba(99,102,241,0.1)', color: 'var(--primary)' }}>
                        <Users size={20} />
                    </div>
                    <div className="kpi-label">Total Footfall</div>
                    <div className="kpi-value" style={{ color: 'var(--primary-light)' }}>{kpis.total_footfall?.toLocaleString()}</div>
                    <div className="kpi-change kpi-up">↑ Live counting</div>
                </div>
                <div className="kpi-card">
                    <div className="kpi-icon" style={{ background: 'rgba(245,158,11,0.1)', color: 'var(--warning)' }}>
                        <Zap size={20} />
                    </div>
                    <div className="kpi-label">Energy (kWh)</div>
                    <div className="kpi-value" style={{ color: 'var(--accent)' }}>{kpis.total_energy_kwh}</div>
                    <div className={`kpi-change ${kpis.total_energy_kwh > 450 ? 'kpi-down' : 'kpi-up'}`}>
                        {kpis.total_energy_kwh > 450 ? '↑ Above average' : '● Normal range'}
                    </div>
                </div>
                <div className="kpi-card">
                    <div className="kpi-icon" style={{ background: 'rgba(16,185,129,0.1)', color: 'var(--success)' }}>
                        <MapPin size={20} />
                    </div>
                    <div className="kpi-label">Active Spaces</div>
                    <div className="kpi-value" style={{ color: 'var(--success)' }}>{kpis.active_spaces} / 8</div>
                    <div className="kpi-change kpi-up">↑ {Math.round(kpis.active_spaces / 8 * 100)}% utilised</div>
                </div>
                <div className="kpi-card">
                    <div className="kpi-icon" style={{ background: 'rgba(59,130,246,0.1)', color: 'var(--info)' }}>
                        <Wind size={20} />
                    </div>
                    <div className="kpi-label">Air Quality (AQI)</div>
                    <div className="kpi-value" style={{ color: kpis.air_quality_aqi < 50 ? 'var(--success)' : kpis.air_quality_aqi < 100 ? 'var(--accent)' : 'var(--danger)' }}>
                        {kpis.air_quality_aqi}
                    </div>
                    <div className={`kpi-change ${kpis.air_quality_aqi < 50 ? 'kpi-up' : 'kpi-down'}`}>
                        {kpis.air_quality_aqi < 50 ? '● Good' : kpis.air_quality_aqi < 100 ? '● Moderate' : '● Unhealthy'}
                    </div>
                </div>
            </div>

            {/* Charts Row */}
            <div className="two-col" style={{ marginBottom: 20 }}>
                <div className="card">
                    <div className="card-title"><Zap size={14} /> 24-Hour Energy (kWh)</div>
                    <ResponsiveContainer width="100%" height={200}>
                        <AreaChart data={history} margin={{ top: 5, right: 5, bottom: 0, left: -20 }}>
                            <defs>
                                <linearGradient id="energyGrad" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis dataKey="hour" tick={{ fill: '#5a5a7a', fontSize: 10 }} tickLine={false} />
                            <YAxis tick={{ fill: '#5a5a7a', fontSize: 10 }} axisLine={false} />
                            <Tooltip content={<CustomTooltip />} />
                            <Area type="monotone" dataKey="energy" name="Energy kWh" stroke="#f59e0b" fill="url(#energyGrad)" strokeWidth={2} dot={false} />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>

                <div className="card">
                    <div className="card-title"><Users size={14} /> 24-Hour Footfall</div>
                    <ResponsiveContainer width="100%" height={200}>
                        <AreaChart data={history} margin={{ top: 5, right: 5, bottom: 0, left: -20 }}>
                            <defs>
                                <linearGradient id="footGrad" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis dataKey="hour" tick={{ fill: '#5a5a7a', fontSize: 10 }} tickLine={false} />
                            <YAxis tick={{ fill: '#5a5a7a', fontSize: 10 }} axisLine={false} />
                            <Tooltip content={<CustomTooltip />} />
                            <Area type="monotone" dataKey="footfall" name="Footfall" stroke="#6366f1" fill="url(#footGrad)" strokeWidth={2} dot={false} />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* Buildings + Alerts */}
            <div className="two-col">
                {/* Space Utilisation */}
                <div className="card">
                    <div className="card-title"><MapPin size={14} /> Space Utilisation</div>
                    <div className="buildings-list">
                        {buildings.map((b, i) => (
                            <div key={b.id} className="building-row">
                                <div className="building-name">{b.name}</div>
                                <div className="building-bar-wrap">
                                    <div className="building-bar" style={{
                                        width: `${(b.occupancy / maxOcc) * 100}%`,
                                        background: BUILDING_COLORS[i % BUILDING_COLORS.length]
                                    }} />
                                </div>
                                <div className="building-pct">{b.occupancy}%</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Alerts */}
                <div className="card">
                    <div className="card-title">
                        <AlertTriangle size={14} />
                        AI Alerts
                        {alerts.length > 0 && <span className="badge badge-warning" style={{ marginLeft: 'auto' }}>{alerts.length}</span>}
                    </div>
                    {alerts.length === 0
                        ? <div className="no-alerts"><CheckCircle size={32} color="var(--success)" /><p>All systems normal</p></div>
                        : <div className="alerts-list">
                            {alerts.map((a, i) => (
                                <div key={i} className={`alert-item alert-${a.severity}`}>
                                    <div className="alert-header">
                                        <SeverityIcon severity={a.severity} />
                                        <span className="alert-loc">{a.location}</span>
                                        <AlertBadge severity={a.severity} />
                                        <span className="alert-time">{a.time}</span>
                                    </div>
                                    <div className="alert-msg">{a.message}</div>
                                </div>
                            ))}
                        </div>
                    }
                </div>
            </div>
        </div>
    )
}
