"use client";

import { useEffect, useMemo, useState } from "react";

export type ComposedClinicalInput = {
  freeText: string;
  context: {
    chief_complaint?: string;
    duration?: string;
    associated_symptoms?: string;
    comorbidities?: string;
  };
};

interface Props {
  onChangeComposed?: (data: ComposedClinicalInput) => void;
}

export function StructuredComposer({ onChangeComposed }: Props) {
  const [chiefComplaint, setChiefComplaint] = useState("");
  const [duration, setDuration] = useState("");
  const [associated, setAssociated] = useState("");
  const [comorbidities, setComorbidities] = useState("");
  const [extraNotes, setExtraNotes] = useState("");

  /**
   * 🔹 Texto clínico AUTOMATICAMENTE COMPOSTO
   * Nunca fica vazio se houver dados estruturados
   */
  const freeText = useMemo(() => {
    const parts: string[] = [];

    if (chiefComplaint) {
      parts.push(`Queixa principal: ${chiefComplaint}.`);
    }

    if (duration) {
      parts.push(`Duração dos sintomas: ${duration}.`);
    }

    if (associated) {
      parts.push(`Sintomas associados: ${associated}.`);
    }

    if (comorbidities) {
      parts.push(`Comorbidades relevantes: ${comorbidities}.`);
    }

    if (extraNotes) {
      parts.push(`Observações adicionais: ${extraNotes}.`);
    }

    return parts.join(" ");
  }, [chiefComplaint, duration, associated, comorbidities, extraNotes]);

  const composed = useMemo<ComposedClinicalInput>(() => {
    return {
      freeText,
      context: {
        chief_complaint: chiefComplaint || undefined,
        duration: duration || undefined,
        associated_symptoms: associated || undefined,
        comorbidities: comorbidities || undefined,
      },
    };
  }, [freeText, chiefComplaint, duration, associated, comorbidities]);

  /**
   * ✅ Side effect correto: notifica o Page
   */
  useEffect(() => {
    if (onChangeComposed) {
      onChangeComposed(composed);
    }
  }, [composed, onChangeComposed]);

  return (
    <div className="space-y-3 border rounded p-4 bg-gray-50">
      <input
        className="w-full border p-2 rounded"
        placeholder="Queixa principal"
        value={chiefComplaint}
        onChange={(e) => setChiefComplaint(e.target.value)}
      />

      <input
        className="w-full border p-2 rounded"
        placeholder="Duração dos sintomas"
        value={duration}
        onChange={(e) => setDuration(e.target.value)}
      />

      <input
        className="w-full border p-2 rounded"
        placeholder="Sintomas associados"
        value={associated}
        onChange={(e) => setAssociated(e.target.value)}
      />

      <input
        className="w-full border p-2 rounded"
        placeholder="Comorbidades"
        value={comorbidities}
        onChange={(e) => setComorbidities(e.target.value)}
      />

      <textarea
        className="w-full border p-2 rounded"
        rows={3}
        placeholder="Observações adicionais (opcional)"
        value={extraNotes}
        onChange={(e) => setExtraNotes(e.target.value)}
      />

      <div className="text-xs text-gray-500">
        O texto clínico será composto automaticamente a partir dos campos acima.
      </div>
    </div>
  );
}
