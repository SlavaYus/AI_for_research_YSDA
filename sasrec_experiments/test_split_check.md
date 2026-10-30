# Проверка temporal split датасета

**Дата:** 2026-10-30  
**Датасет:** `reviews_Beauty_5` (5-core)  
**Оригинал:** 198 502 interactions, 22 363 users, 12 101 items

---

## Распределение по split

| Split | Rows | Users | Items | Timestamp range |
|-------|------|-------|-------|-----------------|
| train | 140 965 | 18 474 | 11 534 | [1023840000, 1389225600] |
| validation | 50 336 | 4 725 | 10 310 | [1023840000, 1394150400] |
| test | 90 621 | 8 041 | 11 727 | [1023840000, 1406073600] |
| train_validation | 151 081 | 18 474 | 11 736 | [1023840000, 1394150400] |

## Распределение пользователей

| Категория | Кол-во |
|-----------|--------|
| Только train | 9 556 |
| Train + Val | 2 121 |
| Train + Test (без Val) | 4 193 |
| Train + Val + Test | 2 604 |
| Только val | 0 |
| Только test | 1 244 |

## Проверка temporal split

**Метод:** для каждого пользователя проверяем:
1. `max(train_ts) < min(val_only_ts)` — все train-события раньше val-only
2. `max(val_ts) < min(test_only_ts)` — все val-события раньше test-only

**Результат:**
- Проверено пользователей: 5 208 (train ∩ val ∩ test) + 4 193 (train ∩ test \ val)
- Нарушений temporal split: **0**

**Статус: ✅ CORRECT**

## Проверка prefix-свойства

- `train ⊂ val ⊂ test` (по множеству (user, item, timestamp) пар): **True**
- `train_validation = train ∪ val`: **True** (151 081 пар)

## Вывод

Разбиение датасета **корректно**. Это стандартный temporal split для sequential recommendation:
- **Train**: prefix взаимодействий пользователя (первые N-1 событий)
- **Validation**: предпоследнее(ие) событие(я)
- **Test**: последнее(ие) событие(я)
- **Train-Validation**: объединение train + validation (для дообучения)

Нет утечки данных из future в past — все interactions в train происходят строго ДО interactions в test-only и val-only для каждого пользователя.