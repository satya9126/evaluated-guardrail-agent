"use client";

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setResponse("");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/chat", {
        method: "POST",
        headers: {
  "Content-Type": "application/json",
  Authorization: `Bearer ${localStorage.getItem("access_token")}`,
},
        body: JSON.stringify({
          message: message,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setResponse(`Blocked: ${data.detail}`);
      } else {
        setResponse(data.response);
      }
    } catch (error) {
      setResponse(
        "Unable to connect to the backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-lg p-8">

        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Evaluated Guardrail Agent
        </h1>

        <p className="text-gray-600 mb-6">
          AI assistant protected by prompt injection and PII guardrails.
        </p>

        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask something..."
          className="w-full h-40 border border-gray-300 rounded-xl p-4 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="mt-4 px-6 py-3 bg-black text-white rounded-xl hover:bg-gray-800 disabled:opacity-50"
        >
          {loading ? "Processing..." : "Send"}
        </button>

        {response && (
          <div className="mt-6">
            <h2 className="font-semibold text-gray-900 mb-2">
              Response
            </h2>

            <div className="bg-gray-100 rounded-xl p-4 whitespace-pre-wrap text-gray-800">
              {response}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}