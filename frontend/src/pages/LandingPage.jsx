import { Link } from 'react-router-dom'
import { Brain, LayoutDashboard, Wand2, Cpu, ArrowRight, Shield, Globe, Zap } from 'lucide-react'
import './LandingPage.css'

const pillars = [
    {
        to: '/learn',
        icon: Brain,
        label: 'LEARN',
        title: 'AI Tutor',
        desc: 'Multilingual concept coaching, step-by-step explanations, spaced repetition quizzes, and voice input — all running on-device.',
        color: '#6366f1',
        tags: ['Hindi', 'Tamil', 'Bengali', 'Voice', 'Quiz'],
    },
    {
        to: '/operate',
        icon: LayoutDashboard,
        label: 'OPERATE',
        title: 'Campus OS',
        desc: 'Real-time campus intelligence: energy, footfall, air quality, space utilisation, and AI-generated alerts with remediation guidance.',
        color: '#10b981',
        tags: ['Live Data', 'IoT', 'Alerts', 'Analytics', 'Digital Twin'],
    },
    {
        to: '/create',
        icon: Wand2,
        label: 'CREATE',
        title: 'App Builder',
        desc: 'Non-CS students can build and deploy AI-powered chatbots for fests, clubs, and departments in minutes — zero code required.',
        color: '#f59e0b',
        tags: ['No-Code', 'Templates', 'Publish', 'AI Powered', 'Deploy'],
    },
]

const stats = [
    { value: '100%', label: 'On-Device', sub: 'No cloud, no API fees' },
    { value: '4+', label: 'Languages', sub: 'Indian language support' },
    { value: '3', label: 'Pillars', sub: 'Learn · Operate · Create' },
    { value: '0', label: 'Data Leaks', sub: 'Privacy by design' },
]

export default function LandingPage() {
    return (
        <div className="landing">
            {/* Orbs */}
            <div className="orb" style={{ width: 400, height: 400, background: 'rgba(99,102,241,0.15)', top: -100, left: -100 }} />
            <div className="orb" style={{ width: 300, height: 300, background: 'rgba(16,185,129,0.1)', top: 200, right: -80 }} />
            <div className="orb" style={{ width: 250, height: 250, background: 'rgba(245,158,11,0.1)', bottom: 0, left: '40%' }} />

            {/* Hero */}
            <section className="hero">
                <div className="hero-badge">
                    <Cpu size={14} /> Powered by AMD Ryzen AI + Radeon GPU
                </div>
                <h1 className="hero-title">
                    The OS Every Indian<br />
                    <span className="gradient-text">Campus Deserves</span>
                </h1>
                <p className="hero-sub">
                    VIDYA OS is a sovereign, on-device AI intelligence platform for colleges —<br />
                    private, multilingual, and running entirely on AMD hardware. No cloud. No cost per query.
                </p>
                <div className="hero-actions">
                    <Link to="/learn" className="btn btn-primary" style={{ fontSize: 15, padding: '12px 28px' }}>
                        Start Learning <ArrowRight size={16} />
                    </Link>
                    <Link to="/operate" className="btn btn-ghost" style={{ fontSize: 15, padding: '12px 28px' }}>
                        View Campus Dashboard
                    </Link>
                </div>
            </section>

            {/* Stats */}
            <div className="stats-row">
                {stats.map((s, i) => (
                    <div key={i} className="stat-card glass">
                        <div className="stat-value gradient-text">{s.value}</div>
                        <div className="stat-label">{s.label}</div>
                        <div className="stat-sub">{s.sub}</div>
                    </div>
                ))}
            </div>

            {/* Pillars */}
            <section className="pillars-section">
                <div className="section-title">Three Superpowers</div>
                <div className="pillars-grid">
                    {pillars.map(({ to, icon: Icon, label, title, desc, color, tags }) => (
                        <Link key={to} to={to} className="pillar-card glass glass-hover" style={{ '--p-color': color }}>
                            <div className="pillar-icon-wrap">
                                <Icon size={28} color={color} />
                            </div>
                            <div className="pillar-badge">{label}</div>
                            <h3 className="pillar-title">{title}</h3>
                            <p className="pillar-desc">{desc}</p>
                            <div className="pillar-tags">
                                {tags.map(t => <span key={t} className="ptag">{t}</span>)}
                            </div>
                            <div className="pillar-cta">Explore {label} <ArrowRight size={14} /></div>
                        </Link>
                    ))}
                </div>
            </section>

            {/* Why AMD */}
            <section className="amd-section glass">
                <div className="amd-left">
                    <div className="section-title">Built for AMD Hardware</div>
                    <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7 }}>
                        VIDYA OS is architected to run entirely on-premise using AMD's AI stack.
                        Every inference call stays on campus — eliminating cloud costs, latency, and data exposure.
                    </p>
                    <div className="amd-features">
                        {[
                            { icon: Cpu, label: 'AMD Radeon GPU', sub: 'LLM inference via ROCm' },
                            { icon: Zap, label: 'Ryzen AI NPU', sub: 'Always-on voice pipeline' },
                            { icon: Shield, label: 'Zero Cloud', sub: 'All data stays on campus' },
                            { icon: Globe, label: 'CUDA Compatible', sub: 'Dev on NVIDIA, deploy on AMD' },
                        ].map(({ icon: I, label, sub }) => (
                            <div key={label} className="amd-feat">
                                <div className="amd-feat-icon"><I size={16} /></div>
                                <div><div className="amd-feat-label">{label}</div><div className="amd-feat-sub">{sub}</div></div>
                            </div>
                        ))}
                    </div>
                </div>
                <div className="amd-right">
                    <div className="arch-diagram">
                        {['React PWA + Voice UI', 'FastAPI + LangGraph Agents', 'Llama 3.2 · Whisper · Qdrant', 'AMD Radeon (ROCm) + Ryzen AI NPU'].map((l, i) => (
                            <div key={i} className="arch-layer" style={{ opacity: 1 - i * 0.08, background: `rgba(99,102,241,${0.08 + i * 0.04})` }}>
                                {l}
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    )
}
