"""
Complete EN and DE translations for Sonel MPI-530 Interactive Guide.
Polish (PL) content stays in server.py as default.
"""

# ============================================
# MEASUREMENT FUNCTIONS TRANSLATIONS
# ============================================

FUNCTIONS_EN = {
    "rcd": {
        "name": "RCD (Residual Current Device) Testing",
        "description": "Measuring trip time and current of residual current devices (RCD/RCCB)",
        "steps": [
            {"title": "Preparation", "description": "Set the function dial to RCD position. Make sure the installation is energized.", "warning": "WARNING: Measurement performed under voltage! Exercise extreme caution.", "tip": "Check that the RCD is switched on before testing."},
            {"title": "Cable connection", "description": "Connect the blue cable to L/L1/L2 socket, red to PE socket. Use a single-pole probe or WS-03 socket adapter.", "warning": "Check connections before starting the test."},
            {"title": "Parameter selection", "description": "Select RCD type (AC, A, B), rated current (10, 30, 100, 300, 500 mA) and test current multiplier (0.5x, 1x, 2x, 5x).", "tip": "For standard household RCDs, use type AC and 30mA."},
            {"title": "Measurement", "description": "Press START. The meter will force a differential current and measure the RCD trip time.", "tip": "After RCD trips, switch it back on before the next measurement."},
            {"title": "Reading the result", "description": "Read the trip time [ms] and touch voltage [V]. For 30mA RCD, time should be <300ms at 1x IΔn."}
        ],
        "parameters": ["RCD Type: AC, A, B, F", "Current IΔn: 10-500 mA", "Multiplier: 0.5x, 1x, 2x, 5x", "Starting phase: 0°, 180°"],
        "safety_notes": ["Measurement under voltage - exercise caution", "RCD will trip during test - warn installation users", "Check PE continuity before RCD testing"],
        "expected_results": "Trip time <300ms for 1x IΔn, <150ms for 2x IΔn, <40ms for 5x IΔn"
    },
    "loop": {
        "name": "Fault Loop Impedance",
        "description": "Measuring L-PE and L-N fault loop impedance to verify shock protection effectiveness",
        "steps": [
            {"title": "Function selection", "description": "Set the dial to Zs (loop impedance). Select L-PE or L-N mode.", "warning": "Measurement performed under voltage!"},
            {"title": "Connection", "description": "Connect WS-03 socket adapter or use probes: L to phase, N to neutral, PE to protective conductor.", "tip": "For L-PE measurement, connection to protective conductor is required."},
            {"title": "Parameter settings", "description": "Select measurement range and type (standard or high-current for better accuracy).", "tip": "High-current mode gives more accurate results in low-impedance installations."},
            {"title": "Measurement", "description": "Press START. The meter will measure loop impedance and calculate expected fault current.", "warning": "Brief current flow through installation may occur during measurement."},
            {"title": "Result analysis", "description": "Read Zs [Ω] and Ik [A]. Compare with permissible values for the given protection device."}
        ],
        "parameters": ["Range Zs: 0.00-1999 Ω", "Resolution: 0.01 Ω", "Test current: up to 7.6 A", "Voltage: 180-253 V"],
        "safety_notes": ["Measurement under voltage - exercise caution", "In circuits with RCD, the device may trip during measurement", "Test current may cause disturbances in the installation"],
        "expected_results": "Zs must ensure protection device operates within required time (Zs < Uo/Ia)"
    },
    "insulation": {
        "name": "Insulation Resistance",
        "description": "Measuring insulation resistance of cables and equipment with voltage up to 1000V DC",
        "steps": [
            {"title": "Disconnecting voltage", "description": "SWITCH OFF the installation power! Disconnect all devices sensitive to test voltage.", "warning": "ABSOLUTELY switch off voltage before insulation measurement! Test voltage up to 1000V DC."},
            {"title": "Function and voltage selection", "description": "Set the dial to RISO. Select test voltage: 50V, 100V, 250V, 500V or 1000V.", "tip": "For 230V installations use 500V test voltage. For 400V installations - 1000V."},
            {"title": "Cable connection", "description": "Connect cables to tested insulation (e.g. L1-PE, L1-N, L1-L2). Use crocodile clips or probes.", "tip": "For whole installation measurement, connect all phases together and measure against PE."},
            {"title": "Measurement", "description": "Press and hold START. The meter will apply test voltage and measure insulation resistance.", "warning": "Do not touch tested circuits during measurement - voltage up to 1000V DC!"},
            {"title": "Discharge and reading", "description": "After releasing START, the meter automatically discharges capacitance. Read the result in MΩ.", "tip": "Minimum value for new installations: 1 MΩ. For existing: 0.5 MΩ."}
        ],
        "parameters": ["Voltage: 50, 100, 250, 500, 1000 V DC", "Range: 0.00 MΩ - 10 GΩ", "Test current: max 1.2 mA"],
        "safety_notes": ["SWITCH OFF voltage before measurement!", "Test voltage up to 1000V DC - electrocution hazard", "Discharge cable capacitance before touching", "Disconnect sensitive elements (meters, controllers, LEDs)"],
        "expected_results": "≥1 MΩ for new installations, ≥0.5 MΩ for existing ones"
    },
    "earthing": {
        "name": "Earth Resistance",
        "description": "Measuring earth resistance using 3-wire and 4-wire technical method",
        "steps": [
            {"title": "Method selection", "description": "Set the dial to RE. Select method: 3-wire (technical) or 4-wire (more accurate).", "tip": "4-wire method eliminates the influence of test lead resistance."},
            {"title": "Electrode preparation", "description": "Drive the current electrode (H) at least 40m from the tested earth, voltage electrode (S) at 62% of that distance.", "warning": "Disconnect the tested earthing from the installation before measurement!"},
            {"title": "Connection", "description": "Connect: E - tested earth, S - voltage electrode, H - current electrode. Use reel cables.", "tip": "Place electrodes in a straight line with the tested earthing."},
            {"title": "Measurement", "description": "Press START. The meter will measure resistance and check measurement validity (RE S and H check).", "tip": "If result is unstable - check soil moisture at auxiliary electrodes."},
            {"title": "Reading and completion", "description": "Read RE [Ω]. For protective earthing, typical value <10 Ω.", "warning": "Remember to reconnect earthing to the installation after measurement!"}
        ],
        "parameters": ["Range: 0.00-9999 Ω", "Resolution: 0.01 Ω", "Frequency: 125 Hz", "Test current: >200 mA"],
        "safety_notes": ["Disconnect earthing from installation before measurement", "Keep safe distance from high voltage lines", "Drive auxiliary electrodes into moist soil", "Reconnect earthing after measurement"],
        "expected_results": "<10 Ω for protective earthing, <2 Ω for functional earthing"
    },
    "voltage": {
        "name": "Voltage Measurement",
        "description": "Measuring AC and DC voltage and frequency (TRMS)",
        "steps": [
            {"title": "Function selection", "description": "Set the dial to U (voltage). The meter automatically detects AC/DC.", "tip": "For phase-to-phase voltage measurement use L-L function."},
            {"title": "Connection", "description": "Connect red probe to measurement point, blue to reference point (N or PE).", "warning": "Do not exceed maximum voltage 550V AC!"},
            {"title": "Reading the result", "description": "Read voltage [V] and frequency [Hz] on the display. TRMS measurement gives accurate results for distorted waveforms.", "tip": "Phase voltage should be 220-240V, phase-to-phase 380-420V."}
        ],
        "parameters": ["AC Range: 0-550 V", "DC Range: 0-550 V", "Frequency: 45-65 Hz", "Accuracy: ±1%"],
        "safety_notes": ["Do not exceed 550V AC/DC", "Use test leads in good condition", "Measurement category CAT III 600V / CAT IV 300V"],
        "expected_results": "Phase voltage: 220-240V, phase-to-phase: 380-420V, frequency: 49.5-50.5 Hz"
    },
    "continuity": {
        "name": "Protective Conductor Continuity",
        "description": "Measuring continuity and resistance of PE conductors and bonding connections with 200mA current",
        "steps": [
            {"title": "Disconnecting voltage", "description": "SWITCH OFF the installation power before continuity measurement!", "warning": "Measurement performed WITHOUT voltage in the installation!"},
            {"title": "Function selection", "description": "Set the dial to RCONT (continuity). Select 200mA test current as per standard.", "tip": "200mA current is required by EN 61557-4 standard."},
            {"title": "Lead compensation", "description": "Short-circuit test lead ends and perform lead resistance compensation (ZERO button).", "tip": "Compensation eliminates the influence of test lead resistance on the result."},
            {"title": "Measurement", "description": "Connect one lead to PE busbar in the distribution board, other to tested point (socket, equipment housing).", "tip": "Measure from distribution board to the farthest point of the circuit."},
            {"title": "Reading and assessment", "description": "Read resistance [Ω]. Maximum permissible value depends on PE conductor cross-section.", "warning": "Value >1 Ω indicates a problem with protective conductor continuity!"}
        ],
        "parameters": ["Range: 0.00-400 Ω", "Current: 200 mA (per EN 61557-4)", "Open voltage: 4-24 V", "Resolution: 0.01 Ω"],
        "safety_notes": ["SWITCH OFF voltage before measurement!", "Compensate test lead resistance", "Check all PE connection points", "200mA current is required by the standard"],
        "expected_results": "<1 Ω for protective conductors, <0.1 Ω for main bonding connections"
    },
    "phase_sequence": {
        "name": "Phase Sequence",
        "description": "Checking correct phase sequence L1-L2-L3 in three-phase installation",
        "steps": [
            {"title": "Function selection", "description": "Set the dial to phase sequence symbol (1-2-3). This function checks phase sequence compliance.", "tip": "Correct phase sequence is essential for proper three-phase motor operation."},
            {"title": "Cable connection", "description": "Connect three test leads to three phases: L1 (yellow), L2 (red), L3 (blue). Use probes or crocodile clips.", "warning": "Measurement under three-phase voltage 400V! Exercise extreme caution."},
            {"title": "Reading the result", "description": "The meter will indicate phase sequence: CORRECT (1-2-3) or INCORRECT (3-2-1). It will also display phase-to-phase voltages.", "tip": "For incorrect sequence, swap any two phases."}
        ],
        "parameters": ["Voltage L-L: 95-500 V", "Frequency: 45-65 Hz", "Indication: correct/incorrect", "Display: UL1-L2, UL2-L3, UL3-L1"],
        "safety_notes": ["Measurement under three-phase voltage 400V!", "Use cables with good insulation", "Do not touch probe tips during measurement", "Category CAT III 600V"],
        "expected_results": "CORRECT sequence (1-2-3), phase-to-phase voltages 380-420V"
    },
    "motor_rotation": {
        "name": "Motor Rotation Direction",
        "description": "Determining three-phase motor rotation direction (clockwise/counter-clockwise) without starting it",
        "steps": [
            {"title": "Function selection", "description": "Set the dial to motor rotation test (motor symbol). This function determines rotation direction without starting the motor.", "tip": "Useful when connecting new motors or after maintenance."},
            {"title": "Connection to power supply", "description": "Connect test leads to motor power terminals (U, V, W or L1, L2, L3) at the network connection point.", "warning": "Motor must be DISCONNECTED from power during cable connection!"},
            {"title": "Switching on power", "description": "After safe cable connection, switch on three-phase power. DO NOT start the motor.", "warning": "Measurement under voltage! Make sure the motor is not accidentally started."},
            {"title": "Reading the result", "description": "The meter will indicate rotation direction: CLOCKWISE (right) or COUNTER-CLOCKWISE (left). Phase voltages will also be displayed.", "tip": "To change rotation direction, swap any two power phase connections."}
        ],
        "parameters": ["Voltage L-L: 95-500 V", "Frequency: 45-65 Hz", "Indication: right/left", "Simulation without motor startup"],
        "safety_notes": ["Disconnect power before connecting cables!", "Make sure motor is not started during test", "Measurement under three-phase voltage", "Disconnect power before removing cables after test"],
        "expected_results": "RIGHT or LEFT direction - depending on phase connection"
    },
    "lux": {
        "name": "Illumination Measurement",
        "description": "Measuring illumination in lux (lx) using external LP-1 or LP-10 probe",
        "steps": [
            {"title": "Probe connection", "description": "Connect the lux probe LP-1, LP-10A or LP-10B to the meter's miniDIN-4P socket. Use WS-06 adapter if required.", "tip": "LP-10B probe has extended range up to 400 klx."},
            {"title": "Function selection", "description": "Set the dial to LUX. The meter will automatically detect the connected probe.", "tip": "Wait about 1 minute for probe stabilization before measurement."},
            {"title": "Probe positioning", "description": "Place the probe at the measurement point. The photocell should face the light source or work surface.", "tip": "For workplace illumination measurement, place probe at desk height (85 cm)."},
            {"title": "Reading the result", "description": "Read illumination in lux [lx] or foot-candles [fc]. The value stabilizes after a few seconds.", "tip": "PN-EN 12464-1 standard specifies minimum values for various workstations."}
        ],
        "parameters": ["Range: 0-400 klx", "Resolution: from 0.001 lx", "Units: lx or fc", "Probes: LP-1, LP-10A, LP-10B"],
        "safety_notes": ["Do not expose probe to direct sunlight for extended periods", "Avoid touching the photocell with fingers", "Store probe in protective case", "Calibrate probe every 12 months"],
        "expected_results": "Office: 500 lx, Production: 300-500 lx, Warehouse: 100-200 lx, Corridor: 100 lx"
    },
    "earthing_clamp": {
        "name": "Earth Resistance - Clamp Method",
        "description": "Measuring earth resistance using two-clamp (2-clamp) method without auxiliary electrodes",
        "steps": [
            {"title": "Clamp preparation", "description": "Prepare clamp set: measuring clamp C-3 and transmitting clamp N-1. Connect them to appropriate meter sockets.", "tip": "Clamp method doesn't require driving electrodes - ideal for hardened surfaces."},
            {"title": "Function selection", "description": "Set the dial to RE and select 2-clamp method (2C or 2-clamp). The meter will switch to clamp measurement mode.", "warning": "Method requires earthing to be part of a closed circuit (e.g., connected to other earth electrodes)."},
            {"title": "Clamp placement", "description": "Place transmitting clamp N-1 on the earthing conductor. At least 30 cm away, place measuring clamp C-3 on the same conductor.", "tip": "Clamps must embrace only the earthing conductor, not other parallel conductors."},
            {"title": "Measurement", "description": "Press START. The meter will force current through transmitting clamp and measure voltage on measuring clamp.", "tip": "Result includes tested earth resistance and parallel combination of remaining earths."},
            {"title": "Result interpretation", "description": "Read resistance RE [Ω]. Remember that the result is the tested earth resistance in the system with other earths.", "warning": "Clamp method gives underestimated result if earths are connected in parallel!"}
        ],
        "parameters": ["Range: 0.00-99.9 kΩ", "Resolution: from 0.01 Ω", "Clamps: C-3 + N-1", "No auxiliary electrodes required"],
        "safety_notes": ["Method requires closed earthing circuit", "Place clamps only on earthing conductor", "Maintain min. 30 cm spacing between clamps", "Result may be underestimated with parallel earths"],
        "expected_results": "<10 Ω for protective earthing (consider influence of parallel earths)"
    }
}

FUNCTIONS_DE = {
    "rcd": {
        "name": "RCD-Prüfung (Fehlerstromschutzschalter)",
        "description": "Messung der Auslösezeit und des Stroms von Fehlerstromschutzschaltern (RCD/RCCB)",
        "steps": [
            {"title": "Vorbereitung", "description": "Stellen Sie den Funktionsdrehschalter auf RCD. Stellen Sie sicher, dass die Anlage unter Spannung steht.", "warning": "ACHTUNG: Messung unter Spannung! Äußerste Vorsicht walten lassen.", "tip": "Prüfen Sie vor der Messung, ob der RCD eingeschaltet ist."},
            {"title": "Kabelanschluss", "description": "Blaues Kabel an L/L1/L2-Buchse, rotes an PE-Buchse anschließen. Einpolige Sonde oder WS-03-Steckdosenadapter verwenden.", "warning": "Verbindungen vor dem Starten des Tests überprüfen."},
            {"title": "Parameterauswahl", "description": "RCD-Typ (AC, A, B), Nennstrom (10, 30, 100, 300, 500 mA) und Prüfstrom-Multiplikator (0.5x, 1x, 2x, 5x) wählen.", "tip": "Für Standard-Haushalts-RCDs Typ AC und 30mA verwenden."},
            {"title": "Messung", "description": "START drücken. Das Messgerät erzwingt einen Differenzstrom und misst die RCD-Auslösezeit.", "tip": "Nach RCD-Auslösung vor der nächsten Messung wieder einschalten."},
            {"title": "Ergebnis ablesen", "description": "Auslösezeit [ms] und Berührungsspannung [V] ablesen. Bei 30mA RCD sollte die Zeit bei 1x IΔn <300ms betragen."}
        ],
        "parameters": ["RCD-Typ: AC, A, B, F", "Strom IΔn: 10-500 mA", "Multiplikator: 0.5x, 1x, 2x, 5x", "Startphase: 0°, 180°"],
        "safety_notes": ["Messung unter Spannung - Vorsicht walten lassen", "RCD löst während des Tests aus - Anlagenbenutzer warnen", "PE-Durchgangsprüfung vor RCD-Test durchführen"],
        "expected_results": "Auslösezeit <300ms bei 1x IΔn, <150ms bei 2x IΔn, <40ms bei 5x IΔn"
    },
    "loop": {
        "name": "Schleifenimpedanz",
        "description": "Messung der L-PE und L-N Schleifenimpedanz zur Überprüfung des Fehlerschutzes",
        "steps": [
            {"title": "Funktionswahl", "description": "Drehschalter auf Zs (Schleifenimpedanz) stellen. L-PE oder L-N Modus wählen.", "warning": "Messung unter Spannung!"},
            {"title": "Anschluss", "description": "WS-03-Adapter anschließen oder Sonden verwenden: L an Phase, N an Neutralleiter, PE an Schutzleiter.", "tip": "Für L-PE-Messung ist Verbindung zum Schutzleiter erforderlich."},
            {"title": "Parametereinstellung", "description": "Messbereich und Typ wählen (Standard oder Hochstrom für höhere Genauigkeit).", "tip": "Hochstrommodus liefert genauere Ergebnisse in Niedrigimpedanz-Anlagen."},
            {"title": "Messung", "description": "START drücken. Das Messgerät misst die Schleifenimpedanz und berechnet den erwarteten Kurzschlussstrom.", "warning": "Kurzzeitiger Stromfluss durch die Anlage während der Messung möglich."},
            {"title": "Ergebnisanalyse", "description": "Zs [Ω] und Ik [A] ablesen. Mit zulässigen Werten für das jeweilige Schutzgerät vergleichen."}
        ],
        "parameters": ["Bereich Zs: 0.00-1999 Ω", "Auflösung: 0.01 Ω", "Prüfstrom: bis 7.6 A", "Spannung: 180-253 V"],
        "safety_notes": ["Messung unter Spannung - Vorsicht walten lassen", "In Stromkreisen mit RCD kann das Gerät während der Messung auslösen", "Prüfstrom kann Störungen in der Anlage verursachen"],
        "expected_results": "Zs muss die Auslösung des Schutzgeräts in der erforderlichen Zeit gewährleisten (Zs < Uo/Ia)"
    },
    "insulation": {
        "name": "Isolationswiderstand",
        "description": "Messung des Isolationswiderstands von Kabeln und Geräten mit Spannung bis 1000V DC",
        "steps": [
            {"title": "Spannungsfreischaltung", "description": "Anlage SPANNUNGSFREI SCHALTEN! Alle spannungsempfindlichen Geräte trennen.", "warning": "Spannung UNBEDINGT vor der Isolationsmessung abschalten! Prüfspannung bis 1000V DC."},
            {"title": "Funktions- und Spannungswahl", "description": "Drehschalter auf RISO stellen. Prüfspannung wählen: 50V, 100V, 250V, 500V oder 1000V.", "tip": "Für 230V-Anlagen 500V Prüfspannung verwenden. Für 400V-Anlagen - 1000V."},
            {"title": "Kabelanschluss", "description": "Kabel an die zu prüfende Isolation anschließen (z.B. L1-PE, L1-N, L1-L2). Krokodilklemmen oder Sonden verwenden.", "tip": "Für Gesamtanlagenmessung alle Phasen zusammenschließen und gegen PE messen."},
            {"title": "Messung", "description": "START drücken und halten. Das Messgerät legt Prüfspannung an und misst den Isolationswiderstand.", "warning": "Geprüfte Stromkreise während der Messung nicht berühren - Spannung bis 1000V DC!"},
            {"title": "Entladung und Ablesen", "description": "Nach Loslassen von START entlädt das Messgerät automatisch die Kapazität. Ergebnis in MΩ ablesen.", "tip": "Mindestwert für neue Anlagen: 1 MΩ. Für bestehende: 0.5 MΩ."}
        ],
        "parameters": ["Spannung: 50, 100, 250, 500, 1000 V DC", "Bereich: 0.00 MΩ - 10 GΩ", "Prüfstrom: max 1.2 mA"],
        "safety_notes": ["Spannung vor der Messung ABSCHALTEN!", "Prüfspannung bis 1000V DC - Stromschlaggefahr", "Kabelkapazität vor dem Berühren entladen", "Empfindliche Geräte trennen (Zähler, Steuerungen, LEDs)"],
        "expected_results": "≥1 MΩ für neue Anlagen, ≥0.5 MΩ für bestehende"
    },
    "earthing": {
        "name": "Erdungswiderstand",
        "description": "Messung des Erdungswiderstands mit 3- und 4-Leiter-Methode",
        "steps": [
            {"title": "Methodenwahl", "description": "Drehschalter auf RE stellen. Methode wählen: 3-Leiter (technisch) oder 4-Leiter (genauer).", "tip": "4-Leiter-Methode eliminiert den Einfluss des Messleitungswiderstands."},
            {"title": "Elektrodenvorbereitung", "description": "Stromelektrode (H) mind. 40m vom Prüferder entfernt einschlagen, Spannungselektrode (S) bei 62% dieser Entfernung.", "warning": "Prüferdung vor der Messung von der Anlage trennen!"},
            {"title": "Anschluss", "description": "Anschließen: E - Prüferder, S - Spannungselektrode, H - Stromelektrode. Trommelkabel verwenden.", "tip": "Elektroden in einer Linie mit dem Prüferder aufstellen."},
            {"title": "Messung", "description": "START drücken. Messgerät misst Widerstand und prüft Messgültigkeit (RE S- und H-Prüfung).", "tip": "Bei instabilem Ergebnis - Bodenfeuchtigkeit an Hilfselektroden prüfen."},
            {"title": "Ablesen und Abschluss", "description": "RE [Ω] ablesen. Für Schutzerdung typischer Wert <10 Ω.", "warning": "Erdung nach der Messung wieder an die Anlage anschließen!"}
        ],
        "parameters": ["Bereich: 0.00-9999 Ω", "Auflösung: 0.01 Ω", "Frequenz: 125 Hz", "Prüfstrom: >200 mA"],
        "safety_notes": ["Erdung vor der Messung von der Anlage trennen", "Sicheren Abstand zu Hochspannungsleitungen einhalten", "Hilfselektroden in feuchten Boden einschlagen", "Erdung nach der Messung wieder anschließen"],
        "expected_results": "<10 Ω für Schutzerdung, <2 Ω für Betriebserdung"
    },
    "voltage": {
        "name": "Spannungsmessung",
        "description": "Messung von AC- und DC-Spannung sowie Frequenz (TRMS)",
        "steps": [
            {"title": "Funktionswahl", "description": "Drehschalter auf U (Spannung) stellen. Das Messgerät erkennt AC/DC automatisch.", "tip": "Für Messung der Spannung zwischen Phasen L-L-Funktion verwenden."},
            {"title": "Anschluss", "description": "Rote Sonde an Messpunkt, blaue an Bezugspunkt (N oder PE) anschließen.", "warning": "Maximalspannung 550V AC nicht überschreiten!"},
            {"title": "Ergebnis ablesen", "description": "Spannung [V] und Frequenz [Hz] am Display ablesen. TRMS-Messung liefert genaue Ergebnisse bei verzerrten Kurvenformen.", "tip": "Phasenspannung sollte 220-240V betragen, Außenleiterspannung 380-420V."}
        ],
        "parameters": ["AC-Bereich: 0-550 V", "DC-Bereich: 0-550 V", "Frequenz: 45-65 Hz", "Genauigkeit: ±1%"],
        "safety_notes": ["550V AC/DC nicht überschreiten", "Messleitungen in gutem Zustand verwenden", "Messkategorie CAT III 600V / CAT IV 300V"],
        "expected_results": "Phasenspannung: 220-240V, Außenleiterspannung: 380-420V, Frequenz: 49.5-50.5 Hz"
    },
    "continuity": {
        "name": "Durchgangsprüfung Schutzleiter",
        "description": "Messung der Durchgängigkeit und des Widerstands von PE-Leitern und Potentialausgleichsverbindungen mit 200mA",
        "steps": [
            {"title": "Spannungsfreischaltung", "description": "Anlage vor der Durchgangsprüfung SPANNUNGSFREI SCHALTEN!", "warning": "Messung OHNE Spannung in der Anlage!"},
            {"title": "Funktionswahl", "description": "Drehschalter auf RCONT (Durchgang) stellen. 200mA Prüfstrom gemäß Norm wählen.", "tip": "200mA Strom ist nach EN 61557-4 vorgeschrieben."},
            {"title": "Leitungskompensation", "description": "Messleitungsenden kurzschließen und Leitungswiderstandskompensation (ZERO-Taste) durchführen.", "tip": "Kompensation eliminiert den Einfluss des Messleitungswiderstands auf das Ergebnis."},
            {"title": "Messung", "description": "Eine Leitung an PE-Schiene in der Verteilung, andere an Prüfpunkt (Steckdose, Gerätegehäuse) anschließen.", "tip": "Von der Verteilung zum entferntesten Punkt des Stromkreises messen."},
            {"title": "Ablesen und Bewertung", "description": "Widerstand [Ω] ablesen. Maximal zulässiger Wert hängt vom PE-Leiterquerschnitt ab.", "warning": "Wert >1 Ω deutet auf ein Problem mit der Schutzleiterdurchgängigkeit hin!"}
        ],
        "parameters": ["Bereich: 0.00-400 Ω", "Strom: 200 mA (nach EN 61557-4)", "Leerlaufspannung: 4-24 V", "Auflösung: 0.01 Ω"],
        "safety_notes": ["Spannung vor der Messung ABSCHALTEN!", "Messleitungswiderstand kompensieren", "Alle PE-Anschlusspunkte prüfen", "200mA Strom ist normativ vorgeschrieben"],
        "expected_results": "<1 Ω für Schutzleiter, <0.1 Ω für Hauptpotentialausgleich"
    },
    "phase_sequence": {
        "name": "Drehfeldrichtung",
        "description": "Prüfung der korrekten Phasenfolge L1-L2-L3 in Drehstromanlagen",
        "steps": [
            {"title": "Funktionswahl", "description": "Drehschalter auf Drehfeldsymbol (1-2-3) stellen. Diese Funktion prüft die Phasenfolge.", "tip": "Korrekte Phasenfolge ist für den einwandfreien Betrieb von Drehstrommotoren unerlässlich."},
            {"title": "Kabelanschluss", "description": "Drei Messleitungen an drei Phasen anschließen: L1 (gelb), L2 (rot), L3 (blau). Sonden oder Krokodilklemmen verwenden.", "warning": "Messung unter Drehstromspannung 400V! Äußerste Vorsicht!"},
            {"title": "Ergebnis ablesen", "description": "Das Messgerät zeigt Phasenfolge an: RICHTIG (1-2-3) oder FALSCH (3-2-1). Außenleiterspannungen werden ebenfalls angezeigt.", "tip": "Bei falscher Reihenfolge beliebige zwei Phasen tauschen."}
        ],
        "parameters": ["Spannung L-L: 95-500 V", "Frequenz: 45-65 Hz", "Anzeige: richtig/falsch", "Anzeige: UL1-L2, UL2-L3, UL3-L1"],
        "safety_notes": ["Messung unter Drehstromspannung 400V!", "Kabel mit guter Isolierung verwenden", "Sondenspitzen während der Messung nicht berühren", "Kategorie CAT III 600V"],
        "expected_results": "RICHTIGE Reihenfolge (1-2-3), Außenleiterspannungen 380-420V"
    },
    "motor_rotation": {
        "name": "Motordrehrichtung",
        "description": "Bestimmung der Drehrichtung eines Drehstrommotors (rechts/links) ohne Inbetriebnahme",
        "steps": [
            {"title": "Funktionswahl", "description": "Drehschalter auf Motordrehrichtungstest stellen. Diese Funktion bestimmt die Drehrichtung ohne Motorstart.", "tip": "Nützlich beim Anschluss neuer Motoren oder nach Wartungsarbeiten."},
            {"title": "Anschluss an Stromversorgung", "description": "Messleitungen an Motoranschlussklemmen (U, V, W oder L1, L2, L3) anschließen.", "warning": "Motor muss während des Kabelanschlusses SPANNUNGSFREI sein!"},
            {"title": "Spannung einschalten", "description": "Nach sicherem Kabelanschluss Drehstromversorgung einschalten. Motor NICHT starten.", "warning": "Messung unter Spannung! Sicherstellen, dass der Motor nicht versehentlich gestartet wird."},
            {"title": "Ergebnis ablesen", "description": "Das Messgerät zeigt Drehrichtung an: RECHTS (im Uhrzeigersinn) oder LINKS (gegen den Uhrzeigersinn). Phasenspannungen werden ebenfalls angezeigt.", "tip": "Zur Änderung der Drehrichtung beliebige zwei Versorgungsphasen tauschen."}
        ],
        "parameters": ["Spannung L-L: 95-500 V", "Frequenz: 45-65 Hz", "Anzeige: rechts/links", "Simulation ohne Motorstart"],
        "safety_notes": ["Stromversorgung vor Kabelanschluss trennen!", "Sicherstellen, dass Motor während des Tests nicht startet", "Messung unter Drehstromspannung", "Stromversorgung nach dem Test vor dem Kabeltrennen abschalten"],
        "expected_results": "RECHTS- oder LINKSDREHUNG - abhängig vom Phasenanschluss"
    },
    "lux": {
        "name": "Beleuchtungsstärkemessung",
        "description": "Messung der Beleuchtungsstärke in Lux (lx) mit externer LP-1 oder LP-10 Sonde",
        "steps": [
            {"title": "Sondenanschluss", "description": "Luxmeter-Sonde LP-1, LP-10A oder LP-10B an miniDIN-4P-Buchse des Messgeräts anschließen. Bei Bedarf WS-06-Adapter verwenden.", "tip": "LP-10B-Sonde hat erweiterten Messbereich bis 400 klx."},
            {"title": "Funktionswahl", "description": "Drehschalter auf LUX stellen. Das Messgerät erkennt die angeschlossene Sonde automatisch.", "tip": "Vor der Messung ca. 1 Minute auf Sondenstabilisierung warten."},
            {"title": "Sondenpositionierung", "description": "Sonde am Messpunkt platzieren. Die Fotozelle sollte zur Lichtquelle oder Arbeitsfläche zeigen.", "tip": "Für Arbeitsplatzmessung Sonde auf Tischhöhe (85 cm) platzieren."},
            {"title": "Ergebnis ablesen", "description": "Beleuchtungsstärke in Lux [lx] oder Foot-Candles [fc] ablesen. Der Wert stabilisiert sich nach einigen Sekunden.", "tip": "PN-EN 12464-1 gibt Mindestwerte für verschiedene Arbeitsplätze vor."}
        ],
        "parameters": ["Bereich: 0-400 klx", "Auflösung: ab 0.001 lx", "Einheiten: lx oder fc", "Sonden: LP-1, LP-10A, LP-10B"],
        "safety_notes": ["Sonde nicht längere Zeit direkter Sonneneinstrahlung aussetzen", "Fotozelle nicht mit Fingern berühren", "Sonde im Schutzetui aufbewahren", "Sonde alle 12 Monate kalibrieren"],
        "expected_results": "Büro: 500 lx, Produktion: 300-500 lx, Lager: 100-200 lx, Flur: 100 lx"
    },
    "earthing_clamp": {
        "name": "Erdung mit Zangenverfahren",
        "description": "Messung des Erdungswiderstands mit Zwei-Zangen-Verfahren ohne Hilfselektroden",
        "steps": [
            {"title": "Zangenvorbereitung", "description": "Zangensatz vorbereiten: Messzange C-3 und Sendezange N-1. An entsprechende Messgerätbuchsen anschließen.", "tip": "Zangenverfahren erfordert keine Elektroden - ideal für befestigte Oberflächen."},
            {"title": "Funktionswahl", "description": "Drehschalter auf RE stellen und 2-Zangen-Verfahren wählen (2C oder 2-clamp). Messgerät schaltet in Zangenmessmodus.", "warning": "Methode erfordert, dass die Erdung Teil eines geschlossenen Kreises ist."},
            {"title": "Zangenplatzierung", "description": "Sendezange N-1 auf den Erdungsleiter setzen. Mind. 30 cm entfernt Messzange C-3 auf denselben Leiter setzen.", "tip": "Zangen dürfen nur den Erdungsleiter umfassen, nicht andere parallele Leiter."},
            {"title": "Messung", "description": "START drücken. Messgerät erzwingt Strom durch Sendezange und misst Spannung an Messzange.", "tip": "Ergebnis umfasst geprüften Erdungswiderstand und Parallelschaltung der übrigen Erdungen."},
            {"title": "Ergebnisinterpretation", "description": "Widerstand RE [Ω] ablesen. Beachten, dass das Ergebnis der Erdungswiderstand im System mit anderen Erdungen ist.", "warning": "Zangenverfahren liefert zu niedrige Ergebnisse bei parallelen Erdungen!"}
        ],
        "parameters": ["Bereich: 0.00-99.9 kΩ", "Auflösung: ab 0.01 Ω", "Zangen: C-3 + N-1", "Keine Hilfselektroden erforderlich"],
        "safety_notes": ["Methode erfordert geschlossenen Erdungskreis", "Zangen nur auf Erdungsleiter setzen", "Mind. 30 cm Abstand zwischen Zangen einhalten", "Ergebnis kann bei parallelen Erdungen zu niedrig sein"],
        "expected_results": "<10 Ω für Schutzerdung (Einfluss paralleler Erdungen berücksichtigen)"
    }
}

# ============================================
# FAQ TRANSLATIONS
# ============================================

FAQ_EN = [
    {"id": "1", "question": "What test current to choose for 30mA RCD?", "answer": "For standard test use 1x IΔn (30mA). For full time test, perform measurements at 0.5x, 1x, 2x and 5x IΔn.", "category": "rcd"},
    {"id": "2", "question": "Why does insulation measurement show 0 MΩ?", "answer": "Check if installation voltage is switched off. Value 0 means short circuit or live supply voltage.", "category": "insulation"},
    {"id": "3", "question": "What is the minimum insulation resistance?", "answer": "For new installations: min. 1 MΩ. For existing: min. 0.5 MΩ at 500V DC test voltage.", "category": "insulation"},
    {"id": "4", "question": "How often to calibrate MPI-530?", "answer": "Manufacturer Sonel recommends calibration every 12 months or after mechanical damage.", "category": "ogolne"},
    {"id": "5", "question": "What does 'PE!' error mean during loop measurement?", "answer": "Missing or too high PE conductor resistance. Check PE conductor continuity before Zs measurement.", "category": "loop"},
    {"id": "6", "question": "How to measure loop impedance behind RCD without tripping?", "answer": "Use Zs RCD function (non-tripping) or perform quick L-L measurement (between phases).", "category": "loop"},
    {"id": "7", "question": "What are the measurement categories of MPI-530?", "answer": "MPI-530 meets CAT III 600V and CAT IV 300V requirements per EN 61010.", "category": "ogolne"},
    {"id": "8", "question": "How to discharge cable capacitance after insulation measurement?", "answer": "MPI-530 automatically discharges capacitance after releasing START button. Wait for completion signal.", "category": "insulation"},
    {"id": "9", "question": "How to fix incorrect phase sequence?", "answer": "Swap any two phases (e.g. L1 with L2 or L2 with L3). After swapping, recheck sequence with meter.", "category": "phase_sequence"},
    {"id": "10", "question": "How to change three-phase motor rotation direction?", "answer": "Swap any two motor supply phases. This will reverse the rotation direction.", "category": "motor_rotation"},
    {"id": "11", "question": "What illumination level is required in an office?", "answer": "Per PN-EN 12464-1, office workstations require min. 500 lx. Corridors 100 lx, archives 200 lx.", "category": "lux"},
    {"id": "12", "question": "When to use clamp method for earth measurement?", "answer": "Use clamp method when auxiliary electrodes cannot be driven (concrete, asphalt) or when earths are in a closed circuit.", "category": "earthing_clamp"},
    {"id": "13", "question": "Why does clamp method give underestimated results?", "answer": "2-clamp method measures earth resistance in parallel with other earths. Actual single earth resistance is higher.", "category": "earthing_clamp"},
]

FAQ_DE = [
    {"id": "1", "question": "Welchen Prüfstrom für 30mA RCD wählen?", "answer": "Für Standardtest 1x IΔn (30mA) verwenden. Für vollständigen Zeittest bei 0.5x, 1x, 2x und 5x IΔn messen.", "category": "rcd"},
    {"id": "2", "question": "Warum zeigt die Isolationsmessung 0 MΩ?", "answer": "Prüfen Sie, ob die Anlagenspannung abgeschaltet ist. Wert 0 bedeutet Kurzschluss oder anliegende Versorgungsspannung.", "category": "insulation"},
    {"id": "3", "question": "Was ist der minimale Isolationswiderstand?", "answer": "Für neue Anlagen: min. 1 MΩ. Für bestehende: min. 0.5 MΩ bei 500V DC Prüfspannung.", "category": "insulation"},
    {"id": "4", "question": "Wie oft das MPI-530 kalibrieren?", "answer": "Hersteller Sonel empfiehlt Kalibrierung alle 12 Monate oder nach mechanischer Beschädigung.", "category": "ogolne"},
    {"id": "5", "question": "Was bedeutet Fehler 'PE!' bei der Schleifenmessung?", "answer": "Fehlender oder zu hoher Schutzleiterwiderstand. PE-Durchgängigkeit vor Zs-Messung prüfen.", "category": "loop"},
    {"id": "6", "question": "Wie Schleifenimpedanz hinter RCD ohne Auslösung messen?", "answer": "Zs RCD-Funktion (ohne Auslösung) verwenden oder L-L-Schnellmessung (zwischen Phasen) durchführen.", "category": "loop"},
    {"id": "7", "question": "Welche Messkategorien hat das MPI-530?", "answer": "MPI-530 erfüllt CAT III 600V und CAT IV 300V Anforderungen nach EN 61010.", "category": "ogolne"},
    {"id": "8", "question": "Wie Kabelkapazität nach Isolationsmessung entladen?", "answer": "MPI-530 entlädt die Kapazität automatisch nach Loslassen der START-Taste. Auf Abschlusssignal warten.", "category": "insulation"},
    {"id": "9", "question": "Wie falsche Phasenfolge korrigieren?", "answer": "Beliebige zwei Phasen tauschen (z.B. L1 mit L2 oder L2 mit L3). Nach dem Tausch erneut mit Messgerät prüfen.", "category": "phase_sequence"},
    {"id": "10", "question": "Wie Drehrichtung eines Drehstrommotors ändern?", "answer": "Beliebige zwei Versorgungsphasen des Motors tauschen. Dies kehrt die Drehrichtung um.", "category": "motor_rotation"},
    {"id": "11", "question": "Welche Beleuchtungsstärke ist im Büro erforderlich?", "answer": "Nach PN-EN 12464-1 erfordern Büroarbeitsplätze min. 500 lx. Flure 100 lx, Archive 200 lx.", "category": "lux"},
    {"id": "12", "question": "Wann Zangenverfahren für Erdungsmessung verwenden?", "answer": "Zangenverfahren verwenden, wenn keine Hilfselektroden eingeschlagen werden können (Beton, Asphalt) oder bei geschlossenem Erdungskreis.", "category": "earthing_clamp"},
    {"id": "13", "question": "Warum liefert das Zangenverfahren zu niedrige Ergebnisse?", "answer": "2-Zangen-Verfahren misst Erdungswiderstand parallel zu anderen Erdungen. Tatsächlicher Einzelerdungswiderstand ist höher.", "category": "earthing_clamp"},
]

# ============================================
# ERROR CODES TRANSLATIONS
# ============================================

ERROR_CODES_EN = [
    {"code": "PE!", "name": "No PE", "description": "No connection to PE conductor or too high resistance", "causes": ["Damaged PE conductor", "No PE continuity", "Bad contact in socket", "Unconnected protective conductor"], "solutions": ["Check PE conductor continuity", "Check connections in distribution board", "Clean socket contacts", "Perform PE continuity measurement"]},
    {"code": "Hi", "name": "Above range", "description": "Measured value exceeds meter measurement range", "causes": ["Too high impedance", "No connection", "Break in circuit"], "solutions": ["Check measurement connections", "Check if circuit is closed", "Use higher measurement range"]},
    {"code": "Lo", "name": "Below range", "description": "Measured value is below lower range limit", "causes": ["Short circuit", "Too low resistance", "Connection error"], "solutions": ["Check for short circuit", "Use lower range", "Check connection correctness"]},
    {"code": "OFL", "name": "Overflow", "description": "Maximum measurement range exceeded", "causes": ["Very high resistance/impedance", "Open circuit", "Damaged test lead insulation"], "solutions": ["Check circuit continuity", "Check test leads", "Change measurement range"]},
    {"code": "U>", "name": "Voltage too high", "description": "Circuit voltage exceeds permissible value for this measurement", "causes": ["Voltage >253V", "Grid disturbances", "Wrong connection"], "solutions": ["Check installation voltage", "Wait for grid stabilization", "Check connection"]},
    {"code": "U<", "name": "Voltage too low", "description": "Circuit voltage too low for measurement", "causes": ["Voltage <180V", "Phase loss", "Grid overload"], "solutions": ["Check supply voltage", "Check fuses", "Wait for voltage restoration"]},
    {"code": "f?", "name": "Wrong frequency", "description": "Grid frequency outside 45-65 Hz range", "causes": ["Generator operation", "Grid disturbances", "Unstable source"], "solutions": ["Check power source", "Connect to stable grid", "Use UPS"]},
    {"code": "RCD!", "name": "RCD tripped", "description": "Residual current device tripped during measurement", "causes": ["Loop impedance measurement triggered RCD", "Very sensitive RCD", "Normal measurement effect"], "solutions": ["Switch RCD back on", "Use non-tripping RCD measurement function", "Perform L-L measurement"]},
    {"code": "CAL", "name": "Calibration required", "description": "Calibration date expired or meter requires checking", "causes": ["Calibration date exceeded", "Mechanical damage", "Internal error"], "solutions": ["Send meter for calibration", "Check last calibration date", "Contact Sonel service"]},
    {"code": "bAt", "name": "Low battery", "description": "Low battery charge level", "causes": ["Discharged battery", "Worn battery", "Long operation without charging"], "solutions": ["Charge battery", "Replace with new battery", "Connect power adapter"]},
    {"code": "Err", "name": "General error", "description": "Unexpected error during measurement", "causes": ["Electromagnetic interference", "Internal error", "Unstable measurement conditions"], "solutions": ["Repeat measurement", "Move meter away from interference sources", "Restart meter"]},
    {"code": "L-PE", "name": "L-PE measurement impossible", "description": "Cannot perform L-PE impedance measurement", "causes": ["No PE", "Too high PE resistance", "Wrong connection"], "solutions": ["Check PE continuity", "Perform continuity test first", "Check connections"]},
]

ERROR_CODES_DE = [
    {"code": "PE!", "name": "Kein PE", "description": "Keine Verbindung zum PE-Leiter oder zu hoher Widerstand", "causes": ["Beschädigter PE-Leiter", "Keine PE-Durchgängigkeit", "Schlechter Kontakt in Steckdose", "Nicht angeschlossener Schutzleiter"], "solutions": ["PE-Leiterdurchgängigkeit prüfen", "Verbindungen in der Verteilung prüfen", "Steckdosenkontakte reinigen", "PE-Durchgangsmessung durchführen"]},
    {"code": "Hi", "name": "Über Bereich", "description": "Messwert überschreitet Messbereich", "causes": ["Zu hohe Impedanz", "Keine Verbindung", "Unterbrechung im Stromkreis"], "solutions": ["Messverbindungen prüfen", "Prüfen ob Stromkreis geschlossen", "Höheren Messbereich verwenden"]},
    {"code": "Lo", "name": "Unter Bereich", "description": "Messwert unter unterer Bereichsgrenze", "causes": ["Kurzschluss", "Zu niedriger Widerstand", "Anschlussfehler"], "solutions": ["Auf Kurzschluss prüfen", "Niedrigeren Bereich verwenden", "Anschluss prüfen"]},
    {"code": "OFL", "name": "Überlauf", "description": "Maximaler Messbereich überschritten", "causes": ["Sehr hoher Widerstand/Impedanz", "Offener Stromkreis", "Beschädigte Messleitungsisolierung"], "solutions": ["Stromkreisdurchgängigkeit prüfen", "Messleitungen prüfen", "Messbereich ändern"]},
    {"code": "U>", "name": "Spannung zu hoch", "description": "Stromkreisspannung überschreitet zulässigen Wert", "causes": ["Spannung >253V", "Netzstörungen", "Falscher Anschluss"], "solutions": ["Anlagenspannung prüfen", "Auf Netzstabilisierung warten", "Anschluss prüfen"]},
    {"code": "U<", "name": "Spannung zu niedrig", "description": "Stromkreisspannung zu niedrig für Messung", "causes": ["Spannung <180V", "Phasenausfall", "Netzüberlastung"], "solutions": ["Versorgungsspannung prüfen", "Sicherungen prüfen", "Auf Spannungswiederherstellung warten"]},
    {"code": "f?", "name": "Falsche Frequenz", "description": "Netzfrequenz außerhalb 45-65 Hz", "causes": ["Generatorbetrieb", "Netzstörungen", "Instabile Quelle"], "solutions": ["Stromquelle prüfen", "An stabiles Netz anschließen", "USV verwenden"]},
    {"code": "RCD!", "name": "RCD ausgelöst", "description": "Fehlerstromschutzschalter während Messung ausgelöst", "causes": ["Schleifenimpedanzmessung löste RCD aus", "Sehr empfindlicher RCD", "Normaler Messeffekt"], "solutions": ["RCD wieder einschalten", "Auslösefreie RCD-Messfunktion verwenden", "L-L-Messung durchführen"]},
    {"code": "CAL", "name": "Kalibrierung erforderlich", "description": "Kalibrierungsdatum abgelaufen oder Messgerät muss geprüft werden", "causes": ["Kalibrierungsdatum überschritten", "Mechanische Beschädigung", "Interner Fehler"], "solutions": ["Messgerät zur Kalibrierung senden", "Letztes Kalibrierungsdatum prüfen", "Sonel-Service kontaktieren"]},
    {"code": "bAt", "name": "Batterie schwach", "description": "Niedriger Akkuladestand", "causes": ["Entladener Akku", "Verschlissener Akku", "Langer Betrieb ohne Laden"], "solutions": ["Akku laden", "Durch neuen Akku ersetzen", "Netzteil anschließen"]},
    {"code": "Err", "name": "Allgemeiner Fehler", "description": "Unerwarteter Fehler während der Messung", "causes": ["Elektromagnetische Störungen", "Interner Fehler", "Instabile Messbedingungen"], "solutions": ["Messung wiederholen", "Messgerät von Störquellen entfernen", "Messgerät neu starten"]},
    {"code": "L-PE", "name": "L-PE Messung nicht möglich", "description": "L-PE Impedanzmessung kann nicht durchgeführt werden", "causes": ["Kein PE", "Zu hoher PE-Widerstand", "Falscher Anschluss"], "solutions": ["PE-Durchgängigkeit prüfen", "Zuerst Durchgangsprüfung durchführen", "Anschlüsse prüfen"]},
]

# ============================================
# QUIZ TRANSLATIONS
# ============================================

QUIZ_EN = [
    {"id": 1, "question": "What is the minimum insulation resistance for a new installation at 500V test voltage?", "options": ["0.5 MΩ", "1 MΩ", "2 MΩ", "0.25 MΩ"], "correct": 1, "explanation": "Per PN-HD 60364-6, minimum insulation resistance for installations up to 500V is 1 MΩ."},
    {"id": 2, "question": "What is the maximum trip time for 30mA RCD at 1x IΔn current?", "options": ["40 ms", "150 ms", "300 ms", "500 ms"], "correct": 2, "explanation": "For AC and A type RCDs, maximum trip time at 1x IΔn is 300 ms."},
    {"id": 3, "question": "At what current multiplier should RCD NOT trip?", "options": ["0.5x IΔn", "1x IΔn", "2x IΔn", "5x IΔn"], "correct": 0, "explanation": "RCD should not trip at 0.5x IΔn - this tests whether RCD is not too sensitive."},
    {"id": 4, "question": "What does 'PE!' error mean on MPI-530?", "options": ["Range exceeded", "No PE connection", "Low battery", "Calibration error"], "correct": 1, "explanation": "PE! error means missing or too high PE conductor resistance."},
    {"id": 5, "question": "What test voltage for insulation measurement of 400V installation?", "options": ["250V", "500V", "1000V", "100V"], "correct": 2, "explanation": "For installations above 500V, test voltage of 1000V DC should be used."},
    {"id": 6, "question": "How far from tested earth should current electrode (H) be driven?", "options": ["10 m", "20 m", "Min. 40 m", "5 m"], "correct": 2, "explanation": "Current electrode should be at least 40 m from the tested earth."},
    {"id": 7, "question": "Where to place voltage electrode (S) for 3-wire earth measurement?", "options": ["At the earth", "Halfway", "At 62% distance to electrode H", "At electrode H"], "correct": 2, "explanation": "Voltage electrode should be placed at 62% of the distance between earth and current electrode."},
    {"id": 8, "question": "What test current is required for PE continuity measurement per standard?", "options": ["10 mA", "50 mA", "200 mA", "1 A"], "correct": 2, "explanation": "Per EN 61557-4, PE continuity should be measured with min. 200 mA current."},
    {"id": 9, "question": "What must be done BEFORE insulation resistance measurement?", "options": ["Switch on voltage", "Switch off voltage and disconnect devices", "Measure RCD", "Check phase sequence"], "correct": 1, "explanation": "Before insulation measurement, voltage MUST be switched off and sensitive devices disconnected."},
    {"id": 10, "question": "What minimum illumination is required at an office workstation?", "options": ["200 lx", "300 lx", "500 lx", "750 lx"], "correct": 2, "explanation": "Per PN-EN 12464-1, office workstations require minimum 500 lx."},
    {"id": 11, "question": "What is the maximum loop impedance for B16 protection (0.4s time)?", "options": ["1.15 Ω", "2.88 Ω", "4.60 Ω", "0.92 Ω"], "correct": 1, "explanation": "For B16 protection at 0.4s and 230V, Zs max = 2.88 Ω."},
    {"id": 12, "question": "What does 'CORRECT' phase sequence mean?", "options": ["L3-L2-L1", "L1-L2-L3", "L2-L1-L3", "Any"], "correct": 1, "explanation": "Correct phase sequence is L1-L2-L3 (clockwise rotation)."},
    {"id": 13, "question": "How often should MPI-530 be calibrated?", "options": ["Every 6 months", "Every 12 months", "Every 24 months", "Every 5 years"], "correct": 1, "explanation": "Sonel recommends meter calibration every 12 months."},
    {"id": 14, "question": "What is the measurement category of MPI-530?", "options": ["CAT I", "CAT II", "CAT III 600V / CAT IV 300V", "CAT V"], "correct": 2, "explanation": "MPI-530 meets CAT III 600V and CAT IV 300V requirements."},
    {"id": 15, "question": "Can loop impedance be measured behind RCD without tripping it?", "options": ["No, RCD always trips", "Yes, using Zs RCD function or L-L measurement", "No, RCD must be removed", "Only with voltage off"], "correct": 1, "explanation": "MPI-530 has non-tripping Zs RCD function and L-L measurement capability."},
]

QUIZ_DE = [
    {"id": 1, "question": "Was ist der minimale Isolationswiderstand für eine neue Anlage bei 500V Prüfspannung?", "options": ["0.5 MΩ", "1 MΩ", "2 MΩ", "0.25 MΩ"], "correct": 1, "explanation": "Nach PN-HD 60364-6 beträgt der minimale Isolationswiderstand für Anlagen bis 500V 1 MΩ."},
    {"id": 2, "question": "Was ist die maximale Auslösezeit für 30mA RCD bei 1x IΔn?", "options": ["40 ms", "150 ms", "300 ms", "500 ms"], "correct": 2, "explanation": "Für RCD Typ AC und A beträgt die maximale Auslösezeit bei 1x IΔn 300 ms."},
    {"id": 3, "question": "Bei welchem Strommultiplikator sollte der RCD NICHT auslösen?", "options": ["0.5x IΔn", "1x IΔn", "2x IΔn", "5x IΔn"], "correct": 0, "explanation": "Der RCD sollte bei 0.5x IΔn nicht auslösen - dies prüft ob der RCD nicht zu empfindlich ist."},
    {"id": 4, "question": "Was bedeutet 'PE!' auf dem MPI-530?", "options": ["Bereich überschritten", "Keine PE-Verbindung", "Batterie schwach", "Kalibrierungsfehler"], "correct": 1, "explanation": "PE! bedeutet fehlender oder zu hoher PE-Leiterwiderstand."},
    {"id": 5, "question": "Welche Prüfspannung für Isolationsmessung einer 400V-Anlage?", "options": ["250V", "500V", "1000V", "100V"], "correct": 2, "explanation": "Für Anlagen über 500V sollte 1000V DC Prüfspannung verwendet werden."},
    {"id": 6, "question": "Wie weit vom Prüferder soll die Stromelektrode (H) eingeschlagen werden?", "options": ["10 m", "20 m", "Mind. 40 m", "5 m"], "correct": 2, "explanation": "Die Stromelektrode sollte mindestens 40 m vom Prüferder entfernt sein."},
    {"id": 7, "question": "Wo die Spannungselektrode (S) bei 3-Leiter-Erdungsmessung platzieren?", "options": ["Am Erder", "In der Mitte", "Bei 62% der Entfernung zur Elektrode H", "An Elektrode H"], "correct": 2, "explanation": "Die Spannungselektrode sollte bei 62% der Entfernung zwischen Erder und Stromelektrode platziert werden."},
    {"id": 8, "question": "Welcher Prüfstrom ist für PE-Durchgangsprüfung normativ vorgeschrieben?", "options": ["10 mA", "50 mA", "200 mA", "1 A"], "correct": 2, "explanation": "Nach EN 61557-4 ist die PE-Durchgangsprüfung mit min. 200 mA durchzuführen."},
    {"id": 9, "question": "Was muss VOR der Isolationswiderstandsmessung geschehen?", "options": ["Spannung einschalten", "Spannung abschalten und Geräte trennen", "RCD messen", "Phasenfolge prüfen"], "correct": 1, "explanation": "Vor der Isolationsmessung MUSS die Spannung abgeschaltet und empfindliche Geräte getrennt werden."},
    {"id": 10, "question": "Welche Mindestbeleuchtungsstärke ist am Büroarbeitsplatz erforderlich?", "options": ["200 lx", "300 lx", "500 lx", "750 lx"], "correct": 2, "explanation": "Nach PN-EN 12464-1 erfordern Büroarbeitsplätze mindestens 500 lx."},
    {"id": 11, "question": "Was ist die maximale Schleifenimpedanz für Schutz B16 (0.4s)?", "options": ["1.15 Ω", "2.88 Ω", "4.60 Ω", "0.92 Ω"], "correct": 1, "explanation": "Für Schutz B16 bei 0.4s und 230V beträgt Zs max = 2.88 Ω."},
    {"id": 12, "question": "Was bedeutet 'RICHTIGE' Phasenfolge?", "options": ["L3-L2-L1", "L1-L2-L3", "L2-L1-L3", "Beliebig"], "correct": 1, "explanation": "Richtige Phasenfolge ist L1-L2-L3 (Rechtsdrehfeld)."},
    {"id": 13, "question": "Wie oft sollte das MPI-530 kalibriert werden?", "options": ["Alle 6 Monate", "Alle 12 Monate", "Alle 24 Monate", "Alle 5 Jahre"], "correct": 1, "explanation": "Sonel empfiehlt die Kalibrierung des Messgeräts alle 12 Monate."},
    {"id": 14, "question": "Welche Messkategorie hat das MPI-530?", "options": ["CAT I", "CAT II", "CAT III 600V / CAT IV 300V", "CAT V"], "correct": 2, "explanation": "MPI-530 erfüllt CAT III 600V und CAT IV 300V."},
    {"id": 15, "question": "Kann Schleifenimpedanz hinter RCD ohne Auslösung gemessen werden?", "options": ["Nein, RCD löst immer aus", "Ja, mit Zs RCD-Funktion oder L-L-Messung", "Nein, RCD muss entfernt werden", "Nur bei abgeschalteter Spannung"], "correct": 1, "explanation": "MPI-530 hat auslösefreie Zs RCD-Funktion und L-L-Messmöglichkeit."},
]

# ============================================
# CHECKLIST TRANSLATIONS
# ============================================

CHECKLISTS_EN = {
    "rcd": {"name": "RCD Test", "items": [
        {"id": 1, "text": "I checked the condition of test leads", "critical": True},
        {"id": 2, "text": "I confirmed the installation is energized", "critical": True},
        {"id": 3, "text": "I warned users about possible power interruption", "critical": True},
        {"id": 4, "text": "I checked PE continuity before RCD test", "critical": False},
        {"id": 5, "text": "I selected the correct RCD type (AC/A/B)", "critical": False},
    ]},
    "insulation": {"name": "Insulation measurement", "items": [
        {"id": 1, "text": "I SWITCHED OFF the installation power", "critical": True},
        {"id": 2, "text": "I verified absence of voltage with meter", "critical": True},
        {"id": 3, "text": "I disconnected devices sensitive to test voltage", "critical": True},
        {"id": 4, "text": "I secured workplace against accidental energization", "critical": True},
        {"id": 5, "text": "I selected appropriate test voltage (500V/1000V)", "critical": False},
    ]},
    "loop": {"name": "Loop impedance", "items": [
        {"id": 1, "text": "I checked the condition of test leads", "critical": True},
        {"id": 2, "text": "I confirmed the installation is energized", "critical": True},
        {"id": 3, "text": "I checked PE continuity", "critical": True},
        {"id": 4, "text": "I considered possible RCD tripping", "critical": False},
    ]},
    "continuity": {"name": "PE Continuity", "items": [
        {"id": 1, "text": "I SWITCHED OFF the installation power", "critical": True},
        {"id": 2, "text": "I verified absence of voltage with meter", "critical": True},
        {"id": 3, "text": "I performed lead compensation (ZERO)", "critical": False},
    ]},
    "earthing": {"name": "Earth resistance", "items": [
        {"id": 1, "text": "I disconnected the tested earth from installation", "critical": True},
        {"id": 2, "text": "I checked safe distance from HV lines", "critical": True},
        {"id": 3, "text": "I drove auxiliary electrodes at correct distances", "critical": True},
        {"id": 4, "text": "I checked soil moisture at electrodes", "critical": False},
    ]},
    "general": {"name": "General pre-measurement check", "items": [
        {"id": 1, "text": "Meter is calibrated (valid date)", "critical": True},
        {"id": 2, "text": "Meter battery is charged", "critical": True},
        {"id": 3, "text": "Test leads are in good condition", "critical": True},
        {"id": 4, "text": "I have appropriate SEP qualifications", "critical": True},
        {"id": 5, "text": "I am using personal protective equipment", "critical": True},
    ]}
}

CHECKLISTS_DE = {
    "rcd": {"name": "RCD-Prüfung", "items": [
        {"id": 1, "text": "Ich habe den Zustand der Messleitungen geprüft", "critical": True},
        {"id": 2, "text": "Ich habe bestätigt, dass die Anlage unter Spannung steht", "critical": True},
        {"id": 3, "text": "Ich habe Benutzer vor möglichem Spannungsausfall gewarnt", "critical": True},
        {"id": 4, "text": "Ich habe PE-Durchgängigkeit vor RCD-Test geprüft", "critical": False},
        {"id": 5, "text": "Ich habe den richtigen RCD-Typ (AC/A/B) gewählt", "critical": False},
    ]},
    "insulation": {"name": "Isolationsmessung", "items": [
        {"id": 1, "text": "Ich habe die Anlage SPANNUNGSFREI geschaltet", "critical": True},
        {"id": 2, "text": "Ich habe Spannungsfreiheit mit Messgerät verifiziert", "critical": True},
        {"id": 3, "text": "Ich habe spannungsempfindliche Geräte getrennt", "critical": True},
        {"id": 4, "text": "Ich habe den Arbeitsplatz gegen versehentliches Einschalten gesichert", "critical": True},
        {"id": 5, "text": "Ich habe die passende Prüfspannung gewählt (500V/1000V)", "critical": False},
    ]},
    "loop": {"name": "Schleifenimpedanz", "items": [
        {"id": 1, "text": "Ich habe den Zustand der Messleitungen geprüft", "critical": True},
        {"id": 2, "text": "Ich habe bestätigt, dass die Anlage unter Spannung steht", "critical": True},
        {"id": 3, "text": "Ich habe die PE-Durchgängigkeit geprüft", "critical": True},
        {"id": 4, "text": "Ich habe mögliche RCD-Auslösung berücksichtigt", "critical": False},
    ]},
    "continuity": {"name": "PE-Durchgangsprüfung", "items": [
        {"id": 1, "text": "Ich habe die Anlage SPANNUNGSFREI geschaltet", "critical": True},
        {"id": 2, "text": "Ich habe Spannungsfreiheit mit Messgerät verifiziert", "critical": True},
        {"id": 3, "text": "Ich habe die Leitungskompensation (ZERO) durchgeführt", "critical": False},
    ]},
    "earthing": {"name": "Erdungswiderstand", "items": [
        {"id": 1, "text": "Ich habe den Prüferder von der Anlage getrennt", "critical": True},
        {"id": 2, "text": "Ich habe sicheren Abstand zu Hochspannungsleitungen geprüft", "critical": True},
        {"id": 3, "text": "Ich habe Hilfselektroden in korrekten Abständen eingeschlagen", "critical": True},
        {"id": 4, "text": "Ich habe die Bodenfeuchtigkeit an den Elektroden geprüft", "critical": False},
    ]},
    "general": {"name": "Allgemeine Prüfung vor der Messung", "items": [
        {"id": 1, "text": "Messgerät ist kalibriert (gültiges Datum)", "critical": True},
        {"id": 2, "text": "Messgerätbatterie ist geladen", "critical": True},
        {"id": 3, "text": "Messleitungen sind in gutem Zustand", "critical": True},
        {"id": 4, "text": "Ich habe die entsprechenden Qualifikationen", "critical": True},
        {"id": 5, "text": "Ich verwende persönliche Schutzausrüstung", "critical": True},
    ]}
}

# Helper: Get translated data by lang
def get_functions_translations(lang):
    if lang == "en":
        return FUNCTIONS_EN
    elif lang == "de":
        return FUNCTIONS_DE
    return None

def get_faq_translations(lang):
    if lang == "en":
        return FAQ_EN
    elif lang == "de":
        return FAQ_DE
    return None

def get_error_codes_translations(lang):
    if lang == "en":
        return ERROR_CODES_EN
    elif lang == "de":
        return ERROR_CODES_DE
    return None

def get_quiz_translations(lang):
    if lang == "en":
        return QUIZ_EN
    elif lang == "de":
        return QUIZ_DE
    return None

def get_checklists_translations(lang):
    if lang == "en":
        return CHECKLISTS_EN
    elif lang == "de":
        return CHECKLISTS_DE
    return None


# ============================================
# PROTOCOL GUIDES TRANSLATIONS
# ============================================

GUIDES_EN = [
    {
        "id": "reports_plus_basics",
        "name": "Sonel Reports Plus - Basics",
        "description": "How to get started with Sonel Reports Plus for creating measurement protocols",
        "icon": "FileText", "color": "#3B82F6",
        "steps": [
            {"step_number": 1, "title": "Software installation", "description": "Download Sonel Reports Plus from sonel.pl (Software section). Install on a computer with Windows 10/11. The software is free for Sonel meter users.", "tip": "Required system: Windows 10 or Windows 11.", "image": "https://cdn.sonel.com/Zdjecia/Programy/Programy+komputerowe/Sonel+Reports+PLUS/image-thumb__36489__img-product-thumb/blank-box-reports-plus_mHqcbIA.webp"},
            {"step_number": 2, "title": "Creating a new project", "description": "Launch the program and select 'New project'. Enter data: object name, address, investor, measurement contractor, date.", "tip": "You can save contractor data template for reuse."},
            {"step_number": 3, "title": "Object tree structure", "description": "Build the building structure: add floors, rooms, distribution boards. For each room you can add circuits and measurement points.", "tip": "Tree structure allows for clear organization of results."},
            {"step_number": 4, "title": "Adding measurement points", "description": "In each room add measurement points: sockets, lighting, fixed equipment. Specify protection type (fuse, circuit breaker).", "tip": "The program contains a library of fuses and protection devices."},
            {"step_number": 5, "title": "Transfer structure to meter", "description": "Connect MPI-530 meter via USB. Select 'Send structure to meter'. The structure will be loaded into meter memory.", "tip": "This way measurement results will be automatically assigned to points."}
        ],
        "tips": ["Sonel Reports Plus supports MPI-530, MPI-525, MPI-520 and other meters", "The program allows creating own report templates", "Regular software updates add new functions and meters"]
    },
    {
        "id": "download_results",
        "name": "Downloading results from the meter",
        "description": "How to transfer measurement results from MPI-530 to computer",
        "icon": "Download", "color": "#10B981",
        "steps": [
            {"step_number": 1, "title": "USB connection", "description": "Connect MPI-530 to computer using the included USB cable. Turn on the meter.", "tip": "Use original Sonel cable for best connection stability."},
            {"step_number": 2, "title": "Communication in Reports Plus", "description": "In Sonel Reports Plus select 'Meter' -> 'Download results'. The program will automatically detect the meter.", "tip": "If meter is not detected - install Sonel USB drivers."},
            {"step_number": 3, "title": "Selecting results to download", "description": "Select which results to download: all or only selected. You can filter by date or measurement type.", "tip": "If you sent the structure - results will be automatically matched to points."},
            {"step_number": 4, "title": "Verification and assignment", "description": "Check downloaded results. Assign unmatched results to appropriate measurement points.", "tip": "The program marks PASS/FAIL results based on norms."}
        ],
        "tips": ["Download results after each measurement session", "Before downloading, ensure the meter is fully charged", "You can also export results directly to CSV or Excel"]
    },
    {
        "id": "generate_protocol",
        "name": "Generating a protocol",
        "description": "How to create a professional measurement protocol from results",
        "icon": "Printer", "color": "#F59E0B",
        "steps": [
            {"step_number": 1, "title": "Checking result completeness", "description": "Before generating a protocol, make sure all measurements are complete and results are assigned to points.", "tip": "Missing results are marked in red."},
            {"step_number": 2, "title": "Template selection", "description": "Select 'Generate protocol'. Choose a template: reception protocol, periodic protocol, or custom template.", "tip": "You can create your own protocol templates."},
            {"step_number": 3, "title": "Completing header data", "description": "Complete data: protocol number, date, client details, purpose of examination (reception/periodic review).", "tip": "Save contractor and qualification data in profile for reuse."},
            {"step_number": 4, "title": "Preview and editing", "description": "Review protocol preview. You can add notes, recommendations, or edit descriptions.", "tip": "Add photos of distribution boards or problems found during measurements."},
            {"step_number": 5, "title": "Export and printing", "description": "Export protocol to PDF or print directly. You can also print labels for measurement points.", "tip": "PDF contains digital signature with generation date."}
        ],
        "tips": ["Protocol should contain: object data, measurement scope, results, assessment, recommendations", "Store protocols for at least 5 years as per regulations", "You can email protocol directly from the program"]
    },
    {
        "id": "pe6_migration",
        "name": "Migration from Sonel PE6",
        "description": "How to transfer data from old PE6 software to Sonel Reports Plus",
        "icon": "FolderSync", "color": "#8B5CF6",
        "steps": [
            {"step_number": 1, "title": "Export from PE6", "description": "In Sonel PE6 open the project. Select 'Export' and save file in .pe6 or .xml format.", "tip": "PE6 is older software - Sonel Reports Plus has more features."},
            {"step_number": 2, "title": "Import to Reports Plus", "description": "In Sonel Reports Plus select 'Import project'. Point to the file exported from PE6.", "tip": "Import preserves structure and measurement results."},
            {"step_number": 3, "title": "Data verification", "description": "Check imported data. Complete missing information (e.g., photos, diagrams).", "tip": "Some PE6 functions may require manual conversion."}
        ],
        "tips": ["Sonel Reports Plus replaces PE6 and PE5", "Reports Plus has better integration with new meters", "Keep a copy of original PE6 files just in case"]
    }
]

GUIDES_DE = [
    {
        "id": "reports_plus_basics",
        "name": "Sonel Reports Plus - Grundlagen",
        "description": "Erste Schritte mit Sonel Reports Plus zur Protokollerstellung",
        "icon": "FileText", "color": "#3B82F6",
        "steps": [
            {"step_number": 1, "title": "Software-Installation", "description": "Laden Sie Sonel Reports Plus von sonel.pl herunter (Bereich Software). Installieren Sie es auf einem Computer mit Windows 10/11. Die Software ist kostenlos für Sonel-Messgerätebenutzer.", "tip": "Erforderliches System: Windows 10 oder Windows 11.", "image": "https://cdn.sonel.com/Zdjecia/Programy/Programy+komputerowe/Sonel+Reports+PLUS/image-thumb__36489__img-product-thumb/blank-box-reports-plus_mHqcbIA.webp"},
            {"step_number": 2, "title": "Neues Projekt erstellen", "description": "Starten Sie das Programm und wählen Sie 'Neues Projekt'. Geben Sie Daten ein: Objektname, Adresse, Auftraggeber, Prüfer, Datum.", "tip": "Sie können eine Vorlage für Prüferdaten zur Wiederverwendung speichern."},
            {"step_number": 3, "title": "Objektbaumstruktur", "description": "Erstellen Sie die Gebäudestruktur: Etagen, Räume, Verteilungen hinzufügen. Für jeden Raum können Sie Stromkreise und Messpunkte anlegen.", "tip": "Die Baumstruktur ermöglicht eine übersichtliche Organisation der Ergebnisse."},
            {"step_number": 4, "title": "Messpunkte hinzufügen", "description": "Fügen Sie in jedem Raum Messpunkte hinzu: Steckdosen, Beleuchtung, fest installierte Geräte. Schutztyp angeben (Sicherung, Leitungsschutzschalter).", "tip": "Das Programm enthält eine Bibliothek von Sicherungen und Schutzgeräten."},
            {"step_number": 5, "title": "Struktur zum Messgerät übertragen", "description": "MPI-530 per USB anschließen. 'Struktur an Messgerät senden' wählen. Die Struktur wird in den Messgerätspeicher geladen.", "tip": "So werden Messergebnisse automatisch den Punkten zugeordnet."}
        ],
        "tips": ["Sonel Reports Plus unterstützt MPI-530, MPI-525, MPI-520 und andere Messgeräte", "Das Programm ermöglicht die Erstellung eigener Berichtsvorlagen", "Regelmäßige Software-Updates fügen neue Funktionen hinzu"]
    },
    {
        "id": "download_results",
        "name": "Ergebnisse vom Messgerät herunterladen",
        "description": "Wie man Messergebnisse vom MPI-530 auf den Computer überträgt",
        "icon": "Download", "color": "#10B981",
        "steps": [
            {"step_number": 1, "title": "USB-Verbindung", "description": "MPI-530 mit dem mitgelieferten USB-Kabel an den Computer anschließen. Messgerät einschalten.", "tip": "Original-Sonel-Kabel für beste Verbindungsstabilität verwenden."},
            {"step_number": 2, "title": "Kommunikation in Reports Plus", "description": "In Sonel Reports Plus 'Messgerät' -> 'Ergebnisse herunterladen' wählen. Das Programm erkennt das Messgerät automatisch.", "tip": "Falls Messgerät nicht erkannt wird - Sonel USB-Treiber installieren."},
            {"step_number": 3, "title": "Ergebnisse zum Download auswählen", "description": "Wählen Sie welche Ergebnisse heruntergeladen werden: alle oder nur ausgewählte. Nach Datum oder Messtyp filtern.", "tip": "Bei gesendeter Struktur werden Ergebnisse automatisch zugeordnet."},
            {"step_number": 4, "title": "Überprüfung und Zuordnung", "description": "Heruntergeladene Ergebnisse prüfen. Nicht zugeordnete Ergebnisse den entsprechenden Messpunkten zuweisen.", "tip": "Das Programm kennzeichnet BESTANDEN/NICHT BESTANDEN basierend auf Normen."}
        ],
        "tips": ["Ergebnisse nach jeder Messsitzung herunterladen", "Vor dem Download sicherstellen, dass das Messgerät vollständig geladen ist", "Sie können Ergebnisse auch direkt nach CSV oder Excel exportieren"]
    },
    {
        "id": "generate_protocol",
        "name": "Protokoll erstellen",
        "description": "Wie man ein professionelles Messprotokoll aus Ergebnissen erstellt",
        "icon": "Printer", "color": "#F59E0B",
        "steps": [
            {"step_number": 1, "title": "Ergebnisvollständigkeit prüfen", "description": "Vor der Protokollerstellung sicherstellen, dass alle Messungen abgeschlossen und Ergebnisse zugeordnet sind.", "tip": "Fehlende Ergebnisse sind rot markiert."},
            {"step_number": 2, "title": "Vorlagenauswahl", "description": "'Protokoll erstellen' wählen. Vorlage wählen: Abnahmeprotokoll, periodisches Protokoll oder eigene Vorlage.", "tip": "Sie können eigene Protokollvorlagen erstellen."},
            {"step_number": 3, "title": "Kopfdaten ergänzen", "description": "Daten ergänzen: Protokollnummer, Datum, Auftraggeberdaten, Prüfungszweck (Abnahme/periodische Prüfung).", "tip": "Prüfer- und Qualifikationsdaten im Profil zur Wiederverwendung speichern."},
            {"step_number": 4, "title": "Vorschau und Bearbeitung", "description": "Protokollvorschau durchsehen. Anmerkungen, Empfehlungen hinzufügen oder Beschreibungen bearbeiten.", "tip": "Fotos von Verteilungen oder bei der Messung gefundenen Problemen hinzufügen."},
            {"step_number": 5, "title": "Export und Druck", "description": "Protokoll nach PDF exportieren oder direkt drucken. Auch Etiketten für Messpunkte können gedruckt werden.", "tip": "PDF enthält digitale Signatur mit Erstellungsdatum."}
        ],
        "tips": ["Protokoll sollte enthalten: Objektdaten, Messumfang, Ergebnisse, Bewertung, Empfehlungen", "Protokolle mindestens 5 Jahre gemäß Vorschriften aufbewahren", "Sie können das Protokoll direkt aus dem Programm per E-Mail versenden"]
    },
    {
        "id": "pe6_migration",
        "name": "Migration von Sonel PE6",
        "description": "Wie man Daten von der alten PE6-Software zu Sonel Reports Plus überträgt",
        "icon": "FolderSync", "color": "#8B5CF6",
        "steps": [
            {"step_number": 1, "title": "Export aus PE6", "description": "In Sonel PE6 Projekt öffnen. 'Exportieren' wählen und Datei im .pe6- oder .xml-Format speichern.", "tip": "PE6 ist ältere Software - Sonel Reports Plus hat mehr Funktionen."},
            {"step_number": 2, "title": "Import in Reports Plus", "description": "In Sonel Reports Plus 'Projekt importieren' wählen. Auf die aus PE6 exportierte Datei verweisen.", "tip": "Import behält Struktur und Messergebnisse bei."},
            {"step_number": 3, "title": "Datenüberprüfung", "description": "Importierte Daten prüfen. Fehlende Informationen ergänzen (z.B. Fotos, Schaltpläne).", "tip": "Einige PE6-Funktionen erfordern möglicherweise manuelle Konvertierung."}
        ],
        "tips": ["Sonel Reports Plus ersetzt PE6 und PE5", "Reports Plus hat bessere Integration mit neuen Messgeräten", "Kopie der Original-PE6-Dateien sicherheitshalber aufbewahren"]
    }
]

# ============================================
# PROTOCOL TEMPLATES TRANSLATIONS
# ============================================

TEMPLATES_EN = [
    {"id": "reception", "name": "Electrical installation acceptance protocol", "description": "Full acceptance measurement protocol for new installation per PN-HD 60364", "measurements": ["Installation visual inspection", "Protective conductor (PE) continuity", "Insulation resistance", "Indirect contact protection (Zs)", "RCD testing", "Phase sequence verification", "Earth resistance measurement"]},
    {"id": "periodic", "name": "Periodic inspection protocol", "description": "Periodic measurement protocol for existing installation (every 5 years or more frequently)", "measurements": ["Installation visual inspection - technical condition", "Protective conductor continuity", "Insulation resistance (min. 0.5 MΩ)", "Shock protection effectiveness", "RCD testing", "Protection device verification"]},
    {"id": "rcd_only", "name": "RCD testing protocol", "description": "Shortened protocol for residual current device testing only", "measurements": ["RCD test at 0.5x IΔn", "RCD test at 1x IΔn (time and touch voltage)", "RCD test at 2x IΔn", "RCD test at 5x IΔn", "TEST button test"]},
    {"id": "earthing", "name": "Earth resistance measurement protocol", "description": "Protocol for protective and functional earth resistance measurements", "measurements": ["Earthing installation visual inspection", "Earth resistance measurement - technical method", "Soil resistivity measurement (optional)", "Bonding connection verification", "Earth electrode condition assessment"]},
    {"id": "lighting", "name": "Illumination measurement protocol", "description": "Workplace illumination measurement protocol per PN-EN 12464-1", "measurements": ["Workstation identification", "Illumination measurement at task area level", "Illumination measurement in surrounding area", "Uniformity assessment", "Comparison with PN-EN 12464-1 requirements"]}
]

TEMPLATES_DE = [
    {"id": "reception", "name": "Abnahmeprotokoll Elektroinstallation", "description": "Vollständiges Abnahmeprotokoll für neue Installation nach PN-HD 60364", "measurements": ["Sichtprüfung der Anlage", "Durchgängigkeit der Schutzleiter (PE)", "Isolationswiderstand", "Schutz bei indirektem Berühren (Zs)", "RCD-Prüfung", "Drehfeldprüfung", "Erdungswiderstandsmessung"]},
    {"id": "periodic", "name": "Protokoll der periodischen Prüfung", "description": "Periodisches Messprotokoll für bestehende Anlagen (alle 5 Jahre oder häufiger)", "measurements": ["Sichtprüfung - technischer Zustand", "Schutzleiterdurchgängigkeit", "Isolationswiderstand (min. 0.5 MΩ)", "Wirksamkeit des Fehlerschutzes", "RCD-Prüfung", "Überprüfung der Schutzeinrichtungen"]},
    {"id": "rcd_only", "name": "RCD-Prüfprotokoll", "description": "Verkürztes Protokoll nur für Fehlerstromschutzschalter-Prüfung", "measurements": ["RCD-Test bei 0.5x IΔn", "RCD-Test bei 1x IΔn (Zeit und Berührungsspannung)", "RCD-Test bei 2x IΔn", "RCD-Test bei 5x IΔn", "TEST-Taste-Prüfung"]},
    {"id": "earthing", "name": "Erdungswiderstand-Messprotokoll", "description": "Protokoll für Schutz- und Betriebserdungsmessungen", "measurements": ["Sichtprüfung der Erdungsanlage", "Erdungswiderstandsmessung - technische Methode", "Spezifischer Bodenwiderstand (optional)", "Potentialausgleichsverbindungen prüfen", "Erderzustandsbewertung"]},
    {"id": "lighting", "name": "Beleuchtungsmessprotokoll", "description": "Messprotokoll für Arbeitsplatzbeleuchtung nach PN-EN 12464-1", "measurements": ["Arbeitsplatzidentifizierung", "Beleuchtungsmessung auf Aufgabenbereichsniveau", "Beleuchtungsmessung im Umgebungsbereich", "Gleichmäßigkeitsbewertung", "Vergleich mit PN-EN 12464-1 Anforderungen"]}
]

# ============================================
# EXAMPLE PROTOCOLS TRANSLATIONS
# ============================================

EXAMPLES_EN = [
    {
        "id": "example_reception", "name": "Example: Apartment acceptance protocol",
        "object_name": "Apartment no. 15, Building B", "object_address": "ul. Słoneczna 10, 00-001 Warsaw",
        "date": "2024-01-15", "inspector": "Jan Kowalski", "inspector_cert": "E-1234/2023",
        "meter_serial": "MPI-530 S/N: 12345678", "meter_calibration": "2024-06-15",
        "measurements": [
            {"point": "Living room", "circuit": "1", "protection": "B16", "value": "0.45", "unit": "Ω", "limit": "2.88", "status": "PASS", "notes": ""},
            {"point": "Living room", "circuit": "1", "protection": "-", "value": "150", "unit": "MΩ", "limit": "1", "status": "PASS", "notes": ""},
            {"point": "Kitchen", "circuit": "2", "protection": "B16", "value": "0.52", "unit": "Ω", "limit": "2.88", "status": "PASS", "notes": ""},
            {"point": "Kitchen RCD", "circuit": "2", "protection": "30mA", "value": "22", "unit": "ms", "limit": "300", "status": "PASS", "notes": "Type A"},
            {"point": "Bathroom", "circuit": "3", "protection": "B10", "value": "0.38", "unit": "Ω", "limit": "4.60", "status": "PASS", "notes": ""},
            {"point": "Bathroom RCD", "circuit": "3", "protection": "30mA", "value": "18", "unit": "ms", "limit": "300", "status": "PASS", "notes": "Type A"}
        ],
        "conclusion": "POSITIVE - Installation meets PN-HD 60364 requirements",
        "recommendations": ["Periodic inspection recommended in 5 years", "All circuits correctly protected"]
    },
    {
        "id": "example_periodic", "name": "Example: Periodic inspection protocol",
        "object_name": "Office building 'Centrum'", "object_address": "ul. Główna 5, 00-002 Warsaw",
        "date": "2024-02-20", "inspector": "Anna Nowak", "inspector_cert": "E-5678/2022",
        "meter_serial": "MPI-530 S/N: 87654321", "meter_calibration": "2024-03-01",
        "measurements": [
            {"point": "Main board", "circuit": "PEN", "protection": "-", "value": "0.12", "unit": "Ω", "limit": "1", "status": "PASS", "notes": "PE continuity"},
            {"point": "Office 1", "circuit": "5", "protection": "B16", "value": "0.68", "unit": "Ω", "limit": "2.88", "status": "PASS", "notes": ""},
            {"point": "Office 2", "circuit": "7", "protection": "B16", "value": "3.15", "unit": "Ω", "limit": "2.88", "status": "FAIL", "notes": "Zs exceeded!"},
            {"point": "Server room", "circuit": "10", "protection": "C32", "value": "0.95", "unit": "Ω", "limit": "1.44", "status": "PASS", "notes": ""},
            {"point": "Corridor", "circuit": "12", "protection": "B10", "value": "1.85", "unit": "Ω", "limit": "4.60", "status": "PASS", "notes": ""}
        ],
        "conclusion": "NEGATIVE - Irregularities found requiring correction",
        "recommendations": ["Office 2, circuit 7: Loop impedance Zs=3.15 Ω exceeds limit 2.88 Ω for B16 protection", "Required: Check wiring and connection condition in circuit 7", "Re-inspection after correction within 30 days"]
    },
    {
        "id": "example_rcd", "name": "Example: RCD testing protocol",
        "object_name": "Single-family house", "object_address": "ul. Ogrodowa 22, 00-003 Warsaw",
        "date": "2024-03-10", "inspector": "Piotr Wiśniewski", "inspector_cert": "E-9012/2021",
        "meter_serial": "MPI-530 S/N: 11223344", "meter_calibration": "2024-05-20",
        "measurements": [
            {"point": "RCD F1", "circuit": "Main", "protection": "30mA AC", "value": "22", "unit": "ms", "limit": "300", "status": "PASS", "notes": "1x IΔn"},
            {"point": "RCD F1", "circuit": "Main", "protection": "30mA AC", "value": "15", "unit": "ms", "limit": "150", "status": "PASS", "notes": "2x IΔn"},
            {"point": "RCD F1", "circuit": "Main", "protection": "30mA AC", "value": "8", "unit": "ms", "limit": "40", "status": "PASS", "notes": "5x IΔn"},
            {"point": "RCD F2", "circuit": "Kitchen", "protection": "30mA A", "value": "28", "unit": "ms", "limit": "300", "status": "PASS", "notes": "1x IΔn"},
            {"point": "RCD F3", "circuit": "Bathroom", "protection": "30mA A", "value": "20", "unit": "ms", "limit": "300", "status": "PASS", "notes": "1x IΔn"}
        ],
        "conclusion": "POSITIVE - All RCDs operate correctly",
        "recommendations": ["All RCDs meet EN 61008 requirements", "Next RCD test recommended in 12 months"]
    },
    {
        "id": "example_earthing", "name": "Example: Earth resistance protocol",
        "object_name": "Transformer station TR-15", "object_address": "ul. Przemysłowa 8, 00-004 Warsaw",
        "date": "2024-04-05", "inspector": "Marek Zieliński", "inspector_cert": "E-3456/2020",
        "meter_serial": "MPI-530 S/N: 55667788", "meter_calibration": "2024-07-10",
        "measurements": [
            {"point": "Main earth E1", "circuit": "-", "protection": "-", "value": "2.8", "unit": "Ω", "limit": "10", "status": "PASS", "notes": "3-wire method"},
            {"point": "Earth E2", "circuit": "-", "protection": "-", "value": "4.2", "unit": "Ω", "limit": "10", "status": "PASS", "notes": "3-wire method"},
            {"point": "Equipment earth", "circuit": "-", "protection": "-", "value": "1.5", "unit": "Ω", "limit": "10", "status": "PASS", "notes": "4-wire method"},
            {"point": "Lightning rod earth", "circuit": "-", "protection": "-", "value": "8.5", "unit": "Ω", "limit": "10", "status": "PASS", "notes": "3-wire method"}
        ],
        "conclusion": "POSITIVE - All earths meet requirements",
        "recommendations": ["All earth resistances below 10 Ω", "Next earth resistance measurement in 12 months", "Check bonding connections annually"]
    },
    {
        "id": "example_lighting", "name": "Example: Illumination measurement protocol",
        "object_name": "Open-plan office 'TechHub'", "object_address": "ul. Nowoczesna 15, p. 3, 00-005 Warsaw",
        "date": "2024-05-12", "inspector": "Katarzyna Lewandowska", "inspector_cert": "E-7890/2023",
        "meter_serial": "MPI-530 S/N: 99887766", "meter_calibration": "2024-08-01",
        "measurements": [
            {"point": "Desk A1", "circuit": "-", "protection": "-", "value": "520", "unit": "lx", "limit": "500", "status": "PASS", "notes": "Office work"},
            {"point": "Desk A2", "circuit": "-", "protection": "-", "value": "485", "unit": "lx", "limit": "500", "status": "FAIL", "notes": "Below norm!"},
            {"point": "Desk B1", "circuit": "-", "protection": "-", "value": "550", "unit": "lx", "limit": "500", "status": "PASS", "notes": "Office work"},
            {"point": "Corridor", "circuit": "-", "protection": "-", "value": "115", "unit": "lx", "limit": "100", "status": "PASS", "notes": "Passage"},
            {"point": "Kitchen", "circuit": "-", "protection": "-", "value": "310", "unit": "lx", "limit": "200", "status": "PASS", "notes": "Social room"}
        ],
        "conclusion": "NEGATIVE - Irregularities found",
        "recommendations": ["Desk A2: Illumination 485 lx below minimum 500 lx for office work", "Recommended: Add additional lighting fixture or replace bulb with higher output", "Re-measurement after correction"]
    }
]

EXAMPLES_DE = [
    {
        "id": "example_reception", "name": "Beispiel: Wohnungsabnahmeprotokoll",
        "object_name": "Wohnung Nr. 15, Gebäude B", "object_address": "ul. Słoneczna 10, 00-001 Warschau",
        "date": "2024-01-15", "inspector": "Jan Kowalski", "inspector_cert": "E-1234/2023",
        "meter_serial": "MPI-530 S/N: 12345678", "meter_calibration": "2024-06-15",
        "measurements": [
            {"point": "Wohnzimmer", "circuit": "1", "protection": "B16", "value": "0.45", "unit": "Ω", "limit": "2.88", "status": "PASS", "notes": ""},
            {"point": "Wohnzimmer", "circuit": "1", "protection": "-", "value": "150", "unit": "MΩ", "limit": "1", "status": "PASS", "notes": ""},
            {"point": "Küche", "circuit": "2", "protection": "B16", "value": "0.52", "unit": "Ω", "limit": "2.88", "status": "PASS", "notes": ""},
            {"point": "Küche RCD", "circuit": "2", "protection": "30mA", "value": "22", "unit": "ms", "limit": "300", "status": "PASS", "notes": "Typ A"},
            {"point": "Badezimmer", "circuit": "3", "protection": "B10", "value": "0.38", "unit": "Ω", "limit": "4.60", "status": "PASS", "notes": ""},
            {"point": "Badezimmer RCD", "circuit": "3", "protection": "30mA", "value": "18", "unit": "ms", "limit": "300", "status": "PASS", "notes": "Typ A"}
        ],
        "conclusion": "POSITIV - Anlage erfüllt PN-HD 60364 Anforderungen",
        "recommendations": ["Periodische Prüfung in 5 Jahren empfohlen", "Alle Stromkreise korrekt geschützt"]
    },
    {
        "id": "example_periodic", "name": "Beispiel: Periodisches Prüfprotokoll",
        "object_name": "Bürogebäude 'Centrum'", "object_address": "ul. Główna 5, 00-002 Warschau",
        "date": "2024-02-20", "inspector": "Anna Nowak", "inspector_cert": "E-5678/2022",
        "meter_serial": "MPI-530 S/N: 87654321", "meter_calibration": "2024-03-01",
        "measurements": [
            {"point": "Hauptverteilung", "circuit": "PEN", "protection": "-", "value": "0.12", "unit": "Ω", "limit": "1", "status": "PASS", "notes": "PE-Durchgang"},
            {"point": "Büro 1", "circuit": "5", "protection": "B16", "value": "0.68", "unit": "Ω", "limit": "2.88", "status": "PASS", "notes": ""},
            {"point": "Büro 2", "circuit": "7", "protection": "B16", "value": "3.15", "unit": "Ω", "limit": "2.88", "status": "FAIL", "notes": "Zs überschritten!"},
            {"point": "Serverraum", "circuit": "10", "protection": "C32", "value": "0.95", "unit": "Ω", "limit": "1.44", "status": "PASS", "notes": ""},
            {"point": "Flur", "circuit": "12", "protection": "B10", "value": "1.85", "unit": "Ω", "limit": "4.60", "status": "PASS", "notes": ""}
        ],
        "conclusion": "NEGATIV - Unregelmäßigkeiten gefunden, Korrektur erforderlich",
        "recommendations": ["Büro 2, Stromkreis 7: Schleifenimpedanz Zs=3.15 Ω überschreitet Grenzwert 2.88 Ω für B16", "Erforderlich: Leitungs- und Anschlusszustand in Stromkreis 7 prüfen", "Nachprüfung nach Korrektur innerhalb von 30 Tagen"]
    },
    {
        "id": "example_rcd", "name": "Beispiel: RCD-Prüfprotokoll",
        "object_name": "Einfamilienhaus", "object_address": "ul. Ogrodowa 22, 00-003 Warschau",
        "date": "2024-03-10", "inspector": "Piotr Wiśniewski", "inspector_cert": "E-9012/2021",
        "meter_serial": "MPI-530 S/N: 11223344", "meter_calibration": "2024-05-20",
        "measurements": [
            {"point": "RCD F1", "circuit": "Haupt", "protection": "30mA AC", "value": "22", "unit": "ms", "limit": "300", "status": "PASS", "notes": "1x IΔn"},
            {"point": "RCD F1", "circuit": "Haupt", "protection": "30mA AC", "value": "15", "unit": "ms", "limit": "150", "status": "PASS", "notes": "2x IΔn"},
            {"point": "RCD F1", "circuit": "Haupt", "protection": "30mA AC", "value": "8", "unit": "ms", "limit": "40", "status": "PASS", "notes": "5x IΔn"},
            {"point": "RCD F2", "circuit": "Küche", "protection": "30mA A", "value": "28", "unit": "ms", "limit": "300", "status": "PASS", "notes": "1x IΔn"},
            {"point": "RCD F3", "circuit": "Bad", "protection": "30mA A", "value": "20", "unit": "ms", "limit": "300", "status": "PASS", "notes": "1x IΔn"}
        ],
        "conclusion": "POSITIV - Alle RCDs funktionieren korrekt",
        "recommendations": ["Alle RCDs erfüllen EN 61008 Anforderungen", "Nächster RCD-Test in 12 Monaten empfohlen"]
    },
    {
        "id": "example_earthing", "name": "Beispiel: Erdungswiderstand-Protokoll",
        "object_name": "Transformatorstation TR-15", "object_address": "ul. Przemysłowa 8, 00-004 Warschau",
        "date": "2024-04-05", "inspector": "Marek Zieliński", "inspector_cert": "E-3456/2020",
        "meter_serial": "MPI-530 S/N: 55667788", "meter_calibration": "2024-07-10",
        "measurements": [
            {"point": "Haupterder E1", "circuit": "-", "protection": "-", "value": "2.8", "unit": "Ω", "limit": "10", "status": "PASS", "notes": "3-Leiter-Methode"},
            {"point": "Erder E2", "circuit": "-", "protection": "-", "value": "4.2", "unit": "Ω", "limit": "10", "status": "PASS", "notes": "3-Leiter-Methode"},
            {"point": "Geräteerder", "circuit": "-", "protection": "-", "value": "1.5", "unit": "Ω", "limit": "10", "status": "PASS", "notes": "4-Leiter-Methode"},
            {"point": "Blitzschutzerder", "circuit": "-", "protection": "-", "value": "8.5", "unit": "Ω", "limit": "10", "status": "PASS", "notes": "3-Leiter-Methode"}
        ],
        "conclusion": "POSITIV - Alle Erdungen erfüllen Anforderungen",
        "recommendations": ["Alle Erdungswiderstände unter 10 Ω", "Nächste Erdungsmessung in 12 Monaten", "Potentialausgleichsverbindungen jährlich prüfen"]
    },
    {
        "id": "example_lighting", "name": "Beispiel: Beleuchtungsmessprotokoll",
        "object_name": "Großraumbüro 'TechHub'", "object_address": "ul. Nowoczesna 15, Et. 3, 00-005 Warschau",
        "date": "2024-05-12", "inspector": "Katarzyna Lewandowska", "inspector_cert": "E-7890/2023",
        "meter_serial": "MPI-530 S/N: 99887766", "meter_calibration": "2024-08-01",
        "measurements": [
            {"point": "Schreibtisch A1", "circuit": "-", "protection": "-", "value": "520", "unit": "lx", "limit": "500", "status": "PASS", "notes": "Büroarbeit"},
            {"point": "Schreibtisch A2", "circuit": "-", "protection": "-", "value": "485", "unit": "lx", "limit": "500", "status": "FAIL", "notes": "Unter Norm!"},
            {"point": "Schreibtisch B1", "circuit": "-", "protection": "-", "value": "550", "unit": "lx", "limit": "500", "status": "PASS", "notes": "Büroarbeit"},
            {"point": "Flur", "circuit": "-", "protection": "-", "value": "115", "unit": "lx", "limit": "100", "status": "PASS", "notes": "Durchgang"},
            {"point": "Küche", "circuit": "-", "protection": "-", "value": "310", "unit": "lx", "limit": "200", "status": "PASS", "notes": "Sozialraum"}
        ],
        "conclusion": "NEGATIV - Unregelmäßigkeiten gefunden",
        "recommendations": ["Schreibtisch A2: Beleuchtungsstärke 485 lx unter Minimum 500 lx für Büroarbeit", "Empfohlen: Zusätzliche Leuchte installieren oder Leuchtmittel mit höherer Leistung verwenden", "Nachmessung nach Korrektur"]
    }
]


def get_guides_translations(lang):
    if lang == "en":
        return GUIDES_EN
    elif lang == "de":
        return GUIDES_DE
    return None

def get_templates_translations(lang):
    if lang == "en":
        return TEMPLATES_EN
    elif lang == "de":
        return TEMPLATES_DE
    return None

def get_examples_translations(lang):
    if lang == "en":
        return EXAMPLES_EN
    elif lang == "de":
        return EXAMPLES_DE
    return None
