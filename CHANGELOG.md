# Changelog

## 0.2.0

- **Breaking:** entity IDs are English and fixed: `sensor.baby_feeding_next_feeding`, `sensor.baby_feeding_next_bottle`, `sensor.baby_feeding_progress`, `sensor.baby_feeding_status` and `calendar.baby_feeding_diary`. The status attributes are English too (`standard_amount`, `feeds`, …) and the status state is `open` or `saved`.
- The integration is called Baby Feeding. Entity names, reminders, lock-screen texts, widget texts and refusal messages are English with a Dutch translation, chosen by the Home Assistant language.
- The dashboard card is English with a Dutch translation, chosen by each user's language.
- Amounts are shown in ml (cc in Dutch); the import accepts both.
- Open-source README, MIT license, contributing guide, brand icon and CI for HACS, hassfest and tests.

## 0.1.0

- First version: feeding diary with its own storage and a read-only calendar, the day and night rhythm, one critical reminder per planned moment, bottles up to 24 hours ahead, widget sensors with `update_widgets`, a silent lock-screen countdown, the bundled dashboard card and a one-time calendar import.
