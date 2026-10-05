import { NavLink, Outlet } from "react-router-dom";
import {
  LayoutDashboard,
  Bot,
  Ticket,
  BookOpen,
  Zap,
  Package,
  Brain,
} from "lucide-react";

const navigation = [
  { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { path: "/assistant", label: "AI Assistant", icon: Bot },
  { path: "/tickets", label: "Tickets", icon: Ticket },
  { path: "/knowledge", label: "Knowledge Base", icon: BookOpen },
  { path: "/automation", label: "Automation", icon: Zap },
  { path: "/provisioning", label: "Provisioning", icon: Package },
  { path: "/ai-analysis", label: "AI Analysis", icon: Brain },
];

export default function Layout() {
  return (
    <div className="app-shell">

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">AI</div>
          <div>
            <h2>AI ITSM</h2>
            <span>Helpdesk Command Center</span>
          </div>
        </div>

        <nav>
          {navigation.map(({ path, label, icon: Icon }) => (
            <NavLink
              key={path}
              to={path}
              className={({ isActive }) =>
                isActive ? "nav-item active" : "nav-item"
              }
            >
              <Icon size={18} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <strong>Enterprise IT Service Management</strong>
          </div>

          <div className="user-area">
            <span className="status-dot"></span>
            IT Environment Online
          </div>
        </header>

        <section className="page-content">
          <Outlet />
        </section>

      </main>

    </div>
  );
}