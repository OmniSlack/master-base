# Session Tracker · KOMPAS / MasterBase

Включен на 07.11.2026 по „да, включи тракера“ от Мартин.

## Какво е
Един дневник на всички чатове и агенти. Един ред на събитие, подредени по час.
Общият ключ е часът (UTC).

- `sessions.jsonl` е оригиналът: един JSON обект на ред. Само се добавя, нищо не се трие и не се пренаписва.
- `sessions.txt` е версия за четене с очи. Прави се от `sessions.jsonl` с `tracker.py render`.
- `tracker.py` добавя ред, проверява файла и прави TXT версията. Без външни библиотеки.

## Кой пише
Пише само един: Архиварят. Докато Архиварят не е пуснат, пише 🧭 00 · ТИХИЯТ.
Всички останали само четат.

## Полета
| Поле | Задължително | Какво е |
|---|---|---|
| `ts` | да | час в UTC, `2026-11-07T13:05:01Z` |
| `ts_precision` | не | `exact` (по подразбиране) или `approx` |
| `session` | да | ID на сесията или `-`, ако събитието не е за сесия |
| `title` | да | име на чата |
| `device` | да | `cloud`, `DESKTOP-70S3JM9` (настолен), `DESKTOP-GD5FDMT` (лаптоп), `phone` или `UNKNOWN` |
| `kind` | да | виж долу |
| `evidence` | да | откъде го знаем |
| `status` | да | `VERIFIED`, `REPORTED`, `PROPOSED` или `UNKNOWN` |
| `note` | не | кратка бележка |
| `by` | да | кой е записал реда |

Видове (`kind`): `start`, `restart`, `compact`, `conn_lost`, `limit`, `crash`, `archived`, `renamed`, `message`, `trust`, `observation`, `handoff`.

## Правила
- Нищо не се трие. Грешен ред се поправя с нов ред с `kind: observation` и бележка какво поправя.
- `VERIFIED` е само това, което записващият е видял сам. Чуждото е `REPORTED`.
- Час, който не е точен, носи `ts_precision: approx`.

## Команди
```
python -I tracker/tracker.py check
python -I tracker/tracker.py render
python -I tracker/tracker.py add '{"ts":"...","session":"...","title":"...","device":"cloud","kind":"observation","evidence":"...","status":"VERIFIED","by":"00 ТИХИЯТ"}'
```
