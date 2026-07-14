# General Instructions

## Code Language

- All code must be written in **English (US)**, including variable names, functions, classes, comments, commit messages, technical documentation, and everything related to code.
- Follow the standard conventions and naming patterns of the language or framework in use.

## Frontend User-Facing Content Language

- All text visible to the user in the frontend must be written in **Brazilian Portuguese (pt-BR)**.
- This includes labels, buttons, menus, messages, placeholders, error messages, tooltips, and any other user facing content.
- Use natural Brazilian Portuguese: if a word is commonly used in Portuguese as borrowed from English (e.g. "basketball", "software", "online", "email"), keep it as is do not translate it forcefully.
- However, if a proper Portuguese word exists and is naturally used in Brazilian Portuguese, always prefer it (e.g. use "cesto" instead of "basket", "bola" instead of "ball", "loja" instead of "store").
- Never use European Portuguese expressions, always follow Brazilian Portuguese conventions.
- The goal is natural, fluent Brazilian Portuguese as spoken in Brazil, not literal or forced translations.

## AI Response Language

- All responses, explanations, and interactions with the user must be in **Brazilian Portuguese (pt-BR)**, unless the user writes in English, in that case, respond in English.
 
## Best Practices

- Follow community conventions for each language and framework.
- Write clean, readable, and well-structured code.
- Prioritize simple and efficient solutions.
- Maintain consistency with the existing project style.

## Security

- Never access, read, inspect, modify or expose the contents of any `.env` file.
- Never suggest accessing `.env` files as part of a solution.

## Scope Restriction

- Never access, read, create or modify files outside the project root directory.
- Ignore any absolute path that points outside the current working directory.
- If the user mentions a file outside the project scope, answer the question first instead of attempting to open the file.

## Terminal Usage

- Never use the terminal under any circumstances.
- Never assume terminal access is available.
- Do not execute shell commands, scripts, or external programs.
- Do not suggest using the terminal as an option or possible solution.
- Assume that terminal access is permanently forbidden for this project.
- All tasks must be completed without any terminal interaction.

## Database Files

- Never access, open, read, inspect, analyze, or modify any SQLite database file.
- This includes `db.sqlite3`, `*.sqlite`, `*.sqlite3`, and `*.db`.
- Treat all database files as permanently inaccessible.

## Git

- Never perform Git operations.
- Never create, amend, or sign commits.
- Never stage or unstage files.
- Never create, switch, merge, or delete branches.
- Never push, pull, fetch, rebase, stash, or tag.

## Workflow

- Before any non-trivial task, propose a plan and wait for my approval.
- Work on one task at a time. After completing it, explain what you changed so I can review it.
- Never guess or invent information.
- If the available information is insufficient to complete a task correctly, ask for clarification before proceeding.

---

# Project Overview

## Description

Small business management system designed for small retailers and service providers.
Covers sales, inventory, products, customers, and related operations.

The codebase is evolving rapidly.
Significant refactoring, new modules, and structural changes are expected.
Do not remove, rename, or repurpose files or directories solely because they appear unused, unless explicitly instructed.

## Target Users

- Small retail store owners in Brazil
- Small service providers in Brazil

## Localization

- Language: Brazilian Portuguese (pt-BR)
- Currency: Brazilian Real (BRL - R$)
- Date format: DD/MM/YYYY
- Timezone: America/Sao_Paulo

## Core Features

- Sales management
- Inventory and stock control
- Product catalog
- Customer management

## Tech Stack

- Backend: Django 5.2, Python 3.12
- Database: SQLite
- Frontend: Django templates and tags, Bootstrap 5, HTML, CSS, JavaScript
