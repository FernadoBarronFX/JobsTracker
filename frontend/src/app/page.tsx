"use client";

import { useEffect, useState } from "react";
import JobCard, { type Job, STATUS_STYLES } from "@/components/JobCard";

const API_URL = "http://localhost:8000";


export default function Home() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [company, setCompany] = useState("");
  const [title, setTitle] = useState("");
  const [location, setLocation] = useState("");
  const [url, setUrl] = useState("");
  const [modality, setModality] = useState("");
  const [salary, setSalary] = useState("");

  async function loadJobs() {
    const res = await fetch(`${API_URL}/jobs`);
    const data = await res.json();
    setJobs(data);
  }

  async function handleDelete(id: number) {
    if (!confirm("¿Eliminar esta vacante?")) return;

    const res = await fetch(`${API_URL}/jobs/${id}`, { method: "DELETE" });

    if (res.ok) {
      loadJobs();
    }
  }


  async function handleStatusChange(id: number, status: string) {
    const res = await fetch(`${API_URL}/jobs/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });

    if (res.ok) {
      loadJobs();
    }
  }


  useEffect(() => {
    loadJobs();
  }, []);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    const res = await fetch(`${API_URL}/jobs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        company,
        title,
        location: location || null,
        url: url || null,
        modality: modality || null,
        salary: salary || null,
      }),
    });

    if (res.ok) {
      setCompany("");
      setTitle("");
      setLocation("");
      setUrl("");
      setModality("");
      setSalary("");
      loadJobs();
    }
  }

  return (
    <main>
      <div className="container">
        <h1 className="title">JobTracker</h1>

        <form onSubmit={handleSubmit} className="form-card">
          <h2 className="section-title form-wide">Nueva vacante</h2>

          <input
            className="field"
            placeholder="Empresa *"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            required
          />
          <input
            className="field"
            placeholder="Puesto *"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
          <input
            className="field"
            placeholder="Ubicación"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
          <select
            className="field"
            value={modality}
            onChange={(e) => setModality(e.target.value)}
          >
            <option value="">Modalidad</option>
            <option value="Remoto">Remoto</option>
            <option value="Híbrido">Híbrido</option>
            <option value="Presencial">Presencial</option>
          </select>
          <input
            className="field"
            placeholder="Salario"
            value={salary}
            onChange={(e) => setSalary(e.target.value)}
          />
          <input
            className="field"
            placeholder="Enlace de la vacante"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          <button type="submit" className="btn-primary form-wide">
            Agregar vacante
          </button>
        </form>

        <h2 className="section-title">Mis vacantes ({jobs.length})</h2>

        <div className="board form-card">
          {Object.entries(STATUS_STYLES).map(([status, { label, className }]) => {
            const columnJobs = jobs.filter((job) => job.status === status);

            return (
              <section key={status}
                className="column"
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {
                  const id = Number(e.dataTransfer.getData("text/plain"));
                  handleStatusChange(id, status)
                }}
              >
                <h3 className="column-title">
                  <span className={`badge ${className}`}>{label}</span>
                  <span className="column-count">{columnJobs.length}</span>
                </h3>

                <ul className="column-list">
                  {columnJobs.map((job) => (
                    <JobCard
                      key={job.id}
                      job={job}
                      onDelete={handleDelete}
                      onStatusChange={handleStatusChange}
                    />
                  ))}
                </ul>
              </section>
            );
          })}
        </div>
      </div>
    </main>
  );
}