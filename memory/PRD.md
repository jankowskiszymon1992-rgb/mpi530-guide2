# Sonel MPI-530 Interaktywna Instrukcja - PRD

## Problem Statement
Użytkownik potrzebował aplikacji instrukcji dla miernika Sonel MPI-530. Aplikacja została zaimplementowana na podstawie zapisanych wytycznych projektowych.

## Poprawki (2026-02-28)
- Wszystkie nazwy i opisy przetłumaczone na polski
- Dodane oficjalne zdjęcia miernika Sonel MPI-530 z CDN producenta (cdn.sonel.com)
- Każdy krok instrukcji ma odpowiednie zdjęcie (miernik, adapter WS-03, sondy, krokodylki)

## Architecture
- **Backend**: FastAPI (Python) - static data API
- **Frontend**: React.js z Tailwind CSS
- **Database**: MongoDB (obecnie nieużywana)

## Core Features

### Backend API
- `GET /api/functions` - 6 funkcji pomiarowych (PO POLSKU)
- `GET /api/functions/{id}` - szczegóły funkcji z obrazkami
- `GET /api/images` - wszystkie zdjęcia miernika MPI-530
- `GET /api/search?q=query` - wyszukiwanie
- `GET /api/faq` - FAQ (8 pytań)

### Frontend (wszystko PO POLSKU)
- Strona główna z Bento grid
- Widok szczegółowy z oficjalnymi zdjęciami Sonel
- Zdjęcia zmieniają się przy każdym kroku
- Dark mode
- Wyszukiwarka

### Zdjęcia miernika (oficjalne z cdn.sonel.com)
- Miernik główny (front, side, LCD)
- Adapter WS-03
- Sondy pomiarowe
- Krokodylki
- Elektrody uziemienia
- Przewody na szpulach

### Funkcje pomiarowe (PO POLSKU)
1. Test Wyłączników Różnicowoprądowych (RCD)
2. Impedancja Pętli Zwarciowej
3. Rezystancja Izolacji
4. Rezystancja Uziemienia
5. Pomiar Napięcia
6. Ciągłość Przewodów Ochronnych

## Testing Status
- Backend: 100% (14 testów)
- Frontend: 100% (15 testów)

## Backlog

### P1 - High Priority
- [ ] Eksport protokołów do PDF
- [ ] Zapisywanie wyników pomiarów

### P2 - Nice to have
- [ ] Filmy instruktażowe (YouTube embed)
- [ ] Offline PWA mode
- [ ] Calculator pomiarów
