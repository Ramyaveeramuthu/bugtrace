import { useState } from "react";
import Login from "./Login";
import BugList from "./BugList";
import { isLoggedIn, logout } from "./api/client";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());

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
      <BugList />
    </div>
  );
}