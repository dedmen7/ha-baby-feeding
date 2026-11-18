"""Texts the integration sends to phones and widgets, in English with translations per Home Assistant language."""

TEXTS = {
    'en': {
        'not_planned': 'Not planned',
        'now': 'Now',
        'next_bottle': 'Next bottle',
        'bottle_due': 'Time for the bottle',
        'countdown': 'at {due} · {feed}',
        'last_bottle': 'last bottle {time}',
        'bottle_ahead': 'bottle at {time}',
        'reminder_title': 'Time for the bottle',
        'reminder_message': 'Fill in the amount drunk and tap Save.',
        'unit': 'ml',
    },
    'nl': {
        'not_planned': 'Niet gepland',
        'now': 'Nu',
        'next_bottle': 'Volgende fles',
        'bottle_due': 'Tijd voor de fles',
        'countdown': 'om {due} · {feed}',
        'last_bottle': 'laatste fles {time}',
        'bottle_ahead': 'fles om {time}',
        'reminder_title': 'Tijd voor de voeding',
        'reminder_message': 'Vul de gedronken hoeveelheid in en tik op Opslaan.',
        'unit': 'cc',
    },
}


def text(language: str, key: str, **values: str) -> str:
    table = TEXTS.get(language.split('-')[0].lower(), TEXTS['en'])
    return table[key].format(**values)
