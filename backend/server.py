from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Sonel MPI-530 Interaktywna Instrukcja API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class InstructionStep(BaseModel):
    step_number: int
    title: str
    description: str
    warning: Optional[str] = None
    tip: Optional[str] = None
    image: Optional[str] = None

class MeasurementFunction(BaseModel):
    id: str
    name: str
    icon: str
    description: str
    category: str
    color: str
    steps: List[InstructionStep]
    parameters: List[str]
    safety_notes: List[str]
    expected_results: str
    main_image: str

class FAQ(BaseModel):
    id: str
    question: str
    answer: str
    category: str

# Oficjalne zdjęcia Sonel MPI-530 z CDN producenta
METER_IMAGES = {
    "main": "https://cdn.sonel.com/Zdjecia/Mierniki/MPI/MPI-530/image-thumb__32614__img-product-thumb/MPI-530_L_EN_logger_01_u%20-pim.webp",
    "front": "https://cdn.sonel.com/Zdjecia/Mierniki/MPI/MPI-530/image-thumb__32611__img-product-thumb/MPI-530%20P%20EN%20logger%2001%20u%20-pim.webp",
    "side": "https://cdn.sonel.com/Zdjecia/Mierniki/MPI/MPI-530/image-thumb__32612__img-product-thumb/MPI-530%20F_EN_logger_u_i%20-pim.webp",
    "lcd": "https://cdn.sonel.com/Zdjecia/Mierniki/MPI/MPI-530/image-thumb__32617__img-product-thumb/_DSC1058_z_LCD.webp",
    "case": "https://cdn.sonel.com/Zdjecia/Mierniki/MPI/MPI-530/image-thumb__32616__img-product-thumb/_DSC2180.webp",
    "adapter_ws03": "https://cdn.sonel.com/Zdjecia/Akcesoria/Adaptery/Adaptery+WS/WAADAWS03/image-thumb__21479__img-product-thumb/WAADAWS03.webp",
    "probes": "https://cdn.sonel.com/Zdjecia/Akcesoria/Sondy/Sondy+ostrzowe/WASONREOGB1/image-thumb__22243__img-product-thumb/WASONREOGB1.webp",
    "earth_probe": "https://cdn.sonel.com/Zdjecia/Akcesoria/Sondy/Sondy+gruntowe/WASONG30/image-thumb__22228__img-product-thumb/WASONG30.webp",
    "crocodile": "https://cdn.sonel.com/Zdjecia/Akcesoria/Krokodylki+i+zaciski/Krokodylki/WAKRORE20K02/image-thumb__21720__img-product-thumb/WAKRORE20K02.webp",
    "test_lead": "https://cdn.sonel.com/Zdjecia/Akcesoria/Przewody/Przewody+pomiarowe/WAPRZ1X2REBB/image-thumb__22077__img-product-thumb/WAPRZ1X2REBB-9318.webp",
    "lux_probe": "https://cdn.sonel.com/Zdjecia/Akcesoria/Sondy/Sondy+luksomierza/WAADALP10BKPL/image-thumb__21338__img-product-thumb/WAADALP10BKPL.webp",
    "clamp_c3": "https://cdn.sonel.com/Zdjecia/Akcesoria/C%C4%99gi/C%C4%99gi+z+twardym+rdzeniem/WACEGC3OKR/image-thumb__21552__img-product-thumb/WACEGC3OKR.webp",
    "clamp_n1": "https://cdn.sonel.com/Zdjecia/Akcesoria/C%C4%99gi/C%C4%99gi+nadawcze/WACEGN1BB/image-thumb__21600__img-product-thumb/WACEGN1BB.webp",
    "clamp_set": "https://cdn.sonel.com/Zdjecia/Akcesoria/C%C4%99gi/C%C4%99gi+z+twardym+rdzeniem/WAKPLC3N1/image-thumb__38771__img-product-thumb/WAKPLC3N1.webp"
}

# Static data for MPI-530 measurement functions - PO POLSKU
MEASUREMENT_FUNCTIONS: List[MeasurementFunction] = [
    MeasurementFunction(
        id="rcd",
        name="Test Wyłączników Różnicowoprądowych (RCD)",
        icon="Shield",
        description="Pomiar czasu i prądu zadziałania wyłączników różnicowoprądowych (RCD/RCCB)",
        category="bezpieczenstwo",
        color="#F39200",
        main_image=METER_IMAGES["main"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Przygotowanie",
                description="Ustaw pokrętło funkcji na pozycję RCD. Upewnij się, że instalacja jest pod napięciem.",
                warning="UWAGA: Pomiar wykonywany pod napięciem! Zachowaj szczególną ostrożność.",
                tip="Sprawdź czy RCD jest załączony przed pomiarem.",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=2,
                title="Podłączenie przewodów",
                description="Podłącz przewód niebieski do gniazda L/L1/L2, czerwony do gniazda PE. Użyj sondy jednobiegunowej lub adaptera gniazda WS-03.",
                warning="Sprawdź poprawność połączeń przed uruchomieniem testu.",
                image=METER_IMAGES["adapter_ws03"]
            ),
            InstructionStep(
                step_number=3,
                title="Wybór parametrów",
                description="Wybierz typ RCD (AC, A, B), prąd znamionowy (10, 30, 100, 300, 500 mA) oraz mnożnik prądu testowego (0.5x, 1x, 2x, 5x).",
                tip="Dla standardowych RCD domowych używaj typu AC i 30mA.",
                image=METER_IMAGES["lcd"]
            ),
            InstructionStep(
                step_number=4,
                title="Wykonanie pomiaru",
                description="Naciśnij przycisk START. Miernik wymusi prąd różnicowy i zmierzy czas zadziałania RCD.",
                tip="Po zadziałaniu RCD, załącz go ponownie przed kolejnym pomiarem.",
                image=METER_IMAGES["front"]
            ),
            InstructionStep(
                step_number=5,
                title="Odczyt wyniku",
                description="Odczytaj czas zadziałania [ms] oraz napięcie dotykowe [V]. Dla RCD 30mA czas powinien być <300ms przy 1x IΔn.",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Typ RCD: AC, A, B, F", "Prąd IΔn: 10-500 mA", "Mnożnik: 0.5x, 1x, 2x, 5x", "Faza początkowa: 0°, 180°"],
        safety_notes=[
            "Pomiar wykonywany pod napięciem - zachowaj ostrożność",
            "RCD zadziała podczas testu - ostrzeż użytkowników instalacji",
            "Sprawdź ciągłość PE przed pomiarem RCD"
        ],
        expected_results="Czas zadziałania <300ms dla 1x IΔn, <150ms dla 2x IΔn, <40ms dla 5x IΔn"
    ),
    MeasurementFunction(
        id="loop",
        name="Impedancja Pętli Zwarciowej",
        icon="Repeat",
        description="Pomiar impedancji pętli zwarcia L-PE i L-N dla weryfikacji skuteczności ochrony przeciwporażeniowej",
        category="impedancja",
        color="#3B82F6",
        main_image=METER_IMAGES["front"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję Zs (impedancja pętli zwarcia). Wybierz tryb L-PE lub L-N.",
                warning="Pomiar wykonywany pod napięciem!",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=2,
                title="Podłączenie",
                description="Podłącz adapter gniazda WS-03 lub użyj sond: L do przewodu fazowego, N do neutralnego, PE do ochronnego.",
                tip="Dla pomiaru L-PE wymagane jest połączenie z przewodem ochronnym.",
                image=METER_IMAGES["adapter_ws03"]
            ),
            InstructionStep(
                step_number=3,
                title="Ustawienie parametrów",
                description="Wybierz zakres pomiarowy i typ pomiaru (standardowy lub z wysokim prądem pomiarowym dla większej dokładności).",
                tip="Tryb wysokoprądowy daje dokładniejsze wyniki w instalacjach z niską impedancją.",
                image=METER_IMAGES["lcd"]
            ),
            InstructionStep(
                step_number=4,
                title="Pomiar",
                description="Naciśnij START. Miernik zmierzy impedancję pętli i wyliczy spodziewany prąd zwarciowy.",
                warning="Podczas pomiaru może nastąpić krótkotrwały przepływ prądu przez instalację.",
                image=METER_IMAGES["front"]
            ),
            InstructionStep(
                step_number=5,
                title="Analiza wyniku",
                description="Odczytaj Zs [Ω] oraz Ik [A]. Porównaj z wartościami dopuszczalnymi dla danego zabezpieczenia.",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Zakres Zs: 0.00-1999 Ω", "Rozdzielczość: 0.01 Ω", "Prąd pomiarowy: do 7.6 A", "Napięcie: 180-253 V"],
        safety_notes=[
            "Pomiar pod napięciem - zachowaj ostrożność",
            "W obwodach z RCD, wyłącznik może zadziałać podczas pomiaru",
            "Prąd pomiarowy może powodować zakłócenia w instalacji"
        ],
        expected_results="Zs musi zapewnić zadziałanie zabezpieczenia w wymaganym czasie (Zs < Uo/Ia)"
    ),
    MeasurementFunction(
        id="insulation",
        name="Rezystancja Izolacji",
        icon="Layers",
        description="Pomiar rezystancji izolacji przewodów i urządzeń napięciem do 1000V DC",
        category="izolacja",
        color="#10B981",
        main_image=METER_IMAGES["side"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Odłączenie napięcia",
                description="WYŁĄCZ zasilanie instalacji! Odłącz wszystkie odbiorniki wrażliwe na napięcie pomiarowe.",
                warning="BEZWZGLĘDNIE wyłącz napięcie przed pomiarem izolacji! Pomiar wykonywany napięciem do 1000V DC.",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=2,
                title="Wybór funkcji i napięcia",
                description="Ustaw pokrętło na pozycję RISO. Wybierz napięcie pomiarowe: 50V, 100V, 250V, 500V lub 1000V.",
                tip="Dla instalacji 230V stosuj napięcie pomiarowe 500V. Dla instalacji 400V - 1000V.",
                image=METER_IMAGES["lcd"]
            ),
            InstructionStep(
                step_number=3,
                title="Podłączenie przewodów",
                description="Podłącz przewód do badanej izolacji (np. L1-PE, L1-N, L1-L2). Użyj krokodylków lub sond.",
                tip="Dla pomiaru całej instalacji połącz wszystkie fazy razem i mierz względem PE.",
                image=METER_IMAGES["crocodile"]
            ),
            InstructionStep(
                step_number=4,
                title="Wykonanie pomiaru",
                description="Naciśnij i przytrzymaj START. Miernik przyłoży napięcie pomiarowe i zmierzy rezystancję izolacji.",
                warning="Nie dotykaj badanych obwodów podczas pomiaru - napięcie do 1000V DC!",
                image=METER_IMAGES["front"]
            ),
            InstructionStep(
                step_number=5,
                title="Rozładowanie i odczyt",
                description="Po zwolnieniu START, miernik automatycznie rozładuje pojemność. Odczytaj wynik w MΩ.",
                tip="Minimalna wartość dla instalacji nowych: 1 MΩ. Dla eksploatowanych: 0.5 MΩ.",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Napięcie: 50, 100, 250, 500, 1000 V DC", "Zakres: 0.00 MΩ - 10 GΩ", "Prąd pomiarowy: max 1.2 mA"],
        safety_notes=[
            "WYŁĄCZ NAPIĘCIE przed pomiarem!",
            "Napięcie pomiarowe do 1000V DC - niebezpieczeństwo porażenia",
            "Rozładuj pojemność kabli przed dotknięciem",
            "Odłącz elementy wrażliwe (liczniki, sterowniki, LED)"
        ],
        expected_results="≥1 MΩ dla instalacji nowych, ≥0.5 MΩ dla eksploatowanych"
    ),
    MeasurementFunction(
        id="earthing",
        name="Rezystancja Uziemienia",
        icon="Zap",
        description="Pomiar rezystancji uziemienia metodą techniczną 3- i 4-przewodową",
        category="uziemienie",
        color="#F59E0B",
        main_image=METER_IMAGES["case"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Wybór metody",
                description="Ustaw pokrętło na RE. Wybierz metodę: 3-przewodową (techniczna) lub 4-przewodową (dokładniejsza).",
                tip="Metoda 4-przewodowa eliminuje wpływ rezystancji przewodów pomiarowych.",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=2,
                title="Przygotowanie elektrod",
                description="Wbij elektrodę prądową (H) w odległości min. 40m od badanego uziomu, elektrodę napięciową (S) w 62% tej odległości.",
                warning="Odłącz badane uziemienie od instalacji przed pomiarem!",
                image=METER_IMAGES["earth_probe"]
            ),
            InstructionStep(
                step_number=3,
                title="Podłączenie",
                description="Połącz: E - badany uziom, S - elektroda napięciowa, H - elektroda prądowa. Użyj przewodów na szpulach.",
                tip="Elektrody ustawiaj w jednej linii z badanym uziemieniem.",
                image=METER_IMAGES["test_lead"]
            ),
            InstructionStep(
                step_number=4,
                title="Pomiar",
                description="Naciśnij START. Miernik zmierzy rezystancję i sprawdzi poprawność pomiaru (kontrola RE S i H).",
                tip="Jeśli wynik niestabilny - sprawdź wilgotność gruntu przy elektrodach pomocniczych.",
                image=METER_IMAGES["front"]
            ),
            InstructionStep(
                step_number=5,
                title="Odczyt i zakończenie",
                description="Odczytaj RE [Ω]. Dla uziemienia ochronnego typowa wartość <10 Ω.",
                warning="Pamiętaj o podłączeniu uziemienia z powrotem do instalacji po pomiarze!",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Zakres: 0.00-9999 Ω", "Rozdzielczość: 0.01 Ω", "Częstotliwość: 125 Hz", "Prąd pomiarowy: >200 mA"],
        safety_notes=[
            "Odłącz uziemienie od instalacji przed pomiarem",
            "Zachowaj bezpieczną odległość od linii wysokiego napięcia",
            "Elektrody pomocnicze wbijaj w wilgotny grunt",
            "Po pomiarze podłącz uziemienie z powrotem"
        ],
        expected_results="<10 Ω dla uziemienia ochronnego, <2 Ω dla uziemienia roboczego"
    ),
    MeasurementFunction(
        id="voltage",
        name="Pomiar Napięcia",
        icon="Activity",
        description="Pomiar napięcia przemiennego AC i stałego DC oraz częstotliwości (TRMS)",
        category="podstawowe",
        color="#6366F1",
        main_image=METER_IMAGES["lcd"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję U (napięcie). Miernik automatycznie wykrywa AC/DC.",
                tip="Dla pomiaru napięcia między fazami użyj funkcji L-L.",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=2,
                title="Podłączenie",
                description="Podłącz czerwoną sondę do mierzonego punktu, niebieską do punktu odniesienia (N lub PE).",
                warning="Nie przekraczaj maksymalnego napięcia 550V AC!",
                image=METER_IMAGES["probes"]
            ),
            InstructionStep(
                step_number=3,
                title="Odczyt wyniku",
                description="Odczytaj napięcie [V] i częstotliwość [Hz] na wyświetlaczu. Pomiar TRMS daje dokładny wynik dla odkształconych przebiegów.",
                tip="Napięcie fazowe powinno wynosić 220-240V, międzyfazowe 380-420V.",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Zakres AC: 0-550 V", "Zakres DC: 0-550 V", "Częstotliwość: 45-65 Hz", "Dokładność: ±1%"],
        safety_notes=[
            "Nie przekraczaj 550V AC/DC",
            "Używaj przewodów pomiarowych w dobrym stanie",
            "Kategoria pomiarowa CAT III 600V / CAT IV 300V"
        ],
        expected_results="Napięcie fazowe: 220-240V, międzyfazowe: 380-420V, częstotliwość: 49.5-50.5 Hz"
    ),
    MeasurementFunction(
        id="continuity",
        name="Ciągłość Przewodów Ochronnych",
        icon="Link",
        description="Pomiar ciągłości i rezystancji przewodów ochronnych PE i połączeń wyrównawczych prądem 200mA",
        category="ciaglosc",
        color="#EC4899",
        main_image=METER_IMAGES["front"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Odłączenie napięcia",
                description="WYŁĄCZ zasilanie instalacji przed pomiarem ciągłości!",
                warning="Pomiar wykonywany BEZ napięcia w instalacji!",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=2,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję RCONT (ciągłość). Wybierz prąd pomiarowy 200mA zgodnie z normą.",
                tip="Prąd 200mA jest wymagany przez normę EN 61557-4.",
                image=METER_IMAGES["lcd"]
            ),
            InstructionStep(
                step_number=3,
                title="Zerowanie przewodów",
                description="Zewrzyj końcówki przewodów pomiarowych i wykonaj kompensację (przycisk ZERO) rezystancji przewodów.",
                tip="Kompensacja eliminuje wpływ rezystancji przewodów pomiarowych na wynik.",
                image=METER_IMAGES["test_lead"]
            ),
            InstructionStep(
                step_number=4,
                title="Pomiar",
                description="Podłącz jeden przewód do szyny PE w rozdzielnicy, drugi do badanego punktu (gniazdko, obudowa urządzenia).",
                tip="Mierz od rozdzielnicy do najdalszego punktu obwodu.",
                image=METER_IMAGES["crocodile"]
            ),
            InstructionStep(
                step_number=5,
                title="Odczyt i ocena",
                description="Odczytaj rezystancję [Ω]. Maksymalna dopuszczalna wartość zależy od przekroju przewodu PE.",
                warning="Wartość >1 Ω wskazuje na problem z ciągłością przewodu ochronnego!",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Zakres: 0.00-400 Ω", "Prąd: 200 mA (zgodnie z EN 61557-4)", "Napięcie otwarte: 4-24 V", "Rozdzielczość: 0.01 Ω"],
        safety_notes=[
            "WYŁĄCZ napięcie przed pomiarem!",
            "Skompensuj rezystancję przewodów pomiarowych",
            "Sprawdź wszystkie punkty przyłączenia PE",
            "Prąd 200mA jest wymagany przez normę"
        ],
        expected_results="<1 Ω dla przewodów ochronnych, <0.1 Ω dla połączeń wyrównawczych głównych"
    ),
    MeasurementFunction(
        id="phase_sequence",
        name="Kolejność Faz",
        icon="RotateCw",
        description="Sprawdzenie prawidłowej kolejności faz L1-L2-L3 w instalacji trójfazowej",
        category="podstawowe",
        color="#8B5CF6",
        main_image=METER_IMAGES["main"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję oznaczoną symbolem kolejności faz (1-2-3). Funkcja służy do sprawdzenia zgodności kolejności faz.",
                tip="Prawidłowa kolejność faz jest niezbędna dla poprawnej pracy silników trójfazowych.",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=2,
                title="Podłączenie przewodów",
                description="Podłącz trzy przewody pomiarowe do trzech faz: L1 (żółty), L2 (czerwony), L3 (niebieski). Użyj sond lub krokodylków.",
                warning="Pomiar wykonywany pod napięciem trójfazowym 400V! Zachowaj szczególną ostrożność.",
                image=METER_IMAGES["probes"]
            ),
            InstructionStep(
                step_number=3,
                title="Odczyt wyniku",
                description="Miernik wskaże kolejność faz: ZGODNA (1-2-3) lub NIEZGODNA (3-2-1). Wyświetli też napięcia międzyfazowe.",
                tip="Przy niezgodnej kolejności zamień dowolne dwie fazy miejscami.",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Napięcie L-L: 95-500 V", "Częstotliwość: 45-65 Hz", "Wskazanie: zgodna/niezgodna", "Wyświetlanie napięć UL1-L2, UL2-L3, UL3-L1"],
        safety_notes=[
            "Pomiar pod napięciem trójfazowym 400V!",
            "Używaj przewodów w dobrym stanie izolacji",
            "Nie dotykaj końcówek sond podczas pomiaru",
            "Kategoria CAT III 600V"
        ],
        expected_results="Kolejność ZGODNA (1-2-3), napięcia międzyfazowe 380-420V"
    ),
    MeasurementFunction(
        id="motor_rotation",
        name="Kierunek Obrotów Silnika",
        icon="RefreshCw",
        description="Określenie kierunku obrotów silnika trójfazowego (prawe/lewe) bez konieczności jego uruchamiania",
        category="podstawowe",
        color="#06B6D4",
        main_image=METER_IMAGES["front"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję testu kierunku obrotów silnika (symbol silnika). Ta funkcja pozwala określić kierunek obrotów bez uruchamiania silnika.",
                tip="Funkcja przydatna przy podłączaniu nowych silników lub po pracach serwisowych.",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=2,
                title="Podłączenie do zasilania",
                description="Podłącz przewody pomiarowe do zacisków zasilania silnika (U, V, W lub L1, L2, L3) w miejscu podłączenia do sieci.",
                warning="Silnik musi być ODŁĄCZONY od zasilania podczas podłączania przewodów!",
                image=METER_IMAGES["crocodile"]
            ),
            InstructionStep(
                step_number=3,
                title="Załączenie zasilania",
                description="Po bezpiecznym podłączeniu przewodów, załącz zasilanie trójfazowe. NIE uruchamiaj silnika.",
                warning="Pomiar wykonywany pod napięciem! Upewnij się, że silnik nie zostanie przypadkowo uruchomiony.",
                image=METER_IMAGES["lcd"]
            ),
            InstructionStep(
                step_number=4,
                title="Odczyt wyniku",
                description="Miernik wskaże kierunek obrotów: PRAWE (zgodnie z ruchem wskazówek zegara) lub LEWE (przeciwnie). Dodatkowo wyświetli napięcia faz.",
                tip="Aby zmienić kierunek obrotów, zamień dowolne dwie fazy zasilania miejscami.",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Napięcie L-L: 95-500 V", "Częstotliwość: 45-65 Hz", "Wskazanie: prawe/lewe", "Symulacja bez uruchamiania silnika"],
        safety_notes=[
            "Odłącz zasilanie przed podłączeniem przewodów!",
            "Upewnij się, że silnik nie zostanie uruchomiony podczas testu",
            "Pomiar wykonywany pod napięciem trójfazowym",
            "Po teście odłącz zasilanie przed odłączeniem przewodów"
        ],
        expected_results="Kierunek PRAWY lub LEWY - zależnie od podłączenia faz"
    )
]

# FAQ data - PO POLSKU
FAQ_DATA: List[FAQ] = [
    FAQ(id="1", question="Jaki prąd testowy wybrać dla RCD 30mA?", answer="Dla standardowego testu używaj 1x IΔn (30mA). Dla pełnego testu czasów wykonaj pomiary przy 0.5x, 1x, 2x i 5x IΔn.", category="rcd"),
    FAQ(id="2", question="Dlaczego pomiar izolacji pokazuje 0 MΩ?", answer="Sprawdź czy napięcie w instalacji jest wyłączone. Wartość 0 oznacza zwarcie lub włączone napięcie zasilające.", category="insulation"),
    FAQ(id="3", question="Jaka jest minimalna rezystancja izolacji?", answer="Dla instalacji nowych: min. 1 MΩ. Dla eksploatowanych: min. 0.5 MΩ przy napięciu pomiarowym 500V DC.", category="insulation"),
    FAQ(id="4", question="Jak często kalibrować miernik MPI-530?", answer="Producent Sonel zaleca kalibrację co 12 miesięcy lub po uszkodzeniu mechanicznym miernika.", category="ogolne"),
    FAQ(id="5", question="Co oznacza błąd 'PE!' podczas pomiaru pętli?", answer="Brak lub zbyt wysoka rezystancja przewodu PE. Sprawdź ciągłość przewodu ochronnego przed pomiarem Zs.", category="loop"),
    FAQ(id="6", question="Jak mierzyć impedancję pętli za RCD bez wyzwalania?", answer="Użyj funkcji Zs RCD (bez wyzwalania) lub wykonaj szybki pomiar L-L (między fazami).", category="loop"),
    FAQ(id="7", question="Jakie są kategorie pomiarowe miernika MPI-530?", answer="MPI-530 spełnia wymagania CAT III 600V i CAT IV 300V zgodnie z normą EN 61010.", category="ogolne"),
    FAQ(id="8", question="Jak rozładować pojemność kabla po pomiarze izolacji?", answer="Miernik MPI-530 automatycznie rozładowuje pojemność po zwolnieniu przycisku START. Poczekaj na sygnał zakończenia.", category="insulation"),
    FAQ(id="9", question="Jak naprawić nieprawidłową kolejność faz?", answer="Zamień dowolne dwie fazy miejscami (np. L1 z L2 lub L2 z L3). Po zamianie ponownie sprawdź kolejność miernikiem.", category="phase_sequence"),
    FAQ(id="10", question="Jak zmienić kierunek obrotów silnika trójfazowego?", answer="Zamień dowolne dwie fazy zasilania silnika miejscami. Spowoduje to zmianę kierunku obrotów na przeciwny.", category="motor_rotation"),
]

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Sonel MPI-530 Interaktywna Instrukcja API", "version": "1.0"}

@api_router.get("/functions", response_model=List[MeasurementFunction])
async def get_all_functions():
    """Pobierz wszystkie funkcje pomiarowe z instrukcjami"""
    return MEASUREMENT_FUNCTIONS

@api_router.get("/functions/{function_id}", response_model=MeasurementFunction)
async def get_function(function_id: str):
    """Pobierz konkretną funkcję pomiarową po ID"""
    for func in MEASUREMENT_FUNCTIONS:
        if func.id == function_id:
            return func
    raise HTTPException(status_code=404, detail=f"Funkcja {function_id} nie znaleziona")

@api_router.get("/images")
async def get_meter_images():
    """Pobierz wszystkie dostępne zdjęcia miernika MPI-530"""
    return METER_IMAGES

@api_router.get("/categories")
async def get_categories():
    """Pobierz wszystkie kategorie funkcji"""
    categories = {}
    for func in MEASUREMENT_FUNCTIONS:
        if func.category not in categories:
            categories[func.category] = {"name": func.category, "functions": []}
        categories[func.category]["functions"].append({
            "id": func.id,
            "name": func.name,
            "icon": func.icon
        })
    return list(categories.values())

@api_router.get("/faq", response_model=List[FAQ])
async def get_faq():
    """Pobierz wszystkie pytania FAQ"""
    return FAQ_DATA

@api_router.get("/faq/{category}")
async def get_faq_by_category(category: str):
    """Pobierz FAQ dla danej kategorii"""
    return [faq for faq in FAQ_DATA if faq.category == category]

@api_router.get("/search")
async def search_instructions(q: str):
    """Wyszukaj w instrukcjach"""
    results = []
    query = q.lower()
    for func in MEASUREMENT_FUNCTIONS:
        # Szukaj w nazwie i opisie funkcji
        if query in func.name.lower() or query in func.description.lower():
            results.append({
                "type": "function",
                "id": func.id,
                "name": func.name,
                "match": "function"
            })
        # Szukaj w krokach
        for step in func.steps:
            if query in step.title.lower() or query in step.description.lower():
                results.append({
                    "type": "step",
                    "function_id": func.id,
                    "function_name": func.name,
                    "step_number": step.step_number,
                    "step_title": step.title,
                    "match": "step"
                })
    # Szukaj w FAQ
    for faq in FAQ_DATA:
        if query in faq.question.lower() or query in faq.answer.lower():
            results.append({
                "type": "faq",
                "id": faq.id,
                "question": faq.question,
                "match": "faq"
            })
    return results

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
