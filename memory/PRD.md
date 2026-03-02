# Sonel MPI-530 Interaktywna Instrukcja - PRD

## Problem Statement
Interactive guide application for the Sonel MPI-530 electrical measurement meter. Supports three languages: Polish (PL), English (EN), German (DE). All content fully translated. Positioned as "Independent User Guide for MPI-530" with legal disclaimer.

## Architecture
- **Frontend**: React + Tailwind CSS + Shadcn/UI + i18n (custom LanguageProvider)
- **Backend**: FastAPI (all data hardcoded in server.py + translations.py)
- **Database**: None (all data mocked/hardcoded)
- **Deployment**: VPS Hostinger (Ubuntu 24.04, CloudPanel) at https://mpi530.elektryk.cloud

## Implemented Features

### Multi-language Support (PL/EN/DE) - COMPLETE
- Language switcher in header (globe icon + dropdown)
- Language persists via localStorage
- ALL content fully translated

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
- Legal disclaimer on home page
- Health check endpoint (/api/health)

### Deployment - COMPLETE (March 2, 2026)
- Deployed to VPS Hostinger (Ubuntu 24.04, CloudPanel)
- URL: https://mpi530.elektryk.cloud
- Backend runs as systemd service (mpi530-backend)
- Nginx proxy configured via CloudPanel
- SSL/HTTPS enabled
- Deployment scripts created in /deployment/ folder
- WordPress on elektryk.cloud remains unaffected

## Key Files
- `/app/backend/server.py` - Backend logic and Polish data
- `/app/backend/translations.py` - EN and DE translations (all content)
- `/app/frontend/src/App.js` - Main component
- `/app/frontend/src/i18n/` - Language context and JSON files
- `/app/frontend/src/components/ToolsComponents.js` - Professional tools
- `/app/deployment/` - Deployment scripts (setup.sh, update.sh, nginx.conf, INSTRUKCJA_WDROZENIA.md)

## Testing
- Iteration 3: Backend 28/28, Frontend 100% (core features)
- Iteration 4: Backend 21/21, Frontend 100% (i18n - functions, tools, quiz)
- Iteration 5: Backend 17/17, Frontend 100% (i18n - protocols fully translated)
- Deployment: Verified live at https://mpi530.elektryk.cloud

### Bug Fix: Frontend API URL (March 2, 2026)
- Fixed frontend hardcoding Emergent preview URL in production build
- Changed `BACKEND_URL` to use `process.env.REACT_APP_BACKEND_URL || ''` (relative URLs in production)
- Files changed: `App.js`, `ToolsComponents.js`
- User rebuilt on VPS — confirmed working on phone (browser + installed PWA)

## Status: COMPLETE - All features implemented, translated, and deployed to production
