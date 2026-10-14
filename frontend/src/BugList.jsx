import { useEffect, useState } from "react";
import { getBugs } from "./api/client";

export default function BugList() {
  const [bugs, setBugs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getBugs()
      .then((data) => setBugs(data.results || data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <h2>Bugs</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Status</th>
            <th>Severity</th>
            <th>Assignee</th>
          </tr>
        </thead>
        <tbody>
          {bugs.map((bug) => (
            <tr key={bug.id}>
              <td>{bug.id}</td>
              <td>{bug.title}</td>
              <td>{bug.status}</td>
              <td>{bug.severity}</td>
              <td>{bug.assignee ? bug.assignee.username : "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}