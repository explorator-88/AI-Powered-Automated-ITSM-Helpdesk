import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Assistant from "./pages/Assistant";
import Tickets from "./pages/Tickets";
import Knowledge from "./pages/Knowledge";
import Automation from "./pages/Automation";
import Provisioning from "./pages/Provisioning";
import AIAnalysis from "./pages/AIAnalysis";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />

        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/assistant" element={<Assistant />} />
        <Route path="/tickets" element={<Tickets />} />
        <Route path="/knowledge" element={<Knowledge />} />
        <Route path="/automation" element={<Automation />} />
        <Route path="/provisioning" element={<Provisioning />} />
        <Route path="/ai-analysis" element={<AIAnalysis />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;