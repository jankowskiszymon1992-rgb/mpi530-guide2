from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict
import uuid
from datetime import datetime, timezone
import math
import copy
from translations import (
    get_functions_translations, get_faq_translations,
    get_error_codes_translations, get_quiz_translations,
    get_checklists_translations
)

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

class ProtocolStep(BaseModel):
    step_number: int
    title: str
    description: str
    tip: Optional[str] = None
    image: Optional[str] = None

class ProtocolGuide(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    color: str
    steps: List[ProtocolStep]
    tips: List[str]

class ProtocolTemplate(BaseModel):
    id: str
    name: str
    description: str
    measurements: List[str]
    image: Optional[str] = None

class MeasurementResult(BaseModel):
    point: str
    circuit: str
    protection: str
    value: str
    unit: str
    limit: str
    status: str  # "OK" or "FAIL"
    notes: Optional[str] = None

class ExampleProtocol(BaseModel):
    id: str
    name: str
    object_name: str
    object_address: str
    date: str
    inspector: str
    inspector_cert: str
    meter_serial: str
    meter_calibration: str
    measurements: List[MeasurementResult]
    conclusion: str
    recommendations: List[str]

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
    ),
    MeasurementFunction(
        id="lux",
        name="Pomiar Natężenia Oświetlenia",
        icon="Sun",
        description="Pomiar natężenia oświetlenia w luksach (lx) za pomocą zewnętrznej sondy LP-1 lub LP-10",
        category="dodatkowe",
        color="#FBBF24",
        main_image=METER_IMAGES["lux_probe"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Podłączenie sondy",
                description="Podłącz sondę luksomierza LP-1, LP-10A lub LP-10B do gniazda miniDIN-4P miernika. Użyj adaptera WS-06 jeśli wymagany.",
                tip="Sonda LP-10B ma rozszerzony zakres pomiarowy do 400 klx.",
                image=METER_IMAGES["lux_probe"]
            ),
            InstructionStep(
                step_number=2,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję LUX. Miernik automatycznie wykryje podłączoną sondę.",
                tip="Przed pomiarem odczekaj ok. 1 minutę na stabilizację sondy.",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=3,
                title="Ustawienie sondy",
                description="Umieść sondę w miejscu pomiaru. Fotokomórka powinna być skierowana w stronę źródła światła lub powierzchni roboczej.",
                tip="Dla pomiaru oświetlenia stanowiska pracy, sondę umieść na wysokości blatu (85 cm).",
                image=METER_IMAGES["lux_probe"]
            ),
            InstructionStep(
                step_number=4,
                title="Odczyt wyniku",
                description="Odczytaj natężenie oświetlenia w luksach [lx] lub foot-candles [fc]. Wartość stabilizuje się po kilku sekundach.",
                tip="Norma PN-EN 12464-1 określa minimalne wartości dla różnych stanowisk pracy.",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Zakres: 0-400 klx", "Rozdzielczość: od 0.001 lx", "Jednostki: lx lub fc", "Sondy: LP-1, LP-10A, LP-10B"],
        safety_notes=[
            "Nie narażaj sondy na bezpośrednie światło słoneczne przez dłuższy czas",
            "Unikaj dotykania fotokomórki palcami",
            "Przechowuj sondę w etui ochronnym",
            "Kalibruj sondę co 12 miesięcy"
        ],
        expected_results="Biuro: 500 lx, Produkcja: 300-500 lx, Magazyn: 100-200 lx, Korytarz: 100 lx"
    ),
    MeasurementFunction(
        id="earthing_clamp",
        name="Uziemienie Metodą Cęgową",
        icon="Circle",
        description="Pomiar rezystancji uziemienia metodą dwóch cęgów (2-clamp) bez wbijania elektrod pomocniczych",
        category="uziemienie",
        color="#14B8A6",
        main_image=METER_IMAGES["clamp_set"],
        steps=[
            InstructionStep(
                step_number=1,
                title="Przygotowanie cęgów",
                description="Przygotuj zestaw cęgów: cęgi pomiarowe C-3 oraz cęgi nadawcze N-1. Podłącz je do odpowiednich gniazd miernika.",
                tip="Metoda cęgowa nie wymaga wbijania elektrod - idealna dla utwardzonych powierzchni.",
                image=METER_IMAGES["clamp_set"]
            ),
            InstructionStep(
                step_number=2,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję RE i wybierz metodę 2-cęgową (2C lub 2-clamp). Miernik przejdzie w tryb pomiaru cęgowego.",
                warning="Metoda wymaga, aby uziemienie było częścią zamkniętego obwodu (np. połączone z innymi uziomami).",
                image=METER_IMAGES["main"]
            ),
            InstructionStep(
                step_number=3,
                title="Założenie cęgów",
                description="Załóż cęgi nadawcze N-1 na przewód uziemiający. W odległości min. 30 cm załóż cęgi pomiarowe C-3 na ten sam przewód.",
                tip="Cęgi muszą objąć tylko przewód uziemiający, nie inne przewody równolegle.",
                image=METER_IMAGES["clamp_c3"]
            ),
            InstructionStep(
                step_number=4,
                title="Pomiar",
                description="Naciśnij START. Miernik wymusi prąd przez cęgi nadawcze i zmierzy napięcie na cęgach pomiarowych.",
                tip="Wynik obejmuje rezystancję badanego uziomu oraz równoległe połączenie pozostałych uziomów.",
                image=METER_IMAGES["lcd"]
            ),
            InstructionStep(
                step_number=5,
                title="Interpretacja wyniku",
                description="Odczytaj rezystancję RE [Ω]. Pamiętaj, że wynik to rezystancja badanego uziomu w układzie z innymi uziomami.",
                warning="Metoda cęgowa daje wynik zaniżony jeśli uziomy są połączone równolegle!",
                image=METER_IMAGES["lcd"]
            )
        ],
        parameters=["Zakres: 0.00-99.9 kΩ", "Rozdzielczość: od 0.01 Ω", "Cęgi: C-3 + N-1", "Nie wymaga elektrod pomocniczych"],
        safety_notes=[
            "Metoda wymaga zamkniętego obwodu uziemienia",
            "Cęgi zakładaj tylko na przewód uziemiający",
            "Zachowaj min. 30 cm odstępu między cęgami",
            "Wynik może być zaniżony przy równoległych uziomach"
        ],
        expected_results="<10 Ω dla uziemienia ochronnego (uwzględnij wpływ równoległych uziomów)"
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
    FAQ(id="11", question="Jakie natężenie oświetlenia jest wymagane w biurze?", answer="Zgodnie z normą PN-EN 12464-1, stanowiska biurowe wymagają min. 500 lx. Korytarze 100 lx, archiwa 200 lx.", category="lux"),
    FAQ(id="12", question="Kiedy stosować metodę cęgową pomiaru uziemienia?", answer="Metodę cęgową stosuj gdy nie można wbić elektrod pomocniczych (beton, asfalt) lub gdy uziomy są połączone w zamknięty obwód.", category="earthing_clamp"),
    FAQ(id="13", question="Dlaczego metoda cęgowa daje zaniżony wynik?", answer="Metoda 2-cęgowa mierzy rezystancję uziomu w połączeniu równoległym z innymi uziomami. Rzeczywista rezystancja pojedynczego uziomu jest wyższa.", category="earthing_clamp"),
]

# Zdjęcia protokołów i oprogramowania
PROTOCOL_IMAGES = {
    "reports_plus_box": "https://cdn.sonel.com/Zdjecia/Programy/Programy+komputerowe/Sonel+Reports+PLUS/image-thumb__36489__img-product-thumb/blank-box-reports-plus_mHqcbIA.webp",
    "reports_plus_screen": "https://cdn.sonel.com/Zdjecia/Programy/Programy+komputerowe/Sonel+Reports+PLUS/image-thumb__36489__img-product-thumb/blank-box-reports-plus_mHqcbIA.webp",
    "pe6_protocol": "https://cdn.sonel.com/Zdjecia/Programy/Programy+komputerowe/Sonel+PE+6/pe6-screen.png",
}

# Instrukcje protokołów - Sonel Reports Plus
PROTOCOL_GUIDES: List[ProtocolGuide] = [
    ProtocolGuide(
        id="reports_plus_basics",
        name="Sonel Reports Plus - Podstawy",
        description="Jak rozpocząć pracę z programem Sonel Reports Plus do tworzenia protokołów",
        icon="FileText",
        color="#3B82F6",
        steps=[
            ProtocolStep(
                step_number=1,
                title="Instalacja programu",
                description="Pobierz Sonel Reports Plus ze strony sonel.pl (sekcja Oprogramowanie). Zainstaluj na komputerze z Windows 10/11. Program jest bezpłatny dla użytkowników mierników Sonel.",
                tip="Wymagany system: Windows 10 lub Windows 11.",
                image=PROTOCOL_IMAGES["reports_plus_box"]
            ),
            ProtocolStep(
                step_number=2,
                title="Utworzenie nowego projektu",
                description="Uruchom program i wybierz 'Nowy projekt'. Wprowadź dane: nazwa obiektu, adres, inwestor, wykonawca pomiarów, data.",
                tip="Możesz zapisać szablon danych wykonawcy do ponownego użycia."
            ),
            ProtocolStep(
                step_number=3,
                title="Struktura drzewa obiektu",
                description="Zbuduj strukturę budynku: dodaj piętra, pomieszczenia, rozdzielnice. Dla każdego pomieszczenia możesz dodać obwody i punkty pomiarowe.",
                tip="Struktura drzewiasta pozwala na czytelną organizację wyników."
            ),
            ProtocolStep(
                step_number=4,
                title="Dodawanie punktów pomiarowych",
                description="W każdym pomieszczeniu dodaj punkty pomiarowe: gniazdka, oświetlenie, urządzenia stałe. Określ typ zabezpieczenia (bezpiecznik, wyłącznik).",
                tip="Program zawiera bibliotekę bezpieczników i zabezpieczeń."
            ),
            ProtocolStep(
                step_number=5,
                title="Transfer struktury do miernika",
                description="Podłącz miernik MPI-530 przez USB. Wybierz 'Wyślij strukturę do miernika'. Struktura zostanie załadowana do pamięci miernika.",
                tip="Dzięki temu wyniki pomiarów będą automatycznie przypisane do punktów."
            )
        ],
        tips=[
            "Zawsze twórz kopię zapasową projektu przed wysłaniem do miernika",
            "Struktura może zawierać zdjęcia schematów instalacji",
            "Program automatycznie ocenia wyniki wg norm"
        ]
    ),
    ProtocolGuide(
        id="download_results",
        name="Pobieranie wyników z miernika",
        description="Jak pobrać wyniki pomiarów z MPI-530 do programu Sonel Reports Plus",
        icon="Download",
        color="#10B981",
        steps=[
            ProtocolStep(
                step_number=1,
                title="Podłączenie miernika",
                description="Podłącz miernik MPI-530 do komputera kablem USB. Włącz miernik. Program automatycznie wykryje urządzenie.",
                tip="Użyj oryginalnego kabla USB dołączonego do miernika."
            ),
            ProtocolStep(
                step_number=2,
                title="Wybór danych do pobrania",
                description="W programie wybierz 'Pobierz dane z miernika'. Wybierz zakres: cała pamięć lub wybrane pomiary.",
                tip="Możesz pobrać tylko nowe pomiary od ostatniego transferu."
            ),
            ProtocolStep(
                step_number=3,
                title="Przypisanie do struktury",
                description="Wyniki zostaną automatycznie przypisane do punktów pomiarowych zgodnie ze strukturą wysłaną wcześniej do miernika.",
                tip="Pomiary wykonane bez struktury można ręcznie przypisać do punktów."
            ),
            ProtocolStep(
                step_number=4,
                title="Weryfikacja wyników",
                description="Program automatycznie oceni wyniki: POZYTYWNY (zielony) lub NEGATYWNY (czerwony) wg norm i ustawień zabezpieczeń.",
                tip="Kliknij na wynik aby zobaczyć szczegóły i warunki oceny."
            )
        ],
        tips=[
            "Regularnie pobieraj wyniki - pamięć miernika jest ograniczona",
            "Wyniki są oceniane automatycznie wg norm PN-HD 60364",
            "Możesz zmienić kryteria oceny w ustawieniach projektu"
        ]
    ),
    ProtocolGuide(
        id="generate_protocol",
        name="Generowanie protokołu",
        description="Jak wygenerować gotowy protokół pomiarowy do wydruku lub PDF",
        icon="Printer",
        color="#F39200",
        steps=[
            ProtocolStep(
                step_number=1,
                title="Sprawdzenie kompletności",
                description="Przed generowaniem protokołu sprawdź czy wszystkie wymagane pomiary są wykonane. Program oznaczy brakujące pomiary.",
                tip="Wymagane minimum: ciągłość PE, izolacja, RCD (jeśli jest), pętla zwarcia."
            ),
            ProtocolStep(
                step_number=2,
                title="Wybór szablonu protokołu",
                description="Wybierz 'Generuj protokół'. Wybierz szablon: protokół odbiorczy, protokół okresowy, lub własny szablon.",
                tip="Możesz stworzyć własne szablony protokołów."
            ),
            ProtocolStep(
                step_number=3,
                title="Uzupełnienie danych nagłówka",
                description="Uzupełnij dane: numer protokołu, data, dane zleceniodawcy, cel badania (odbiór/przegląd okresowy).",
                tip="Dane wykonawcy i uprawnień zapisz w profilu do ponownego użycia."
            ),
            ProtocolStep(
                step_number=4,
                title="Podgląd i edycja",
                description="Przejrzyj podgląd protokołu. Możesz dodać uwagi, zalecenia, lub edytować opisy.",
                tip="Dodaj zdjęcia rozdzielnic lub problemów znalezionych podczas pomiarów."
            ),
            ProtocolStep(
                step_number=5,
                title="Eksport i wydruk",
                description="Eksportuj protokół do PDF lub wydrukuj bezpośrednio. Możesz też wydrukować etykiety na punkty pomiarowe.",
                tip="PDF zawiera podpis cyfrowy z datą wygenerowania."
            )
        ],
        tips=[
            "Protokół powinien zawierać: dane obiektu, zakres pomiarów, wyniki, ocenę, zalecenia",
            "Przechowuj protokoły min. 5 lat zgodnie z przepisami",
            "Możesz wysłać protokół emailem bezpośrednio z programu"
        ]
    ),
    ProtocolGuide(
        id="pe6_migration",
        name="Migracja z Sonel PE6",
        description="Jak przenieść dane ze starego programu PE6 do Sonel Reports Plus",
        icon="FolderSync",
        color="#8B5CF6",
        steps=[
            ProtocolStep(
                step_number=1,
                title="Eksport z PE6",
                description="W programie Sonel PE6 otwórz projekt. Wybierz 'Eksportuj' i zapisz plik w formacie .pe6 lub .xml.",
                tip="PE6 to starsze oprogramowanie - Sonel Reports Plus ma więcej funkcji."
            ),
            ProtocolStep(
                step_number=2,
                title="Import do Reports Plus",
                description="W Sonel Reports Plus wybierz 'Importuj projekt'. Wskaż plik wyeksportowany z PE6.",
                tip="Import zachowuje strukturę i wyniki pomiarów."
            ),
            ProtocolStep(
                step_number=3,
                title="Weryfikacja danych",
                description="Sprawdź zaimportowane dane. Uzupełnij brakujące informacje (np. zdjęcia, schematy).",
                tip="Niektóre funkcje PE6 mogą wymagać ręcznej konwersji."
            )
        ],
        tips=[
            "Sonel Reports Plus zastępuje PE6 i PE5",
            "Reports Plus ma lepszą integrację z nowymi miernikami",
            "Zachowaj kopię oryginalnych plików PE6 na wszelki wypadek"
        ]
    )
]

# Przykładowe szablony protokołów
PROTOCOL_TEMPLATES: List[ProtocolTemplate] = [
    ProtocolTemplate(
        id="reception",
        name="Protokół odbioru instalacji elektrycznej",
        description="Pełny protokół pomiarów odbiorczych nowej instalacji zgodny z normą PN-HD 60364",
        measurements=[
            "Oględziny instalacji",
            "Ciągłość przewodów ochronnych (PE)",
            "Rezystancja izolacji",
            "Ochrona przed dotykiem pośrednim (Zs)",
            "Badanie wyłączników RCD",
            "Sprawdzenie kolejności faz",
            "Pomiar rezystancji uziemienia"
        ]
    ),
    ProtocolTemplate(
        id="periodic",
        name="Protokół przeglądu okresowego",
        description="Protokół pomiarów okresowych instalacji eksploatowanej (co 5 lat lub częściej)",
        measurements=[
            "Oględziny instalacji - stan techniczny",
            "Ciągłość przewodów ochronnych",
            "Rezystancja izolacji (min. 0.5 MΩ)",
            "Skuteczność ochrony przeciwporażeniowej",
            "Badanie wyłączników RCD",
            "Sprawdzenie zabezpieczeń"
        ]
    ),
    ProtocolTemplate(
        id="rcd_only",
        name="Protokół badania wyłączników RCD",
        description="Skrócony protokół badania samych wyłączników różnicowoprądowych",
        measurements=[
            "Test RCD przy 0.5x IΔn",
            "Test RCD przy 1x IΔn (czas i napięcie dotykowe)",
            "Test RCD przy 2x IΔn",
            "Test RCD przy 5x IΔn",
            "Test przycisku TEST"
        ]
    ),
    ProtocolTemplate(
        id="earthing",
        name="Protokół pomiaru uziemień",
        description="Protokół pomiarów rezystancji uziemień ochronnych i roboczych",
        measurements=[
            "Oględziny instalacji uziemiającej",
            "Pomiar rezystancji uziemienia metodą techniczną",
            "Pomiar rezystywności gruntu (opcjonalnie)",
            "Sprawdzenie połączeń wyrównawczych",
            "Ocena stanu uziomów"
        ]
    ),
    ProtocolTemplate(
        id="lighting",
        name="Protokół pomiaru oświetlenia",
        description="Protokół pomiarów natężenia oświetlenia stanowisk pracy wg PN-EN 12464-1",
        measurements=[
            "Identyfikacja stanowisk pracy",
            "Pomiar natężenia oświetlenia [lx]",
            "Pomiar równomierności oświetlenia",
            "Ocena olśnienia (UGR)",
            "Porównanie z wymaganiami normy"
        ]
    )
]

# Przykładowe wypełnione protokoły
EXAMPLE_PROTOCOLS: List[ExampleProtocol] = [
    ExampleProtocol(
        id="example_reception",
        name="Przykład: Protokół odbioru mieszkania",
        object_name="Mieszkanie nr 15",
        object_address="ul. Kwiatowa 10/15, 00-001 Warszawa",
        date="2024-01-15",
        inspector="Jan Kowalski",
        inspector_cert="E-1234/2020",
        meter_serial="MPI-530 S/N: 123456",
        meter_calibration="2024-06-15",
        measurements=[
            MeasurementResult(point="Kuchnia G1", circuit="1", protection="B16", value="0.12", unit="Ω", limit="<1 Ω", status="OK", notes="Ciągłość PE"),
            MeasurementResult(point="Kuchnia G1", circuit="1", protection="B16", value="245", unit="MΩ", limit=">1 MΩ", status="OK", notes="Izolacja 500V"),
            MeasurementResult(point="Kuchnia G1", circuit="1", protection="B16", value="0.38", unit="Ω", limit="<1.15 Ω", status="OK", notes="Zs L-PE"),
            MeasurementResult(point="Salon G2", circuit="2", protection="B16", value="0.15", unit="Ω", limit="<1 Ω", status="OK", notes="Ciągłość PE"),
            MeasurementResult(point="Salon G2", circuit="2", protection="B16", value="312", unit="MΩ", limit=">1 MΩ", status="OK", notes="Izolacja 500V"),
            MeasurementResult(point="Salon G2", circuit="2", protection="B16", value="0.42", unit="Ω", limit="<1.15 Ω", status="OK", notes="Zs L-PE"),
            MeasurementResult(point="Łazienka G3", circuit="3", protection="B16", value="0.18", unit="Ω", limit="<1 Ω", status="OK", notes="Ciągłość PE"),
            MeasurementResult(point="Łazienka G3", circuit="3", protection="B16", value="198", unit="MΩ", limit=">1 MΩ", status="OK", notes="Izolacja 500V"),
            MeasurementResult(point="Łazienka G3", circuit="3", protection="B16", value="0.51", unit="Ω", limit="<1.15 Ω", status="OK", notes="Zs L-PE"),
            MeasurementResult(point="RCD Łazienka", circuit="3", protection="30mA AC", value="18.5", unit="ms", limit="<300 ms", status="OK", notes="RCD 1xIΔn"),
            MeasurementResult(point="RCD Łazienka", circuit="3", protection="30mA AC", value="12.1", unit="ms", limit="<40 ms", status="OK", notes="RCD 5xIΔn"),
            MeasurementResult(point="Sypialnia G4", circuit="4", protection="B10", value="0.14", unit="Ω", limit="<1 Ω", status="OK", notes="Ciągłość PE"),
            MeasurementResult(point="Sypialnia G4", circuit="4", protection="B10", value="289", unit="MΩ", limit=">1 MΩ", status="OK", notes="Izolacja 500V"),
            MeasurementResult(point="Sypialnia G4", circuit="4", protection="B10", value="0.45", unit="Ω", limit="<1.84 Ω", status="OK", notes="Zs L-PE"),
            MeasurementResult(point="Rozdzielnica", circuit="-", protection="-", value="ZGODNA", unit="-", limit="1-2-3", status="OK", notes="Kolejność faz"),
        ],
        conclusion="POZYTYWNA - Instalacja elektryczna spełnia wymagania normy PN-HD 60364",
        recommendations=[
            "Zaleca się wykonanie przeglądu okresowego za 5 lat",
            "Zachować protokół w dokumentacji budynku"
        ]
    ),
    ExampleProtocol(
        id="example_periodic",
        name="Przykład: Protokół przeglądu okresowego",
        object_name="Lokal usługowy - Sklep ABC",
        object_address="ul. Handlowa 5, 00-002 Kraków",
        date="2024-02-20",
        inspector="Anna Nowak",
        inspector_cert="E-5678/2019",
        meter_serial="MPI-530 S/N: 789012",
        meter_calibration="2023-12-01",
        measurements=[
            MeasurementResult(point="Oświetlenie sala", circuit="1", protection="B10", value="0.22", unit="Ω", limit="<1 Ω", status="OK", notes="Ciągłość PE"),
            MeasurementResult(point="Oświetlenie sala", circuit="1", protection="B10", value="85", unit="MΩ", limit=">0.5 MΩ", status="OK", notes="Izolacja - instalacja eksploatowana"),
            MeasurementResult(point="Oświetlenie sala", circuit="1", protection="B10", value="0.68", unit="Ω", limit="<1.84 Ω", status="OK", notes="Zs L-PE"),
            MeasurementResult(point="Gniazdka lada", circuit="2", protection="B16", value="0.19", unit="Ω", limit="<1 Ω", status="OK", notes="Ciągłość PE"),
            MeasurementResult(point="Gniazdka lada", circuit="2", protection="B16", value="0.42", unit="MΩ", limit=">0.5 MΩ", status="FAIL", notes="Izolacja - PONIŻEJ NORMY!"),
            MeasurementResult(point="Gniazdka lada", circuit="2", protection="B16", value="0.55", unit="Ω", limit="<1.15 Ω", status="OK", notes="Zs L-PE"),
            MeasurementResult(point="RCD główny", circuit="-", protection="30mA AC", value="22.3", unit="ms", limit="<300 ms", status="OK", notes="RCD 1xIΔn"),
            MeasurementResult(point="Zaplecze G3", circuit="3", protection="B16", value="0.28", unit="Ω", limit="<1 Ω", status="OK", notes="Ciągłość PE"),
            MeasurementResult(point="Zaplecze G3", circuit="3", protection="B16", value="156", unit="MΩ", limit=">0.5 MΩ", status="OK", notes="Izolacja 500V"),
        ],
        conclusion="NEGATYWNA - Wykryto usterkę wymagającą naprawy",
        recommendations=[
            "PILNE: Naprawa izolacji obwodu nr 2 (gniazdka lada) - wartość 0.42 MΩ poniżej wymaganego minimum 0.5 MΩ",
            "Sprawdzić stan przewodów w obwodzie nr 2",
            "Po naprawie wykonać ponowny pomiar izolacji",
            "Kolejny przegląd okresowy za 5 lat po usunięciu usterki"
        ]
    ),
    ExampleProtocol(
        id="example_rcd",
        name="Przykład: Protokół badania RCD",
        object_name="Dom jednorodzinny",
        object_address="ul. Słoneczna 25, 00-003 Gdańsk",
        date="2024-03-10",
        inspector="Piotr Wiśniewski",
        inspector_cert="E-9012/2021",
        meter_serial="MPI-530 S/N: 345678",
        meter_calibration="2024-02-28",
        measurements=[
            MeasurementResult(point="RCD F1 (łazienki)", circuit="1-3", protection="30mA typ A", value="28.5", unit="V", limit="<50 V", status="OK", notes="Napięcie dotykowe Uc"),
            MeasurementResult(point="RCD F1 (łazienki)", circuit="1-3", protection="30mA typ A", value="NIE", unit="-", limit="-", status="OK", notes="Test 0.5x IΔn - brak zadziałania"),
            MeasurementResult(point="RCD F1 (łazienki)", circuit="1-3", protection="30mA typ A", value="24.2", unit="ms", limit="<300 ms", status="OK", notes="Test 1x IΔn (30mA)"),
            MeasurementResult(point="RCD F1 (łazienki)", circuit="1-3", protection="30mA typ A", value="15.8", unit="ms", limit="<150 ms", status="OK", notes="Test 2x IΔn (60mA)"),
            MeasurementResult(point="RCD F1 (łazienki)", circuit="1-3", protection="30mA typ A", value="11.2", unit="ms", limit="<40 ms", status="OK", notes="Test 5x IΔn (150mA)"),
            MeasurementResult(point="RCD F1 (łazienki)", circuit="1-3", protection="30mA typ A", value="TAK", unit="-", limit="-", status="OK", notes="Test przycisku TEST"),
            MeasurementResult(point="RCD F2 (kuchnia)", circuit="4-5", protection="30mA typ AC", value="31.2", unit="V", limit="<50 V", status="OK", notes="Napięcie dotykowe Uc"),
            MeasurementResult(point="RCD F2 (kuchnia)", circuit="4-5", protection="30mA typ AC", value="NIE", unit="-", limit="-", status="OK", notes="Test 0.5x IΔn - brak zadziałania"),
            MeasurementResult(point="RCD F2 (kuchnia)", circuit="4-5", protection="30mA typ AC", value="19.8", unit="ms", limit="<300 ms", status="OK", notes="Test 1x IΔn (30mA)"),
            MeasurementResult(point="RCD F2 (kuchnia)", circuit="4-5", protection="30mA typ AC", value="12.4", unit="ms", limit="<150 ms", status="OK", notes="Test 2x IΔn (60mA)"),
            MeasurementResult(point="RCD F2 (kuchnia)", circuit="4-5", protection="30mA typ AC", value="9.8", unit="ms", limit="<40 ms", status="OK", notes="Test 5x IΔn (150mA)"),
            MeasurementResult(point="RCD F2 (kuchnia)", circuit="4-5", protection="30mA typ AC", value="TAK", unit="-", limit="-", status="OK", notes="Test przycisku TEST"),
            MeasurementResult(point="RCD F3 (garaż)", circuit="6", protection="30mA typ A", value="35.8", unit="V", limit="<50 V", status="OK", notes="Napięcie dotykowe Uc"),
            MeasurementResult(point="RCD F3 (garaż)", circuit="6", protection="30mA typ A", value="NIE", unit="-", limit="-", status="OK", notes="Test 0.5x IΔn - brak zadziałania"),
            MeasurementResult(point="RCD F3 (garaż)", circuit="6", protection="30mA typ A", value="21.5", unit="ms", limit="<300 ms", status="OK", notes="Test 1x IΔn (30mA)"),
            MeasurementResult(point="RCD F3 (garaż)", circuit="6", protection="30mA typ A", value="14.2", unit="ms", limit="<150 ms", status="OK", notes="Test 2x IΔn (60mA)"),
            MeasurementResult(point="RCD F3 (garaż)", circuit="6", protection="30mA typ A", value="10.5", unit="ms", limit="<40 ms", status="OK", notes="Test 5x IΔn (150mA)"),
            MeasurementResult(point="RCD F3 (garaż)", circuit="6", protection="30mA typ A", value="TAK", unit="-", limit="-", status="OK", notes="Test przycisku TEST"),
        ],
        conclusion="POZYTYWNA - Wszystkie wyłączniki różnicowoprądowe działają prawidłowo",
        recommendations=[
            "Wszystkie RCD spełniają wymagania normy PN-HD 60364-4-41",
            "Zaleca się comiesięczne testowanie przyciskiem TEST",
            "Następne badanie okresowe za 5 lat"
        ]
    ),
    ExampleProtocol(
        id="example_earthing",
        name="Przykład: Protokół pomiaru uziemień",
        object_name="Budynek biurowy OMEGA",
        object_address="ul. Biznesowa 100, 00-004 Poznań",
        date="2024-04-05",
        inspector="Marek Zieliński",
        inspector_cert="E-3456/2018",
        meter_serial="MPI-530 S/N: 567890",
        meter_calibration="2024-01-20",
        measurements=[
            MeasurementResult(point="Uziom główny U1", circuit="-", protection="-", value="2.8", unit="Ω", limit="<10 Ω", status="OK", notes="Metoda techniczna 3p"),
            MeasurementResult(point="Uziom główny U1", circuit="-", protection="-", value="85", unit="Ωm", limit="-", status="OK", notes="Rezystywność gruntu"),
            MeasurementResult(point="Uziom odgromowy U2", circuit="-", protection="-", value="4.2", unit="Ω", limit="<10 Ω", status="OK", notes="Metoda techniczna 3p"),
            MeasurementResult(point="Uziom odgromowy U3", circuit="-", protection="-", value="3.9", unit="Ω", limit="<10 Ω", status="OK", notes="Metoda techniczna 3p"),
            MeasurementResult(point="Połączenie wyrównawcze PW1", circuit="-", protection="-", value="0.05", unit="Ω", limit="<0.1 Ω", status="OK", notes="Szyna PE - rury wodne"),
            MeasurementResult(point="Połączenie wyrównawcze PW2", circuit="-", protection="-", value="0.08", unit="Ω", limit="<0.1 Ω", status="OK", notes="Szyna PE - rury gazowe"),
            MeasurementResult(point="Połączenie wyrównawcze PW3", circuit="-", protection="-", value="0.04", unit="Ω", limit="<0.1 Ω", status="OK", notes="Szyna PE - konstrukcja stalowa"),
        ],
        conclusion="POZYTYWNA - Instalacja uziemiająca spełnia wymagania",
        recommendations=[
            "Stan techniczny uziomów dobry",
            "Połączenia wyrównawcze prawidłowe",
            "Kolejna kontrola za 5 lat lub po modernizacji instalacji"
        ]
    ),
    ExampleProtocol(
        id="example_lighting",
        name="Przykład: Protokół pomiaru oświetlenia",
        object_name="Biuro projektowe XYZ",
        object_address="ul. Techniczna 50/3, 00-005 Wrocław",
        date="2024-05-12",
        inspector="Katarzyna Adamska",
        inspector_cert="E-7890/2022",
        meter_serial="MPI-530 S/N: 901234 + LP-10B",
        meter_calibration="2024-03-15",
        measurements=[
            MeasurementResult(point="Stanowisko CAD 1", circuit="-", protection="-", value="620", unit="lx", limit=">500 lx", status="OK", notes="Praca przy monitorze"),
            MeasurementResult(point="Stanowisko CAD 2", circuit="-", protection="-", value="585", unit="lx", limit=">500 lx", status="OK", notes="Praca przy monitorze"),
            MeasurementResult(point="Stanowisko CAD 3", circuit="-", protection="-", value="540", unit="lx", limit=">500 lx", status="OK", notes="Praca przy monitorze"),
            MeasurementResult(point="Biurko kierownika", circuit="-", protection="-", value="510", unit="lx", limit=">500 lx", status="OK", notes="Praca biurowa"),
            MeasurementResult(point="Sala konferencyjna", circuit="-", protection="-", value="380", unit="lx", limit=">300 lx", status="OK", notes="Spotkania"),
            MeasurementResult(point="Korytarz", circuit="-", protection="-", value="125", unit="lx", limit=">100 lx", status="OK", notes="Komunikacja"),
            MeasurementResult(point="Archiwum", circuit="-", protection="-", value="185", unit="lx", limit=">200 lx", status="FAIL", notes="PONIŻEJ NORMY"),
            MeasurementResult(point="Kuchnia pracownicza", circuit="-", protection="-", value="245", unit="lx", limit=">200 lx", status="OK", notes="Pomieszczenie socjalne"),
            MeasurementResult(point="WC", circuit="-", protection="-", value="210", unit="lx", limit=">200 lx", status="OK", notes="Sanitariat"),
        ],
        conclusion="NEGATYWNA - Wykryto niedobór oświetlenia w archiwum",
        recommendations=[
            "Wymiana lub dodanie oprawy oświetleniowej w archiwum (wymagane min. 200 lx, zmierzono 185 lx)",
            "Po naprawie wykonać ponowny pomiar",
            "Pozostałe pomieszczenia spełniają wymagania PN-EN 12464-1"
        ]
    )
]

# ============================================
# NARZĘDZIA - Kalkulator, Tabele Norm, Błędy, Schematy
# ============================================

# Tabele maksymalnych impedancji pętli zwarcia dla różnych zabezpieczeń
# Zgodnie z PN-HD 60364-4-41 dla Uo=230V, czas 0.4s (obwody końcowe)
ZS_MAX_TABLES = {
    "B": {
        "6": {"Ia": 30, "Zs_max": 7.67, "time": "0.4s"},
        "10": {"Ia": 50, "Zs_max": 4.60, "time": "0.4s"},
        "13": {"Ia": 65, "Zs_max": 3.54, "time": "0.4s"},
        "16": {"Ia": 80, "Zs_max": 2.88, "time": "0.4s"},
        "20": {"Ia": 100, "Zs_max": 2.30, "time": "0.4s"},
        "25": {"Ia": 125, "Zs_max": 1.84, "time": "0.4s"},
        "32": {"Ia": 160, "Zs_max": 1.44, "time": "0.4s"},
        "40": {"Ia": 200, "Zs_max": 1.15, "time": "0.4s"},
        "50": {"Ia": 250, "Zs_max": 0.92, "time": "0.4s"},
        "63": {"Ia": 315, "Zs_max": 0.73, "time": "0.4s"},
    },
    "C": {
        "6": {"Ia": 60, "Zs_max": 3.83, "time": "0.4s"},
        "10": {"Ia": 100, "Zs_max": 2.30, "time": "0.4s"},
        "13": {"Ia": 130, "Zs_max": 1.77, "time": "0.4s"},
        "16": {"Ia": 160, "Zs_max": 1.44, "time": "0.4s"},
        "20": {"Ia": 200, "Zs_max": 1.15, "time": "0.4s"},
        "25": {"Ia": 250, "Zs_max": 0.92, "time": "0.4s"},
        "32": {"Ia": 320, "Zs_max": 0.72, "time": "0.4s"},
        "40": {"Ia": 400, "Zs_max": 0.58, "time": "0.4s"},
        "50": {"Ia": 500, "Zs_max": 0.46, "time": "0.4s"},
        "63": {"Ia": 630, "Zs_max": 0.37, "time": "0.4s"},
    },
    "D": {
        "6": {"Ia": 120, "Zs_max": 1.92, "time": "0.4s"},
        "10": {"Ia": 200, "Zs_max": 1.15, "time": "0.4s"},
        "16": {"Ia": 320, "Zs_max": 0.72, "time": "0.4s"},
        "20": {"Ia": 400, "Zs_max": 0.58, "time": "0.4s"},
        "25": {"Ia": 500, "Zs_max": 0.46, "time": "0.4s"},
        "32": {"Ia": 640, "Zs_max": 0.36, "time": "0.4s"},
    }
}

# Tabele norm - rezystancja izolacji
INSULATION_NORMS = [
    {"voltage_range": "SELV/PELV", "test_voltage": 250, "min_resistance": 0.5, "unit": "MΩ"},
    {"voltage_range": "do 500V", "test_voltage": 500, "min_resistance": 1.0, "unit": "MΩ"},
    {"voltage_range": "powyżej 500V", "test_voltage": 1000, "min_resistance": 1.0, "unit": "MΩ"},
    {"voltage_range": "instalacja eksploatowana", "test_voltage": 500, "min_resistance": 0.5, "unit": "MΩ"},
]

# Tabele norm - czasy zadziałania RCD
RCD_TIMES = [
    {"type": "AC/A", "multiplier": "0.5x", "max_time_ms": None, "description": "Nie powinien zadziałać"},
    {"type": "AC/A", "multiplier": "1x", "max_time_ms": 300, "description": "Standardowy test"},
    {"type": "AC/A", "multiplier": "2x", "max_time_ms": 150, "description": "Podwójny prąd"},
    {"type": "AC/A", "multiplier": "5x", "max_time_ms": 40, "description": "Pięciokrotny prąd"},
    {"type": "S (selektywny)", "multiplier": "1x", "max_time_ms": 500, "description": "RCD selektywny"},
    {"type": "S (selektywny)", "multiplier": "2x", "max_time_ms": 200, "description": "RCD selektywny"},
    {"type": "S (selektywny)", "multiplier": "5x", "max_time_ms": 150, "description": "RCD selektywny"},
]

# Tabele norm - oświetlenie PN-EN 12464-1
LIGHTING_NORMS = [
    {"area": "Biuro - praca przy komputerze", "min_lux": 500, "ugr_max": 19},
    {"area": "Biuro - pisanie, czytanie", "min_lux": 500, "ugr_max": 19},
    {"area": "Sala konferencyjna", "min_lux": 300, "ugr_max": 22},
    {"area": "Recepcja", "min_lux": 300, "ugr_max": 22},
    {"area": "Archiwum", "min_lux": 200, "ugr_max": 25},
    {"area": "Korytarz, komunikacja", "min_lux": 100, "ugr_max": 28},
    {"area": "Schody", "min_lux": 150, "ugr_max": 25},
    {"area": "Toalety", "min_lux": 200, "ugr_max": 25},
    {"area": "Magazyn", "min_lux": 100, "ugr_max": 25},
    {"area": "Hala produkcyjna - prace zgrubne", "min_lux": 200, "ugr_max": 25},
    {"area": "Hala produkcyjna - prace precyzyjne", "min_lux": 500, "ugr_max": 19},
    {"area": "Kontrola jakości", "min_lux": 1000, "ugr_max": 16},
    {"area": "Warsztat mechaniczny", "min_lux": 300, "ugr_max": 22},
    {"area": "Sklep - strefa sprzedaży", "min_lux": 300, "ugr_max": 22},
    {"area": "Kuchnia", "min_lux": 500, "ugr_max": 22},
    {"area": "Garaż", "min_lux": 75, "ugr_max": 25},
]

# Kody błędów miernika MPI-530
ERROR_CODES = [
    {
        "code": "PE!",
        "name": "Brak PE",
        "description": "Brak połączenia z przewodem ochronnym PE lub zbyt wysoka rezystancja",
        "causes": ["Uszkodzony przewód PE", "Brak ciągłości PE", "Zły kontakt w gnieździe", "Niepodłączony przewód ochronny"],
        "solutions": ["Sprawdź ciągłość przewodu PE", "Sprawdź połączenia w rozdzielnicy", "Wyczyść styki gniazda", "Wykonaj pomiar ciągłości PE"]
    },
    {
        "code": "Hi",
        "name": "Wartość powyżej zakresu",
        "description": "Zmierzona wartość przekracza zakres pomiarowy miernika",
        "causes": ["Zbyt wysoka impedancja", "Brak połączenia", "Przerwa w obwodzie"],
        "solutions": ["Sprawdź połączenia pomiarowe", "Sprawdź czy obwód jest zamknięty", "Użyj wyższego zakresu pomiarowego"]
    },
    {
        "code": "Lo",
        "name": "Wartość poniżej zakresu",
        "description": "Zmierzona wartość jest poniżej dolnej granicy zakresu",
        "causes": ["Zwarcie w obwodzie", "Zbyt niska rezystancja", "Błąd podłączenia"],
        "solutions": ["Sprawdź czy nie ma zwarcia", "Użyj niższego zakresu", "Sprawdź poprawność podłączenia"]
    },
    {
        "code": "OFL",
        "name": "Przepełnienie (Overflow)",
        "description": "Przekroczenie maksymalnego zakresu pomiarowego",
        "causes": ["Bardzo wysoka rezystancja/impedancja", "Obwód otwarty", "Uszkodzona izolacja przewodów pomiarowych"],
        "solutions": ["Sprawdź ciągłość obwodu", "Sprawdź przewody pomiarowe", "Zmień zakres pomiarowy"]
    },
    {
        "code": "U>",
        "name": "Napięcie zbyt wysokie",
        "description": "Napięcie w obwodzie przekracza dopuszczalną wartość dla danego pomiaru",
        "causes": ["Napięcie >253V", "Zakłócenia w sieci", "Błędne podłączenie"],
        "solutions": ["Sprawdź napięcie w instalacji", "Poczekaj na stabilizację sieci", "Sprawdź podłączenie"]
    },
    {
        "code": "U<",
        "name": "Napięcie zbyt niskie",
        "description": "Napięcie w obwodzie jest zbyt niskie do wykonania pomiaru",
        "causes": ["Napięcie <180V", "Zanik fazy", "Przeciążenie sieci"],
        "solutions": ["Sprawdź napięcie zasilania", "Sprawdź bezpieczniki", "Poczekaj na przywrócenie napięcia"]
    },
    {
        "code": "f?",
        "name": "Błędna częstotliwość",
        "description": "Częstotliwość sieci poza zakresem 45-65 Hz",
        "causes": ["Praca z generatora", "Zakłócenia sieci", "Niestabilne źródło"],
        "solutions": ["Sprawdź źródło zasilania", "Podłącz do stabilnej sieci", "Użyj UPS"]
    },
    {
        "code": "RCD!",
        "name": "RCD zadziałał",
        "description": "Wyłącznik różnicowoprądowy zadziałał podczas pomiaru",
        "causes": ["Pomiar impedancji pętli wyzwolił RCD", "RCD bardzo czuły", "Normalny efekt pomiaru"],
        "solutions": ["Załącz ponownie RCD", "Użyj funkcji pomiaru bez wyzwalania RCD", "Wykonaj pomiar L-L"]
    },
    {
        "code": "CAL",
        "name": "Wymagana kalibracja",
        "description": "Upłynął termin kalibracji lub miernik wymaga sprawdzenia",
        "causes": ["Przekroczony termin kalibracji", "Uszkodzenie mechaniczne", "Błąd wewnętrzny"],
        "solutions": ["Wyślij miernik do kalibracji", "Sprawdź datę ostatniej kalibracji", "Skontaktuj się z serwisem Sonel"]
    },
    {
        "code": "bAt",
        "name": "Słaba bateria",
        "description": "Niski poziom naładowania akumulatora",
        "causes": ["Rozładowany akumulator", "Zużyty akumulator", "Długa praca bez ładowania"],
        "solutions": ["Naładuj akumulator", "Wymień akumulator na nowy", "Podłącz zasilacz"]
    },
    {
        "code": "Err",
        "name": "Błąd ogólny",
        "description": "Wystąpił nieoczekiwany błąd podczas pomiaru",
        "causes": ["Zakłócenia elektromagnetyczne", "Błąd wewnętrzny", "Niestabilne warunki pomiaru"],
        "solutions": ["Powtórz pomiar", "Odsuń miernik od źródeł zakłóceń", "Zrestartuj miernik"]
    },
    {
        "code": "L-PE",
        "name": "Pomiar L-PE niemożliwy",
        "description": "Nie można wykonać pomiaru impedancji L-PE",
        "causes": ["Brak PE", "Za wysoka rezystancja PE", "Błędne podłączenie"],
        "solutions": ["Sprawdź ciągłość PE", "Wykonaj najpierw test ciągłości", "Sprawdź podłączenia"]
    },
]

# Schematy podłączeń
CONNECTION_DIAGRAMS = [
    {
        "id": "rcd_test",
        "name": "Test RCD",
        "description": "Podłączenie do pomiaru czasu zadziałania wyłącznika różnicowoprądowego",
        "connections": [
            {"terminal": "L/L1", "color": "#FF0000", "connect_to": "Faza (L)", "cable": "Czerwony"},
            {"terminal": "N", "color": "#0000FF", "connect_to": "Neutralny (N)", "cable": "Niebieski"},
            {"terminal": "PE", "color": "#00FF00", "connect_to": "Ochronny (PE)", "cable": "Zielono-żółty"},
        ],
        "notes": ["Można użyć adaptera WS-03 do gniazda", "Instalacja musi być pod napięciem", "RCD zadziała podczas testu"],
        "image": "adapter_ws03"
    },
    {
        "id": "loop_impedance",
        "name": "Impedancja pętli zwarcia",
        "description": "Podłączenie do pomiaru impedancji pętli zwarcia L-PE lub L-N",
        "connections": [
            {"terminal": "L/L1", "color": "#FF0000", "connect_to": "Faza (L)", "cable": "Czerwony"},
            {"terminal": "N", "color": "#0000FF", "connect_to": "Neutralny (N)", "cable": "Niebieski"},
            {"terminal": "PE", "color": "#00FF00", "connect_to": "Ochronny (PE)", "cable": "Zielono-żółty"},
        ],
        "notes": ["Dla L-PE: wymagane połączenie z PE", "Dla L-N: pomiar impedancji faza-neutral", "Może wyzwolić RCD"],
        "image": "adapter_ws03"
    },
    {
        "id": "insulation",
        "name": "Rezystancja izolacji",
        "description": "Podłączenie do pomiaru rezystancji izolacji między przewodami",
        "connections": [
            {"terminal": "L/L1", "color": "#FF0000", "connect_to": "Przewód badany (L)", "cable": "Czerwony"},
            {"terminal": "PE", "color": "#00FF00", "connect_to": "Przewód odniesienia (PE/N)", "cable": "Zielono-żółty"},
        ],
        "notes": ["WYŁĄCZ NAPIĘCIE przed pomiarem!", "Odłącz odbiorniki wrażliwe", "Napięcie pomiarowe do 1000V DC"],
        "image": "crocodile"
    },
    {
        "id": "continuity",
        "name": "Ciągłość PE",
        "description": "Podłączenie do pomiaru ciągłości przewodu ochronnego",
        "connections": [
            {"terminal": "L/L1", "color": "#FF0000", "connect_to": "Szyna PE w rozdzielnicy", "cable": "Czerwony"},
            {"terminal": "PE", "color": "#00FF00", "connect_to": "Badany punkt (gniazdko)", "cable": "Zielono-żółty"},
        ],
        "notes": ["WYŁĄCZ NAPIĘCIE!", "Wykonaj kompensację przewodów (ZERO)", "Prąd pomiarowy 200mA"],
        "image": "test_lead"
    },
    {
        "id": "earthing_3p",
        "name": "Uziemienie metodą 3-przewodową",
        "description": "Podłączenie do pomiaru rezystancji uziemienia metodą techniczną",
        "connections": [
            {"terminal": "E", "color": "#00FF00", "connect_to": "Badany uziom", "cable": "Zielono-żółty"},
            {"terminal": "S", "color": "#FFFF00", "connect_to": "Elektroda napięciowa (62% odległości)", "cable": "Żółty"},
            {"terminal": "H", "color": "#FF0000", "connect_to": "Elektroda prądowa (min. 40m)", "cable": "Czerwony"},
        ],
        "notes": ["Odłącz uziom od instalacji!", "Elektrody w linii prostej", "Wbij elektrody w wilgotny grunt"],
        "image": "earth_probe"
    },
    {
        "id": "earthing_clamp",
        "name": "Uziemienie metodą cęgową",
        "description": "Podłączenie do pomiaru uziemienia bez elektrod pomocniczych",
        "connections": [
            {"terminal": "C3", "color": "#FF0000", "connect_to": "Cęgi pomiarowe na przewód PE", "cable": "C-3"},
            {"terminal": "N1", "color": "#0000FF", "connect_to": "Cęgi nadawcze na przewód PE (min. 30cm od C3)", "cable": "N-1"},
        ],
        "notes": ["Uziemienie musi być w zamkniętym obwodzie", "Min. 30cm między cęgami", "Wynik może być zaniżony"],
        "image": "clamp_set"
    },
    {
        "id": "phase_sequence",
        "name": "Kolejność faz",
        "description": "Podłączenie do sprawdzenia kolejności faz L1-L2-L3",
        "connections": [
            {"terminal": "L1", "color": "#FFFF00", "connect_to": "Faza L1", "cable": "Żółty"},
            {"terminal": "L2", "color": "#FF0000", "connect_to": "Faza L2", "cable": "Czerwony"},
            {"terminal": "L3", "color": "#0000FF", "connect_to": "Faza L3", "cable": "Niebieski"},
        ],
        "notes": ["Pomiar pod napięciem 3x400V!", "Wynik: ZGODNA lub NIEZGODNA", "Zamień 2 fazy aby naprawić"],
        "image": "probes"
    },
    {
        "id": "lux",
        "name": "Pomiar oświetlenia",
        "description": "Podłączenie sondy luksomierza LP-1/LP-10",
        "connections": [
            {"terminal": "miniDIN-4P", "color": "#FFFF00", "connect_to": "Sonda LP-1 lub LP-10", "cable": "Kabel sondy"},
        ],
        "notes": ["Odczekaj 1 min na stabilizację", "Sondę ustaw na wysokości blatu (85cm)", "Kieruj fotokomórkę w stronę światła"],
        "image": "lux_probe"
    },
]

# ============================================
# KALKULATOR PRZEWODÓW - tabele przekrojów
# ============================================

CABLE_SECTIONS = {
    "cu_pvc": {  # Miedź w izolacji PVC
        "description": "Przewód miedziany w izolacji PVC",
        "sections": [
            {"mm2": 1.5, "Iz_A": 15.5, "R_ohm_km": 12.1},
            {"mm2": 2.5, "Iz_A": 21, "R_ohm_km": 7.41},
            {"mm2": 4, "Iz_A": 28, "R_ohm_km": 4.61},
            {"mm2": 6, "Iz_A": 36, "R_ohm_km": 3.08},
            {"mm2": 10, "Iz_A": 50, "R_ohm_km": 1.83},
            {"mm2": 16, "Iz_A": 68, "R_ohm_km": 1.15},
            {"mm2": 25, "Iz_A": 89, "R_ohm_km": 0.727},
            {"mm2": 35, "Iz_A": 110, "R_ohm_km": 0.524},
            {"mm2": 50, "Iz_A": 134, "R_ohm_km": 0.387},
            {"mm2": 70, "Iz_A": 171, "R_ohm_km": 0.268},
            {"mm2": 95, "Iz_A": 207, "R_ohm_km": 0.193},
            {"mm2": 120, "Iz_A": 239, "R_ohm_km": 0.153},
        ]
    },
    "al_pvc": {  # Aluminium w izolacji PVC
        "description": "Przewód aluminiowy w izolacji PVC",
        "sections": [
            {"mm2": 16, "Iz_A": 53, "R_ohm_km": 1.91},
            {"mm2": 25, "Iz_A": 70, "R_ohm_km": 1.2},
            {"mm2": 35, "Iz_A": 86, "R_ohm_km": 0.868},
            {"mm2": 50, "Iz_A": 104, "R_ohm_km": 0.641},
            {"mm2": 70, "Iz_A": 133, "R_ohm_km": 0.443},
            {"mm2": 95, "Iz_A": 161, "R_ohm_km": 0.32},
            {"mm2": 120, "Iz_A": 186, "R_ohm_km": 0.253},
        ]
    }
}

# ============================================
# CHECKLISTA BEZPIECZEŃSTWA
# ============================================

SAFETY_CHECKLISTS = {
    "rcd": {
        "name": "Test RCD",
        "items": [
            {"id": 1, "text": "Sprawdziłem stan przewodów pomiarowych", "critical": True},
            {"id": 2, "text": "Upewniłem się, że instalacja jest pod napięciem", "critical": True},
            {"id": 3, "text": "Ostrzegłem użytkowników o możliwym zaniku zasilania", "critical": True},
            {"id": 4, "text": "Sprawdziłem ciągłość PE przed testem RCD", "critical": False},
            {"id": 5, "text": "Wybrałem prawidłowy typ RCD (AC/A/B)", "critical": False},
        ]
    },
    "insulation": {
        "name": "Pomiar izolacji",
        "items": [
            {"id": 1, "text": "WYŁĄCZYŁEM zasilanie instalacji", "critical": True},
            {"id": 2, "text": "Zweryfikowałem brak napięcia miernikiem", "critical": True},
            {"id": 3, "text": "Odłączyłem odbiorniki wrażliwe na napięcie pomiarowe", "critical": True},
            {"id": 4, "text": "Zabezpieczyłem miejsce pracy przed przypadkowym załączeniem", "critical": True},
            {"id": 5, "text": "Wybrałem odpowiednie napięcie pomiarowe (500V/1000V)", "critical": False},
        ]
    },
    "loop": {
        "name": "Impedancja pętli",
        "items": [
            {"id": 1, "text": "Sprawdziłem stan przewodów pomiarowych", "critical": True},
            {"id": 2, "text": "Upewniłem się, że instalacja jest pod napięciem", "critical": True},
            {"id": 3, "text": "Sprawdziłem ciągłość PE", "critical": True},
            {"id": 4, "text": "Uwzględniłem możliwość zadziałania RCD", "critical": False},
        ]
    },
    "continuity": {
        "name": "Ciągłość PE",
        "items": [
            {"id": 1, "text": "WYŁĄCZYŁEM zasilanie instalacji", "critical": True},
            {"id": 2, "text": "Zweryfikowałem brak napięcia miernikiem", "critical": True},
            {"id": 3, "text": "Wykonałem kompensację przewodów (ZERO)", "critical": False},
        ]
    },
    "earthing": {
        "name": "Uziemienie",
        "items": [
            {"id": 1, "text": "Odłączyłem badany uziom od instalacji", "critical": True},
            {"id": 2, "text": "Sprawdziłem bezpieczną odległość od linii WN", "critical": True},
            {"id": 3, "text": "Wbiłem elektrody pomocnicze w odpowiednich odległościach", "critical": True},
            {"id": 4, "text": "Sprawdziłem wilgotność gruntu przy elektrodach", "critical": False},
        ]
    },
    "general": {
        "name": "Ogólna kontrola przed pomiarem",
        "items": [
            {"id": 1, "text": "Miernik jest skalibrowany (data ważności)", "critical": True},
            {"id": 2, "text": "Bateria miernika jest naładowana", "critical": True},
            {"id": 3, "text": "Przewody pomiarowe są w dobrym stanie", "critical": True},
            {"id": 4, "text": "Mam odpowiednie uprawnienia SEP", "critical": True},
            {"id": 5, "text": "Używam środków ochrony osobistej", "critical": True},
        ]
    }
}

# ============================================
# QUIZ - pytania i odpowiedzi
# ============================================

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Jaka jest minimalna rezystancja izolacji dla nowej instalacji przy napięciu pomiarowym 500V?",
        "options": ["0.5 MΩ", "1 MΩ", "2 MΩ", "0.25 MΩ"],
        "correct": 1,
        "explanation": "Zgodnie z PN-HD 60364-6, minimalna rezystancja izolacji dla instalacji o napięciu do 500V wynosi 1 MΩ."
    },
    {
        "id": 2,
        "question": "Jaki jest maksymalny czas zadziałania RCD 30mA przy prądzie 1x IΔn?",
        "options": ["40 ms", "150 ms", "300 ms", "500 ms"],
        "correct": 2,
        "explanation": "Dla RCD typu AC i A, maksymalny czas zadziałania przy prądzie 1x IΔn wynosi 300 ms."
    },
    {
        "id": 3,
        "question": "Przy jakim mnożniku prądu RCD NIE powinien zadziałać?",
        "options": ["0.5x IΔn", "1x IΔn", "2x IΔn", "5x IΔn"],
        "correct": 0,
        "explanation": "RCD nie powinien zadziałać przy prądzie 0.5x IΔn - to test sprawdzający, czy RCD nie jest zbyt czuły."
    },
    {
        "id": 4,
        "question": "Co oznacza błąd 'PE!' na mierniku MPI-530?",
        "options": ["Przekroczony zakres", "Brak połączenia PE", "Słaba bateria", "Błąd kalibracji"],
        "correct": 1,
        "explanation": "Błąd PE! oznacza brak lub zbyt wysoką rezystancję przewodu ochronnego PE."
    },
    {
        "id": 5,
        "question": "Jakie napięcie pomiarowe należy wybrać do pomiaru izolacji instalacji 400V?",
        "options": ["250V", "500V", "1000V", "100V"],
        "correct": 2,
        "explanation": "Dla instalacji o napięciu powyżej 500V należy stosować napięcie pomiarowe 1000V DC."
    },
    {
        "id": 6,
        "question": "W jakiej odległości od badanego uziomu należy wbić elektrodę prądową (H)?",
        "options": ["10 m", "20 m", "Min. 40 m", "5 m"],
        "correct": 2,
        "explanation": "Elektroda prądowa powinna być w odległości minimum 40 m od badanego uziomu."
    },
    {
        "id": 7,
        "question": "Gdzie umieścić elektrodę napięciową (S) przy pomiarze uziemienia metodą 3-przewodową?",
        "options": ["Przy uziomie", "W połowie odległości", "W 62% odległości do elektrody H", "Przy elektrodzie H"],
        "correct": 2,
        "explanation": "Elektroda napięciowa powinna być umieszczona w 62% odległości między uziomem a elektrodą prądową."
    },
    {
        "id": 8,
        "question": "Jaki prąd pomiarowy jest wymagany przy pomiarze ciągłości PE zgodnie z normą?",
        "options": ["10 mA", "50 mA", "200 mA", "1 A"],
        "correct": 2,
        "explanation": "Zgodnie z EN 61557-4, pomiar ciągłości PE należy wykonywać prądem min. 200 mA."
    },
    {
        "id": 9,
        "question": "Co należy zrobić PRZED pomiarem rezystancji izolacji?",
        "options": ["Załączyć napięcie", "Wyłączyć napięcie i odłączyć odbiorniki", "Zmierzyć RCD", "Sprawdzić kolejność faz"],
        "correct": 1,
        "explanation": "Przed pomiarem izolacji BEZWZGLĘDNIE należy wyłączyć napięcie i odłączyć wrażliwe odbiorniki."
    },
    {
        "id": 10,
        "question": "Jakie minimalne natężenie oświetlenia jest wymagane na stanowisku biurowym?",
        "options": ["200 lx", "300 lx", "500 lx", "750 lx"],
        "correct": 2,
        "explanation": "Zgodnie z PN-EN 12464-1, stanowiska biurowe wymagają minimum 500 lx."
    },
    {
        "id": 11,
        "question": "Jaka jest maksymalna impedancja pętli zwarcia dla zabezpieczenia B16 (czas 0.4s)?",
        "options": ["1.15 Ω", "2.88 Ω", "4.60 Ω", "0.92 Ω"],
        "correct": 1,
        "explanation": "Dla zabezpieczenia B16 przy czasie 0.4s i napięciu 230V, Zs max = 2.88 Ω."
    },
    {
        "id": 12,
        "question": "Co oznacza 'ZGODNA' kolejność faz?",
        "options": ["L3-L2-L1", "L1-L2-L3", "L2-L1-L3", "Dowolna"],
        "correct": 1,
        "explanation": "Zgodna kolejność faz to L1-L2-L3 (obroty prawe)."
    },
    {
        "id": 13,
        "question": "Jak często należy kalibrować miernik MPI-530?",
        "options": ["Co 6 miesięcy", "Co 12 miesięcy", "Co 24 miesiące", "Co 5 lat"],
        "correct": 1,
        "explanation": "Producent Sonel zaleca kalibrację miernika co 12 miesięcy."
    },
    {
        "id": 14,
        "question": "Jaka jest kategoria pomiarowa miernika MPI-530?",
        "options": ["CAT I", "CAT II", "CAT III 600V / CAT IV 300V", "CAT V"],
        "correct": 2,
        "explanation": "MPI-530 spełnia wymagania CAT III 600V i CAT IV 300V."
    },
    {
        "id": 15,
        "question": "Czy można wykonać pomiar impedancji pętli za wyłącznikiem RCD bez jego wyzwolenia?",
        "options": ["Nie, RCD zawsze zadziała", "Tak, używając funkcji Zs RCD lub pomiaru L-L", "Nie, trzeba wymontować RCD", "Tylko przy wyłączonym napięciu"],
        "correct": 1,
        "explanation": "MPI-530 posiada funkcję pomiaru Zs bez wyzwalania RCD oraz możliwość pomiaru L-L."
    }
]

# API Routes

def translate_function(func, lang):
    """Apply translation to a measurement function if available."""
    if lang == "pl":
        return func
    translations = get_functions_translations(lang)
    if not translations or func.id not in translations:
        return func
    tr = translations[func.id]
    d = func.model_dump()
    d["name"] = tr["name"]
    d["description"] = tr["description"]
    d["parameters"] = tr["parameters"]
    d["safety_notes"] = tr["safety_notes"]
    d["expected_results"] = tr["expected_results"]
    for i, step in enumerate(d["steps"]):
        if i < len(tr["steps"]):
            ts = tr["steps"][i]
            step["title"] = ts.get("title", step["title"])
            step["description"] = ts.get("description", step["description"])
            if "warning" in ts:
                step["warning"] = ts["warning"]
            if "tip" in ts:
                step["tip"] = ts["tip"]
    return MeasurementFunction(**d)

@api_router.get("/")
async def root():
    return {"message": "Sonel MPI-530 Interactive Guide API", "version": "1.1"}

@api_router.get("/functions", response_model=List[MeasurementFunction])
async def get_all_functions(lang: str = Query("pl", regex="^(pl|en|de)$")):
    return [translate_function(f, lang) for f in MEASUREMENT_FUNCTIONS]

@api_router.get("/functions/{function_id}", response_model=MeasurementFunction)
async def get_function(function_id: str, lang: str = Query("pl", regex="^(pl|en|de)$")):
    for func in MEASUREMENT_FUNCTIONS:
        if func.id == function_id:
            return translate_function(func, lang)
    raise HTTPException(status_code=404, detail=f"Function {function_id} not found")

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

@api_router.get("/faq")
async def get_faq(lang: str = Query("pl", regex="^(pl|en|de)$")):
    tr = get_faq_translations(lang)
    if tr:
        return [FAQ(**item) for item in tr]
    return FAQ_DATA

@api_router.get("/faq/{category}")
async def get_faq_by_category(category: str, lang: str = Query("pl", regex="^(pl|en|de)$")):
    tr = get_faq_translations(lang)
    if tr:
        return [FAQ(**item) for item in tr if item["category"] == category]
    return [faq for faq in FAQ_DATA if faq.category == category]

@api_router.get("/protocols/guides", response_model=List[ProtocolGuide])
async def get_protocol_guides():
    """Pobierz instrukcje tworzenia protokołów w Sonel Reports Plus"""
    return PROTOCOL_GUIDES

@api_router.get("/protocols/guides/{guide_id}", response_model=ProtocolGuide)
async def get_protocol_guide(guide_id: str):
    """Pobierz konkretną instrukcję protokołu"""
    for guide in PROTOCOL_GUIDES:
        if guide.id == guide_id:
            return guide
    raise HTTPException(status_code=404, detail=f"Instrukcja {guide_id} nie znaleziona")

@api_router.get("/protocols/templates", response_model=List[ProtocolTemplate])
async def get_protocol_templates():
    """Pobierz szablony protokołów pomiarowych"""
    return PROTOCOL_TEMPLATES

@api_router.get("/protocols/templates/{template_id}", response_model=ProtocolTemplate)
async def get_protocol_template(template_id: str):
    """Pobierz konkretny szablon protokołu"""
    for template in PROTOCOL_TEMPLATES:
        if template.id == template_id:
            return template
    raise HTTPException(status_code=404, detail=f"Szablon {template_id} nie znaleziony")

@api_router.get("/protocols/examples", response_model=List[ExampleProtocol])
async def get_example_protocols():
    """Pobierz przykładowe wypełnione protokoły"""
    return EXAMPLE_PROTOCOLS

@api_router.get("/protocols/examples/{example_id}", response_model=ExampleProtocol)
async def get_example_protocol(example_id: str):
    """Pobierz konkretny przykładowy protokół"""
    for example in EXAMPLE_PROTOCOLS:
        if example.id == example_id:
            return example
    raise HTTPException(status_code=404, detail=f"Przykład {example_id} nie znaleziony")

# ============================================
# NARZĘDZIA API
# ============================================

@api_router.get("/tools/calculator")
async def calculate_fault_current(zs: float, voltage: float = 230):
    """Kalkulator prądu zwarciowego Ik = Uo/Zs"""
    if zs <= 0:
        raise HTTPException(status_code=400, detail="Impedancja musi być większa od 0")
    
    ik = voltage / zs
    
    # Znajdź odpowiednie zabezpieczenie
    recommendations = []
    for char_type, values in ZS_MAX_TABLES.items():
        for rating, data in values.items():
            if zs <= data["Zs_max"]:
                recommendations.append({
                    "type": f"{char_type}{rating}",
                    "Ia": data["Ia"],
                    "Zs_max": data["Zs_max"],
                    "margin": round((data["Zs_max"] - zs) / data["Zs_max"] * 100, 1)
                })
    
    # Sortuj po marginesie
    recommendations.sort(key=lambda x: x["margin"], reverse=True)
    
    return {
        "input": {"Zs": zs, "Uo": voltage},
        "result": {
            "Ik": round(ik, 1),
            "unit": "A",
            "description": f"Prąd zwarciowy przy Zs={zs}Ω i Uo={voltage}V"
        },
        "recommendations": recommendations[:10],
        "formula": "Ik = Uo / Zs"
    }

@api_router.get("/tools/zs-tables")
async def get_zs_tables():
    """Pobierz tabele maksymalnych impedancji pętli dla zabezpieczeń"""
    return {
        "description": "Maksymalne impedancje pętli zwarcia wg PN-HD 60364-4-41",
        "voltage": "230V",
        "time": "0.4s (obwody końcowe)",
        "tables": ZS_MAX_TABLES
    }

@api_router.get("/tools/norms")
async def get_all_norms():
    """Pobierz wszystkie tabele norm"""
    return {
        "insulation": {
            "title": "Minimalna rezystancja izolacji",
            "standard": "PN-HD 60364-6",
            "data": INSULATION_NORMS
        },
        "rcd_times": {
            "title": "Maksymalne czasy zadziałania RCD",
            "standard": "PN-HD 60364-4-41",
            "data": RCD_TIMES
        },
        "lighting": {
            "title": "Minimalne natężenie oświetlenia",
            "standard": "PN-EN 12464-1",
            "data": LIGHTING_NORMS
        },
        "zs_tables": {
            "title": "Maksymalne impedancje pętli zwarcia",
            "standard": "PN-HD 60364-4-41",
            "voltage": "230V, czas 0.4s",
            "data": ZS_MAX_TABLES
        }
    }

@api_router.get("/tools/error-codes")
async def get_error_codes(lang: str = Query("pl", regex="^(pl|en|de)$")):
    tr = get_error_codes_translations(lang)
    return tr if tr else ERROR_CODES

@api_router.get("/tools/error-codes/{code}")
async def get_error_code(code: str):
    """Pobierz szczegóły konkretnego kodu błędu"""
    for error in ERROR_CODES:
        if error["code"].lower() == code.lower():
            return error
    raise HTTPException(status_code=404, detail=f"Kod błędu '{code}' nie znaleziony")

@api_router.get("/tools/diagrams")
async def get_connection_diagrams():
    """Pobierz schematy podłączeń"""
    return CONNECTION_DIAGRAMS

@api_router.get("/tools/diagrams/{diagram_id}")
async def get_connection_diagram(diagram_id: str):
    """Pobierz konkretny schemat podłączenia"""
    for diagram in CONNECTION_DIAGRAMS:
        if diagram["id"] == diagram_id:
            return diagram
    raise HTTPException(status_code=404, detail=f"Schemat '{diagram_id}' nie znaleziony")

# ============================================
# NOWE API - Kalkulator przewodów, Checklista, Quiz
# ============================================

@api_router.get("/tools/cable-calculator")
async def calculate_cable_section(
    power_kw: float,
    voltage: float = 230,
    length_m: float = 10,
    max_drop_percent: float = 3,
    phases: int = 1,
    cable_type: str = "cu_pvc"
):
    """Kalkulator doboru przekroju przewodu"""
    if cable_type not in CABLE_SECTIONS:
        raise HTTPException(status_code=400, detail="Nieznany typ przewodu")
    
    # Oblicz prąd
    if phases == 1:
        current = (power_kw * 1000) / voltage
    else:
        current = (power_kw * 1000) / (voltage * 1.732)
    
    # Oblicz maksymalną rezystancję dla spadku napięcia
    max_voltage_drop = voltage * (max_drop_percent / 100)
    max_resistance = max_voltage_drop / current
    
    # Dla przewodu 2-żyłowego (tam i z powrotem)
    max_r_per_km = (max_resistance * 1000) / (2 * length_m)
    
    # Znajdź odpowiedni przekrój
    cable_data = CABLE_SECTIONS[cable_type]
    recommended = None
    for section in cable_data["sections"]:
        if section["Iz_A"] >= current and section["R_ohm_km"] <= max_r_per_km:
            if recommended is None or section["mm2"] < recommended["mm2"]:
                recommended = section
    
    # Jeśli nie znaleziono dla spadku napięcia, znajdź dla obciążalności
    if recommended is None:
        for section in cable_data["sections"]:
            if section["Iz_A"] >= current:
                recommended = section
                break
    
    # Oblicz rzeczywisty spadek napięcia
    actual_drop = None
    actual_drop_percent = None
    if recommended:
        resistance = 2 * length_m * recommended["R_ohm_km"] / 1000
        actual_drop = current * resistance
        actual_drop_percent = (actual_drop / voltage) * 100
    
    return {
        "input": {
            "power_kw": power_kw,
            "voltage": voltage,
            "length_m": length_m,
            "max_drop_percent": max_drop_percent,
            "phases": phases,
            "cable_type": cable_type
        },
        "calculated": {
            "current_A": round(current, 2),
            "max_resistance_ohm": round(max_resistance, 4)
        },
        "recommended": {
            "section_mm2": recommended["mm2"] if recommended else None,
            "Iz_A": recommended["Iz_A"] if recommended else None,
            "actual_drop_V": round(actual_drop, 2) if actual_drop else None,
            "actual_drop_percent": round(actual_drop_percent, 2) if actual_drop_percent else None
        },
        "all_suitable": [s for s in cable_data["sections"] if s["Iz_A"] >= current]
    }

@api_router.get("/tools/cable-sections")
async def get_cable_sections():
    """Pobierz tabele przekrojów przewodów"""
    return CABLE_SECTIONS

@api_router.get("/tools/checklists")
async def get_all_checklists(lang: str = Query("pl", regex="^(pl|en|de)$")):
    tr = get_checklists_translations(lang)
    return tr if tr else SAFETY_CHECKLISTS

@api_router.get("/tools/checklists/{checklist_id}")
async def get_checklist(checklist_id: str, lang: str = Query("pl", regex="^(pl|en|de)$")):
    tr = get_checklists_translations(lang)
    data = tr if tr else SAFETY_CHECKLISTS
    if checklist_id in data:
        return data[checklist_id]
    raise HTTPException(status_code=404, detail=f"Checklist '{checklist_id}' not found")

@api_router.get("/quiz/questions")
async def get_quiz_questions(lang: str = Query("pl", regex="^(pl|en|de)$")):
    tr = get_quiz_translations(lang)
    source = tr if tr else QUIZ_QUESTIONS
    return [{"id": q["id"], "question": q["question"], "options": q["options"]} for q in source]

@api_router.post("/quiz/check")
async def check_quiz_answers(answers: Dict[int, int], lang: str = Query("pl", regex="^(pl|en|de)$")):
    tr = get_quiz_translations(lang)
    source = tr if tr else QUIZ_QUESTIONS
    results = []
    correct_count = 0
    for q in source:
        user_answer = answers.get(q["id"])
        is_correct = user_answer == q["correct"]
        if is_correct:
            correct_count += 1
        results.append({
            "id": q["id"], "question": q["question"],
            "user_answer": user_answer, "correct_answer": q["correct"],
            "is_correct": is_correct, "explanation": q["explanation"]
        })
    total = len(source)
    percentage = (correct_count / total) * 100
    passed = percentage >= 70
    grade_map = {"pl": ("ZDANY", "NIEZDANY"), "en": ("PASSED", "FAILED"), "de": ("BESTANDEN", "NICHT BESTANDEN")}
    grades = grade_map.get(lang, grade_map["pl"])
    return {
        "results": results,
        "summary": {
            "correct": correct_count, "total": total,
            "percentage": round(percentage, 1), "passed": passed,
            "grade": grades[0] if passed else grades[1]
        }
    }

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
