import { BrowserRouter, Routes, Route, NavLink, Navigate } from 'react-router-dom'
import { Brain, LayoutDashboard, Wand2, Cpu, Zap, Menu, X } from 'lucide-react'
import { useState } from 'react'
import LearnPage from './pages/LearnPage'
import OperatePage from './pages/OperatePage'
import CreatePage from './pages/CreatePage'
import LandingPage from './pages/LandingPage'
import './App.css'

const navItems = [
  { to: '/learn', icon: Brain, label: 'LEARN', sub: 'AI Tutor', color: '#6366f1' },
  { to: '/operate', icon: LayoutDashboard, label: 'OPERATE', sub: 'Campus OS', color: '#10b981' },
  { to: '/create', icon: Wand2, label: 'CREATE', sub: 'App Builder', color: '#f59e0b' },
]

function Sidebar({ open, setOpen }) {
  return (
    <>
      {open && <div className="sidebar-overlay" onClick={() => setOpen(false)} />}
      <aside className={`sidebar ${open ? 'open' : ''}`}>
        {/* Logo */}
        <div className="sidebar-logo">
          <div className="logo-icon"><Cpu size={22} /></div>
          <div>
            <div className="logo-name">VIDYA OS</div>
            <div className="logo-sub">AMD Slingshot 2025</div>
          </div>
        </div>

        {/* Status */}
        <div className="sidebar-status">
          <div className="pulse-dot" />
          <span>On-device AI Active</span>
        </div>

        {/* Nav */}
        <nav className="sidebar-nav">
          <div className="nav-section-label">Pillars</div>
          {navItems.map(({ to, icon: Icon, label, sub, color }) => (
            <NavLink key={to} to={to} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              style={({ isActive }) => isActive ? { '--nav-color': color } : {}}>
              <div className="nav-icon"><Icon size={18} /></div>
              <div>
                <div className="nav-label">{label}</div>
                <div className="nav-sub">{sub}</div>
              </div>
            </NavLink>
          ))}
        </nav>

        {/* Hardware Badge */}
        <div className="sidebar-footer">
          <div className="hw-badge">
            <Zap size={14} />
            <div>
              <div className="hw-title">On-Premise Compute</div>
              <div className="hw-sub">AMD Radeon + Ryzen AI</div>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}

function TopBar({ setOpen }) {
  return (
    <header className="topbar">
      <button className="topbar-menu btn btn-ghost" onClick={() => setOpen(o => !o)}>
        <Menu size={20} />
      </button>
      <div className="topbar-title gradient-text">VIDYA OS</div>
      <div className="topbar-right">
        <span className="badge badge-success">● Live</span>
      </div>
    </header>
  )
}

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
        <div className="app-main">
          <TopBar setOpen={setSidebarOpen} />
          <main className="app-content">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/learn" element={<LearnPage />} />
              <Route path="/operate" element={<OperatePage />} />
              <Route path="/create" element={<CreatePage />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}
