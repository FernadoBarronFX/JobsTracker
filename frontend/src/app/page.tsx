"use client";

import { useEffect, useState } from "react";

type Job = {
  id: number;
  company: string;
  title: string;
  status: string;
  modality:string;
  salary:string;
};

export default function Home() {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/jobs")
      .then((res) => res.json())
      .then((data) => setJobs(data));
  }, []);

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">JobTracker</h1>
      <ul className="space-y-2">
        {jobs.map((job) => (
          <li key={job.id} className="border rounded p-3">
            <p className="font-semibold">{job.title}</p>
            <p className="text-sm text-gray-600">
              {job.company} · {job.status} - {job.modality} - ${job.salary}
            </p>
          </li>
        ))}
      </ul>
    </main>
  );
}