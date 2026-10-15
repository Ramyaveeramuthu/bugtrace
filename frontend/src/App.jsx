import { useCallback, useEffect, useState } from "react";
import Login from "./Login";
import BugList from "./BugList";
import BugForm from "./BugForm";
import { isLoggedIn, logout, getBugs } from "./api/client";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());
  const [bugs, setBugs] = useState([]);
  const [error, setError] = useState("");

  const loadBugs = useCallback(() => {
    setError("");
    getBugs()
      .then((data) => setBugs(data.results || data))
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    if (loggedIn) loadBugs();
  }, [loggedIn, loadBugs]);

  function handleLogout() {
    logout();
    setLoggedIn(false);
  }

  if (!loggedIn) {
    return <Login onLogin={() => setLoggedIn(true)} />;
  }

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", textAlign: "left" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>BugTrace</h1>
        <button onClick={handleLogout}>Logout</button>
      </div>
      <BugForm onCreated={loadBugs} />
      <BugList bugs={bugs} error={error} />
    </div>
  );
}