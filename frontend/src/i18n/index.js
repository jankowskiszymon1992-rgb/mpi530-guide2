import React, { createContext, useContext, useState, useCallback } from 'react';
import pl from './pl.json';
import en from './en.json';
import de from './de.json';

const translations = { pl, en, de };
const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
    const [lang, setLang] = useState(() => localStorage.getItem('sonel-lang') || 'pl');

    const switchLang = useCallback((newLang) => {
        setLang(newLang);
        localStorage.setItem('sonel-lang', newLang);
    }, []);

    const t = useCallback((key) => {
        return translations[lang]?.[key] || translations['pl']?.[key] || key;
    }, [lang]);

    return (
        <LanguageContext.Provider value={{ lang, switchLang, t }}>
            {children}
        </LanguageContext.Provider>
    );
};

export const useLanguage = () => useContext(LanguageContext);
