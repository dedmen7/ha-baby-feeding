# Contributing

Issues and pull requests are welcome.

## Before you open a pull request

1. Describe the behaviour you want to change in an issue first when it changes reminders or the feeding rhythm; parents rely on these.
2. Add or change a test that fails without your change. The rules in `schedule.py`, `planning.py`, `diary.py` and `display.py` have plain Python tests; the integration has tests in `tests/test_integration.py` and the card in `tests/card.test.mjs`.
3. Run the checks:

```bash
python -m pip install pytest-homeassistant-custom-component
python -m pytest
```

```bash
npm install
npm run test:card
```

## Translations

User-facing texts are Dutch. Service and setup texts are in `custom_components/baby_feeding/translations/`; the card texts are in `frontend/baby-feeding-card.js`. Translations that keep the Dutch behaviour unchanged are a good first contribution.
