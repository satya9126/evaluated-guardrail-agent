Evaluated Guardrail Agent

An LLM-powered application for AI security, privacy protection, and systematic guardrail evaluation.

GitHub Repository: https://github.com/satya9126/evaluated-guardrail-agent

Overview

Evaluated Guardrail Agent is a full-stack application designed to improve the security and reliability of Large Language Model (LLM) interactions. It implements input validation, personally identifiable information (PII) redaction, output inspection, authentication, rate limiting, security-event logging, and an evaluation framework.

The application integrates OpenAI with LangGraph for LLM workflow orchestration and uses FastAPI to expose secure REST endpoints.

Features

- Prompt Injection Detection: Identifies predefined malicious instruction-override patterns.
- PII Detection and Redaction: Redacts email addresses and 10-digit phone numbers before LLM processing.
- Output Guardrails: Checks generated responses for configured instruction-leakage patterns and personal information.
- LLM Orchestration: Integrates OpenAI with LangGraph.
- JWT Authentication: Supports user registration, login, password hashing, and protected API endpoints.
- Rate Limiting: Uses Redis to restrict excessive requests per client IP.
- Security Event Logging: Persists security-related request outcomes in PostgreSQL.
- Evaluation Framework: Measures guardrail performance using predefined test datasets.
- Evaluation Dashboard: Displays evaluation metrics through a Next.js frontend.
- Containerized Infrastructure: Uses Docker Compose for backend, database, and Redis services.
- Automated Testing: Uses Pytest and GitHub Actions CI.

Tech Stack

Category| Technologies
Language| Python
Backend| FastAPI
LLM| OpenAI API
Workflow Orchestration| LangGraph
Frontend| Next.js, React, TypeScript
Database| PostgreSQL
Rate Limiting| Redis
Authentication| JWT, Passlib, bcrypt
Migrations| Alembic
Testing| Pytest
Containerization| Docker, Docker Compose
CI| GitHub Actions


Evaluation Results

Initial evaluation on the current test dataset produced the following results:

Metric| Result
Prompt Injection Block Rate| 100%
PII Redaction Rate| 100%
Output Leakage Block Rate| 100%
Normal Request Pass Rate| 100%
False Positive Rate| 0%

Note: These metrics represent results on the current, limited evaluation dataset. They do not guarantee protection against all real-world attacks or unseen inputs.

Project Structure


Prerequisites

- Python 3.10
- Node.js and npm
- Docker Desktop with Docker Compose
- OpenAI API key

Setup and Installation

1. Clone the repository

git clone https://github.com/satya9126/evaluated-guardrail-agent.git
cd evaluated-guardrail-agent

2. Configure environment variables

Create a ".env" file in the project root:

OPENAI_API_KEY=your_openai_api_key
LLM_PROVIDER=openai

POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=evaluated_guardrail

JWT_SECRET_KEY=your_long_random_secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

Use your own credentials. Never commit the ".env" file or publish API keys and secrets.

3. Start the Docker services

docker compose up --build -d

4. Apply database migrations

docker compose exec backend python -m alembic upgrade head

5. Verify the backend

Health endpoint:

http://localhost:8000/health

Interactive API documentation:

http://localhost:8000/docs

6. Start the frontend

Open a separate terminal:

cd frontend
npm install
npm run dev

Open the application:

http://localhost:3000

Register an account and log in to access the protected chat interface. The evaluation dashboard is available at:

http://localhost:3000/evaluation

API Endpoints

Method| Endpoint| Description
GET| "/health"| Backend health check
POST| "/api/v1/auth/register"| Register a user
POST| "/api/v1/auth/login"| Authenticate and receive a JWT
POST| "/api/v1/chat"| Submit an authenticated chat request
GET| "/api/v1/evaluation/results"| Retrieve evaluation metrics

Testing

Run the test suite from the project root:

pytest -v

The current test suite covers prompt-injection detection, PII redaction, output guardrails, and rate limiting.

Evaluation Framework

The evaluation runner executes predefined datasets and calculates:

- Prompt injection block rate
- PII redaction rate
- Output leakage block rate
- Normal request pass rate
- False positive rate

The generated metrics are saved to "backend/evaluations/results.json" and exposed through the evaluation API.

Security Considerations

- Prompt-injection detection is pattern-based and may miss novel or indirect attacks.
- PII redaction currently covers email addresses and 10-digit phone numbers, not every type of sensitive data.
- Output guardrails use predefined patterns and cannot guarantee complete detection of unsafe responses.
- Broader adversarial testing, monitoring, and additional security controls are required before production deployment.

Future Improvements

- Expand adversarial evaluation datasets.
- Improve detection of indirect prompt injection.
- Extend PII detection to additional sensitive data types.
- Enhance security-event analytics.
- Add integration and load testing.
- Strengthen production monitoring and deployment security.

Author

Satya Krishna Chowdary

GitHub: https://github.com/satya9126

LinkedIn: https://www.linkedin.com/in/kurra-satya-krishna-chowdary-588186269/

---

Developed as a hands-on project exploring LLM application security, backend engineering, and AI guardrail evaluation.
