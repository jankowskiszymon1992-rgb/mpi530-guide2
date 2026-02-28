# Sonel MPI-530 Interaktywna Instrukcja - PRD

## Problem Statement
Aplikacja instrukcji dla miernika Sonel MPI-530 z wszystkimi funkcjami pomiarowymi.

## Aktualizacja (2026-02-28)
- Dodano: **Kolejność Faz** (L1-L2-L3)
- Dodano: **Kierunek Obrotów Silnika** (prawe/lewe)
- Łącznie: **8 funkcji pomiarowych**

## Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: React.js z Tailwind CSS
- **Database**: MongoDB (nieużywana)

## Funkcje pomiarowe (8)
1. Test Wyłączników Różnicowoprądowych (RCD)
2. Impedancja Pętli Zwarciowej
3. Rezystancja Izolacji
4. Rezystancja Uziemienia
5. Pomiar Napięcia
6. Ciągłość Przewodów Ochronnych
7. **Kolejność Faz** - sprawdzenie 1-2-3 / 3-2-1
8. **Kierunek Obrotów Silnika** - prawe/lewe

## Features
- Wszystko po polsku
- Oficjalne zdjęcia miernika z cdn.sonel.com
- Instrukcje krok po kroku z obrazkami
- Dark mode
- Wyszukiwarka
- FAQ (10 pytań)

## Testing Status
- Backend: 8 funkcji działa
- Frontend: wszystkie widoki działają

## Backlog
- [ ] Eksport protokołów PDF
- [ ] Filmy z YouTube Sonel
- [ ] Zapisywanie wyników
