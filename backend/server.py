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
app = FastAPI(title="Sonel MPI-530 Interactive Guide API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class InstructionStep(BaseModel):
    step_number: int
    title: str
    description: str
    warning: Optional[str] = None
    tip: Optional[str] = None

class MeasurementFunction(BaseModel):
    id: str
    name: str
    name_en: str
    icon: str
    description: str
    category: str
    color: str
    steps: List[InstructionStep]
    parameters: List[str]
    safety_notes: List[str]
    expected_results: str

class FAQ(BaseModel):
    id: str
    question: str
    answer: str
    category: str

# Static data for MPI-530 measurement functions
MEASUREMENT_FUNCTIONS: List[MeasurementFunction] = [
    MeasurementFunction(
        id="rcd",
        name="Test RCD / Wyłączników Różnicowoprądowych",
        name_en="RCD Testing",
        icon="Shield",
        description="Pomiar czasu i prądu zadziałania wyłączników różnicowoprądowych (RCD/RCCB)",
        category="safety",
        color="#F39200",
        steps=[
            InstructionStep(
                step_number=1,
                title="Przygotowanie",
                description="Ustaw pokrętło funkcji na pozycję RCD. Upewnij się, że instalacja jest pod napięciem.",
                warning="UWAGA: Pomiar wykonywany pod napięciem! Zachowaj szczególną ostrożność.",
                tip="Sprawdź czy RCD jest załączony przed pomiarem."
            ),
            InstructionStep(
                step_number=2,
                title="Podłączenie przewodów",
                description="Podłącz przewód niebieski do gniazda L/L1/L2, czerwony do gniazda PE. Użyj sondy jednobiegunowej lub adaptera gniazda.",
                warning="Sprawdź poprawność połączeń przed uruchomieniem testu."
            ),
            InstructionStep(
                step_number=3,
                title="Wybór parametrów",
                description="Wybierz typ RCD (AC, A, B), prąd znamionowy (10, 30, 100, 300, 500 mA) oraz mnożnik prądu testowego (0.5x, 1x, 2x, 5x).",
                tip="Dla standardowych RCD domowych używaj typu AC i 30mA."
            ),
            InstructionStep(
                step_number=4,
                title="Wykonanie pomiaru",
                description="Naciśnij przycisk START. Miernik wymusi prąd różnicowy i zmierzy czas zadziałania RCD.",
                tip="Po zadziałaniu RCD, załącz go ponownie przed kolejnym pomiarem."
            ),
            InstructionStep(
                step_number=5,
                title="Odczyt wyniku",
                description="Odczytaj czas zadziałania [ms] oraz napięcie dotykowe [V]. Dla RCD 30mA czas powinien być <300ms przy 1x IΔn."
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
        name_en="Loop Impedance",
        icon="Repeat",
        description="Pomiar impedancji pętli zwarcia L-PE i L-N dla weryfikacji skuteczności ochrony przeciwporażeniowej",
        category="impedance",
        color="#3B82F6",
        steps=[
            InstructionStep(
                step_number=1,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję Zs (impedancja pętli zwarcia). Wybierz tryb L-PE lub L-N.",
                warning="Pomiar wykonywany pod napięciem!"
            ),
            InstructionStep(
                step_number=2,
                title="Podłączenie",
                description="Podłącz adapter gniazda lub użyj sond: L do przewodu fazowego, N do neutralnego, PE do ochronnego.",
                tip="Dla pomiaru L-PE wymagane jest połączenie z przewodem ochronnym."
            ),
            InstructionStep(
                step_number=3,
                title="Ustawienie parametrów",
                description="Wybierz zakres pomiarowy i typ pomiaru (standardowy lub z wysokim prądem pomiarowym dla większej dokładności).",
                tip="Tryb wysokoprądowy daje dokładniejsze wyniki w instalacjach z niską impedancją."
            ),
            InstructionStep(
                step_number=4,
                title="Pomiar",
                description="Naciśnij START. Miernik zmierzy impedancję pętli i wyliczy spodziewany prąd zwarciowy.",
                warning="Podczas pomiaru może nastąpić krótkotrwały przepływ prądu przez instalację."
            ),
            InstructionStep(
                step_number=5,
                title="Analiza wyniku",
                description="Odczytaj Zs [Ω] oraz Ik [A]. Porównaj z wartościami dopuszczalnymi dla danego zabezpieczenia."
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
        name_en="Insulation Resistance",
        icon="Layers",
        description="Pomiar rezystancji izolacji przewodów i urządzeń napięciem do 1000V DC",
        category="insulation",
        color="#10B981",
        steps=[
            InstructionStep(
                step_number=1,
                title="Odłączenie napięcia",
                description="WYŁĄCZ zasilanie instalacji! Odłącz wszystkie odbiorniki wrażliwe na napięcie pomiarowe.",
                warning="BEZWZGLĘDNIE wyłącz napięcie przed pomiarem izolacji! Pomiar wykonywany napięciem do 1000V DC."
            ),
            InstructionStep(
                step_number=2,
                title="Wybór funkcji i napięcia",
                description="Ustaw pokrętło na pozycję RISO. Wybierz napięcie pomiarowe: 50V, 100V, 250V, 500V lub 1000V.",
                tip="Dla instalacji 230V stosuj napięcie pomiarowe 500V. Dla instalacji 400V - 1000V."
            ),
            InstructionStep(
                step_number=3,
                title="Podłączenie przewodów",
                description="Podłącz przewód do badanej izolacji (np. L1-PE, L1-N, L1-L2). Użyj krokodylków lub sond.",
                tip="Dla pomiaru całej instalacji połącz wszystkie fazy razem i mierz względem PE."
            ),
            InstructionStep(
                step_number=4,
                title="Wykonanie pomiaru",
                description="Naciśnij i przytrzymaj START. Miernik przyłoży napięcie pomiarowe i zmierzy rezystancję izolacji.",
                warning="Nie dotykaj badanych obwodów podczas pomiaru - napięcie do 1000V DC!"
            ),
            InstructionStep(
                step_number=5,
                title="Rozładowanie i odczyt",
                description="Po zwolnieniu START, miernik automatycznie rozładuje pojemność. Odczytaj wynik w MΩ.",
                tip="Minimalna wartość dla instalacji nowych: 1 MΩ. Dla eksploatowanych: 0.5 MΩ."
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
        name_en="Earth Resistance",
        icon="Zap",
        description="Pomiar rezystancji uziemienia metodą techniczną lub udarową",
        category="earthing",
        color="#F59E0B",
        steps=[
            InstructionStep(
                step_number=1,
                title="Wybór metody",
                description="Ustaw pokrętło na RE. Wybierz metodę: 3-przewodową (techniczna) lub 2-przewodową (z cęgami).",
                tip="Metoda 3-przewodowa jest dokładniejsza, 2-przewodowa szybsza."
            ),
            InstructionStep(
                step_number=2,
                title="Przygotowanie elektrod",
                description="Dla metody 3p: wbij elektrodę prądową (H) w odległości min. 40m, napięciową (S) w 62% tej odległości.",
                warning="Odłącz badane uziemienie od instalacji przed pomiarem!"
            ),
            InstructionStep(
                step_number=3,
                title="Podłączenie",
                description="Połącz: E - badany uziom, S - elektroda napięciowa, H - elektroda prądowa.",
                tip="Elektrody w jednej linii z badanym uziemieniem."
            ),
            InstructionStep(
                step_number=4,
                title="Pomiar",
                description="Naciśnij START. Miernik zmierzy rezystancję i sprawdzi poprawność pomiaru.",
                tip="Jeśli wynik niestabilny - sprawdź wilgotność gruntu przy elektrodach."
            ),
            InstructionStep(
                step_number=5,
                title="Odczyt",
                description="Odczytaj RE [Ω]. Dla uziemienia ochronnego typowa wartość <10 Ω.",
                warning="Pamiętaj o podłączeniu uziemienia z powrotem do instalacji!"
            )
        ],
        parameters=["Zakres: 0.00-9999 Ω", "Rozdzielczość: 0.01 Ω", "Częstotliwość: 125 Hz", "Prąd pomiarowy: >200 mA"],
        safety_notes=[
            "Odłącz uziemienie od instalacji przed pomiarem",
            "Zachowaj bezpieczną odległość od linii wysokiego napięcia",
            "Elektrody pomocnicze wbijaj w wilgotny grunt"
        ],
        expected_results="<10 Ω dla uziemienia ochronnego, <2 Ω dla uziemienia roboczego"
    ),
    MeasurementFunction(
        id="voltage",
        name="Pomiar Napięcia",
        name_en="Voltage Measurement",
        icon="Activity",
        description="Pomiar napięcia przemiennego AC i stałego DC oraz częstotliwości",
        category="basic",
        color="#6366F1",
        steps=[
            InstructionStep(
                step_number=1,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję U (napięcie). Miernik automatycznie wykrywa AC/DC.",
                tip="Dla pomiaru napięcia między fazami używaj funkcji L-L."
            ),
            InstructionStep(
                step_number=2,
                title="Podłączenie",
                description="Podłącz czerwony przewód do mierzonego punktu, niebieski do punktu odniesienia (N lub PE).",
                warning="Nie przekraczaj maksymalnego napięcia 550V AC!"
            ),
            InstructionStep(
                step_number=3,
                title="Odczyt",
                description="Odczytaj napięcie [V] i częstotliwość [Hz] na wyświetlaczu. TRMS daje dokładny wynik.",
                tip="Dla napięcia między fazami oczekuj ~400V, faza-neutral ~230V."
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
        name_en="Continuity Test",
        icon="Link",
        description="Pomiar ciągłości i rezystancji przewodów ochronnych PE i połączeń wyrównawczych",
        category="continuity",
        color="#EC4899",
        steps=[
            InstructionStep(
                step_number=1,
                title="Odłączenie napięcia",
                description="WYŁĄCZ zasilanie instalacji przed pomiarem ciągłości!",
                warning="Pomiar wykonywany BEZ napięcia w instalacji!"
            ),
            InstructionStep(
                step_number=2,
                title="Wybór funkcji",
                description="Ustaw pokrętło na pozycję RCONT (ciągłość). Wybierz prąd pomiarowy 200mA lub 10A (dla niskich rezystancji).",
                tip="Prąd 200mA wystarczy dla większości pomiarów. 10A dla połączeń wyrównawczych."
            ),
            InstructionStep(
                step_number=3,
                title="Zerowanie przewodów",
                description="Zewrzyj końcówki przewodów pomiarowych i wykonaj kompensację (ZERO) rezystancji przewodów.",
                tip="Kompensacja eliminuje wpływ rezystancji przewodów pomiarowych na wynik."
            ),
            InstructionStep(
                step_number=4,
                title="Pomiar",
                description="Podłącz jeden przewód do szyny PE w rozdzielnicy, drugi do badanego punktu (gniazdko, obudowa).",
                tip="Mierz od rozdzielnicy do najdalszego punktu obwodu."
            ),
            InstructionStep(
                step_number=5,
                title="Odczyt",
                description="Odczytaj rezystancję [Ω]. Maksymalna dopuszczalna wartość zależy od przekroju przewodu.",
                warning="Wartość >1 Ω wskazuje na problem z ciągłością!"
            )
        ],
        parameters=["Zakres: 0.00-999.9 Ω", "Prąd: 200 mA lub 10 A", "Napięcie otwarte: 4-24 V", "Rozdzielczość: 0.01 Ω"],
        safety_notes=[
            "WYŁĄCZ napięcie przed pomiarem!",
            "Skompensuj rezystancję przewodów pomiarowych",
            "Sprawdź wszystkie punkty przyłączenia PE"
        ],
        expected_results="<1 Ω dla przewodów ochronnych, <0.1 Ω dla połączeń wyrównawczych głównych"
    )
]

# FAQ data
FAQ_DATA: List[FAQ] = [
    FAQ(id="1", question="Jaki prąd testowy wybrać dla RCD 30mA?", answer="Dla standardowego testu używaj 1x IΔn (30mA). Dla testu czasów użyj 0.5x, 1x, 2x i 5x.", category="rcd"),
    FAQ(id="2", question="Dlaczego pomiar izolacji pokazuje 0 MΩ?", answer="Sprawdź czy napięcie w instalacji jest wyłączone. Wartość 0 oznacza zwarcie lub włączone napięcie.", category="insulation"),
    FAQ(id="3", question="Jaka jest minimalna rezystancja izolacji?", answer="Dla instalacji nowych: min. 1 MΩ. Dla eksploatowanych: min. 0.5 MΩ przy napięciu 500V DC.", category="insulation"),
    FAQ(id="4", question="Jak często kalibrować miernik?", answer="Producent zaleca kalibrację co 12 miesięcy lub po uszkodzeniu mechanicznym.", category="general"),
    FAQ(id="5", question="Co oznacza błąd 'PE!' podczas pomiaru pętli?", answer="Brak lub zbyt wysoka rezystancja przewodu PE. Sprawdź ciągłość PE przed pomiarem Zs.", category="loop"),
    FAQ(id="6", question="Jak mierzyć impedancję za RCD?", answer="Użyj funkcji Zs bez wyzwalania RCD lub wykonaj pomiar szybki L-L.", category="loop"),
]

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Sonel MPI-530 Interactive Guide API", "version": "1.0"}

@api_router.get("/functions", response_model=List[MeasurementFunction])
async def get_all_functions():
    """Get all measurement functions with instructions"""
    return MEASUREMENT_FUNCTIONS

@api_router.get("/functions/{function_id}", response_model=MeasurementFunction)
async def get_function(function_id: str):
    """Get a specific measurement function by ID"""
    for func in MEASUREMENT_FUNCTIONS:
        if func.id == function_id:
            return func
    raise HTTPException(status_code=404, detail=f"Function {function_id} not found")

@api_router.get("/categories")
async def get_categories():
    """Get all function categories"""
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
    """Get all FAQ items"""
    return FAQ_DATA

@api_router.get("/faq/{category}")
async def get_faq_by_category(category: str):
    """Get FAQ items by category"""
    return [faq for faq in FAQ_DATA if faq.category == category]

@api_router.get("/search")
async def search_instructions(q: str):
    """Search through all instructions"""
    results = []
    query = q.lower()
    for func in MEASUREMENT_FUNCTIONS:
        # Search in function name and description
        if query in func.name.lower() or query in func.description.lower():
            results.append({
                "type": "function",
                "id": func.id,
                "name": func.name,
                "match": "function"
            })
        # Search in steps
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
    # Search in FAQ
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
