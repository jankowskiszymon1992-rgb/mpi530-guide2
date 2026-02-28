# Sonel MPI-530 Interactive Guide - PRD

## Original Problem Statement
Użytkownik wrócił do rozmowy gdzie tworzył aplikację dotyczącą instrukcji miernika Sonel MPI-530 - w środowisku były zapisane wytyczne projektowe (design_guidelines.json) ale kod nie był zaimplementowany.

## Architecture
- **Backend**: FastAPI (Python) - static data API dla funkcji pomiarowych
- **Frontend**: React.js z Tailwind CSS - industrialny styl UI
- **Database**: MongoDB (obecnie nieużywana - dane statyczne)

## Core Features Implemented (2026-02-28)

### Backend API
- `GET /api/functions` - wszystkie 6 funkcji pomiarowych
- `GET /api/functions/{id}` - szczegóły konkretnej funkcji
- `GET /api/search?q=query` - wyszukiwanie w instrukcjach
- `GET /api/faq` - często zadawane pytania

### Frontend
- **Strona główna**: Bento grid z kartami funkcji
- **Widok szczegółowy**: Split view (instrukcje + wyniki LCD)
- **Dark mode**: Przełącznik trybu jasnego/ciemnego
- **Sidebar**: Nawigacja po funkcjach
- **Wyszukiwarka**: Wyszukiwanie instrukcji i FAQ

### Funkcje pomiarowe
1. RCD Testing - test wyłączników różnicowoprądowych
2. Loop Impedance - impedancja pętli zwarciowej
3. Insulation Resistance - rezystancja izolacji
4. Earth Resistance - rezystancja uziemienia
5. Voltage Measurement - pomiar napięcia
6. Continuity Test - ciągłość przewodów

## User Personas
- **Elektrycy instalatorzy** - wykonujący pomiary odbiorcze
- **Serwisanci** - przeglądy okresowe instalacji
- **Uczniowie/studenci** - nauka obsługi miernika

## Design System (design_guidelines.json)
- Kolor główny: Sonel Orange (#F39200)
- Fonty: Oswald (nagłówki), Inter (body), JetBrains Mono (wartości)
- Styl: Industrial Technical

## Testing Status
- Backend: 100% (11/11 testów)
- Frontend: 100% (14/14 testów)

## Backlog (P0/P1/P2)

### P0 - Critical (done)
- [x] API funkcji pomiarowych
- [x] Instrukcje krok po kroku
- [x] Nawigacja i wyszukiwarka
- [x] Dark mode

### P1 - High Priority
- [ ] Zapisywanie wyników pomiarów
- [ ] Eksport protokołów do PDF
- [ ] Zdjęcia/diagramy podłączeń

### P2 - Nice to have
- [ ] Offline PWA mode
- [ ] Animacje kroków instrukcji
- [ ] Calculator pomiarów (np. Zs -> Ik)
- [ ] Historia wyszukiwań
