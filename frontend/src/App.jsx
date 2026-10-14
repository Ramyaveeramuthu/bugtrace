import { useState } from "react";
import Login from "./Login";
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
    <div style={{ maxWidth: 600, margin: "80px auto", textAlign: "left" }}>
      <h1>BugTrace</h1>
      <p>Login success! 🎉</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}