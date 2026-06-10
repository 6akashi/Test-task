from fastapi import FastAPI
from app.database import engine, Base, SessionLocal
from app.models import Role, User, Permission
from app.routers import auth, users, admin, items

# Создаём таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Test Task API", version="1.0.0")

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(items.router)


def seed_data():
    """Заполняет БД тестовыми данными: роли, права, пользователи."""
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже роли
        existing_roles = db.query(Role).count()
        if existing_roles > 0:
            return  # Уже заполнено

        # Создаём роли
        admin_role = Role(name="admin")
        user_role = Role(name="user")
        db.add(admin_role)
        db.add(user_role)
        db.commit()
        db.refresh(admin_role)
        db.refresh(user_role)

        # Создаём права (permissions) для админа — полный доступ ко всему
        admin_permissions = [
            Permission(resource="items", action="read", role_id=admin_role.id),
            Permission(resource="items", action="write",
                       role_id=admin_role.id),
            Permission(resource="items", action="delete",
                       role_id=admin_role.id),
            Permission(resource="users", action="read", role_id=admin_role.id),
            Permission(resource="users", action="write",
                       role_id=admin_role.id),
            Permission(resource="permissions",
                       action="read", role_id=admin_role.id),
            Permission(resource="permissions",
                       action="write", role_id=admin_role.id),
        ]
        for perm in admin_permissions:
            db.add(perm)

        # Создаём права для обычного пользователя — только чтение items
        user_permissions = [
            Permission(resource="items", action="read", role_id=user_role.id),
        ]
        for perm in user_permissions:
            db.add(perm)

        db.commit()

        # Создаём тестовых пользователей
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        admin_user = User(
            name="Иван",
            surname="Админов",
            secondname="Иванович",
            email="admin@test.ru",
            password=pwd_context.hash("12345678"),
            role_id=admin_role.id,
            is_active=True,
        )
        regular_user = User(
            name="Пётр",
            surname="Пользователев",
            secondname=None,
            email="user@test.ru",
            password=pwd_context.hash("12345678"),
            role_id=user_role.id,
            is_active=True,
        )
        db.add(admin_user)
        db.add(regular_user)
        db.commit()

        print("Тестовые данные успешно добавлены:")
        print(f"admin@test.ru / 12345678 (admin)")
        print(f"user@test.ru / 12345678 (user)")

    finally:
        db.close()


@app.on_event("startup")
def startup():
    seed_data()


@app.get("/")
def root():
    return {"message": "Test Task API работает", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
