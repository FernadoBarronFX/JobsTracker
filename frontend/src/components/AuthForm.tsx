"use client";

import { useState } from "react";
import { API_URL, setToken } from "@/lib/api";

type Props = { onLogin: () => void };

export default function AuthForm({ onLogin }: Props) {
    const [mode, setMode] = useState<"login" | "register">("login");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            if (mode === "register") {
                const res = await fetch(`${API_URL}/auth/register`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password }),
                });
                if (res.status === 409) {
                    setError("Ese correo ya está registrado");
                    return;
                }
                if (!res.ok) {
                    setError("Revisa el correo y que la contraseña tenga al menos 8 caracteres");
                    return;
                }
            }

            // El login va como formulario (no JSON) y el campo se llama "username"
            const res = await fetch(`${API_URL}/auth/login`, {
                method: "POST",
                body: new URLSearchParams({ username: email, password }),
            });
            if (!res.ok) {
                setError("Correo o contraseña incorrectos");
                return;
            }

            const data = await res.json();
            setToken(data.access_token);
            onLogin();
        } catch {
            setError("No se pudo conectar con el servidor");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="auth-wrap">
            <form onSubmit={handleSubmit} className="auth-card">
                <h1 className="title">JobTracker</h1>
                <h2 className="section-title">
                    {mode === "login" ? "Iniciar sesión" : "Crear cuenta"}
                </h2>

                <input
                    className="field"
                    type="email"
                    placeholder="Correo"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    className="field"
                    type="password"
                    placeholder="Contraseña (mínimo 8 caracteres)"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                {error && <p className="auth-error">{error}</p>}

                <button type="submit" className="btn-primary" disabled={loading}>
                    {loading ? "Un momento..." : mode === "login" ? "Entrar" : "Registrarme"}
                </button>

                <button
                    type="button"
                    className="auth-switch"
                    onClick={() => {
                        setMode(mode === "login" ? "register" : "login");
                        setError("");
                    }}
                >
                    {mode === "login"
                        ? "¿No tienes cuenta? Regístrate"
                        : "¿Ya tienes cuenta? Inicia sesión"}
                </button>
            </form>
        </div>
    );
}