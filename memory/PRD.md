# Sonel MPI-530 Interaktywna Instrukcja - PRD

## Problem Statement
Interactive guide application for the Sonel MPI-530 electrical measurement meter. Fully in Polish. Provides step-by-step instructions, tools, calculators, protocol generation, and professional features.

## Architecture
- **Frontend**: React + Tailwind CSS + Shadcn/UI
- **Backend**: FastAPI (all data hardcoded in server.py - no database)
- **PWA**: Service Worker + manifest.json for offline capability

## Implemented Features

### Core (10 measurement functions)
1. Test Wyłączników Różnicowoprądowych (RCD)
2. Impedancja Pętli Zwarciowej
3. Rezystancja Izolacji
4. Rezystancja Uziemienia
5. Pomiar Napięcia
6. Ciągłość Przewodów Ochronnych
7. Kolejność Faz
8. Kierunek Obrotów Silnika
9. Pomiar Natężenia Oświetlenia
10. Uziemienie Metodą Cęgową

### Tools (9 tabs)
1. Kalkulator Zs → Ik
2. Kalkulator doboru przewodów (Cable Calculator)
3. Tabele norm PN-HD 60364
4. Kody błędów (12)
5. Schematy podłączeń (8)
6. Checklista bezpieczeństwa (6 checklist)
7. Generator protokołu PDF (jsPDF)
8. Quiz z certyfikatem (15 pytań, 70% do zaliczenia)
9. Notatki i historia (localStorage)

### Protokoły
- 4 instrukcje Sonel Reports Plus
- 5 szablonów protokołów
- 5 przykładowych wypełnionych protokołów

### FAQ: 13 pytań

### PWA
- Service Worker (cache-first strategy for static, network-first for API)
- Web App Manifest

## Key Files
- `/app/backend/server.py` - All backend logic and hardcoded data
- `/app/frontend/src/App.js` - Main React component with all views
- `/app/frontend/src/components/ToolsComponents.js` - Professional tools components
- `/app/frontend/public/service-worker.js` - PWA service worker
- `/app/frontend/public/manifest.json` - PWA manifest

## Testing
- Backend: 28/28 tests passed (iteration_3)
- Frontend: 100% features verified
- Test file: `/app/backend/tests/test_mpi530_api.py`

## Status: COMPLETE - All features implemented and tested

## Backlog
- Refactor server.py monolith (1900+ lines) into modular files
- UI/UX improvements if requested by user
