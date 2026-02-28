# Sonel MPI-530 Interaktywna Instrukcja - PRD

## Problem Statement
Interactive guide application for the Sonel MPI-530 electrical measurement meter. Supports three languages: Polish (PL), English (EN), German (DE). All content fully translated.

## Architecture
- **Frontend**: React + Tailwind CSS + Shadcn/UI + i18n (custom LanguageProvider)
- **Backend**: FastAPI (all data hardcoded in server.py + translations.py)
- **Database**: None (all data mocked/hardcoded)

## Implemented Features

### Multi-language Support (PL/EN/DE) - COMPLETE
- Language switcher in header (globe icon + dropdown)
- Language persists via localStorage
- ALL content fully translated: functions, steps, FAQ, quiz, error codes, checklists, protocols, guides, templates, examples

### Core (10 measurement functions) - COMPLETE
1. RCD Testing / Impedance / Insulation / Earthing / Voltage
2. Continuity / Phase Sequence / Motor Rotation / Lux / Earthing Clamp

### Tools (9 tabs) - COMPLETE
Zs Calculator, Cable Sizing, Norm Tables, Error Codes, Diagrams, Safety Checklist, PDF Generator, Quiz, Notes

### Protocols - COMPLETE (all translated)
- 4 Sonel Reports Plus guides (PL/EN/DE)
- 5 protocol templates (PL/EN/DE)
- 5 example protocols with measurements (PL/EN/DE)
- 13 FAQ (PL/EN/DE)

### Other
- Dark mode
- Search functionality
- Static PDF export (34 pages)

## Key Files
- `/app/backend/server.py` - Backend logic and Polish data
- `/app/backend/translations.py` - EN and DE translations (all content)
- `/app/frontend/src/App.js` - Main component
- `/app/frontend/src/i18n/` - Language context and JSON files
- `/app/frontend/src/components/ToolsComponents.js` - Professional tools

## Testing
- Iteration 3: Backend 28/28, Frontend 100% (core features)
- Iteration 4: Backend 21/21, Frontend 100% (i18n - functions, tools, quiz)
- Iteration 5: Backend 17/17, Frontend 100% (i18n - protocols fully translated)

## Status: COMPLETE - All features implemented and fully translated
