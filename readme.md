# TeamFinder — Вариант 1: Управление проектами и участниками

## Для ревьюера: как запустить проект

### 1. Клонировать и войти в папку
```bash
git clone <repo-url>
cd team-finder
```
### 2. Создать `.env`
```bash
cp .env_example .env
```
Заполнить `.env` (важно: `TASK_VERSION=1`):
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
TASK_VERSION=1
```
### 3. Запустить базу данных
```bash
docker compose up -d
```
# TeamFinder — Вариант 2: Навыки пользователей + фильтрация

## Для ревьюера: как запустить проект

### 1. Клонировать и войти в папку
```bash
git clone <repo-url>
cd team-finder
```

### 2. Создать `.env`
```bash
cp .env_example .env
```
Заполнить `.env` (важно: `TASK_VERSION=2`):
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
TASK_VERSION=2
```

### 3. Запустить базу данных
```bash
docker compose up -d
```

### 4. Виртуальное окружение и зависимости
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 5. Миграции и тестовые данные
```bash
python manage.py migrate
python manage.py create_test_data   # создаёт 3 пользователей + 3 проекта
python manage.py createsuperuser    # опционально
```
# TeamFinder — Вариант 2: Навыки пользователей + фильтрация

## Для ревьюера: как запустить проект

### 1. Клонировать и войти в папку
```bash
git clone <repo-url>
cd team-finder
```

### 2. Создать `.env`
```bash
cp .env_example .env
```
Заполнить `.env` (важно: `TASK_VERSION=2`):
```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
TASK_VERSION=2
```

### 3. Запустить базу данных
```bash
docker compose up -d
```

### 4. Виртуальное окружение и зависимости
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 5. Миграции и тестовые данные
```bash
python manage.py migrate
python manage.py create_test_data   # создаёт 3 пользователей + 3 проекта
python manage.py createsuperuser    # опционально
```

### 6. Запуск
```bash
python manage.py runserver
```

Открыть: http://localhost:8000

---

## Тестовые аккаунты

| Email | Пароль | О себе                     |
|---|---|----------------------------|
| dmitry@example.com | TestPass123! | Backend-разработчик, люблю Django и PostgreSQL |
| anna@example.com | TestPass123! | Frontend-разработчик, React & Vue     |
| maxim@example.com | TestPass123! | DevOps & Python энтузиаст            |

---

## Структура приложений

```
users/       — кастомная модель User, модель Skill, регистрация/вход/профиль
projects/    — модель Project, CRUD проектов, участие
```

## Реализованный функционал (Вариант 1)

### 🔐 Система авторизации и профили
- **Регистрация:** Форма с полями Имя, Фамилия, Email (уникальный), Пароль.
- **Вход/Выход:** Авторизация по Email и паролю.
- **Личный кабинет:** Страница профиля с отображением аватара, контактов (GitHub, телефон) и списка проектов пользователя.
- **Редактирование профиля:** Возможность менять личные данные и загружать **аватар**.
  - *Фишка:* Мгновенное превью картинки (JS FileReader) перед сохранением.
- **Смена пароля:** Безопасная смена пароля с проверкой старого пароля.
- **Кастомная модель User:** Поле `email` используется как уникальный идентификатор для входа (`USERNAME_FIELD = 'email'`).

###  Управление проектами
- **Список проектов:** Главная страница с пагинацией (12 проектов на страницу).
- **Создание и редактирование:** Полноценные формы Django с валидацией данных.
- **Статусы:** Проекты могут быть «Открыты» или «Закрыты».
- **Завершение проекта:** Только автор может изменить статус на «Закрыт» (через AJAX без перезагрузки).

### 🤝 Командное взаимодействие
- **Участие в проектах:**
  - Пользователь может нажать «Участвовать» (кнопка меняется на «Отказаться» без перезагрузки).
  - Автор проекта **автоматически** становится первым участником при создании.
  - Список участников отображается на странице проекта с ролями (Автор / Участник).
- **Избранное:**
  - Любой авторизованный пользователь может добавить проект в «Избранное» (AJAX-сердечко).
  - Отдельная страница `/projects/favorites/` со списком сохраненных проектов.

### 🎨 Интерфейс и UX
- **Обработка ошибок:** Вывод ошибок форм валидации, сообщения 404, защита страниц авторизацией (`@login_required`).
- **Уведомления:** Визуальное подтверждение действий (смена состояния кнопок).


## Валидация форм
- Телефон: `8XXXXXXXXXX` или `+7XXXXXXXXXX`, сохраняется в формате `+7...`, уникальный
- GitHub URL: обязательно ведёт на `github.com`
- Email уникален