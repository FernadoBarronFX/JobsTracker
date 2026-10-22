export type Job = {
    id: number;
    company: string;
    title: string;
    status: string;
    location: string | null;
    url: string | null;
    modality: string | null;
    salary: string | null;
};

export const STATUS_STYLES: Record<string, { label: string; className: string }> = {
    saved: { label: "Guardada", className: "badge-saved" },
    applied: { label: "Postulada", className: "badge-applied" },
    interview: { label: "Entrevista", className: "badge-interview" },
    offer: { label: "Oferta", className: "badge-offer" },
    rejected: { label: "Rechazada", className: "badge-rejected" },
};

function normalizeUrl(url: string) {
    return url.startsWith("http") ? url : `https://${url}`;
}

type JobCardProps = {
    job: Job;
    onDelete: (id: number) => void;
    onStatusChange: (id: number, status: string) => void;
};

export default function JobCard({ job, onDelete, onStatusChange }: JobCardProps) {
    const status = STATUS_STYLES[job.status];

    return (
        <li className="job-card"
            draggable
            onDragStart={(e) => {
                e.dataTransfer.setData("text/plain", String(job.id))
            }}
        >
            <div className="job-header">
                <div>
                    <p className="job-title">
                        {job.title}
                    </p>
                    <p className="job-company">{job.company}</p>
                </div>
                <select
                    className={`badge badge-select ${status?.className ?? ""}`}
                    value={job.status}
                    onChange={(e) => onStatusChange(job.id, e.target.value)}
                >
                    {Object.entries(STATUS_STYLES).map(([value, { label }]) => (
                        <option key={value} value={value}>
                            {label}
                        </option>
                    ))}
                </select>
            </div>

            <div className="chips">
                {job.location && <span className="chip">📍 {job.location}</span>}
                {job.modality && <span className="chip">🏢 {job.modality}</span>}
                {job.salary && <span className="chip">💰 {job.salary}</span>}
            </div>

            {job.url && (
                <a
                    href={normalizeUrl(job.url)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="job-link"
                >
                    Ver vacante →
                </a>
            )}

            <button className="btn-danger" onClick={() => onDelete(job.id)}>
                Eliminar
            </button>
        </li>
    );
}