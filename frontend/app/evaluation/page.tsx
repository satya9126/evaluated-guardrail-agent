"use client";

import { useEffect, useState } from "react";

type EvaluationResults = {
  prompt_injection_block_rate: number;
  pii_redaction_rate: number;
  output_leakage_block_rate: number;
  normal_request_pass_rate: number;
  false_positive_rate: number;
};

export default function EvaluationPage() {
  const [results, setResults] = useState<EvaluationResults | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchResults() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/v1/evaluation/results"
        );

        const data = await response.json();

        if (!response.ok) {
          setError(data.detail || "Failed to load evaluation results.");
          return;
        }

        setResults(data);
      } catch {
        setError("Unable to connect to the backend.");
      }
    }

    fetchResults();
  }, []);

  if (error) {
    return (
      <main style={{ padding: "40px" }}>
        <h1>Evaluation Dashboard</h1>
        <p>{error}</p>
      </main>
    );
  }

  if (!results) {
    return (
      <main style={{ padding: "40px" }}>
        <h1>Evaluation Dashboard</h1>
        <p>Loading evaluation results...</p>
      </main>
    );
  }

  return (
    <main
      style={{
        padding: "40px",
        minHeight: "100vh",
        background: "#f5f5f5",
      }}
    >
      <h1>Evaluation Dashboard</h1>

      <p>
        Security and reliability evaluation results from the current
        evaluation dataset.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: "20px",
          maxWidth: "900px",
          marginTop: "30px",
        }}
      >
        <MetricCard
          title="Prompt Injection Block Rate"
          value={results.prompt_injection_block_rate}
        />

        <MetricCard
          title="PII Redaction Rate"
          value={results.pii_redaction_rate}
        />

        <MetricCard
          title="Output Leakage Block Rate"
          value={results.output_leakage_block_rate}
        />

        <MetricCard
          title="Normal Request Pass Rate"
          value={results.normal_request_pass_rate}
        />

        <MetricCard
          title="False Positive Rate"
          value={results.false_positive_rate}
        />
      </div>
    </main>
  );
}

function MetricCard({
  title,
  value,
}: {
  title: string;
  value: number;
}) {
  return (
    <div
      style={{
        padding: "25px",
        background: "white",
        borderRadius: "10px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
      }}
    >
      <h2 style={{ fontSize: "18px" }}>{title}</h2>

      <p
        style={{
          fontSize: "32px",
          fontWeight: "bold",
          marginTop: "15px",
        }}
      >
        {value.toFixed(2)}%
      </p>
    </div>
  );
}