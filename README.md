# Babyvoeding for Home Assistant

[![Validate](https://github.com/dedmen7/ha-baby-feeding/actions/workflows/validate.yml/badge.svg)](https://github.com/dedmen7/ha-baby-feeding/actions/workflows/validate.yml)
[![Tests](https://github.com/dedmen7/ha-baby-feeding/actions/workflows/tests.yml/badge.svg)](https://github.com/dedmen7/ha-baby-feeding/actions/workflows/tests.yml)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/docs/faq/custom_repositories/)

A Home Assistant integration for bottle feeding. It keeps a diary of the bottles you give, reminds both parents when the next bottle is due, and shows the countdown on a dashboard card, in phone widgets and on the iPhone lock screen.

> **Status:** early and opinionated. The texts are Dutch and the rhythm is the one this was built for: three hours by day, a configurable night interval for bottles started between 22:30 and 07:00. Amounts are in cc (ml). Translations and configurable times are welcome as contributions.

## Features

- **Feeding rhythm** – three hours between bottles by day; bottles started between 22:30 and 07:00 use the night interval (four hours by default, or your own choice of three to eight). Intervals are elapsed hours, so daylight-saving changes are handled correctly.
- **One reminder per planned moment** – a critical notification on the phones you choose. Changing the settings never repeats a reminder for a moment that has already alerted.
- **Bottles ahead** – a bottle can be saved up to 24 hours in advance; the next reminder then counts from that bottle.
- **Diary** – add earlier feeds, change or delete feeds, and see daily and weekly totals. The diary is stored by the integration and is also shown as a read-only calendar.
- **Widgets** – `sensor.volgende_fles` (for example `14:30`, `Nu` or `Niet gepland`) and `sensor.voeding_voortgang` (0–100 % in steps of five). Phones get an `update_widgets` command after a change.
- **Lock screen** – a silent Live Activity with a countdown to the next bottle, also in the Dynamic Island.
- **Dashboard card** – shipped with the integration and loaded on every dashboard; there is no resource to add.

## Requirements

- Home Assistant 2026.7.0 or later.
- The Home Assistant Companion app on the phones that should get reminders. For iPhones, allow **Critical Notifications** and **Live Activities** for Home Assistant in the iOS settings (iOS 17.2 or later for Live Activities).

## Installation

### HACS (recommended)

1. In HACS, open **⋮ → Custom repositories**.
2. Add `https://github.com/dedmen7/ha-baby-feeding` with type **Integration**.
3. Install **Babyvoeding** and restart Home Assistant.

### Manual

Copy `custom_components/baby_feeding` into the `custom_components` folder of your Home Assistant configuration and restart.

## Configuration

Go to **Settings → Devices & services → Add integration → Babyvoeding**. Choose:

- **Phones for reminders** – the `notify.mobile_app_*` actions of the parents' phones.
- **Dashboard path** – the view the reminder and the lock-screen countdown open, for example `/dashboard-main/voeding`.

Both can be changed later under **Configure**. The default amount, the agreed maximum and the night interval are set on the card's settings tab.

## Dashboard card

```yaml
type: custom:baby-feeding-card
mode: main   # main, history, settings or timer
```

| Mode | Shows |
|---|---|
| `main` | Countdown, the bottle form, totals and the expected bottles for the next 24 hours |
| `history` | The diary per day, with editing |
| `settings` | Default amount, maximum and night interval |
| `timer` | Only the countdown, for a home view; add `navigation_path: /dashboard-main/voeding` to open the feeding view on tap |

## Entities

| Entity | Content |
|---|---|
| `sensor.volgende_voeding` | Timestamp of the next bottle |
| `sensor.volgende_fles` | Time of the next bottle as text, for widgets |
| `sensor.voeding_voortgang` | Progress towards the next bottle in % |
| `sensor.voeding_status` | Plan, open bottle, settings and last week's feeds, used by the card |
| `calendar.voedingsdagboek` | The diary as a read-only calendar |

## Actions

| Action | Purpose |
|---|---|
| `baby_feeding.save_bottle` | Save a bottle (`start`, `amount`); the next reminder counts from it. Up to 24 hours ahead. |
| `baby_feeding.add_earlier_feed` | Add a past feed without moving the reminder |
| `baby_feeding.update_feed` | Change the time or amount of a feed (`feed_id`, `start`, `amount`) |
| `baby_feeding.delete_feed` | Remove a feed (`feed_id`) |
| `baby_feeding.new_bottle` | Open a new bottle in the card |
| `baby_feeding.set_settings` | Default amount, maximum and night interval |
| `baby_feeding.import_calendar` | One-time import of feeds named like `70 cc` from an existing calendar, into an empty diary |

Refused changes return a clear message, for example a second feed in the same minute or a bottle more than 24 hours ahead.

## Privacy

Everything stays in your Home Assistant. The diary is stored in `.storage/baby_feeding`; notifications go only to the phones you select. The large card attributes are excluded from the recorder.

## Development

```bash
python -m pip install pytest-homeassistant-custom-component
python -m pytest
```

```bash
npm install
npm run test:card
```

The feeding rules live in plain Python (`schedule.py`, `planning.py`, `diary.py`, `display.py`) and are tested without Home Assistant; `test_integration.py` covers the integration in a running Home Assistant. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
