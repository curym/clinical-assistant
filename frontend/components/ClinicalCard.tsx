"use client";

import { useState } from "react";

interface Props {
  title: string;
  children: React.ReactNode;
  highlight?: "danger" | "info" | "neutral";
  defaultOpen?: boolean;
}

export function ClinicalCard({
  title,
  children,
  highlight = "neutral",
  defaultOpen = true,
}: Props) {
  const [open, setOpen] = useState(defaultOpen);

  const colorMap = {
    danger: "border-red-500 bg-red-50",
    info: "border-blue-500 bg-blue-50",
    neutral: "border-gray-300 bg-white",
  };

  return (
    <div className={`border rounded-lg mb-4 ${colorMap[highlight]}`}>
      <button
        onClick={() => setOpen(!open)}
        className="w-full text-left px-4 py-3 font-semibold flex justify-between items-center"
      >
        <span>{title}</span>
        <span className="text-sm">{open ? "−" : "+"}</span>
      </button>

      {open && <div className="px-4 pb-4">{children}</div>}
    </div>
  );
}
