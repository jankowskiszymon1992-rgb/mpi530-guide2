import { useState, useEffect, useCallback } from "react";
import "@/App.css";
import axios from "axios";
import { Toaster, toast } from "sonner";
import { 
    Shield, Repeat, Layers, Zap, Activity, Link, 
    Search, Moon, Sun, Menu, X, ChevronRight, 
    AlertTriangle, Lightbulb, CheckCircle2, ArrowLeft,
    BookOpen, HelpCircle, ImageIcon, RotateCw, RefreshCw, Circle,
    FileText, Download, Printer, FolderSync, ClipboardList,
    Calculator, Table2, AlertOctagon, Cable, Wrench,
    ClipboardCheck, Award, StickyNote, Globe
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { CableCalculatorTab, SafetyChecklistTab, QuizTab, NotesHistoryTab, PDFGeneratorTab } from "@/components/ToolsComponents";
import { LanguageProvider, useLanguage } from "@/i18n";

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
const Header = ({ darkMode, setDarkMode, onMenuClick, showBackButton, onBack, lang, switchLang, t }) => {
    const [langOpen, setLangOpen] = useState(false);
    const langs = [
        { code: 'pl', label: 'PL', flag: '🇵🇱' },
        { code: 'en', label: 'EN', flag: '🇬🇧' },
        { code: 'de', label: 'DE', flag: '🇩🇪' },
    ];
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
                                aria-label={t('back')}
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
                                <p className="text-xs text-muted-foreground uppercase tracking-wider">{t('app_subtitle')}</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        {/* Language Switcher */}
                        <div className="relative" data-testid="language-switcher">
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => setLangOpen(!langOpen)}
                                className="flex items-center gap-1.5 px-2"
                                data-testid="language-toggle"
                            >
                                <Globe className="h-4 w-4" />
                                <span className="text-xs font-bold">{lang.toUpperCase()}</span>
                            </Button>
                            {langOpen && (
                                <div className="absolute right-0 top-full mt-1 bg-popover border border-border rounded-md shadow-lg py-1 min-w-[100px] z-50">
                                    {langs.map(l => (
                                        <button
                                            key={l.code}
                                            onClick={() => { switchLang(l.code); setLangOpen(false); }}
                                            className={`w-full text-left px-3 py-1.5 text-sm hover:bg-accent flex items-center gap-2 ${lang === l.code ? 'bg-accent font-bold' : ''}`}
                                            data-testid={`lang-${l.code}`}
                                        >
                                            <span>{l.flag}</span>
                                            <span>{l.label}</span>
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => setDarkMode(!darkMode)}
                            data-testid="dark-mode-toggle"
                            aria-label={darkMode ? t('light_mode') : t('dark_mode')}
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
const FunctionCard = ({ func, onClick, t }) => {
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
                <span className="uppercase tracking-wider">{func.steps.length} {t('steps_count')}</span>
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
const LCDDisplay = ({ func, t }) => {
    return (
        <div className="lcd-result p-6 rounded-sm" data-testid="lcd-display">
            <div className="text-xs uppercase tracking-wider opacity-70 mb-2">{t('expected_result')}</div>
            <div className="text-2xl font-mono font-bold mb-4">{func.expected_results}</div>
            <div className="border-t border-green-900/50 pt-4 mt-4">
                <div className="text-xs uppercase tracking-wider opacity-70 mb-2">{t('parameters')}</div>
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
const SafetyNotes = ({ notes, t }) => {
    return (
        <div className="bg-red-500/5 border border-red-500/20 p-4 rounded-sm" data-testid="safety-notes">
            <h4 className="font-bold uppercase tracking-wider text-sm mb-3 flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-red-500" />
                {t('safety_rules')}
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
const DetailView = ({ func, onBack, t }) => {
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
                        {t('step_by_step')}
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
                    <LCDDisplay func={func} t={t} />
                    <SafetyNotes notes={func.safety_notes} t={t} />
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
const HomeView = ({ functions, onSelectFunction, searchQuery, setSearchQuery, searchResults, onSearch, onShowProtocols, onShowTools, t }) => {
    const [showResults, setShowResults] = useState(false);

    return (
        <div className="animate-fade-in">
            {/* Hero Section */}
            <div className="mb-12">
                <h2 className="text-4xl lg:text-5xl font-black mb-4 tracking-tight">
                    <span className="gradient-text">{t('hero_title')}</span>
                </h2>
                <p className="text-lg text-muted-foreground max-w-2xl">
                    {t('hero_desc')}
                </p>
            </div>

            {/* Search */}
            <div className="relative mb-10 max-w-xl">
                <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                    <Input
                        type="text"
                        placeholder={t('search_placeholder')}
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
                        t={t}
                    />
                ))}
            </div>

            {/* Tools Section - NEW */}
            <div className="mt-12 p-6 bg-green-500/5 border border-green-500/20 rounded-sm">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold text-xl flex items-center gap-2">
                        <Wrench className="h-6 w-6 text-green-500" />
                        {t('section_tools')}
                    </h3>
                    <Button 
                        onClick={onShowTools}
                        className="bg-green-500 text-white hover:bg-green-600"
                        data-testid="show-tools-btn"
                    >
                        {t('open_tools')}
                        <ChevronRight className="h-4 w-4 ml-2" />
                    </Button>
                </div>
                <p className="text-muted-foreground mb-4">
                    {t('section_tools_desc')}
                </p>
                <div className="grid md:grid-cols-4 gap-4 text-sm">
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <Calculator className="h-4 w-4 text-green-500" />
                        <span>{t('tools_subtitle1')}</span>
                    </div>
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <Table2 className="h-4 w-4 text-blue-500" />
                        <span>{t('tools_subtitle2')}</span>
                    </div>
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <AlertOctagon className="h-4 w-4 text-red-500" />
                        <span>{t('tools_subtitle3')}</span>
                    </div>
                    <div className="flex items-center gap-2 text-muted-foreground">
                        <Cable className="h-4 w-4 text-purple-500" />
                        <span>{t('tools_subtitle4')}</span>
                    </div>
                </div>
            </div>

            {/* Protocols Section */}
            <div className="mt-8 p-6 bg-blue-500/5 border border-blue-500/20 rounded-sm">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold text-xl flex items-center gap-2">
                        <ClipboardList className="h-6 w-6 text-blue-500" />
                        {t('section_protocols')}
                    </h3>
                    <Button 
                        onClick={onShowProtocols}
                        className="bg-blue-500 text-white hover:bg-blue-600"
                        data-testid="show-protocols-btn"
                    >
                        {t('show_instructions')}
                        <ChevronRight className="h-4 w-4 ml-2" />
                    </Button>
                </div>
                <p className="text-muted-foreground mb-4">
                    {t('section_protocols_desc')}
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
const ProtocolGuideCard = ({ guide, onClick, t }) => {
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
                <span className="uppercase tracking-wider">{guide.steps.length} {t('steps_count')}</span>
                <ChevronRight className="h-4 w-4 group-hover:translate-x-1 transition-transform duration-150" style={{ color: guide.color }} />
            </div>
        </button>
    );
};

// Protocol Template Card
const ProtocolTemplateCard = ({ template, t }) => {
    return (
        <div className="card-industrial" data-testid={`template-${template.id}`}>
            <h4 className="font-bold mb-2">{template.name}</h4>
            <p className="text-sm text-muted-foreground mb-4">{template.description}</p>
            <div className="space-y-2">
                <p className="text-xs uppercase tracking-wider text-muted-foreground font-bold">{t('protocols_required_measurements')}:</p>
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
const ProtocolGuideDetailView = ({ guide, onBack, t }) => {
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
const ProtocolsView = ({ onSelectGuide, onSelectExample, onBack, t, lang }) => {
    const [guides, setGuides] = useState([]);
    const [templates, setTemplates] = useState([]);
    const [examples, setExamples] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [guidesRes, templatesRes, examplesRes] = await Promise.all([
                    axios.get(`${API}/protocols/guides`, { params: { lang } }),
                    axios.get(`${API}/protocols/templates`, { params: { lang } }),
                    axios.get(`${API}/protocols/examples`, { params: { lang } })
                ]);
                setGuides(guidesRes.data);
                setTemplates(templatesRes.data);
                setExamples(examplesRes.data);
            } catch (error) {
                toast.error(t('error_loading_protocols'));
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [lang, t]);

    if (loading) {
        return (
            <div className="flex items-center justify-center py-20">
                <div className="text-center">
                    <div className="w-12 h-12 bg-blue-500 mx-auto mb-4 flex items-center justify-center animate-pulse">
                        <FileText className="h-6 w-6 text-white" />
                    </div>
                    <p className="text-muted-foreground">{t('loading')}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="animate-fade-in" data-testid="protocols-view">
            {/* Header */}
            <div className="mb-10">
                <h2 className="text-4xl font-black mb-4 tracking-tight">
                    <span className="gradient-text">{t('section_protocols')}</span>
                </h2>
                <p className="text-lg text-muted-foreground max-w-2xl">
                    {t('section_protocols_desc')}
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
                            {t('protocols_reports_desc')}
                        </p>
                        <div className="flex gap-4 text-sm">
                            <span className="text-muted-foreground">System: Windows 10/11</span>
                            <a 
                                href="https://sonel.pl/en/product/software-sonel-reports-plus" 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:underline"
                            >
                                {t('protocols_download_link')} →
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            {/* Guides */}
            <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-primary" />
                {t('protocols_step_by_step')}
            </h3>
            <div className="bento-grid mb-12">
                {guides.map((guide) => (
                    <ProtocolGuideCard 
                        key={guide.id} 
                        guide={guide} 
                        onClick={onSelectGuide}
                        t={t}
                    />
                ))}
            </div>

            {/* Example Protocols */}
            <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
                <FileText className="h-5 w-5 text-green-500" />
                {t('protocols_example_title')}
            </h3>
            <p className="text-muted-foreground mb-6">
                {t('protocols_example_desc')}
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
                            <div className={`w-10 h-10 flex items-center justify-center ${example.conclusion.includes('POZYTYWNA') || example.conclusion.includes('POSITIVE') || example.conclusion.includes('POSITIV') ? 'bg-green-500' : 'bg-red-500'}`}>
                                {example.conclusion.includes('POZYTYWNA') || example.conclusion.includes('POSITIVE') || example.conclusion.includes('POSITIV') ? (
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
                            <p>{t('protocols_date')}: {example.date}</p>
                            <p>{t('protocols_measurement_count')}: {example.measurements.length}</p>
                            <p className={example.conclusion.includes('POZYTYWNA') || example.conclusion.includes('POSITIVE') || example.conclusion.includes('POSITIV') ? 'text-green-500' : 'text-red-500'}>
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
                {t('protocols_templates_section')}
            </h3>
            <p className="text-muted-foreground mb-6">
                {t('protocols_templates_section_desc')}
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {templates.map((template) => (
                    <ProtocolTemplateCard key={template.id} template={template} t={t} />
                ))}
            </div>
        </div>
    );
};

// Tools View Component
const ToolsView = ({ onBack, t, lang }) => {
    const [activeTab, setActiveTab] = useState('calculator');
    const [zsInput, setZsInput] = useState('');
    const [voltageInput, setVoltageInput] = useState('230');
    const [calcResult, setCalcResult] = useState(null);
    const [norms, setNorms] = useState(null);
    const [errorCodes, setErrorCodes] = useState([]);
    const [diagrams, setDiagrams] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [normsRes, errorsRes, diagramsRes] = await Promise.all([
                    axios.get(`${API}/tools/norms`),
                    axios.get(`${API}/tools/error-codes`, { params: { lang } }),
                    axios.get(`${API}/tools/diagrams`)
                ]);
                setNorms(normsRes.data);
                setErrorCodes(errorsRes.data);
                setDiagrams(diagramsRes.data);
            } catch (error) {
                console.error("Error loading tools:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [lang]);

    const handleCalculate = async () => {
        if (!zsInput || parseFloat(zsInput) <= 0) {
            toast.error(t('calc_enter_valid_zs'));
            return;
        }
        try {
            const response = await axios.get(`${API}/tools/calculator`, {
                params: { zs: parseFloat(zsInput), voltage: parseFloat(voltageInput) }
            });
            setCalcResult(response.data);
        } catch (error) {
            toast.error(t('calc_error'));
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center py-20">
                <div className="w-12 h-12 bg-green-500 flex items-center justify-center animate-pulse">
                    <Wrench className="h-6 w-6 text-white" />
                </div>
            </div>
        );
    }

    return (
        <div className="animate-fade-in" data-testid="tools-view">
            {/* Header */}
            <div className="mb-8">
                <h2 className="text-4xl font-black mb-4 tracking-tight">
                    <span className="gradient-text">{t('section_tools')}</span>
                </h2>
                <p className="text-lg text-muted-foreground">
                    Kalkulator, tabele norm, kody błędów i schematy podłączeń dla MPI-530.
                </p>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
                {[
                    { id: 'calculator', icon: Calculator, label: t('tools_calc_zs'), color: 'green' },
                    { id: 'cable', icon: Zap, label: t('tools_cable'), color: 'yellow' },
                    { id: 'norms', icon: Table2, label: t('tools_norms'), color: 'blue' },
                    { id: 'errors', icon: AlertOctagon, label: t('tools_errors'), color: 'red' },
                    { id: 'diagrams', icon: Cable, label: t('tools_diagrams'), color: 'purple' },
                    { id: 'checklist', icon: ClipboardCheck, label: t('tools_checklist'), color: 'orange' },
                    { id: 'pdf', icon: FileText, label: t('tools_pdf'), color: 'blue' },
                    { id: 'quiz', icon: Award, label: t('tools_quiz'), color: 'green' },
                    { id: 'notes', icon: StickyNote, label: t('tools_notes'), color: 'blue' },
                ].map(tab => (
                    <Button
                        key={tab.id}
                        variant={activeTab === tab.id ? 'default' : 'outline'}
                        onClick={() => setActiveTab(tab.id)}
                        className={activeTab === tab.id ? `bg-${tab.color}-500` : ''}
                        data-testid={`tab-${tab.id}`}
                    >
                        <tab.icon className="h-4 w-4 mr-2" />
                        {tab.label}
                    </Button>
                ))}
            </div>

            {/* Calculator Tab */}
            {activeTab === 'calculator' && (
                <div className="space-y-6">
                    <div className="card-industrial">
                        <h3 className="font-bold text-xl mb-4 flex items-center gap-2">
                            <Calculator className="h-5 w-5 text-green-500" />
                            {t('calc_title')}
                        </h3>
                        <p className="text-muted-foreground mb-6">
                            {t('calc_desc')}
                        </p>
                        
                        <div className="grid md:grid-cols-3 gap-4 mb-6">
                            <div>
                                <label className="block text-sm font-bold mb-2">{t('calc_zs_label')}</label>
                                <Input
                                    type="number"
                                    step="0.01"
                                    value={zsInput}
                                    onChange={(e) => setZsInput(e.target.value)}
                                    placeholder="np. 0.45"
                                    data-testid="zs-input"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-bold mb-2">{t('calc_voltage_label')}</label>
                                <Input
                                    type="number"
                                    value={voltageInput}
                                    onChange={(e) => setVoltageInput(e.target.value)}
                                    placeholder="230"
                                    data-testid="voltage-input"
                                />
                            </div>
                            <div className="flex items-end">
                                <Button 
                                    onClick={handleCalculate}
                                    className="bg-green-500 text-white w-full"
                                    data-testid="calculate-btn"
                                >
                                    {t('calc_calculate')}
                                </Button>
                            </div>
                        </div>

                        {calcResult && (
                            <div className="mt-6 space-y-4">
                                <div className="lcd-result p-6">
                                    <div className="text-xs uppercase tracking-wider opacity-70 mb-2">Prąd zwarciowy</div>
                                    <div className="text-4xl font-mono font-bold">
                                        Ik = {calcResult.result.Ik} A
                                    </div>
                                    <div className="text-sm mt-2 opacity-70">
                                        Wzór: {calcResult.formula} = {calcResult.input.Uo}V / {calcResult.input.Zs}Ω
                                    </div>
                                </div>

                                {calcResult.recommendations.length > 0 && (
                                    <div>
                                        <h4 className="font-bold mb-3">Pasujące zabezpieczenia:</h4>
                                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
                                            {calcResult.recommendations.slice(0, 6).map((rec, idx) => (
                                                <div key={idx} className="p-3 bg-green-500/10 border border-green-500/20 rounded-sm">
                                                    <div className="font-bold text-lg">{rec.type}</div>
                                                    <div className="text-sm text-muted-foreground">
                                                        Zs max: {rec.Zs_max} Ω
                                                    </div>
                                                    <div className="text-sm text-green-500">
                                                        Margines: {rec.margin}%
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Norms Tab */}
            {activeTab === 'norms' && norms && (
                <div className="space-y-8">
                    {/* Zs Tables */}
                    <div className="card-industrial">
                        <h3 className="font-bold text-xl mb-4">Maksymalne impedancje pętli zwarcia</h3>
                        <p className="text-muted-foreground mb-4">Wg PN-HD 60364-4-41, Uo=230V, czas 0.4s</p>
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm border border-border">
                                <thead className="bg-muted/50">
                                    <tr>
                                        <th className="p-2 border-b text-left">Typ</th>
                                        <th className="p-2 border-b text-right">In [A]</th>
                                        <th className="p-2 border-b text-right">Ia [A]</th>
                                        <th className="p-2 border-b text-right">Zs max [Ω]</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {Object.entries(norms.zs_tables.data).map(([type, values]) => (
                                        Object.entries(values).map(([rating, data], idx) => (
                                            <tr key={`${type}${rating}`} className="hover:bg-muted/30">
                                                <td className="p-2 border-b font-bold">{type}{rating}</td>
                                                <td className="p-2 border-b text-right">{rating}</td>
                                                <td className="p-2 border-b text-right">{data.Ia}</td>
                                                <td className="p-2 border-b text-right font-mono">{data.Zs_max}</td>
                                            </tr>
                                        ))
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* Insulation */}
                    <div className="card-industrial">
                        <h3 className="font-bold text-xl mb-4">Minimalna rezystancja izolacji</h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm border border-border">
                                <thead className="bg-muted/50">
                                    <tr>
                                        <th className="p-2 border-b text-left">Napięcie instalacji</th>
                                        <th className="p-2 border-b text-right">Napięcie pomiarowe [V]</th>
                                        <th className="p-2 border-b text-right">Min. izolacja [MΩ]</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {norms.insulation.data.map((row, idx) => (
                                        <tr key={idx} className="hover:bg-muted/30">
                                            <td className="p-2 border-b">{row.voltage_range}</td>
                                            <td className="p-2 border-b text-right">{row.test_voltage}</td>
                                            <td className="p-2 border-b text-right font-mono font-bold">{row.min_resistance}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* RCD Times */}
                    <div className="card-industrial">
                        <h3 className="font-bold text-xl mb-4">Maksymalne czasy zadziałania RCD</h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm border border-border">
                                <thead className="bg-muted/50">
                                    <tr>
                                        <th className="p-2 border-b text-left">Typ RCD</th>
                                        <th className="p-2 border-b text-left">Mnożnik</th>
                                        <th className="p-2 border-b text-right">Max czas [ms]</th>
                                        <th className="p-2 border-b text-left">Opis</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {norms.rcd_times.data.map((row, idx) => (
                                        <tr key={idx} className="hover:bg-muted/30">
                                            <td className="p-2 border-b">{row.type}</td>
                                            <td className="p-2 border-b">{row.multiplier}</td>
                                            <td className="p-2 border-b text-right font-mono font-bold">
                                                {row.max_time_ms || '-'}
                                            </td>
                                            <td className="p-2 border-b text-muted-foreground">{row.description}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* Lighting */}
                    <div className="card-industrial">
                        <h3 className="font-bold text-xl mb-4">Minimalne natężenie oświetlenia (PN-EN 12464-1)</h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm border border-border">
                                <thead className="bg-muted/50">
                                    <tr>
                                        <th className="p-2 border-b text-left">Pomieszczenie / Czynność</th>
                                        <th className="p-2 border-b text-right">Min. [lx]</th>
                                        <th className="p-2 border-b text-right">UGR max</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {norms.lighting.data.map((row, idx) => (
                                        <tr key={idx} className="hover:bg-muted/30">
                                            <td className="p-2 border-b">{row.area}</td>
                                            <td className="p-2 border-b text-right font-mono font-bold">{row.min_lux}</td>
                                            <td className="p-2 border-b text-right">{row.ugr_max}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            )}

            {/* Error Codes Tab */}
            {activeTab === 'errors' && (
                <div className="space-y-4">
                    <h3 className="font-bold text-xl mb-4">Kody błędów miernika MPI-530</h3>
                    {errorCodes.map((error, idx) => (
                        <div key={idx} className="card-industrial">
                            <div className="flex items-start gap-4">
                                <div className="w-16 h-16 bg-red-500 flex items-center justify-center flex-shrink-0">
                                    <span className="text-white font-mono font-bold text-lg">{error.code}</span>
                                </div>
                                <div className="flex-1">
                                    <h4 className="font-bold text-lg">{error.name}</h4>
                                    <p className="text-muted-foreground mb-3">{error.description}</p>
                                    
                                    <div className="grid md:grid-cols-2 gap-4">
                                        <div>
                                            <p className="font-bold text-sm mb-2">Przyczyny:</p>
                                            <ul className="text-sm text-muted-foreground space-y-1">
                                                {error.causes.map((cause, i) => (
                                                    <li key={i} className="flex items-start gap-2">
                                                        <span className="text-red-500">•</span>
                                                        {cause}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                        <div>
                                            <p className="font-bold text-sm mb-2">Rozwiązania:</p>
                                            <ul className="text-sm text-muted-foreground space-y-1">
                                                {error.solutions.map((solution, i) => (
                                                    <li key={i} className="flex items-start gap-2">
                                                        <span className="text-green-500">•</span>
                                                        {solution}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Diagrams Tab */}
            {activeTab === 'diagrams' && (
                <div className="space-y-6">
                    <h3 className="font-bold text-xl mb-4">Schematy podłączeń</h3>
                    {diagrams.map((diagram, idx) => (
                        <div key={idx} className="card-industrial">
                            <h4 className="font-bold text-lg mb-2">{diagram.name}</h4>
                            <p className="text-muted-foreground mb-4">{diagram.description}</p>
                            
                            <div className="grid md:grid-cols-2 gap-6">
                                {/* Connections */}
                                <div>
                                    <p className="font-bold text-sm mb-3 uppercase tracking-wider">Podłączenia:</p>
                                    <div className="space-y-2">
                                        {diagram.connections.map((conn, i) => (
                                            <div key={i} className="flex items-center gap-3 p-2 bg-muted/30 rounded-sm">
                                                <div 
                                                    className="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold"
                                                    style={{ backgroundColor: conn.color }}
                                                >
                                                    {conn.terminal.substring(0, 2)}
                                                </div>
                                                <div>
                                                    <p className="font-bold text-sm">{conn.terminal}</p>
                                                    <p className="text-xs text-muted-foreground">{conn.connect_to}</p>
                                                </div>
                                                <span className="text-xs text-muted-foreground ml-auto">
                                                    {conn.cable}
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Notes */}
                                <div>
                                    <p className="font-bold text-sm mb-3 uppercase tracking-wider">Uwagi:</p>
                                    <ul className="space-y-2 text-sm">
                                        {diagram.notes.map((note, i) => (
                                            <li key={i} className={`flex items-start gap-2 ${note.includes('WYŁĄCZ') || note.includes('napięciem') ? 'text-red-500 font-bold' : 'text-muted-foreground'}`}>
                                                <AlertTriangle className={`h-4 w-4 flex-shrink-0 mt-0.5 ${note.includes('WYŁĄCZ') || note.includes('napięciem') ? 'text-red-500' : 'text-yellow-500'}`} />
                                                {note}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Cable Calculator Tab */}
            {activeTab === 'cable' && <CableCalculatorTab lang={lang} t={t} />}

            {/* Safety Checklist Tab */}
            {activeTab === 'checklist' && <SafetyChecklistTab lang={lang} t={t} />}

            {/* PDF Generator Tab */}
            {activeTab === 'pdf' && <PDFGeneratorTab t={t} />}

            {/* Quiz Tab */}
            {activeTab === 'quiz' && <QuizTab lang={lang} t={t} />}

            {/* Notes Tab */}
            {activeTab === 'notes' && <NotesHistoryTab t={t} />}
        </div>
    );
};

// Example Protocol Detail View
const ExampleProtocolDetailView = ({ example, onBack, t }) => {
    const isPositive = example.conclusion.includes('POZYTYWNA') || example.conclusion.includes('POSITIVE') || example.conclusion.includes('POSITIV');
    
    // Check for PASS or OK status (supports both EN/DE/PL formats)
    const isStatusPass = (status) => status === 'OK' || status === 'PASS' || status === 'BESTANDEN';
    
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
                    <h3 className="font-bold mb-4 uppercase text-sm tracking-wider">{t('protocols_object')}</h3>
                    <div className="space-y-2 text-sm">
                        <p><span className="text-muted-foreground">{t('protocols_object')}:</span> {example.object_name}</p>
                        <p><span className="text-muted-foreground">{t('protocols_notes')}:</span> {example.object_address}</p>
                        <p><span className="text-muted-foreground">{t('protocols_date')}:</span> {example.date}</p>
                    </div>
                </div>
                <div className="card-industrial">
                    <h3 className="font-bold mb-4 uppercase text-sm tracking-wider">{t('protocols_inspector')}</h3>
                    <div className="space-y-2 text-sm">
                        <p><span className="text-muted-foreground">{t('protocols_inspector')}:</span> {example.inspector}</p>
                        <p><span className="text-muted-foreground">{t('protocols_calibration')}:</span> {example.inspector_cert}</p>
                        <p><span className="text-muted-foreground">{t('protocols_meter')}:</span> {example.meter_serial}</p>
                        <p><span className="text-muted-foreground">{t('protocols_calibration')}:</span> {example.meter_calibration}</p>
                    </div>
                </div>
            </div>

            {/* Measurements Table */}
            <h3 className="font-bold mb-4 uppercase text-sm tracking-wider flex items-center gap-2">
                <ClipboardList className="h-4 w-4" />
                {t('protocols_measurements_table')} ({example.measurements.length})
            </h3>
            <div className="overflow-x-auto mb-8">
                <table className="w-full text-sm border border-border">
                    <thead className="bg-muted/50">
                        <tr>
                            <th className="text-left p-3 border-b border-border font-bold">{t('protocols_point')}</th>
                            <th className="text-left p-3 border-b border-border font-bold">{t('protocols_circuit')}</th>
                            <th className="text-left p-3 border-b border-border font-bold">{t('protocols_protection')}</th>
                            <th className="text-right p-3 border-b border-border font-bold">{t('protocols_value')}</th>
                            <th className="text-left p-3 border-b border-border font-bold">{t('protocols_limit')}</th>
                            <th className="text-center p-3 border-b border-border font-bold">{t('protocols_status')}</th>
                            <th className="text-left p-3 border-b border-border font-bold">{t('protocols_notes')}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {example.measurements.map((m, idx) => (
                            <tr key={idx} className={`${!isStatusPass(m.status) ? 'bg-red-500/10' : ''} hover:bg-muted/30`}>
                                <td className="p-3 border-b border-border">{m.point}</td>
                                <td className="p-3 border-b border-border font-mono">{m.circuit}</td>
                                <td className="p-3 border-b border-border">{m.protection}</td>
                                <td className="p-3 border-b border-border text-right font-mono font-bold">
                                    {m.value} {m.unit !== '-' && m.unit}
                                </td>
                                <td className="p-3 border-b border-border text-muted-foreground">{m.limit}</td>
                                <td className="p-3 border-b border-border text-center">
                                    {isStatusPass(m.status) ? (
                                        <span className="inline-flex items-center gap-1 text-green-500 font-bold">
                                            <CheckCircle2 className="h-4 w-4" /> {t('pdf_result_pass')}
                                        </span>
                                    ) : (
                                        <span className="inline-flex items-center gap-1 text-red-500 font-bold">
                                            <AlertTriangle className="h-4 w-4" /> {t('pdf_result_fail')}
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
                        {t('protocols_recommendations')}
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
    const { lang, switchLang, t } = useLanguage();
    const [functions, setFunctions] = useState([]);
    const [selectedFunction, setSelectedFunction] = useState(null);
    const [loading, setLoading] = useState(true);
    const [darkMode, setDarkMode] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [currentView, setCurrentView] = useState('home'); // 'home', 'protocols', 'protocol-detail', 'example-detail', 'tools'
    const [selectedGuide, setSelectedGuide] = useState(null);
    const [selectedExample, setSelectedExample] = useState(null);

    // Fetch functions on mount and when language changes
    useEffect(() => {
        const fetchFunctions = async () => {
            try {
                const response = await axios.get(`${API}/functions`, { params: { lang } });
                setFunctions(response.data);
            } catch (error) {
                toast.error(t('error_loading'));
            } finally {
                setLoading(false);
            }
        };
        fetchFunctions();
    }, [lang, t]);

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
            const response = await axios.get(`${API}/search`, { params: { q: query, lang } });
            setSearchResults(response.data);
        } catch (error) {
            console.error("Search error:", error);
        }
    }, [lang]);

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
            const response = await axios.get(`${API}/protocols/guides/${guideId}`, { params: { lang } });
            setSelectedGuide(response.data);
            setCurrentView('protocol-detail');
        } catch (error) {
            console.error("Error loading instructions:", error);
            toast.error(t('error_loading_instructions'));
        }
    };

    // Select example handler
    const handleSelectExample = async (exampleId) => {
        try {
            const response = await axios.get(`${API}/protocols/examples/${exampleId}`, { params: { lang } });
            setSelectedExample(response.data);
            setCurrentView('example-detail');
        } catch (error) {
            console.error("Error loading example:", error);
            toast.error(t('error_loading_example'));
        }
    };

    // Show tools
    const handleShowTools = () => {
        setSelectedFunction(null);
        setCurrentView('tools');
    };

    // Back handler
    const handleBack = () => {
        if (currentView === 'protocol-detail' || currentView === 'example-detail') {
            setSelectedGuide(null);
            setSelectedExample(null);
            setCurrentView('protocols');
        } else if (currentView === 'protocols' || currentView === 'tools') {
            setCurrentView('home');
        } else {
            setSelectedFunction(null);
        }
    };

    const showBackButton = selectedFunction || currentView === 'protocols' || currentView === 'protocol-detail' || currentView === 'example-detail' || currentView === 'tools';

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background">
                <div className="text-center">
                    <div className="w-16 h-16 bg-primary mx-auto mb-4 flex items-center justify-center animate-pulse">
                        <span className="text-primary-foreground font-bold font-mono">MPI</span>
                    </div>
                    <p className="text-muted-foreground uppercase tracking-wider text-sm">{t('loading')}</p>
                </div>
            </div>
        );
    }

    // Render current view
    const renderMainContent = () => {
        if (selectedFunction) {
            return <DetailView func={selectedFunction} onBack={handleBack} t={t} />;
        }
        
        switch (currentView) {
            case 'protocols':
                return <ProtocolsView onSelectGuide={handleSelectGuide} onSelectExample={handleSelectExample} onBack={handleBack} t={t} lang={lang} />;
            case 'protocol-detail':
                return selectedGuide ? <ProtocolGuideDetailView guide={selectedGuide} onBack={handleBack} t={t} /> : null;
            case 'example-detail':
                return selectedExample ? <ExampleProtocolDetailView example={selectedExample} onBack={handleBack} t={t} /> : null;
            case 'tools':
                return <ToolsView onBack={handleBack} t={t} lang={lang} />;
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
                        onShowTools={handleShowTools}
                        t={t}
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
                lang={lang}
                switchLang={switchLang}
                t={t}
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

function AppWrapper() {
    return (
        <LanguageProvider>
            <App />
        </LanguageProvider>
    );
}

export default AppWrapper;
