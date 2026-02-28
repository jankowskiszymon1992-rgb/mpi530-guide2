import { useState, useEffect, useCallback } from "react";
import "@/App.css";
import axios from "axios";
import { Toaster, toast } from "sonner";
import { 
    Shield, Repeat, Layers, Zap, Activity, Link, 
    Search, Moon, Sun, Menu, X, ChevronRight, 
    AlertTriangle, Lightbulb, CheckCircle2, ArrowLeft,
    BookOpen, HelpCircle, ImageIcon, RotateCw, RefreshCw, Circle,
    FileText, Download, Printer, FolderSync, ClipboardList
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Icon mapping
const iconMap = {
    Shield: Shield,
    Repeat: Repeat,
    Layers: Layers,
    Zap: Zap,
    Activity: Activity,
    Link: Link,
    RotateCw: RotateCw,
    RefreshCw: RefreshCw,
    Sun: Sun,
    Circle: Circle,
    FileText: FileText,
    Download: Download,
    Printer: Printer,
    FolderSync: FolderSync
};

// Header Component
const Header = ({ darkMode, setDarkMode, onMenuClick, showBackButton, onBack }) => {
    return (
        <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    <div className="flex items-center gap-4">
                        {showBackButton ? (
                            <Button
                                variant="ghost"
                                size="icon"
                                onClick={onBack}
                                data-testid="back-button"
                                aria-label="Wróć"
                            >
                                <ArrowLeft className="h-5 w-5" />
                            </Button>
                        ) : (
                            <Button
                                variant="ghost"
                                size="icon"
                                className="lg:hidden"
                                onClick={onMenuClick}
                                data-testid="menu-button"
                                aria-label="Menu"
                            >
                                <Menu className="h-5 w-5" />
                            </Button>
                        )}
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-primary flex items-center justify-center">
                                <span className="text-primary-foreground font-bold text-sm font-mono">MPI</span>
                            </div>
                            <div>
                                <h1 className="text-lg font-bold tracking-tight">SONEL MPI-530</h1>
                                <p className="text-xs text-muted-foreground uppercase tracking-wider">Interaktywna Instrukcja</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => setDarkMode(!darkMode)}
                            data-testid="dark-mode-toggle"
                            aria-label={darkMode ? "Tryb jasny" : "Tryb ciemny"}
                        >
                            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
                        </Button>
                    </div>
                </div>
            </div>
        </header>
    );
};

// Sidebar Navigation
const Sidebar = ({ functions, selectedId, onSelect, isOpen, onClose }) => {
    return (
        <>
            {isOpen && (
                <div 
                    className="fixed inset-0 bg-black/50 z-40 lg:hidden"
                    onClick={onClose}
                />
            )}
            <aside className={`
                fixed lg:sticky top-16 left-0 z-50 lg:z-0
                w-72 h-[calc(100vh-4rem)] 
                bg-background border-r border-border
                transform transition-transform duration-200 ease-out
                ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
            `}>
                <div className="p-4 border-b border-border flex items-center justify-between lg:hidden">
                    <span className="font-bold uppercase text-sm">Menu</span>
                    <Button variant="ghost" size="icon" onClick={onClose}>
                        <X className="h-5 w-5" />
                    </Button>
                </div>
                <ScrollArea className="h-full p-4">
                    <nav className="space-y-1" data-testid="sidebar-nav">
                        {functions.map((func) => {
                            const IconComponent = iconMap[func.icon] || Activity;
                            const isActive = selectedId === func.id;
                            return (
                                <button
                                    key={func.id}
                                    onClick={() => {
                                        onSelect(func.id);
                                        onClose();
                                    }}
                                    className={`
                                        nav-item w-full text-left px-4 py-3 flex items-center gap-3
                                        ${isActive ? 'active' : ''}
                                    `}
                                    data-testid={`nav-${func.id}`}
                                >
                                    <IconComponent 
                                        className="h-5 w-5 flex-shrink-0" 
                                        style={{ color: func.color }}
                                    />
                                    <span className="text-sm font-medium truncate">{func.name}</span>
                                </button>
                            );
                        })}
                    </nav>
                </ScrollArea>
            </aside>
        </>
    );
};

// Function Card Component
const FunctionCard = ({ func, onClick }) => {
    const IconComponent = iconMap[func.icon] || Activity;
    
    return (
        <button
            onClick={() => onClick(func.id)}
            className="function-card card-industrial text-left group"
            data-testid={`function-card-${func.id}`}
        >
            <div className="flex items-start gap-4">
                <div 
                    className="w-14 h-14 flex items-center justify-center flex-shrink-0"
                    style={{ backgroundColor: func.color }}
                >
                    <IconComponent className="h-7 w-7 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                    <h3 className="font-bold text-lg mb-1 group-hover:text-primary transition-colors duration-150">
                        {func.name}
                    </h3>
                    <p className="text-sm text-muted-foreground line-clamp-2">
                        {func.description}
                    </p>
                </div>
            </div>
            <div className="mt-4 flex items-center justify-between text-xs text-muted-foreground">
                <span className="uppercase tracking-wider">{func.steps.length} kroków</span>
                <ChevronRight className="h-4 w-4 group-hover:translate-x-1 transition-transform duration-150" style={{ color: func.color }} />
            </div>
        </button>
    );
};

// Step Component with Image
const StepComponent = ({ step, stepIndex, currentStep, totalSteps }) => {
    const isActive = stepIndex === currentStep;
    const isCompleted = stepIndex < currentStep;
    const isPending = stepIndex > currentStep;
    const [imageError, setImageError] = useState(false);

    return (
        <div 
            className={`
                p-4 mb-4 transition-opacity duration-200
                ${isActive ? 'step-active' : ''}
                ${isCompleted ? 'step-completed' : ''}
                ${isPending ? 'step-pending' : ''}
            `}
            data-testid={`step-${step.step_number}`}
        >
            <div className="flex items-start gap-4">
                <div className={`
                    step-indicator rounded-sm
                    ${isActive ? 'bg-primary text-primary-foreground' : ''}
                    ${isCompleted ? 'bg-green-500 text-white' : ''}
                    ${isPending ? 'bg-muted text-muted-foreground' : ''}
                `}>
                    {isCompleted ? (
                        <CheckCircle2 className="h-5 w-5" />
                    ) : (
                        step.step_number
                    )}
                </div>
                <div className="flex-1">
                    <h4 className="font-bold text-lg mb-2">{step.title}</h4>
                    <p className="text-muted-foreground mb-3">{step.description}</p>
                    
                    {/* Zdjęcie kroku */}
                    {step.image && !imageError && isActive && (
                        <div className="my-4 rounded-sm overflow-hidden border border-border bg-muted/30">
                            <img 
                                src={step.image} 
                                alt={`Krok ${step.step_number}: ${step.title}`}
                                className="w-full h-auto max-h-64 object-contain"
                                onError={() => setImageError(true)}
                            />
                        </div>
                    )}
                    
                    {step.warning && (
                        <div className="warning-box flex items-start gap-3 mb-3">
                            <AlertTriangle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
                            <p>{step.warning}</p>
                        </div>
                    )}
                    
                    {step.tip && (
                        <div className="tip-box flex items-start gap-3">
                            <Lightbulb className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" />
                            <p>{step.tip}</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

// LCD Display Component
const LCDDisplay = ({ func }) => {
    return (
        <div className="lcd-result p-6 rounded-sm" data-testid="lcd-display">
            <div className="text-xs uppercase tracking-wider opacity-70 mb-2">Oczekiwany Wynik</div>
            <div className="text-2xl font-mono font-bold mb-4">{func.expected_results}</div>
            <div className="border-t border-green-900/50 pt-4 mt-4">
                <div className="text-xs uppercase tracking-wider opacity-70 mb-2">Parametry</div>
                <div className="grid grid-cols-1 gap-2 text-sm">
                    {func.parameters.map((param, idx) => (
                        <div key={idx} className="opacity-80">{param}</div>
                    ))}
                </div>
            </div>
        </div>
    );
};

// Safety Notes Component
const SafetyNotes = ({ notes }) => {
    return (
        <div className="bg-red-500/5 border border-red-500/20 p-4 rounded-sm" data-testid="safety-notes">
            <h4 className="font-bold uppercase tracking-wider text-sm mb-3 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-red-500" />
                Zasady Bezpieczeństwa
            </h4>
            <ul className="space-y-2">
                {notes.map((note, idx) => (
                    <li key={idx} className="text-sm text-muted-foreground flex items-start gap-2">
                        <span className="text-red-500">•</span>
                        {note}
                    </li>
                ))}
            </ul>
        </div>
    );
};

// Meter Image Gallery
const MeterImageGallery = ({ mainImage, funcName }) => {
    const [imageError, setImageError] = useState(false);
    
    if (imageError || !mainImage) return null;
    
    return (
        <div className="mb-6 rounded-sm overflow-hidden border border-border bg-card" data-testid="meter-image">
            <div className="p-2 bg-muted/50 border-b border-border flex items-center gap-2">
                <ImageIcon className="h-4 w-4 text-muted-foreground" />
                <span className="text-xs uppercase tracking-wider text-muted-foreground">Sonel MPI-530</span>
            </div>
            <img 
                src={mainImage} 
                alt={`Sonel MPI-530 - ${funcName}`}
                className="w-full h-auto max-h-80 object-contain bg-white p-4"
                onError={() => setImageError(true)}
            />
        </div>
    );
};

// Detail View Component
const DetailView = ({ func, onBack }) => {
    const [currentStep, setCurrentStep] = useState(0);

    const handleNextStep = () => {
        if (currentStep < func.steps.length - 1) {
            setCurrentStep(currentStep + 1);
        }
    };

    const handlePrevStep = () => {
        if (currentStep > 0) {
            setCurrentStep(currentStep - 1);
        }
    };

    const IconComponent = iconMap[func.icon] || Activity;

    return (
        <div className="animate-fade-in" data-testid="detail-view">
            {/* Header */}
            <div className="mb-8 pb-6 border-b border-border">
                <div className="flex items-center gap-4 mb-4">
                    <div 
                        className="w-16 h-16 flex items-center justify-center"
                        style={{ backgroundColor: func.color }}
                    >
                        <IconComponent className="h-8 w-8 text-white" />
                    </div>
                    <div>
                        <h2 className="text-3xl font-bold gradient-text">{func.name}</h2>
                        <p className="text-muted-foreground mt-1">{func.description}</p>
                    </div>
                </div>
            </div>

            {/* Split View */}
            <div className="split-view">
                {/* Left: Instructions */}
                <div>
                    <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
                        <BookOpen className="h-5 w-5 text-primary" />
                        Instrukcja Krok Po Kroku
                    </h3>
                    <div className="space-y-2">
                        {func.steps.map((step, idx) => (
                            <StepComponent
                                key={step.step_number}
                                step={step}
                                stepIndex={idx}
                                currentStep={currentStep}
                                totalSteps={func.steps.length}
                            />
                        ))}
                    </div>
                    
                    {/* Navigation */}
                    <div className="flex items-center justify-between mt-6 pt-6 border-t border-border">
                        <Button
                            variant="outline"
                            onClick={handlePrevStep}
                            disabled={currentStep === 0}
                            data-testid="prev-step-btn"
                        >
                            Poprzedni
                        </Button>
                        <span className="text-sm text-muted-foreground font-mono">
                            {currentStep + 1} / {func.steps.length}
                        </span>
                        <Button
                            onClick={handleNextStep}
                            disabled={currentStep === func.steps.length - 1}
                            className="bg-primary text-primary-foreground"
                            data-testid="next-step-btn"
                        >
                            Następny
                        </Button>
                    </div>
                </div>

                {/* Right: Image, Results & Safety */}
                <div className="space-y-6">
                    <MeterImageGallery mainImage={func.main_image} funcName={func.name} />
                    <LCDDisplay func={func} />
                    <SafetyNotes notes={func.safety_notes} />
                </div>
            </div>
        </div>
    );
};

// Search Results Component
const SearchResults = ({ results, onSelect, onClose }) => {
    if (results.length === 0) return null;

    return (
        <div className="absolute top-full left-0 right-0 mt-2 bg-card border border-border shadow-lg z-50 max-h-80 overflow-auto rounded-sm" data-testid="search-results">
            <div className="p-2">
                {results.map((result, idx) => (
                    <button
                        key={idx}
                        onClick={() => {
                            onSelect(result.function_id || result.id);
                            onClose();
                        }}
                        className="w-full text-left px-4 py-3 hover:bg-muted transition-colors duration-150 flex items-center gap-3"
                    >
                        {result.type === 'function' && <BookOpen className="h-4 w-4 text-primary" />}
                        {result.type === 'step' && <ChevronRight className="h-4 w-4 text-blue-500" />}
                        {result.type === 'faq' && <HelpCircle className="h-4 w-4 text-yellow-500" />}
                        <div>
                            <p className="font-medium text-sm">
                                {result.name || result.step_title || result.question}
                            </p>
                            {result.function_name && (
                                <p className="text-xs text-muted-foreground">{result.function_name}</p>
                            )}
                        </div>
                    </button>
                ))}
            </div>
        </div>
    );
};

// Home View Component
const HomeView = ({ functions, onSelectFunction, searchQuery, setSearchQuery, searchResults, onSearch, onShowProtocols }) => {
    const [showResults, setShowResults] = useState(false);

    return (
        <div className="animate-fade-in">
            {/* Hero Section */}
            <div className="mb-12">
                <h2 className="text-4xl lg:text-5xl font-black mb-4 tracking-tight">
                    <span className="gradient-text">Interaktywna Instrukcja</span>
                </h2>
                <p className="text-lg text-muted-foreground max-w-2xl">
                    Wybierz funkcję pomiarową, aby zobaczyć szczegółową instrukcję krok po kroku dla miernika Sonel MPI-530.
                </p>
            </div>

            {/* Search */}
            <div className="relative mb-10 max-w-xl">
                <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                    <Input
                        type="text"
                        placeholder="Szukaj instrukcji, procedur, FAQ..."
                        value={searchQuery}
                        onChange={(e) => {
                            setSearchQuery(e.target.value);
                            onSearch(e.target.value);
                            setShowResults(true);
                        }}
                        onFocus={() => setShowResults(true)}
                        className="search-input pl-12 h-12 text-base"
                        data-testid="search-input"
                    />
                </div>
                {showResults && searchQuery && (
                    <SearchResults 
                        results={searchResults} 
                        onSelect={onSelectFunction}
                        onClose={() => setShowResults(false)}
                    />
                )}
            </div>

            {/* Function Grid */}
            <div className="bento-grid" data-testid="functions-grid">
                {functions.map((func) => (
                    <FunctionCard 
                        key={func.id} 
                        func={func} 
                        onClick={onSelectFunction}
                    />
                ))}
            </div>

            {/* Protocols Section */}
            <div className="mt-12 p-6 bg-blue-500/5 border border-blue-500/20 rounded-sm">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold text-xl flex items-center gap-2">
                        <ClipboardList className="h-6 w-6 text-blue-500" />
                        Protokoły Pomiarowe
                    </h3>
                    <Button 
                        onClick={onShowProtocols}
                        className="bg-blue-500 text-white hover:bg-blue-600"
                        data-testid="show-protocols-btn"
                    >
                        Zobacz instrukcje
                        <ChevronRight className="h-4 w-4 ml-2" />
                    </Button>
                </div>
                <p className="text-muted-foreground mb-4">
                    Jak tworzyć protokoły pomiarowe w programie <strong>Sonel Reports Plus</strong> - od projektu po wydruk.
                </p>
                <div className="grid md:grid-cols-4 gap-4 text-sm">
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <FileText className="h-4 w-4 text-blue-500" />
                        <span>Tworzenie projektu</span>
                    </div>
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <Download className="h-4 w-4 text-green-500" />
                        <span>Pobieranie wyników</span>
                    </div>
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <Printer className="h-4 w-4 text-primary" />
                        <span>Generowanie protokołu</span>
                    </div>
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <FolderSync className="h-4 w-4 text-purple-500" />
                        <span>Migracja z PE6</span>
                    </div>
                </div>
            </div>

            {/* Quick Tips */}
            <div className="mt-8 p-6 bg-secondary/5 border border-secondary/20 rounded-sm">
                <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
                    <Lightbulb className="h-5 w-5 text-primary" />
                    Szybkie Porady
                </h3>
                <div className="grid md:grid-cols-3 gap-4 text-sm text-muted-foreground">
                    <div className="flex items-start gap-2">
                        <span className="text-primary font-bold">01</span>
                        <p>Zawsze sprawdź stan przewodów pomiarowych przed rozpoczęciem pracy</p>
                    </div>
                    <div className="flex items-start gap-2">
                        <span className="text-primary font-bold">02</span>
                        <p>Przestrzegaj kategorii pomiarowej CAT III/IV dla bezpieczeństwa</p>
                    </div>
                    <div className="flex items-start gap-2">
                        <span className="text-primary font-bold">03</span>
                        <p>Kalibruj miernik co 12 miesięcy zgodnie z zaleceniami Sonel</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Protocol Guide Card
const ProtocolGuideCard = ({ guide, onClick }) => {
    const IconComponent = iconMap[guide.icon] || FileText;
    
    return (
        <button
            onClick={() => onClick(guide.id)}
            className="function-card card-industrial text-left group"
            data-testid={`protocol-card-${guide.id}`}
        >
            <div className="flex items-start gap-4">
                <div 
                    className="w-14 h-14 flex items-center justify-center flex-shrink-0"
                    style={{ backgroundColor: guide.color }}
                >
                    <IconComponent className="h-7 w-7 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                    <h3 className="font-bold text-lg mb-1 group-hover:text-primary transition-colors duration-150">
                        {guide.name}
                    </h3>
                    <p className="text-sm text-muted-foreground line-clamp-2">
                        {guide.description}
                    </p>
                </div>
            </div>
            <div className="mt-4 flex items-center justify-between text-xs text-muted-foreground">
                <span className="uppercase tracking-wider">{guide.steps.length} kroków</span>
                <ChevronRight className="h-4 w-4 group-hover:translate-x-1 transition-transform duration-150" style={{ color: guide.color }} />
            </div>
        </button>
    );
};

// Protocol Template Card
const ProtocolTemplateCard = ({ template }) => {
    return (
        <div className="card-industrial" data-testid={`template-${template.id}`}>
            <h4 className="font-bold mb-2">{template.name}</h4>
            <p className="text-sm text-muted-foreground mb-4">{template.description}</p>
            <div className="space-y-2">
                <p className="text-xs uppercase tracking-wider text-muted-foreground font-bold">Wymagane pomiary:</p>
                <ul className="text-sm space-y-1">
                    {template.measurements.map((m, idx) => (
                        <li key={idx} className="flex items-center gap-2 text-muted-foreground">
                            <CheckCircle2 className="h-3 w-3 text-green-500 flex-shrink-0" />
                            {m}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

// Protocol Guide Detail View
const ProtocolGuideDetailView = ({ guide, onBack }) => {
    const [currentStep, setCurrentStep] = useState(0);
    const IconComponent = iconMap[guide.icon] || FileText;

    return (
        <div className="animate-fade-in" data-testid="protocol-detail-view">
            {/* Header */}
            <div className="mb-8 pb-6 border-b border-border">
                <div className="flex items-center gap-4 mb-4">
                    <div 
                        className="w-16 h-16 flex items-center justify-center"
                        style={{ backgroundColor: guide.color }}
                    >
                        <IconComponent className="h-8 w-8 text-white" />
                    </div>
                    <div>
                        <h2 className="text-3xl font-bold gradient-text">{guide.name}</h2>
                        <p className="text-muted-foreground mt-1">{guide.description}</p>
                    </div>
                </div>
            </div>

            {/* Steps */}
            <div className="space-y-4 mb-8">
                {guide.steps.map((step, idx) => (
                    <div 
                        key={step.step_number}
                        className={`p-4 transition-opacity duration-200 ${idx === currentStep ? 'step-active' : idx < currentStep ? 'step-completed' : 'step-pending'}`}
                    >
                        <div className="flex items-start gap-4">
                            <div className={`step-indicator rounded-sm ${idx === currentStep ? 'bg-primary text-primary-foreground' : idx < currentStep ? 'bg-green-500 text-white' : 'bg-muted text-muted-foreground'}`}>
                                {idx < currentStep ? <CheckCircle2 className="h-5 w-5" /> : step.step_number}
                            </div>
                            <div className="flex-1">
                                <h4 className="font-bold text-lg mb-2">{step.title}</h4>
                                <p className="text-muted-foreground mb-3">{step.description}</p>
                                
                                {step.image && idx === currentStep && (
                                    <div className="my-4 rounded-sm overflow-hidden border border-border bg-muted/30">
                                        <img 
                                            src={step.image} 
                                            alt={step.title}
                                            className="w-full h-auto max-h-64 object-contain"
                                        />
                                    </div>
                                )}
                                
                                {step.tip && (
                                    <div className="tip-box flex items-start gap-3">
                                        <Lightbulb className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" />
                                        <p>{step.tip}</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Navigation */}
            <div className="flex items-center justify-between pt-6 border-t border-border">
                <Button
                    variant="outline"
                    onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                    disabled={currentStep === 0}
                >
                    Poprzedni
                </Button>
                <span className="text-sm text-muted-foreground font-mono">
                    {currentStep + 1} / {guide.steps.length}
                </span>
                <Button
                    onClick={() => setCurrentStep(Math.min(guide.steps.length - 1, currentStep + 1))}
                    disabled={currentStep === guide.steps.length - 1}
                    className="bg-primary text-primary-foreground"
                >
                    Następny
                </Button>
            </div>

            {/* Tips */}
            {guide.tips && guide.tips.length > 0 && (
                <div className="mt-8 p-4 bg-blue-500/5 border border-blue-500/20 rounded-sm">
                    <h4 className="font-bold mb-3 flex items-center gap-2">
                        <Lightbulb className="h-4 w-4 text-blue-500" />
                        Wskazówki
                    </h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                        {guide.tips.map((tip, idx) => (
                            <li key={idx} className="flex items-start gap-2">
                                <span className="text-blue-500">•</span>
                                {tip}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

// Protocols View Component
const ProtocolsView = ({ onSelectGuide, onSelectExample, onBack }) => {
    const [guides, setGuides] = useState([]);
    const [templates, setTemplates] = useState([]);
    const [examples, setExamples] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [guidesRes, templatesRes, examplesRes] = await Promise.all([
                    axios.get(`${API}/protocols/guides`),
                    axios.get(`${API}/protocols/templates`),
                    axios.get(`${API}/protocols/examples`)
                ]);
                setGuides(guidesRes.data);
                setTemplates(templatesRes.data);
                setExamples(examplesRes.data);
            } catch (error) {
                console.error("Błąd ładowania protokołów:", error);
                toast.error("Błąd ładowania danych protokołów");
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center py-20">
                <div className="text-center">
                    <div className="w-12 h-12 bg-blue-500 mx-auto mb-4 flex items-center justify-center animate-pulse">
                        <FileText className="h-6 w-6 text-white" />
                    </div>
                    <p className="text-muted-foreground">Ładowanie...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="animate-fade-in" data-testid="protocols-view">
            {/* Header */}
            <div className="mb-10">
                <h2 className="text-4xl font-black mb-4 tracking-tight">
                    <span className="gradient-text">Protokoły Pomiarowe</span>
                </h2>
                <p className="text-lg text-muted-foreground max-w-2xl">
                    Instrukcje tworzenia protokołów w programie <strong>Sonel Reports Plus</strong> - od projektu po wydruk dokumentacji.
                </p>
            </div>

            {/* Sonel Reports Plus Info */}
            <div className="mb-10 p-6 bg-card border border-border rounded-sm">
                <div className="flex items-start gap-4">
                    <img 
                        src="https://cdn.sonel.com/Zdjecia/Programy/Programy+komputerowe/Sonel+Reports+PLUS/image-thumb__36489__img-product-thumb/blank-box-reports-plus_mHqcbIA.webp"
                        alt="Sonel Reports Plus"
                        className="w-24 h-24 object-contain"
                    />
                    <div>
                        <h3 className="font-bold text-xl mb-2">Sonel Reports Plus</h3>
                        <p className="text-muted-foreground mb-3">
                            Bezpłatne oprogramowanie do tworzenia dokumentacji pomiarowej. Współpracuje z miernikami Sonel MPI-530, MPI-540 i innymi.
                        </p>
                        <div className="flex gap-4 text-sm">
                            <span className="text-muted-foreground">System: Windows 10/11</span>
                            <a 
                                href="https://sonel.pl/en/product/software-sonel-reports-plus" 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:underline"
                            >
                                Pobierz ze strony Sonel →
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            {/* Guides */}
            <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-primary" />
                Instrukcje krok po kroku
            </h3>
            <div className="bento-grid mb-12">
                {guides.map((guide) => (
                    <ProtocolGuideCard 
                        key={guide.id} 
                        guide={guide} 
                        onClick={onSelectGuide}
                    />
                ))}
            </div>

            {/* Example Protocols */}
            <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
                <FileText className="h-5 w-5 text-green-500" />
                Przykładowe wypełnione protokoły
            </h3>
            <p className="text-muted-foreground mb-6">
                Wzory protokołów z rzeczywistymi wynikami pomiarów - zobacz jak prawidłowo dokumentować badania.
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
                {examples.map((example) => (
                    <button
                        key={example.id}
                        onClick={() => onSelectExample(example.id)}
                        className="card-industrial text-left group hover:border-green-500/50"
                        data-testid={`example-${example.id}`}
                    >
                        <div className="flex items-center gap-3 mb-3">
                            <div className={`w-10 h-10 flex items-center justify-center ${example.conclusion.includes('POZYTYWNA') ? 'bg-green-500' : 'bg-red-500'}`}>
                                {example.conclusion.includes('POZYTYWNA') ? (
                                    <CheckCircle2 className="h-5 w-5 text-white" />
                                ) : (
                                    <AlertTriangle className="h-5 w-5 text-white" />
                                )}
                            </div>
                            <div>
                                <h4 className="font-bold text-sm">{example.name}</h4>
                                <p className="text-xs text-muted-foreground">{example.object_name}</p>
                            </div>
                        </div>
                        <div className="text-xs text-muted-foreground space-y-1">
                            <p>Data: {example.date}</p>
                            <p>Pomiary: {example.measurements.length}</p>
                            <p className={example.conclusion.includes('POZYTYWNA') ? 'text-green-500' : 'text-red-500'}>
                                {example.conclusion.split(' - ')[0]}
                            </p>
                        </div>
                        <ChevronRight className="h-4 w-4 absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity text-green-500" />
                    </button>
                ))}
            </div>

            {/* Templates */}
            <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
                <ClipboardList className="h-5 w-5 text-primary" />
                Szablony protokołów
            </h3>
            <p className="text-muted-foreground mb-6">
                Wymagane pomiary dla różnych typów badań instalacji elektrycznych.
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {templates.map((template) => (
                    <ProtocolTemplateCard key={template.id} template={template} />
                ))}
            </div>
        </div>
    );
};

// Example Protocol Detail View
const ExampleProtocolDetailView = ({ example, onBack }) => {
    const isPositive = example.conclusion.includes('POZYTYWNA');
    
    return (
        <div className="animate-fade-in" data-testid="example-protocol-detail">
            {/* Header */}
            <div className="mb-8 pb-6 border-b border-border">
                <div className="flex items-center gap-4 mb-4">
                    <div className={`w-16 h-16 flex items-center justify-center ${isPositive ? 'bg-green-500' : 'bg-red-500'}`}>
                        {isPositive ? (
                            <CheckCircle2 className="h-8 w-8 text-white" />
                        ) : (
                            <AlertTriangle className="h-8 w-8 text-white" />
                        )}
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold">{example.name}</h2>
                        <p className={`mt-1 font-bold ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
                            {example.conclusion}
                        </p>
                    </div>
                </div>
            </div>

            {/* Protocol Info */}
            <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div className="card-industrial">
                    <h3 className="font-bold mb-4 uppercase text-sm tracking-wider">Dane obiektu</h3>
                    <div className="space-y-2 text-sm">
                        <p><span className="text-muted-foreground">Obiekt:</span> {example.object_name}</p>
                        <p><span className="text-muted-foreground">Adres:</span> {example.object_address}</p>
                        <p><span className="text-muted-foreground">Data pomiaru:</span> {example.date}</p>
                    </div>
                </div>
                <div className="card-industrial">
                    <h3 className="font-bold mb-4 uppercase text-sm tracking-wider">Dane wykonawcy</h3>
                    <div className="space-y-2 text-sm">
                        <p><span className="text-muted-foreground">Wykonawca:</span> {example.inspector}</p>
                        <p><span className="text-muted-foreground">Uprawnienia:</span> {example.inspector_cert}</p>
                        <p><span className="text-muted-foreground">Miernik:</span> {example.meter_serial}</p>
                        <p><span className="text-muted-foreground">Kalibracja:</span> {example.meter_calibration}</p>
                    </div>
                </div>
            </div>

            {/* Measurements Table */}
            <h3 className="font-bold mb-4 uppercase text-sm tracking-wider flex items-center gap-2">
                <ClipboardList className="h-4 w-4" />
                Wyniki pomiarów ({example.measurements.length})
            </h3>
            <div className="overflow-x-auto mb-8">
                <table className="w-full text-sm border border-border">
                    <thead className="bg-muted/50">
                        <tr>
                            <th className="text-left p-3 border-b border-border font-bold">Punkt</th>
                            <th className="text-left p-3 border-b border-border font-bold">Obwód</th>
                            <th className="text-left p-3 border-b border-border font-bold">Zabezp.</th>
                            <th className="text-right p-3 border-b border-border font-bold">Wynik</th>
                            <th className="text-left p-3 border-b border-border font-bold">Limit</th>
                            <th className="text-center p-3 border-b border-border font-bold">Status</th>
                            <th className="text-left p-3 border-b border-border font-bold">Uwagi</th>
                        </tr>
                    </thead>
                    <tbody>
                        {example.measurements.map((m, idx) => (
                            <tr key={idx} className={`${m.status === 'FAIL' ? 'bg-red-500/10' : ''} hover:bg-muted/30`}>
                                <td className="p-3 border-b border-border">{m.point}</td>
                                <td className="p-3 border-b border-border font-mono">{m.circuit}</td>
                                <td className="p-3 border-b border-border">{m.protection}</td>
                                <td className="p-3 border-b border-border text-right font-mono font-bold">
                                    {m.value} {m.unit !== '-' && m.unit}
                                </td>
                                <td className="p-3 border-b border-border text-muted-foreground">{m.limit}</td>
                                <td className="p-3 border-b border-border text-center">
                                    {m.status === 'OK' ? (
                                        <span className="inline-flex items-center gap-1 text-green-500 font-bold">
                                            <CheckCircle2 className="h-4 w-4" /> OK
                                        </span>
                                    ) : (
                                        <span className="inline-flex items-center gap-1 text-red-500 font-bold">
                                            <AlertTriangle className="h-4 w-4" /> FAIL
                                        </span>
                                    )}
                                </td>
                                <td className="p-3 border-b border-border text-muted-foreground text-xs">{m.notes}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Recommendations */}
            {example.recommendations && example.recommendations.length > 0 && (
                <div className={`p-4 rounded-sm border ${isPositive ? 'bg-green-500/5 border-green-500/20' : 'bg-red-500/5 border-red-500/20'}`}>
                    <h4 className="font-bold mb-3 flex items-center gap-2">
                        <Lightbulb className={`h-4 w-4 ${isPositive ? 'text-green-500' : 'text-red-500'}`} />
                        Zalecenia i uwagi
                    </h4>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                        {example.recommendations.map((rec, idx) => (
                            <li key={idx} className="flex items-start gap-2">
                                <span className={isPositive ? 'text-green-500' : 'text-red-500'}>•</span>
                                {rec}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

// Main App Component
function App() {
    const [functions, setFunctions] = useState([]);
    const [selectedFunction, setSelectedFunction] = useState(null);
    const [loading, setLoading] = useState(true);
    const [darkMode, setDarkMode] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [currentView, setCurrentView] = useState('home'); // 'home', 'protocols', 'protocol-detail', 'example-detail'
    const [selectedGuide, setSelectedGuide] = useState(null);
    const [selectedExample, setSelectedExample] = useState(null);

    // Fetch functions on mount
    useEffect(() => {
        const fetchFunctions = async () => {
            try {
                const response = await axios.get(`${API}/functions`);
                setFunctions(response.data);
            } catch (error) {
                console.error("Błąd ładowania danych:", error);
                toast.error("Błąd ładowania danych");
            } finally {
                setLoading(false);
            }
        };
        fetchFunctions();
    }, []);

    // Dark mode toggle
    useEffect(() => {
        if (darkMode) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }, [darkMode]);

    // Search handler
    const handleSearch = useCallback(async (query) => {
        if (!query || query.length < 2) {
            setSearchResults([]);
            return;
        }
        try {
            const response = await axios.get(`${API}/search`, { params: { q: query } });
            setSearchResults(response.data);
        } catch (error) {
            console.error("Błąd wyszukiwania:", error);
        }
    }, []);

    // Select function handler
    const handleSelectFunction = (functionId) => {
        const func = functions.find(f => f.id === functionId);
        if (func) {
            setSelectedFunction(func);
            setCurrentView('home');
            setSearchQuery("");
            setSearchResults([]);
        }
    };

    // Show protocols
    const handleShowProtocols = () => {
        setSelectedFunction(null);
        setCurrentView('protocols');
    };

    // Select guide handler
    const handleSelectGuide = async (guideId) => {
        try {
            const response = await axios.get(`${API}/protocols/guides/${guideId}`);
            setSelectedGuide(response.data);
            setCurrentView('protocol-detail');
        } catch (error) {
            console.error("Błąd ładowania instrukcji:", error);
            toast.error("Błąd ładowania instrukcji");
        }
    };

    // Select example handler
    const handleSelectExample = async (exampleId) => {
        try {
            const response = await axios.get(`${API}/protocols/examples/${exampleId}`);
            setSelectedExample(response.data);
            setCurrentView('example-detail');
        } catch (error) {
            console.error("Błąd ładowania przykładu:", error);
            toast.error("Błąd ładowania przykładu");
        }
    };

    // Back handler
    const handleBack = () => {
        if (currentView === 'protocol-detail' || currentView === 'example-detail') {
            setSelectedGuide(null);
            setSelectedExample(null);
            setCurrentView('protocols');
        } else if (currentView === 'protocols') {
            setCurrentView('home');
        } else {
            setSelectedFunction(null);
        }
    };

    const showBackButton = selectedFunction || currentView === 'protocols' || currentView === 'protocol-detail' || currentView === 'example-detail';

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background">
                <div className="text-center">
                    <div className="w-16 h-16 bg-primary mx-auto mb-4 flex items-center justify-center animate-pulse">
                        <span className="text-primary-foreground font-bold font-mono">MPI</span>
                    </div>
                    <p className="text-muted-foreground uppercase tracking-wider text-sm">Ładowanie...</p>
                </div>
            </div>
        );
    }

    // Render current view
    const renderMainContent = () => {
        if (selectedFunction) {
            return <DetailView func={selectedFunction} onBack={handleBack} />;
        }
        
        switch (currentView) {
            case 'protocols':
                return <ProtocolsView onSelectGuide={handleSelectGuide} onSelectExample={handleSelectExample} onBack={handleBack} />;
            case 'protocol-detail':
                return selectedGuide ? <ProtocolGuideDetailView guide={selectedGuide} onBack={handleBack} /> : null;
            case 'example-detail':
                return selectedExample ? <ExampleProtocolDetailView example={selectedExample} onBack={handleBack} /> : null;
            default:
                return (
                    <HomeView 
                        functions={functions}
                        onSelectFunction={handleSelectFunction}
                        searchQuery={searchQuery}
                        setSearchQuery={setSearchQuery}
                        searchResults={searchResults}
                        onSearch={handleSearch}
                        onShowProtocols={handleShowProtocols}
                    />
                );
        }
    };

    return (
        <div className={`App ${darkMode ? 'dark' : ''}`}>
            <Toaster position="top-right" />
            
            <Header 
                darkMode={darkMode}
                setDarkMode={setDarkMode}
                onMenuClick={() => setSidebarOpen(true)}
                showBackButton={showBackButton}
                onBack={handleBack}
            />

            <div className="flex flex-1">
                <Sidebar 
                    functions={functions}
                    selectedId={selectedFunction?.id}
                    onSelect={handleSelectFunction}
                    isOpen={sidebarOpen}
                    onClose={() => setSidebarOpen(false)}
                />

                <main className="flex-1 p-6 lg:p-10 max-w-5xl" data-testid="main-content">
                    {renderMainContent()}
                </main>
            </div>
        </div>
    );
}

export default App;
