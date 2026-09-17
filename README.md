# DrugScope

DrugScope is a compound research workspace that uses PubChem as the traceable source for compound descriptors and provides clearly labelled prototype ADMET/toxicity placeholders plus optional AI-assisted interpretation.

## Architecture

- React + Vite frontend in `artifacts/drugscope`
- Express API in `artifacts/api-server`
- PostgreSQL + Drizzle in `lib/db`
- Shared generated API contracts in `lib/api-client-react` and `lib/api-zod`
- PubChem PUG REST for compound records
- Optional OpenAI integration for research-oriented summaries
- Vercel deployment configuration in `vercel.json`

## Local setup

Requirements: Node.js 20+ and pnpm 9+.

1. Copy `.env.example` to `.env` and fill in the Clerk/database values.
2. Install dependencies: `pnpm install`
3. Push the database schema for a development database: `pnpm --filter @workspace/db run push`
4. Run the API: `pnpm --filter @workspace/api-server run dev`
5. In a second terminal, run the frontend: `pnpm --filter @workspace/drugscope run dev`

## Vercel

This repository is configured so Vercel can build the Vite frontend and expose the Express application as a serverless function at `/api`. Set these Vercel environment variables:

- `VITE_CLERK_PUBLISHABLE_KEY`
- `CLERK_PUBLISHABLE_KEY`
- `CLERK_SECRET_KEY`
- `DATABASE_URL`
- `OPENAI_API_KEY` (optional)

Do not commit `.env` or real API keys.

## Important scientific limitation

The current ADMET and toxicity endpoints intentionally report `unavailable`; they are not validated prediction models. PubChem descriptors and Lipinski-style threshold checks are not substitutes for validated ADMET/toxicity models, experimental assays, or clinical evidence.
