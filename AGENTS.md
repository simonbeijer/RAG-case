# AGENTS.md

## Project
A chat that answers questions in Swedish about compileit.com, built with RAG.
It is a small code test, not a production app. Keep it small, simple and easy to explain.

This file describes how we work, not what is built. To see what exists, read the code.
Do not create files or folders for parts that are not built yet.

## Why I work like this
I want control over the code. I must understand every line and be able to defend it.
You are fast. My role is to slow down, ask how it holds up long term, and decide.
When something goes wrong, we stop and talk before we fix.

## How we work
- Discuss first, then code. A question from me is a discussion, not a task.
- Do only the task. No extra files, functions, packages or "improvements".
- Simple and readable over smart. Few, short comments.
- If something is unclear, or you hit a problem: stop and ask. Do not build around it.
- If there is a better way, tell me. Do not just do it.
- After a change: say in short, plain words what you did, why, and what you assumed.
  Help me understand the code, not only get it.

## My files
- Often I write the skeleton: names, parameters with types, return type, one-line docstring.
  You write the body. Do not change the skeleton. If it looks wrong: stop and ask.
- Do not rewrite or reformat code I wrote unless I ask.

## Rules
- Nothing that changes the answer is hardcoded. Settings go in `backend/config.yaml`,
  prompts in `backend/prompts/`.
- Add a package only when the code that uses it is written. Say which, why, and the command (`uv add ...`).
- Never read, print or log `.env` or the API key.
- Do not run anything that costs tokens (LLM calls, indexing, eval) unless I ask.
- Do not commit or push. Do not add yourself as author.

## Run
From the repo root:

```
make setup     # install backend packages
make ingest    # fetch the site and build the index
make chat      # terminal chat with logs
make api       # FastAPI server
make test      # pytest
```

Frontend: `npm run dev` in `frontend/`.

## Test
`make test` runs the unit tests. After every change to the prompt or `backend/config.yaml`,
run the test questions from the README by hand and compare the answers.

## This file
It grows with the project. Suggest changes when you see a need, but do not edit it without asking.
If this file and the code do not agree: tell me, and I decide which is correct.