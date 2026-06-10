# Test Task API — Система разграничения прав доступа

## База данных
Используется SQLite (файл `test_task.db`). При необходимости легко меняется на PostgreSQL.

## Модели

### User
- `id` — Primary Key
- `name`, `surname` — обязательные поля
- `secondname` — необязательное (может отсутствовать)
- `email` — уникальный, обязательный
- `password` — хранится в виде bcrypt-хэша
- `role_id` — FK → roles.id
- `is_active` — boolean, default=True. При мягком удалении ставится False.

### Role
- `id` — Primary Key
- `name` — уникальное название роли (admin, user и т.д.)
- Связь: один ко многим с User и Permission

### Permission
- `id` — Primary Key
- `resource` — имя ресурса (например `items`, `users`, `permissions`)
- `action` — действие (`read`, `write`, `delete`)
- `role_id` — FK → roles.id
- Одна запись = одно право для одной роли на один ресурс + действие

## Схема разграничения доступа

Система построена на основе Role-Based Access Control 

### Правила проверки доступа

1. **Аутентификация**: пользователь передаёт JWT-токен в заголовке `Authorization: Bearer <token>`.
   - Если токен отсутствует или невалиден → **401 Unauthorized**
   - Если пользователь найден, но `is_active=False` → **401 Unauthorized**

2. **Авторизация**: проверяется, есть ли у роли пользователя запись в таблице `permissions` для запрашиваемого ресурса и действия.
   - Если права нет → **403 Forbidden**

3. **Роль администратора**: пользователь с ролью `admin` имеет полный доступ ко всем ресурсам (см. seed-данные).

### Таблица прав (seed-данные)

| Роль  | Ресурс       | Действие |
|-------|-------------|----------|
| admin | items       | read     |
| admin | items       | write    |
| admin | items       | delete   |
| admin | users       | read     |
| admin | users       | write    |
| admin | permissions | read     |
| admin | permissions | write    |
| user  | items       | read     |

Таким образом:
- **admin** может читать, создавать, изменять и удалять items; читать и редактировать пользователей; управлять правами доступа.
- **user** может только читать items.

### API управления правами (только admin)

- `GET    /admin/permissions` — получить все права
- `POST   /admin/permissions` — создать новое право
- `PUT    /admin/permissions/{id}` — обновить право
- `DELETE /admin/permissions/{id}` — удалить право

## Тестовые пользователи 

| Email           | Пароль    | Роль  |
|-----------------|-----------|-------|
| admin@test.ru   | 12345678  | admin |
| user@test.ru    | 12345678  | user  |

## API Endpoints

### Auth
- `POST /auth/register` — регистрация (имя, фамилия, отчество, email, пароль, role_id)
- `POST /auth/login` — логин, возвращает JWT
- `POST /auth/logout` — логаут (заглушка)

### Users
- `GET  /users/me` — текущий пользователь
- `PUT  /users/me` — обновление профиля
- `DELETE /users/me` — мягкое удаление (is_active=False)

### Items (Mock)
- `GET /items` — список объектов (admin видит все, user — только свои)
- `GET /items/{id}` — конкретный объект (с проверкой прав)

## Запуск

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Swagger-документация: http://localhost:8000/docs