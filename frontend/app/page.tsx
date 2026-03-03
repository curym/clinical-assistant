"use client";

import { useState, useMemo } from "react";
import {
  StructuredComposer,
  ComposedClinicalInput,
} from "@/components/StructuredComposer";
import { ClinicalCard } from "@/components/ClinicalCard";

/* =========================
   TIPOS
========================= */

type ClinicalRisk = {
  level: "alto" | "moderado" | "baixo";
  color: "red" | "yellow" | "green";
  label: string;
};

type ClinicalResponse = {
  syndrome: string;
  questions_needed: string[];
  red_flags: string[];
  recommended_tests: string[];
  educational_management: string[];
  disclaimer: string;
  prompt_version?: string;
  clinical_risk?: ClinicalRisk; // ⬅️ opcional
};

/* =========================
   RISCO FRONTEND (FALLBACK)
========================= */

function computeFrontendRisk(result: ClinicalResponse): ClinicalRisk {
  const normalizedSyndrome = result.syndrome
    ?.toLowerCase()
    ?.trim()
    ?.replace(/\s+/g, "_");

  const highRiskSyndromes = [
    "dor_toracica",
    "dispneia",
    "sepse",
    "avc",
    "hemorragia",
    "cauda_equina",
  ];

  if (highRiskSyndromes.includes(normalizedSyndrome)) {
    return {
      level: "alto",
      color: "red",
      label: "ALTO RISCO",
    };
  }

  if (normalizedSyndrome && normalizedSyndrome !== "indefinido") {
    return {
      level: "moderado",
      color: "yellow",
      label: "RISCO MODERADO",
    };
  }

  return {
    level: "baixo",
    color: "green",
    label: "BAIXO RISCO",
  };
}



/* =========================
   PAGE
========================= */

export default function Page() {
  const [composed, setComposed] =
    useState<ComposedClinicalInput | null>(null);
  const [result, setResult] = useState<ClinicalResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!composed) return;

    setLoading(true);
    setResult(null);

    const payload = {
      doctor_id: "marcelo",
      message: composed.freeText,
      context: composed.context,
      input_mode: "structured",
    };

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    setResult(data);
    setLoading(false);
  }

  /* =========================
     RISCO FINAL (BACK + FRONT)
  ========================= */

  const risk: ClinicalRisk | null = useMemo(() => {
    if (!result) return null;
    return result.clinical_risk ?? computeFrontendRisk(result);
  }, [result]);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-bold">Clinical Assistant</h1>

      <StructuredComposer onChangeComposed={setComposed} />

      <button
        onClick={send}
        disabled={loading || !composed?.freeText}
        className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {loading ? "Analisando..." : "Enviar"}
      </button>

      {result && risk && (
        <div className="space-y-4">
          {/* ===== NÍVEL DE RISCO ===== */}
          <div
            className={`rounded p-3 font-semibold text-center ${
              risk.color === "red"
                ? "bg-red-600 text-red-100"
                : risk.color === "yellow"
                ? "bg-yellow-400 text-yellow-900"
                : "bg-green-600 text-green-100"
            }`}
          >
            NÍVEL DE RISCO CLÍNICO: {risk.label}
          </div>

          <ClinicalCard title={`Síndrome: ${result.syndrome}`} highlight="info">
            <p className="text-sm">
              Análise sindrômica inicial baseada na apresentação clínica.
            </p>
          </ClinicalCard>

          <ClinicalCard title="Perguntas essenciais">
            <ul className="list-disc pl-5">
              {result.questions_needed.map((q, i) => (
                <li key={i}>{q}</li>
              ))}
            </ul>
          </ClinicalCard>

          <ClinicalCard title="Red Flags" highlight="danger">
            <ul className="list-disc pl-5 text-red-700">
              {result.red_flags.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          </ClinicalCard>

          <ClinicalCard title="Exames sugeridos">
            <ul className="list-disc pl-5">
              {result.recommended_tests.map((e, i) => (
                <li key={i}>{e}</li>
              ))}
            </ul>
          </ClinicalCard>

          <ClinicalCard title="Conduta educacional">
            <ul className="list-disc pl-5">
              {result.educational_management.map((m, i) => (
                <li key={i}>{m}</li>
              ))}
            </ul>
          </ClinicalCard>

          <p className="text-xs text-gray-500">{result.disclaimer}</p>
        </div>
      )}
    </div>
  );
}
