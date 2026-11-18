# Babyvoeding

Een Home Assistant-integratie voor flesvoeding: een dagboek van gegeven flessen, een herinnering op het juiste moment, sensoren voor widgets, een aftelklok op het iPhone-vergrendelscherm en een dashboardkaart.

## Wat het doet

- **Ritme:** overdag drie uur tussen flessen. Een fles die tussen 22:30 en 07:00 begint krijgt het nachtinterval: standaard vier uur, of een eigen interval van drie tot acht uur. Gerekend in verstreken uren, ook bij zomer- en wintertijd.
- **Herinnering:** op het geplande moment een kritieke melding op de ingestelde telefoons, één keer per gepland moment.
- **Vooruit:** een fles mag tot 24 uur vooruit worden opgeslagen; de herinnering telt dan vanaf die fles.
- **Widgets:** `sensor.volgende_fles` (bijvoorbeeld `14:30`, `Nu` of `Niet gepland`) en `sensor.voeding_voortgang` (0 tot 100 % in stappen van vijf). Na een wijziging krijgen de telefoons de opdracht `update_widgets`.
- **Vergrendelscherm:** een stille Live Activity met een aftelklok tot de volgende fles.
- **Kaart:** de integratie levert de kaart `custom:baby-feeding-card` mee en laadt hem op alle dashboards; een dashboardbron toevoegen is niet nodig.

## Installeren

1. Voeg in HACS via **⋮ → Aangepaste repository's** deze repository toe als type **Integration**. HACS werkt alleen met openbare GitHub-repository's.
2. Installeer **Babyvoeding** en herstart Home Assistant.
3. Voeg via **Instellingen → Apparaten en diensten → Integratie toevoegen** de integratie **Babyvoeding** toe. Kies de telefoons die herinneringen krijgen en het dashboardpad dat de melding opent.

Vereist Home Assistant 2026.7.0 of later. Sta op elke iPhone bij Instellingen → Home Assistant **Kritieke meldingen** en **Live-activiteiten** toe.

## Dashboard

```yaml
type: custom:baby-feeding-card
mode: main        # main, history, settings of timer
```

Met `mode: timer` toont de kaart alleen de aftelklok. Met `navigation_path: /dashboard-main/voeding` opent een tik de voedingsview.

## Entiteiten

| Entiteit | Inhoud |
|---|---|
| `sensor.volgende_voeding` | Tijdstip van de volgende fles |
| `sensor.volgende_fles` | Tijd als tekst voor widgets |
| `sensor.voeding_voortgang` | Voortgang tot de volgende fles in % |
| `sensor.voeding_status` | Plan, open fles, instellingen en de voedingen van de afgelopen week, voor de kaart |
| `calendar.voedingsdagboek` | Het dagboek als kalender, alleen-lezen |

## Acties

`baby_feeding.save_bottle`, `add_earlier_feed`, `update_feed`, `delete_feed`, `new_bottle`, `set_settings` en `import_calendar`. Een geweigerde wijziging geeft een melding met de reden, bijvoorbeeld een tweede voeding op dezelfde minuut of een tijd meer dan 24 uur vooruit.

## Overstappen vanaf het YAML-package

1. Maak een back-up van `/config/packages/baby_voeding.yaml`, `/config/www/voeding/` en het dashboard.
2. Verwijder het package en de dashboardbron `/local/voeding/baby-feeding-card.js`, en herstart.
3. Installeer en stel de integratie in zoals hierboven.
4. Neem het dagboek over met de actie `baby_feeding.import_calendar` en de oude kalender als `entity_id`. Dit kan alleen in een leeg dagboek. Een gepland moment dat al voorbij is, meldt niet opnieuw.
5. Controleer het dagboek en de volgende fles, en verwijder daarna de oude Local calendar. Zolang die bestaat, heet de nieuwe kalender `calendar.voedingsdagboek_2`; hernoem hem daarna naar `calendar.voedingsdagboek`.

## Ontwikkelen

```bash
python -m pytest
```

```bash
npm install && npm run test:card
```
