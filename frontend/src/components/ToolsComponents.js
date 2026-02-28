import { useState, useEffect } from "react";
import axios from "axios";
import { toast } from "sonner";
import { jsPDF } from "jspdf";
import "jspdf-autotable";
import { 
    Calculator, Table2, AlertOctagon, Cable, Wrench,
    CheckCircle2, AlertTriangle, Lightbulb, ChevronRight,
    FileText, Award, ClipboardCheck, Download, Zap
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Cable Calculator Component
export const CableCalculatorTab = () => {
    const [powerInput, setPowerInput] = useState('');
    const [voltageInput, setVoltageInput] = useState('230');
    const [lengthInput, setLengthInput] = useState('10');
    const [dropInput, setDropInput] = useState('3');
    const [phasesInput, setPhasesInput] = useState('1');
    const [calcResult, setCalcResult] = useState(null);

    const handleCalculate = async () => {
        if (!powerInput || parseFloat(powerInput) <= 0) {
            toast.error("Wprowadź poprawną moc");
            return;
        }
        try {
            const response = await axios.get(`${API}/tools/cable-calculator`, {
                params: {
                    power_kw: parseFloat(powerInput),
                    voltage: parseFloat(voltageInput),
                    length_m: parseFloat(lengthInput),
                    max_drop_percent: parseFloat(dropInput),
                    phases: parseInt(phasesInput),
                    cable_type: "cu_pvc"
                }
            });
            setCalcResult(response.data);
        } catch (error) {
            toast.error("Błąd obliczania");
        }
    };

    return (
        <div className="space-y-6">
            <div className="card-industrial">
                <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
                    <Zap className="h-5 w-5 text-yellow-500" />
                    Kalkulator doboru przewodów
                </h3>
                <p className="text-muted-foreground mb-6">
                    Dobierz przekrój przewodu na podstawie mocy, długości i dopuszczalnego spadku napięcia.
                </p>
                
                <div className="grid md:grid-cols-3 gap-4 mb-6">
                    <div>
                        <label className="block text-sm font-bold mb-2">Moc [kW]</label>
                        <Input
                            type="number"
                            step="0.1"
                            value={powerInput}
                            onChange={(e) => setPowerInput(e.target.value)}
                            placeholder="np. 3.5"
                            data-testid="power-input"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-bold mb-2">Napięcie [V]</label>
                        <select 
                            value={voltageInput}
                            onChange={(e) => setVoltageInput(e.target.value)}
                            className="w-full h-10 px-3 border-2 border-input bg-background rounded-sm"
                        >
                            <option value="230">230V (1-fazowe)</option>
                            <option value="400">400V (3-fazowe)</option>
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-bold mb-2">Długość [m]</label>
                        <Input
                            type="number"
                            value={lengthInput}
                            onChange={(e) => setLengthInput(e.target.value)}
                            placeholder="10"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-bold mb-2">Max spadek napięcia [%]</label>
                        <Input
                            type="number"
                            step="0.5"
                            value={dropInput}
                            onChange={(e) => setDropInput(e.target.value)}
                            placeholder="3"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-bold mb-2">Liczba faz</label>
                        <select 
                            value={phasesInput}
                            onChange={(e) => setPhasesInput(e.target.value)}
                            className="w-full h-10 px-3 border-2 border-input bg-background rounded-sm"
                        >
                            <option value="1">1-fazowy</option>
                            <option value="3">3-fazowy</option>
                        </select>
                    </div>
                    <div className="flex items-end">
                        <Button 
                            onClick={handleCalculate}
                            className="bg-yellow-500 text-white w-full hover:bg-yellow-600"
                            data-testid="calc-cable-btn"
                        >
                            Oblicz przekrój
                        </Button>
                    </div>
                </div>

                {calcResult && calcResult.recommended.section_mm2 && (
                    <div className="mt-6 space-y-4">
                        <div className="lcd-result p-6">
                            <div className="text-xs uppercase tracking-wider opacity-70 mb-2">Zalecany przekrój</div>
                            <div className="text-4xl font-mono font-bold">
                                {calcResult.recommended.section_mm2} mm²
                            </div>
                            <div className="grid grid-cols-2 gap-4 mt-4 text-sm">
                                <div>
                                    <span className="opacity-70">Prąd obliczeniowy:</span>
                                    <span className="font-bold ml-2">{calcResult.calculated.current_A} A</span>
                                </div>
                                <div>
                                    <span className="opacity-70">Obciążalność przewodu:</span>
                                    <span className="font-bold ml-2">{calcResult.recommended.Iz_A} A</span>
                                </div>
                                <div>
                                    <span className="opacity-70">Spadek napięcia:</span>
                                    <span className="font-bold ml-2">{calcResult.recommended.actual_drop_V} V ({calcResult.recommended.actual_drop_percent}%)</span>
                                </div>
                            </div>
                        </div>

                        {calcResult.all_suitable.length > 1 && (
                            <div>
                                <h4 className="font-bold mb-3">Inne pasujące przekroje:</h4>
                                <div className="grid grid-cols-4 md:grid-cols-6 gap-2">
                                    {calcResult.all_suitable.map((s, idx) => (
                                        <div key={idx} className={`p-2 text-center border rounded-sm ${s.mm2 === calcResult.recommended.section_mm2 ? 'bg-yellow-500/20 border-yellow-500' : 'border-border'}`}>
                                            <div className="font-bold">{s.mm2} mm²</div>
                                            <div className="text-xs text-muted-foreground">{s.Iz_A} A</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

// Safety Checklist Component
export const SafetyChecklistTab = () => {
    const [checklists, setChecklists] = useState(null);
    const [selectedChecklist, setSelectedChecklist] = useState(null);
    const [checkedItems, setCheckedItems] = useState({});

    useEffect(() => {
        axios.get(`${API}/tools/checklists`)
            .then(res => setChecklists(res.data))
            .catch(() => {});
    }, []);

    const handleCheck = (itemId) => {
        setCheckedItems(prev => ({
            ...prev,
            [itemId]: !prev[itemId]
        }));
    };

    const allCriticalChecked = () => {
        if (!selectedChecklist) return false;
        const criticalItems = checklists[selectedChecklist].items.filter(i => i.critical);
        return criticalItems.every(i => checkedItems[i.id]);
    };

    const resetChecklist = () => {
        setCheckedItems({});
    };

    if (!checklists) return <div className="text-center py-10">Ładowanie...</div>;

    return (
        <div className="space-y-6">
            <h3 className="font-bold text-xl flex items-center gap-2">
                <ClipboardCheck className="h-5 w-5 text-orange-500" />
                Checklista bezpieczeństwa
            </h3>
            
            {!selectedChecklist ? (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {Object.entries(checklists).map(([key, checklist]) => (
                        <button
                            key={key}
                            onClick={() => setSelectedChecklist(key)}
                            className="card-industrial text-left hover:border-orange-500/50"
                        >
                            <h4 className="font-bold">{checklist.name}</h4>
                            <p className="text-sm text-muted-foreground mt-1">
                                {checklist.items.length} punktów do sprawdzenia
                            </p>
                            <ChevronRight className="h-4 w-4 mt-2 text-orange-500" />
                        </button>
                    ))}
                </div>
            ) : (
                <div className="card-industrial">
                    <div className="flex items-center justify-between mb-6">
                        <h4 className="font-bold text-lg">{checklists[selectedChecklist].name}</h4>
                        <Button variant="outline" onClick={() => { setSelectedChecklist(null); resetChecklist(); }}>
                            Wróć
                        </Button>
                    </div>

                    <div className="space-y-3">
                        {checklists[selectedChecklist].items.map((item) => (
                            <label
                                key={item.id}
                                className={`flex items-start gap-3 p-3 border rounded-sm cursor-pointer transition-colors
                                    ${checkedItems[item.id] ? 'bg-green-500/10 border-green-500' : 'border-border hover:border-orange-500/50'}
                                    ${item.critical ? 'border-l-4 border-l-red-500' : ''}
                                `}
                            >
                                <input
                                    type="checkbox"
                                    checked={!!checkedItems[item.id]}
                                    onChange={() => handleCheck(item.id)}
                                    className="mt-1 h-5 w-5"
                                />
                                <div className="flex-1">
                                    <span className={checkedItems[item.id] ? 'line-through text-muted-foreground' : ''}>
                                        {item.text}
                                    </span>
                                    {item.critical && (
                                        <span className="ml-2 text-xs bg-red-500 text-white px-2 py-0.5 rounded-full">
                                            WYMAGANE
                                        </span>
                                    )}
                                </div>
                                {checkedItems[item.id] && (
                                    <CheckCircle2 className="h-5 w-5 text-green-500 flex-shrink-0" />
                                )}
                            </label>
                        ))}
                    </div>

                    <div className="mt-6 pt-6 border-t border-border">
                        {allCriticalChecked() ? (
                            <div className="p-4 bg-green-500/10 border border-green-500 rounded-sm flex items-center gap-3">
                                <CheckCircle2 className="h-6 w-6 text-green-500" />
                                <div>
                                    <p className="font-bold text-green-500">Wszystkie wymagane punkty sprawdzone!</p>
                                    <p className="text-sm text-muted-foreground">Możesz bezpiecznie przystąpić do pomiaru.</p>
                                </div>
                            </div>
                        ) : (
                            <div className="p-4 bg-red-500/10 border border-red-500 rounded-sm flex items-center gap-3">
                                <AlertTriangle className="h-6 w-6 text-red-500" />
                                <div>
                                    <p className="font-bold text-red-500">Nie wszystkie wymagane punkty sprawdzone!</p>
                                    <p className="text-sm text-muted-foreground">Sprawdź wszystkie punkty oznaczone jako WYMAGANE przed pomiarem.</p>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

// Quiz Component
export const QuizTab = () => {
    const [questions, setQuestions] = useState([]);
    const [answers, setAnswers] = useState({});
    const [results, setResults] = useState(null);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [quizStarted, setQuizStarted] = useState(false);

    useEffect(() => {
        axios.get(`${API}/quiz/questions`)
            .then(res => setQuestions(res.data))
            .catch(err => console.error(err));
    }, []);

    const handleAnswer = (questionId, answerIndex) => {
        setAnswers(prev => ({
            ...prev,
            [questionId]: answerIndex
        }));
    };

    const handleSubmit = async () => {
        try {
            const response = await axios.post(`${API}/quiz/check`, answers);
            setResults(response.data);
        } catch (error) {
            toast.error("Błąd sprawdzania odpowiedzi");
        }
    };

    const generateCertificate = () => {
        if (!results || !results.summary.passed) return;

        const doc = new jsPDF();
        const pageWidth = doc.internal.pageSize.getWidth();
        
        // Header
        doc.setFillColor(243, 146, 0);
        doc.rect(0, 0, pageWidth, 40, 'F');
        
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(24);
        doc.setFont('helvetica', 'bold');
        doc.text('CERTYFIKAT', pageWidth / 2, 25, { align: 'center' });
        
        // Body
        doc.setTextColor(0, 0, 0);
        doc.setFontSize(14);
        doc.setFont('helvetica', 'normal');
        doc.text('Niniejszym zaświadcza się, że', pageWidth / 2, 60, { align: 'center' });
        
        doc.setFontSize(20);
        doc.setFont('helvetica', 'bold');
        doc.text('Użytkownik', pageWidth / 2, 80, { align: 'center' });
        
        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        doc.text('ukończył szkolenie z obsługi miernika', pageWidth / 2, 100, { align: 'center' });
        
        doc.setFontSize(18);
        doc.setFont('helvetica', 'bold');
        doc.text('SONEL MPI-530', pageWidth / 2, 115, { align: 'center' });
        
        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        doc.text(`Wynik testu: ${results.summary.correct}/${results.summary.total} (${results.summary.percentage}%)`, pageWidth / 2, 135, { align: 'center' });
        doc.text(`Data: ${new Date().toLocaleDateString('pl-PL')}`, pageWidth / 2, 150, { align: 'center' });
        
        // Footer
        doc.setFontSize(10);
        doc.setTextColor(128, 128, 128);
        doc.text('Certyfikat wygenerowany przez aplikację Sonel MPI-530 Interactive Guide', pageWidth / 2, 280, { align: 'center' });
        
        doc.save('certyfikat_mpi530.pdf');
        toast.success('Certyfikat został pobrany!');
    };

    const resetQuiz = () => {
        setAnswers({});
        setResults(null);
        setCurrentQuestion(0);
        setQuizStarted(false);
    };

    if (questions.length === 0) return <div className="text-center py-10">Ładowanie pytań...</div>;

    if (results) {
        return (
            <div className="space-y-6">
                <div className={`p-6 rounded-sm border ${results.summary.passed ? 'bg-green-500/10 border-green-500' : 'bg-red-500/10 border-red-500'}`}>
                    <div className="flex items-center gap-4">
                        {results.summary.passed ? (
                            <Award className="h-16 w-16 text-green-500" />
                        ) : (
                            <AlertTriangle className="h-16 w-16 text-red-500" />
                        )}
                        <div>
                            <h3 className={`text-3xl font-bold ${results.summary.passed ? 'text-green-500' : 'text-red-500'}`}>
                                {results.summary.grade}
                            </h3>
                            <p className="text-xl">
                                Wynik: {results.summary.correct}/{results.summary.total} ({results.summary.percentage}%)
                            </p>
                            <p className="text-muted-foreground">
                                {results.summary.passed ? 'Gratulacje! Zdałeś test!' : 'Wymagane minimum: 70%'}
                            </p>
                        </div>
                    </div>
                </div>

                {results.summary.passed && (
                    <Button onClick={generateCertificate} className="bg-green-500 text-white">
                        <Download className="h-4 w-4 mr-2" />
                        Pobierz certyfikat PDF
                    </Button>
                )}

                <div className="space-y-4">
                    <h4 className="font-bold">Szczegółowe wyniki:</h4>
                    {results.results.map((r, idx) => (
                        <div key={idx} className={`p-4 border rounded-sm ${r.is_correct ? 'border-green-500/50 bg-green-500/5' : 'border-red-500/50 bg-red-500/5'}`}>
                            <div className="flex items-start gap-3">
                                {r.is_correct ? (
                                    <CheckCircle2 className="h-5 w-5 text-green-500 flex-shrink-0 mt-1" />
                                ) : (
                                    <AlertTriangle className="h-5 w-5 text-red-500 flex-shrink-0 mt-1" />
                                )}
                                <div>
                                    <p className="font-bold">{r.question}</p>
                                    <p className="text-sm text-muted-foreground mt-1">{r.explanation}</p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <Button onClick={resetQuiz} variant="outline">
                    Spróbuj ponownie
                </Button>
            </div>
        );
    }

    if (!quizStarted) {
        return (
            <div className="card-industrial text-center py-10">
                <Award className="h-20 w-20 text-primary mx-auto mb-6" />
                <h3 className="text-2xl font-bold mb-4">Quiz: Obsługa MPI-530</h3>
                <p className="text-muted-foreground mb-6">
                    Test składa się z {questions.length} pytań.<br />
                    Wymagane minimum do zaliczenia: 70%<br />
                    Po zdaniu otrzymasz certyfikat PDF.
                </p>
                <Button onClick={() => setQuizStarted(true)} className="bg-primary text-primary-foreground">
                    Rozpocznij quiz
                </Button>
            </div>
        );
    }

    const q = questions[currentQuestion];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                    Pytanie {currentQuestion + 1} z {questions.length}
                </span>
                <div className="w-48 h-2 bg-muted rounded-full overflow-hidden">
                    <div 
                        className="h-full bg-primary transition-all duration-300"
                        style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
                    />
                </div>
            </div>

            <div className="card-industrial">
                <h4 className="text-xl font-bold mb-6">{q.question}</h4>
                <div className="space-y-3">
                    {q.options.map((option, idx) => (
                        <button
                            key={idx}
                            onClick={() => handleAnswer(q.id, idx)}
                            className={`w-full text-left p-4 border rounded-sm transition-colors
                                ${answers[q.id] === idx ? 'border-primary bg-primary/10' : 'border-border hover:border-primary/50'}
                            `}
                        >
                            <span className="font-bold mr-3">{String.fromCharCode(65 + idx)}.</span>
                            {option}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex justify-between">
                <Button
                    variant="outline"
                    onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
                    disabled={currentQuestion === 0}
                >
                    Poprzednie
                </Button>

                {currentQuestion < questions.length - 1 ? (
                    <Button
                        onClick={() => setCurrentQuestion(currentQuestion + 1)}
                        disabled={answers[q.id] === undefined}
                    >
                        Następne
                    </Button>
                ) : (
                    <Button
                        onClick={handleSubmit}
                        disabled={Object.keys(answers).length < questions.length}
                        className="bg-green-500 text-white"
                    >
                        Zakończ i sprawdź
                    </Button>
                )}
            </div>
        </div>
    );
};

// Notes/History Component (uses localStorage)
export const NotesHistoryTab = () => {
    const [notes, setNotes] = useState([]);
    const [newNote, setNewNote] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('general');

    const categories = [
        { id: 'general', name: 'Ogólne' },
        { id: 'rcd', name: 'RCD' },
        { id: 'loop', name: 'Pętla zwarcia' },
        { id: 'insulation', name: 'Izolacja' },
        { id: 'earthing', name: 'Uziemienie' },
    ];

    useEffect(() => {
        const saved = localStorage.getItem('mpi530_notes');
        if (saved) {
            setNotes(JSON.parse(saved));
        }
    }, []);

    const saveNotes = (newNotes) => {
        setNotes(newNotes);
        localStorage.setItem('mpi530_notes', JSON.stringify(newNotes));
    };

    const addNote = () => {
        if (!newNote.trim()) return;
        const note = {
            id: Date.now(),
            text: newNote,
            category: selectedCategory,
            date: new Date().toISOString()
        };
        saveNotes([note, ...notes]);
        setNewNote('');
        toast.success('Notatka zapisana!');
    };

    const deleteNote = (id) => {
        saveNotes(notes.filter(n => n.id !== id));
        toast.success('Notatka usunięta');
    };

    const filteredNotes = selectedCategory === 'all' 
        ? notes 
        : notes.filter(n => n.category === selectedCategory);

    return (
        <div className="space-y-6">
            <h3 className="font-bold text-xl flex items-center gap-2">
                <FileText className="h-5 w-5 text-blue-500" />
                Notatki i historia
            </h3>

            <div className="card-industrial">
                <h4 className="font-bold mb-4">Dodaj nową notatkę</h4>
                <div className="flex gap-3 mb-4">
                    <select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        className="px-3 py-2 border-2 border-input bg-background rounded-sm"
                    >
                        {categories.map(cat => (
                            <option key={cat.id} value={cat.id}>{cat.name}</option>
                        ))}
                    </select>
                    <Input
                        value={newNote}
                        onChange={(e) => setNewNote(e.target.value)}
                        placeholder="Wpisz notatkę..."
                        className="flex-1"
                        onKeyPress={(e) => e.key === 'Enter' && addNote()}
                    />
                    <Button onClick={addNote} className="bg-blue-500 text-white">
                        Dodaj
                    </Button>
                </div>
            </div>

            <div className="flex gap-2 flex-wrap">
                <Button
                    variant={selectedCategory === 'all' ? 'default' : 'outline'}
                    onClick={() => setSelectedCategory('all')}
                    size="sm"
                >
                    Wszystkie ({notes.length})
                </Button>
                {categories.map(cat => (
                    <Button
                        key={cat.id}
                        variant={selectedCategory === cat.id ? 'default' : 'outline'}
                        onClick={() => setSelectedCategory(cat.id)}
                        size="sm"
                    >
                        {cat.name} ({notes.filter(n => n.category === cat.id).length})
                    </Button>
                ))}
            </div>

            <div className="space-y-3">
                {filteredNotes.length === 0 ? (
                    <div className="text-center py-10 text-muted-foreground">
                        Brak notatek. Dodaj pierwszą notatkę powyżej.
                    </div>
                ) : (
                    filteredNotes.map(note => (
                        <div key={note.id} className="card-industrial flex items-start justify-between gap-4">
                            <div>
                                <p>{note.text}</p>
                                <p className="text-xs text-muted-foreground mt-1">
                                    {categories.find(c => c.id === note.category)?.name} • {new Date(note.date).toLocaleString('pl-PL')}
                                </p>
                            </div>
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => deleteNote(note.id)}
                                className="text-red-500 hover:text-red-600"
                            >
                                Usuń
                            </Button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

// PDF Generator Component
export const PDFGeneratorTab = () => {
    const [formData, setFormData] = useState({
        objectName: '',
        objectAddress: '',
        inspectorName: '',
        inspectorCert: '',
        meterSerial: 'MPI-530 S/N: ',
        meterCalibration: '',
        date: new Date().toISOString().split('T')[0],
        measurements: []
    });

    const [measurementInput, setMeasurementInput] = useState({
        point: '',
        circuit: '',
        type: 'Zs',
        value: '',
        unit: 'Ω',
        status: 'OK'
    });

    const addMeasurement = () => {
        if (!measurementInput.point || !measurementInput.value) {
            toast.error('Wypełnij punkt i wartość');
            return;
        }
        setFormData(prev => ({
            ...prev,
            measurements: [...prev.measurements, { ...measurementInput, id: Date.now() }]
        }));
        setMeasurementInput({ point: '', circuit: '', type: 'Zs', value: '', unit: 'Ω', status: 'OK' });
    };

    const removeMeasurement = (id) => {
        setFormData(prev => ({
            ...prev,
            measurements: prev.measurements.filter(m => m.id !== id)
        }));
    };

    const generatePDF = () => {
        if (!formData.objectName || !formData.inspectorName || formData.measurements.length === 0) {
            toast.error('Wypełnij wszystkie wymagane pola i dodaj pomiary');
            return;
        }

        const doc = new jsPDF();
        const pageWidth = doc.internal.pageSize.getWidth();

        // Header
        doc.setFillColor(243, 146, 0);
        doc.rect(0, 0, pageWidth, 25, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('PROTOKÓŁ POMIARÓW ELEKTRYCZNYCH', pageWidth / 2, 16, { align: 'center' });

        // Object info
        doc.setTextColor(0, 0, 0);
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        let y = 35;

        doc.setFont('helvetica', 'bold');
        doc.text('DANE OBIEKTU:', 15, y);
        doc.setFont('helvetica', 'normal');
        y += 7;
        doc.text(`Obiekt: ${formData.objectName}`, 15, y);
        y += 5;
        doc.text(`Adres: ${formData.objectAddress}`, 15, y);
        y += 5;
        doc.text(`Data pomiaru: ${formData.date}`, 15, y);

        y += 12;
        doc.setFont('helvetica', 'bold');
        doc.text('DANE WYKONAWCY:', 15, y);
        doc.setFont('helvetica', 'normal');
        y += 7;
        doc.text(`Wykonawca: ${formData.inspectorName}`, 15, y);
        y += 5;
        doc.text(`Uprawnienia: ${formData.inspectorCert}`, 15, y);
        y += 5;
        doc.text(`Miernik: ${formData.meterSerial}`, 15, y);
        y += 5;
        doc.text(`Kalibracja: ${formData.meterCalibration}`, 15, y);

        // Measurements table
        y += 15;
        doc.setFont('helvetica', 'bold');
        doc.text('WYNIKI POMIARÓW:', 15, y);

        const tableData = formData.measurements.map(m => [
            m.point,
            m.circuit,
            m.type,
            `${m.value} ${m.unit}`,
            m.status
        ]);

        doc.autoTable({
            startY: y + 5,
            head: [['Punkt', 'Obwód', 'Typ', 'Wynik', 'Status']],
            body: tableData,
            theme: 'grid',
            headStyles: { fillColor: [243, 146, 0] },
            styles: { fontSize: 9 }
        });

        // Footer
        const finalY = doc.lastAutoTable.finalY + 20;
        doc.setFontSize(10);
        doc.text('Podpis wykonawcy: _______________________', 15, finalY);
        doc.text('Podpis zleceniodawcy: _______________________', 110, finalY);

        doc.save(`protokol_${formData.objectName.replace(/\s+/g, '_')}_${formData.date}.pdf`);
        toast.success('Protokół PDF został wygenerowany!');
    };

    return (
        <div className="space-y-6">
            <h3 className="font-bold text-xl flex items-center gap-2">
                <FileText className="h-5 w-5 text-primary" />
                Generator protokołu PDF
            </h3>

            <div className="grid md:grid-cols-2 gap-6">
                <div className="card-industrial space-y-4">
                    <h4 className="font-bold">Dane obiektu</h4>
                    <Input
                        placeholder="Nazwa obiektu *"
                        value={formData.objectName}
                        onChange={(e) => setFormData(prev => ({ ...prev, objectName: e.target.value }))}
                    />
                    <Input
                        placeholder="Adres"
                        value={formData.objectAddress}
                        onChange={(e) => setFormData(prev => ({ ...prev, objectAddress: e.target.value }))}
                    />
                    <Input
                        type="date"
                        value={formData.date}
                        onChange={(e) => setFormData(prev => ({ ...prev, date: e.target.value }))}
                    />
                </div>

                <div className="card-industrial space-y-4">
                    <h4 className="font-bold">Dane wykonawcy</h4>
                    <Input
                        placeholder="Imię i nazwisko *"
                        value={formData.inspectorName}
                        onChange={(e) => setFormData(prev => ({ ...prev, inspectorName: e.target.value }))}
                    />
                    <Input
                        placeholder="Nr uprawnień"
                        value={formData.inspectorCert}
                        onChange={(e) => setFormData(prev => ({ ...prev, inspectorCert: e.target.value }))}
                    />
                    <Input
                        placeholder="Nr seryjny miernika"
                        value={formData.meterSerial}
                        onChange={(e) => setFormData(prev => ({ ...prev, meterSerial: e.target.value }))}
                    />
                    <Input
                        placeholder="Data kalibracji"
                        value={formData.meterCalibration}
                        onChange={(e) => setFormData(prev => ({ ...prev, meterCalibration: e.target.value }))}
                    />
                </div>
            </div>

            <div className="card-industrial">
                <h4 className="font-bold mb-4">Dodaj pomiar</h4>
                <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
                    <Input
                        placeholder="Punkt *"
                        value={measurementInput.point}
                        onChange={(e) => setMeasurementInput(prev => ({ ...prev, point: e.target.value }))}
                    />
                    <Input
                        placeholder="Obwód"
                        value={measurementInput.circuit}
                        onChange={(e) => setMeasurementInput(prev => ({ ...prev, circuit: e.target.value }))}
                    />
                    <select
                        value={measurementInput.type}
                        onChange={(e) => setMeasurementInput(prev => ({ ...prev, type: e.target.value }))}
                        className="px-3 border-2 border-input bg-background rounded-sm"
                    >
                        <option value="Zs">Zs (pętla)</option>
                        <option value="RISO">RISO (izolacja)</option>
                        <option value="RCD">RCD</option>
                        <option value="PE">PE (ciągłość)</option>
                        <option value="RE">RE (uziemienie)</option>
                    </select>
                    <Input
                        placeholder="Wartość *"
                        value={measurementInput.value}
                        onChange={(e) => setMeasurementInput(prev => ({ ...prev, value: e.target.value }))}
                    />
                    <select
                        value={measurementInput.status}
                        onChange={(e) => setMeasurementInput(prev => ({ ...prev, status: e.target.value }))}
                        className="px-3 border-2 border-input bg-background rounded-sm"
                    >
                        <option value="OK">OK</option>
                        <option value="FAIL">FAIL</option>
                    </select>
                    <Button onClick={addMeasurement} className="bg-primary text-primary-foreground">
                        Dodaj
                    </Button>
                </div>

                {formData.measurements.length > 0 && (
                    <div className="mt-4 overflow-x-auto">
                        <table className="w-full text-sm border border-border">
                            <thead className="bg-muted/50">
                                <tr>
                                    <th className="p-2 text-left">Punkt</th>
                                    <th className="p-2 text-left">Obwód</th>
                                    <th className="p-2 text-left">Typ</th>
                                    <th className="p-2 text-left">Wynik</th>
                                    <th className="p-2 text-center">Status</th>
                                    <th className="p-2"></th>
                                </tr>
                            </thead>
                            <tbody>
                                {formData.measurements.map(m => (
                                    <tr key={m.id}>
                                        <td className="p-2 border-t">{m.point}</td>
                                        <td className="p-2 border-t">{m.circuit}</td>
                                        <td className="p-2 border-t">{m.type}</td>
                                        <td className="p-2 border-t font-mono">{m.value} {m.unit}</td>
                                        <td className={`p-2 border-t text-center font-bold ${m.status === 'OK' ? 'text-green-500' : 'text-red-500'}`}>
                                            {m.status}
                                        </td>
                                        <td className="p-2 border-t">
                                            <Button variant="ghost" size="sm" onClick={() => removeMeasurement(m.id)}>
                                                ✕
                                            </Button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            <Button onClick={generatePDF} className="bg-primary text-primary-foreground" disabled={formData.measurements.length === 0}>
                <Download className="h-4 w-4 mr-2" />
                Generuj protokół PDF
            </Button>
        </div>
    );
};
