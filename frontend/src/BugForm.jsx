import { useState } from "react";
import { createBug } from "./api/client";

export default function BugForm({ onCreated }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState("medium");
  const [project, setProject] = useState(1);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await createBug({
        project: Number(project),
        title,
        description,
        severity,
      });
      setTitle("");
      setDescription("");
      setSeverity("medium");
      onCreated();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      style={{ marginBottom: 24, padding: 16, background: "white", border: "1px solid #ccc" }}
    >
      <h2>Report a Bug</h2>
      <input
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
        style={{ display: "block", width: "100%", marginBottom: 12, padding: 8, boxSizing: "border-box" }}
      />
      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
        rows={3}
        style={{ display: "block", width: "100%", marginBottom: 12, padding: 8, boxSizing: "border-box" }}
      />
      <select
        value={severity}
        onChange={(e) => setSeverity(e.target.value)}
        style={{ marginRight: 12, padding: 8 }}
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
        <option value="critical">Critical</option>
      </select>
      <input
        type="number"
        value={project}
        onChange={(e) => setProject(e.target.value)}
        title="Project ID"
        style={{ width: 60, marginRight: 12, padding: 8 }}
      />
      <button type="submit" style={{ padding: "8px 16px" }}>
        Create
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}