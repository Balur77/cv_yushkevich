# Портфолио системного аналитика

**Банковские интеграции · требования · BPMN/UML · OpenAPI · UAT**

![BPMN 2.0](https://img.shields.io/badge/BPMN-2.0-2F5D8A?style=flat-square)
![UML](https://img.shields.io/badge/UML-use%20case%20%7C%20sequence%20%7C%20state-2F5D8A?style=flat-square)
![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-2F5D8A?style=flat-square)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL%20%7C%20Oracle-2F5D8A?style=flat-square)
![UAT](https://img.shields.io/badge/UAT-test%20scenarios-2F5D8A?style=flat-square)

---

## О репозитории

Это портфолио системного аналитика с опытом **2+ года** в банковских интеграционных проектах. Здесь собраны обезличенные артефакты, которые показывают полный цикл работы над требованием:

1. **Понять проблему** — контекст, стейкхолдеры, цели, ограничения.
2. **Описать процесс** — AS-IS/TO-BE, BPMN, use case, state machine.
3. **Спроектировать интеграцию** — REST/SOAP, OpenAPI, ошибки, идемпотентность, retry.
4. **Связать данные** — ERD, маппинг, правила сверки, SQL-проверки.
5. **Проверить и внедрить** — UAT, traceability, чек-листы релиза, runbook.

> **Важно:** все материалы переработаны. Названия банка, внутренних систем, API-пути, имена полей, идентификаторы и бизнес-правила заменены на обезличенные. В репозитории нет коммерческой тайны, персональных данных и реальных скриншотов. Подробнее — в [docs/11-sanitization.md](docs/11-sanitization.md).

---

## Кейс

**Договоры хранения ценностей и операции с драгоценными металлами**

Банковский процесс, в котором участвуют четыре системы и три канала обслуживания:

| Контур | Роль в процессе |
|---|---|
| Фронт-офис | Заявка, проверка документов, статусы для клиента |
| АБС | Договоры, счета, остатки, комиссии, выписки |
| Кассовая система | Приём и выдача ценностей, подтверждение операции |
| Процессинг | Асинхронная обработка операций с металлом, статусы, сверка |

**Моя роль:** системный аналитик end-to-end — от интервью и scope до API-контрактов, UAT и передачи в поддержку.

**Что было сложного:**
- несколько стейкхолдеров с разными представлениями о процессе;
- асинхронные ответы и расхождения остатков между системами;
- статусная модель договора, счёта и ордера с guard-условиями;
- требования к идемпотентности и безопасному повтору операций;
- необходимость выпустить MVP, не потеряв обязательные проверки.

**Результат:** согласованный сквозной процесс, 20+ REST-операций, прозрачные статусы и ошибки, UAT-сценарии, мониторинг и runbook для поддержки.

Подробный разбор — в [docs/01-case-study.md](docs/01-case-study.md).

---

## Что внутри

### 1. Процесс и сценарии

| Артефакт | Что показывает |
|---|---|
| [Процессный ландшафт](diagrams/rendered/01-process-contract-lifecycle.png) | Сквозной процесс по дорожкам: клиент → фронт-офис → АБС → касса |
| [Use case](diagrams/rendered/02-use-case.png) | Границы системы, акторы, include-связи |
| [State machine](diagrams/rendered/03-state-machine.png) | Статусы договора, переходы и guard-условия |
| [Sequence](diagrams/rendered/04-sequence-deposit.png) | Открытие договора, внесение металла, сверка, закрытие |
| [ERD](diagrams/rendered/05-data-model.png) | Логическая модель: клиент, договор, счёт, операция, ордер, комиссия, выписка |
| [Карта интеграций](diagrams/rendered/06-integration-map.png) | Системы, протоколы, синхронный и асинхронный контуры |

Исходники диаграмм — в [diagrams/](diagrams/): PlantUML `.puml` и отрендеренные `.svg` / `.png`.

### 2. Требования

| Артефакт | Что показывает |
|---|---|
| [BRD/FRD](docs/02-requirements.md) | Контекст, scope, стейкхолдеры, функциональные и нефункциональные требования, бизнес-правила |
| [Шаблон требований](docs/08-requirements-template.md) | Шаблон ТЗ, user story, acceptance criteria, definition of ready/done |
| [Матрица трассировки](docs/06-traceability-matrix.md) | Связь требование → use case → API → тест |
| [Глоссарий](docs/10-glossary.md) | Единый язык проекта |

### 3. API и данные

| Артефакт | Что показывает |
|---|---|
| [OpenAPI 3.0](docs/03-api-specification.yaml) | Контракты, схемы, ошибки, идемпотентность, коды ответов |
| [Маппинг данных](docs/04-data-mapping.md) | Source → target, преобразования, валидации, правила сверки |
| [Чек-лист ревью API](docs/07-api-review-checklist.md) | 40+ проверок контракта до разработки |

### 4. Тестирование и внедрение

| Артефакт | Что показывает |
|---|---|
| [UAT-сценарии](docs/05-test-scenarios.md) | Позитивные, негативные, граничные сценарии и проверки идемпотентности |
| [UAT-план](docs/09-uat-plan.md) | Роли, окружение, критерии входа/выхода, дефекты, sign-off |

---

## Стек

**Моделирование:** BPMN 2.0, UML (use case, sequence, activity, state machine), ERD, DFD, PlantUML, draw.io, Miro.

**Требования:** BRD/FRD, ТЗ, user stories, use cases, acceptance criteria, traceability matrix, backlog, change request.

**Интеграции:** REST, SOAP, OpenAPI 3.0, Swagger, Postman, JSON, XML, HTTP, идемпотентность, retry, timeout, circuit breaker, Problem Details.

**Данные:** SQL, PostgreSQL, Oracle, MS SQL, DBeaver, маппинг данных, сверка остатков, ERD.

**Процесс:** Jira, Confluence, GitLab, Scrum, Kanban, UAT, release checklist, runbook.

---

## Как читать репозиторий

Если у вас 10 минут:

1. [Кейс](docs/01-case-study.md) — контекст и результат.
2. [Карта интеграций](diagrams/rendered/06-integration-map.png) — как устроен ландшафт.
3. [OpenAPI](docs/03-api-specification.yaml) — качество контрактов.
4. [UAT-сценарии](docs/05-test-scenarios.md) — как проверялись требования.

Если вы готовите техническое интервью:

- [Требования](docs/02-requirements.md) → [Трассировка](docs/06-traceability-matrix.md) → [Тесты](docs/05-test-scenarios.md) — сквозная логика.
- [State machine](diagrams/rendered/03-state-machine.png) — guard-условия и исключения.
- [Чек-лист ревью API](docs/07-api-review-checklist.md) — системность проверки контракта.
- [Гайд по интервью](docs/12-interview-guide.md) — как рассказывать кейс, типовые вопросы и разбор ответов.

---

## Обезличивание

Перед публикацией удалены или заменены:

- название банка и работодателя;
- названия внутренних систем и модулей;
- реальные API-пути, имена полей и статусы;
- номера счетов, идентификаторы, GUID, номера договоров;
- персональные данные клиентов и сотрудников;
- коммерческие правила, лимиты, тарифы и внутренние коды;
- скриншоты продукта.

Диаграммы **перерисованы с нуля** по мотивам рабочих кейсов, а не отрендерены из внутренних систем. Это безопаснее и показывает ход мышления, а не копию экрана.

Проверка перед публикацией:

```powershell
python scripts/scan_sensitive.py
```

Скрипт ищет запрещённые термины, реальные контакты и названия систем. Подробнее — [docs/11-sanitization.md](docs/11-sanitization.md).

---

## Локальный запуск

### Диаграммы

Нужны Java 11+ и PlantUML. Скрипт сам скачает `plantuml.jar` в `%TEMP%`, если его нет:

```powershell
.\scripts\build-diagrams.ps1
```

Либо вручную:

```powershell
java -jar plantuml.jar -charset UTF-8 -tsvg -o diagrams/rendered diagrams/*.puml
java -jar plantuml.jar -charset UTF-8 -tpng -Sdpi=200 -o diagrams/rendered diagrams/*.puml
```

### Проверка OpenAPI

```powershell
python -c "import yaml, json; yaml.safe_load(open('docs/03-api-specification.yaml', encoding='utf-8')); print('YAML OK')"
```

---

## Контакты

- GitHub: [github.com/yushkevich-sa](https://github.com/yushkevich-sa)
- Email: [yv10082006@gmail.com](mailto:yv10082006@gmail.com)

Открыт к роли **Middle системного аналитика** в банковском или финтех-проекте. Готов к техническому интервью и тестовому заданию.

---

## Лицензия

Код и шаблоны — [MIT](LICENSE). Документы и диаграммы — CC BY 4.0: можно использовать с указанием авторства. Материалы не содержат коммерческой тайны и предоставляются «как есть» в образовательных целях.
