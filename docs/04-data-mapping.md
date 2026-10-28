# Маппинг данных: source → target

> Обезличенный пример. Названия систем, полей и правил заменены.
> Связанные артефакты: [ERD](../diagrams/rendered/05-data-model.png), [OpenAPI](03-api-specification.yaml), [требования](02-requirements.md).

---

## 1. Принципы

1. **Один источник истины.** Для каждой сущности определён владелец: договор и счёт — АБС, фактическая операция — касса/процессинг.
2. **Явные преобразования.** Любое изменение значения описано; «магия» на стороне кода не допускается.
3. **Валидация на входе.** Проверки выполняются до записи, а не после.
4. **Идемпотентность.** Повторная обработка того же сообщения не создаёт дубль.
5. **Трассируемость.** Для каждой строки маппинга есть требование и тест.

## 2. Соглашения

| Тип | Формат | Пример |
|---|---|---|
| Дата | ISO 8601, `YYYY-MM-DD` | `2026-10-29` |
| Дата-время | ISO 8601, UTC | `2026-10-29T12:30:00Z` |
| Сумма | decimal(18,2) | `12500.00` |
| Вес металла | decimal(18,6), граммы | `12.500000` |
| Валюта | ISO 4217 | `BYN` |
| Страна | ISO 3166-1 alpha-2 | `BY` |
| Идентификатор | UUID v4 | `6f1c2a9e-3b7d-4e21-9c5a-1a2b3c4d5e6f` |
| Телефон | E.164 | `+375 (XX) XXX-XX-XX` |

## 3. Маппинг сущностей

### 3.1. Клиент

| Source | Source field | Target | Target field | Тип | Преобразование | Валидация |
|---|---|---|---|---|---|---|
| front-office | `client.id` | CLIENT | `client_id` | uuid | trim, lower | обязателен, UUID |
| front-office | `client.type` | CLIENT | `client_type` | enum | справочник `CLIENT_TYPE` | `INDIVIDUAL / LEGAL` |
| front-office | `client.name` | CLIENT | `display_name` | string | trim, collapse spaces | 1–200 символов |
| front-office | `client.taxId` | CLIENT | `tax_id` | string | удалить пробелы и дефисы | 9–12 цифр, контрольная сумма |
| front-office | `client.country` | CLIENT | `country_code` | char(2) | upper | ISO 3166-1 alpha-2 |
| front-office | `client.status` | CLIENT | `status` | enum | справочник `CLIENT_STATUS` | `ACTIVE / BLOCKED / CLOSED` |

### 3.2. Договор

| Source | Source field | Target | Target field | Тип | Преобразование | Валидация |
|---|---|---|---|---|---|---|
| front-office | `contract.externalNumber` | CONTRACT | `external_number` | string | trim, upper | уникален, ≤ 64 символов |
| front-office | `contract.type` | CONTRACT | `contract_type` | enum | справочник `CONTRACT_TYPE` | `STORAGE / SAFE_DEPOSIT_BOX / METAL_ACCOUNT` |
| front-office | `contract.currency` | CONTRACT | `currency` | char(3) | upper | ISO 4217 |
| front-office | `contract.openDate` | CONTRACT | `open_date` | date | `yyyy-MM-dd` | не позже текущей даты |
| front-office | `contract.closeDate` | CONTRACT | `close_date` | date | `yyyy-MM-dd` | ≥ `open_date` |
| ABS | `contract.status` | CONTRACT | `status` | enum | mapping table | допустимый переход |

**Mapping статусов:**

| Source status | Target status | Комментарий |
|---|---|---|
| `DRAFT` | `DRAFT` | Черновик |
| `OPEN` | `OPEN` | Открыт, счёт создан |
| `ACTIVE` | `ACTIVE` | Активен |
| `SUSPENDED` | `SUSPENDED` | Арест / блокировка |
| `CLOSING` | `CLOSING` | Заявка на закрытие |
| `CLOSED` | `CLOSED` | Закрыт |
| `CANCELLED` | `CANCELLED` | Отменён |
| неизвестно | — | Ошибка `UNKNOWN_STATUS`, ручной разбор |

### 3.3. Счёт

| Source | Source field | Target | Target field | Тип | Преобразование | Валидация |
|---|---|---|---|---|---|---|
| ABS | `account.id` | ACCOUNT | `account_id` | uuid | — | UUID |
| ABS | `account.contractId` | ACCOUNT | `contract_id` | uuid | — | существует |
| ABS | `account.type` | ACCOUNT | `account_type` | enum | справочник | `STORAGE / METAL / COMMISSION / TRANSIT` |
| ABS | `account.number` | ACCOUNT | `account_number_mask` | string | маска по типу клиента | не хранить полный номер |
| ABS | `account.currency` | ACCOUNT | `currency` | char(3) | upper | ISO 4217 |
| ABS | `account.balance` | ACCOUNT | `balance` | decimal(18,2) | `ROUND_HALF_UP` | ≥ 0 для активного счёта |
| ABS | `account.status` | ACCOUNT | `status` | enum | mapping table | допустимый переход |

### 3.4. Операция с металлом

| Source | Source field | Target | Target field | Тип | Преобразование | Валидация |
|---|---|---|---|---|---|---|
| cash | `operation.externalId` | METAL_OPERATION | `external_id` | string | trim | уникален в рамках счёта |
| cash | `operation.type` | METAL_OPERATION | `operation_type` | enum | справочник | `DEPOSIT / WITHDRAWAL` |
| cash | `operation.metalCode` | METAL_OPERATION | `metal_code` | enum | upper | `XAU / XAG / XPT / XPD` |
| cash | `operation.weight` | METAL_OPERATION | `weight` | decimal(18,6) | `ROUND_HALF_UP` | > 0 |
| cash | `operation.amount` | METAL_OPERATION | `amount` | decimal(18,2) | `ROUND_HALF_UP` | ≥ 0 |
| processing | `operation.status` | METAL_OPERATION | `status` | enum | mapping table | допустимый переход |
| processing | `operation.confirmedAt` | METAL_OPERATION | `confirmed_at` | timestamp | ISO 8601 → UTC | не раньше `requested_at` |

**Mapping статусов операции:**

| Processing | Target | Действие |
|---|---|---|
| `PENDING` | `PENDING` | Продолжать polling |
| `CONFIRMED` | `CONFIRMED` | Провести по АБС, запустить сверку |
| `REJECTED` | `REJECTED` | Создать инцидент, уведомить |
| `CANCELLED` | `CANCELLED` | Завершить, уведомить |
| `TIMEOUT` | `MANUAL_REVIEW` | Ручной разбор |
| неизвестно | `MANUAL_REVIEW` | Инцидент |

### 3.5. Интеграционный ордер

| Source | Source field | Target | Target field | Тип | Преобразование | Валидация |
|---|---|---|---|---|---|---|
| integration bus | `request.id` | INTEGRATION_ORDER | `order_id` | uuid | — | UUID |
| integration bus | `request.operationId` | INTEGRATION_ORDER | `operation_id` | uuid | — | существует |
| integration bus | `request.target` | INTEGRATION_ORDER | `target_system` | enum | справочник | `ABS / CASH / PROCESSING` |
| integration bus | `request.idempotencyKey` | INTEGRATION_ORDER | `idempotency_key` | string | trim | 16–128 символов |
| integration bus | `request.status` | INTEGRATION_ORDER | `status` | enum | mapping table | `NEW / IN_PROGRESS / DONE / FAILED` |
| integration bus | `request.attempt` | INTEGRATION_ORDER | `attempt_count` | int | — | 0–5 |
| integration bus | `request.errorCode` | INTEGRATION_ORDER | `last_error_code` | string | — | ≤ 64 символов |

## 4. Правила сверки остатков

После подтверждения операции:

1. Запросить остаток в АБС.
2. Запросить остаток в кассовой системе.
3. Сравнить с точностью до 6 знаков для металла и 2 знаков для денег.
4. Если значения совпадают — операция считается успешной, инцидент не создаётся.
5. Если не совпадают:
   - создать инцидент с `operationId`, обоими значениями и разницей;
   - перевести операцию в `MANUAL_REVIEW`;
   - уведомить бэк-офис;
   - не закрывать договор до разрешения.

## 5. Обработка ошибок

| Ситуация | Код | Действие |
|---|---|---|
| Дубликат `Idempotency-Key` | `409 IDEMPOTENCY_CONFLICT` | Вернуть исходный результат, если payload совпадает |
| Дубликат с другим payload | `409 IDEMPOTENCY_PAYLOAD_MISMATCH` | Ошибка, ручной разбор |
| Неизвестный металл | `422 UNKNOWN_METAL_CODE` | Отклонить, вернуть справочник |
| Отрицательный вес | `422 INVALID_WEIGHT` | Отклонить |
| Остаток недостаточен | `409 INSUFFICIENT_BALANCE` | Отклонить, показать доступный остаток |
| Таймаут процессинга | `504 PROCESSING_TIMEOUT` | Retry / ручной разбор |
| Расхождение остатков | `409 BALANCE_MISMATCH` | Инцидент, ручной разбор |

## 6. SQL-проверки (примеры)

```sql
-- 1. Договоры, которые нельзя закрыть
SELECT c.contract_id, a.balance, a.status
FROM contract c
JOIN account a ON a.contract_id = c.contract_id
WHERE c.status = 'ACTIVE'
  AND (a.balance <> 0 OR a.status = 'BLOCKED');

-- 2. Операции без подтверждения дольше 15 минут
SELECT operation_id, status, requested_at
FROM metal_operation
WHERE status = 'PENDING'
  AND requested_at < now() - interval '15 minutes';

-- 3. Расхождения остатков по инцидентам
SELECT operation_id, abs(balance_abs - balance_cash) AS diff
FROM reconciliation
WHERE abs(balance_abs - balance_cash) > 0.000001
ORDER BY diff DESC;
```

## 7. Чек-лист маппинга

- [ ] Для каждого поля указан source и target.
- [ ] Тип и точность совпадают.
- [ ] Описаны преобразования и округления.
- [ ] Описаны значения по умолчанию.
- [ ] Описаны ошибки и реакции.
- [ ] Есть примеры «до / после».
- [ ] Есть SQL-проверка или автотест.
- [ ] Нет ПДн в логах и аналитике.
- [ ] Согласовано с владельцем данных.
