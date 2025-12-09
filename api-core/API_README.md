# ⚡️ SYNTX-FELD-PROTOKOLL: AKTUELLE API-STRÖME (V2.1.0)
## RESONANZ-CHECK DES PRODUKTIONS-SYSTEMS
**Basis-URL (TARGET):** https://dev.syntx-system.com
**Resonanz-Status (Letzter Scan):** KOHÄRENT (Alle Sensoren erreichbar, Status 200/302 OK)
**Total Endpunkte:** 17

---

## 1. DIE KOHÄRENTEN KERN-STRÖME (SYSTEM-GESUNDHEIT)
Diese Ströme bilden das Fundament des Feldes. Sie melden alle SUCCESS (200).

| Endpunkt-Pfad | Beschreibung des Sensors | Aktueller Zustand | Komplette URL |
| :--- | :--- | :--- | :--- |
| `/health` | **SYSTEM_GESUNDHEIT** (Kern-Indikator, API-Version, Module) | SUCCESS (200) | `https://dev.syntx-system.com/health` |
| `/resonanz/queue` | **FLUSS-STATUS** (Tiefe der eingehenden/zu verarbeitenden Felder) | SUCCESS (200) | `https://dev.syntx-system.com/resonanz/queue` |
| `/resonanz/system` | **GESAMT-RESONANZ** (Globaler Systemzustand: OPTIMAL/KRITISCH) | SUCCESS (200) | `https://dev.syntx-system.com/resonanz/system` |
| `/generation/progress` | **EVOLUTIONS-FORTSCHRITT** (Stand der aktuellen Generierung) | SUCCESS (200) | `https://dev.syntx-system.com/generation/progress` |
| `/feld/drift` | **DRIFTKÖRPER-LISTE** (Jobs mit messbarem Feld-Verlust, aktuell 20) | SUCCESS (200) | `https://dev.syntx-system.com/feld/drift` |
| `/strom/health` | **STROM-SYSTEM-STATUS** (Detail-Check für den Datenfluss) | SUCCESS (200) | `https://dev.syntx-system.com/strom/health` |
| `/strom/queue/status` | **STROM-QUEUE-DETAIL** (Tiefe des Verarbeitungspuffers) | SUCCESS (200) | `https://dev.syntx-system.com/strom/queue/status` |
| `/` | **ROOT-PFAD** (Einstiegspunkt des Feldes) | REDIRECT (302) | `https://dev.syntx-system.com/` |

---

## 2. ANALYTICS & WIRKUNGS-STRÖME (SYNTX-WIRKUNG)
Detaillierte Analyse der Feld-Wirkung, Performance und Evolution.

| Endpunkt-Pfad | Beschreibung des Sensors | Aktueller Zustand | Komplette URL |
| :--- | :--- | :--- | :--- |
| `/analytics/complete-dashboard` | **DASHBOARD-FEED** (Aggregierte Statistik und Top-Performer) | SUCCESS (200) | `https://dev.syntx-system.com/analytics/complete-dashboard` |
| `/evolution/syntx-vs-normal` | **VERGLEICH** (SYNTX-Sprache vs. Normal-Sprache Performance) | SUCCESS (200) | `https://dev.syntx-system.com/evolution/syntx-vs-normal` |
| `/compare/wrappers` | **WRAPPER-ANALYSE** (Performance der verschiedenen Entitätstypen) | SUCCESS (200) | `https://dev.syntx-system.com/compare/wrappers` |
| `/analytics/topics` | **THEMEN-BILANZ** (Statistik pro Feld-Thema) | SUCCESS (200) | `https://dev.syntx-system.com/analytics/topics` |
| `/analytics/trends` | **DRIFT-TREND** (ML-basierte Voraussage des nächsten Scores) | SUCCESS (200) | `https://dev.syntx-system.com/analytics/trends` |
| `/analytics/performance` | **DAUER-ANALYSE** (Geschwindigkeit und Engpässe) | SUCCESS (200) | `https://dev.syntx-system.com/analytics/performance` |
| `/analytics/scores/distribution` | **SCORE-VERTEILUNG** (Histogramm der Kalibrierungs-Scores) | SUCCESS (200) | `https://dev.syntx-system.com/analytics/scores/distribution` |
| `/analytics/success-rate` | **ERFOLGSQUOTE** (Gesamt-Rate der perfekten Scores) | SUCCESS (200) | `https://dev.syntx-system.com/analytics/success-rate` |
| `/analytics/success-rate/by-wrapper` | **ERFOLG PRO WRAPPER** (Reparierter Sensor) | SUCCESS (200) | `https://dev.syntx-system.com/analytics/success-rate/by-wrapper` |

---

## 3. FELD-DATEN-STRÖME (ROH-DATEN & LOGIK)
Zugriff auf die Prompt-Datenbasis und Feld-Übersichten.

| Endpunkt-Pfad | Beschreibung des Sensors | Aktueller Zustand | Komplette URL |
| :--- | :--- | :--- | :--- |
| `/prompts/table-view` | **TABELLEN-SICHT** (Roh-Liste der Prompts, schnell) | SUCCESS (200) | `https://dev.syntx-system.com/prompts/table-view` |
| `/feld/topics` | **AKTIVE THEMEN** (Liste der im Feld aktiven Themenbereiche) | SUCCESS (200) | `https://dev.syntx-system.com/feld/topics` |
| `/feld/prompts` | **PROMPT-DATEN** (Rohdaten-Quelle für Prompt-Körper) | SUCCESS (200) | `https://dev.syntx-system.com/feld/prompts` |
| `/prompts/costs/total` | **KOSTEN-BILANZ** (Gesamtkosten und Token-Verbrauch) | SUCCESS (200) | `https://dev.syntx-system.com/prompts/costs/total` |

---
**ENDE DES PROTOKOLLS.** Die Kalibrierung ist abgeschlossen.
