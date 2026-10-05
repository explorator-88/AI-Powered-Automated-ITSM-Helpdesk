import {
  Ticket,
  CheckCircle,
  AlertTriangle,
  Package,
  Zap,
} from "lucide-react";

const stats = [
  {
    title: "Total Tickets",
    value: "128",
    change: "+12%",
    icon: Ticket,
  },
  {
    title: "Open Tickets",
    value: "37",
    change: "-8%",
    icon: AlertTriangle,
  },
  {
    title: "AI Resolved",
    value: "64",
    change: "+21%",
    icon: CheckCircle,
  },
  {
    title: "Software Requests",
    value: "18",
    change: "+6%",
    icon: Package,
  },
  {
    title: "Automation Success",
    value: "92%",
    change: "+4%",
    icon: Zap,
  },
];

export default function Dashboard() {
  return (
    <div>

      <div className="page-header">
        <div>
          <h1>AI ITSM Command Center</h1>
          <p>
            Intelligent automation across incidents, knowledge,
            self-healing and software provisioning.
          </p>
        </div>
      </div>

      <div className="stats-grid">

        {stats.map(({ title, value, change, icon: Icon }) => (

          <div className="stat-card" key={title}>

            <div className="stat-top">
              <span>{title}</span>
              <Icon size={20} />
            </div>

            <div className="stat-value">
              {value}
            </div>

            <div className="stat-change">
              {change} from previous period
            </div>

          </div>

        ))}

      </div>

      <div className="dashboard-grid">

        <div className="panel">

          <div className="panel-header">
            <h2>Recent Incidents</h2>
            <span>Live</span>
          </div>

          <div className="incident-row">
            <div>
              <strong>INC1007</strong>
              <p>VPN authentication failure</p>
            </div>

            <span className="badge warning">P2</span>

            <span className="badge open">Open</span>
          </div>

          <div className="incident-row">
            <div>
              <strong>INC1006</strong>
              <p>Password expired</p>
            </div>

            <span className="badge high">P2</span>

            <span className="badge resolved">AI Resolved</span>
          </div>

          <div className="incident-row">
            <div>
              <strong>INC1005</strong>
              <p>Outlook synchronization issue</p>
            </div>

            <span className="badge medium">P3</span>

            <span className="badge open">Open</span>
          </div>

        </div>

        <div className="panel">

          <div className="panel-header">
            <h2>Automation Activity</h2>
          </div>

          <div className="activity">
            <span className="activity-dot"></span>
            Password reset completed
          </div>

          <div className="activity">
            <span className="activity-dot"></span>
            VPN status verified
          </div>

          <div className="activity">
            <span className="activity-dot"></span>
            Visual Studio Code provisioning completed
          </div>

          <div className="activity">
            <span className="activity-dot"></span>
            Outlook restart automation executed
          </div>

        </div>

      </div>

    </div>
  );
}