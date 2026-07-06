# Технічне завдання

## Сайт медичної клініки TEN clinic

| Параметр | Значення |
|----------|----------|
| **Версія документа** | 1.0 |
| **Дата** | 30.06.2026 |
| **Замовник** | TEN clinic — Medicine & Surgery |
| **Мова інтерфейсу** | Українська |
| **Технологічний стек** | Django + Python |

---

## Зміст

1. [Загальні положення](#1-загальні-положення)
2. [Цілі та задачі](#2-цілі-та-задачі)
3. [Цільова аудиторія](#3-цільова-аудиторія)
4. [Фірмовий стиль](#4-фірмовий-стиль)
5. [Структура сайту](#5-структура-сайту)
6. [Опис сторінок і блоків](#6-опис-сторінок-і-блоків)
7. [Функціональні вимоги](#7-функціональні-вимоги)
8. [Моделі даних](#8-моделі-даних)
9. [Нефункціональні вимоги](#9-нефункціональні-вимоги)
10. [Технічна архітектура](#10-технічна-архітектура)
11. [UI/UX вимоги](#11-uiux-вимоги)
12. [Контент від замовника](#12-контент-від-замовника)
13. [Етапи розробки](#13-етапи-розробки)
14. [Критерії приймання](#14-критерії-приймання)
15. [Поза scope (фаза 2)](#15-поза-scope-фаза-2)

---

## 1. Загальні положення

### 1.1. Призначення документа

Цей документ визначає вимоги до розробки офіційного веб-сайту медичної клініки **TEN clinic** (Medicine & Surgery). ТЗ призначене для розробників, дизайнерів, тестувальників та замовника.

### 1.2. Призначення сайту

Сайт має:

- лаконічно розповісти про медичну клініку та її напрямки діяльності;
- представити лікарів, послуги та прайс;
- надати контактну інформацію, графік роботи та схему проїзду;
- забезпечити можливість **онлайн-запису** через форму заявки на сайті.

### 1.3. Очікуваний результат

Повнофункціональний адаптивний веб-сайт на Django з адмін-панеллю для самостійного управління контентом. Заявки на запис надходять адміністратору через Django Admin, email та (опційно) Telegram.

### 1.4. Глосарій

| Термін | Визначення |
|--------|------------|
| **CTA** | Call-to-Action — кнопка або посилання, що спонукає до дії (наприклад, «Записатися») |
| **CRUD** | Create, Read, Update, Delete — базові операції з даними |
| **ПД** | Персональні дані пацієнта |
| **Admin** | Django Admin — панель управління контентом сайту |
| **Slug** | URL-friendly ідентифікатор сторінки (наприклад, `hirurgiya`) |

---

## 2. Цілі та задачі

### 2.1. Бізнес-цілі

- Підвищити обізнаність про клініку в цільовій аудиторії.
- Спростити процес запису на прийом без дзвінка в клініку.
- Сформувати професійний, довірливий digital-образ бренду TEN clinic.

### 2.2. Задачі сайту

| № | Задача | Розділ сайту |
|---|--------|--------------|
| 1 | Інформування про клініку | Головна |
| 2 | Представлення медичних напрямків | Напрямки |
| 3 | Представлення команди лікарів | Лікарі |
| 4 | Каталог медичних послуг | Послуги |
| 5 | Прозоре ціноутворення | Прайс |
| 6 | Контакти, графік, схема проїзду | Контакти |
| 7 | Онлайн-запис на прийом | Онлайн-запис |

### 2.3. Обмеження першої версії

- Запис реалізується як **форма заявки** (без вибору вільного слоту з календарем).
- Підтвердження запису здійснює адміністратор клініки вручну (телефоном або email).
- Інтеграція з зовнішніми медичними платформами (Helsi, Doc.ua) — поза scope v1.

---

## 3. Цільова аудиторія

### 3.1. Основна аудиторія

- Дорослі пацієнти (25–65 років), що шукають медичні послуги в регіоні.
- Родичі пацієнтів, які допомагають з пошуком клініки та записом.

### 3.2. Очікування користувачів

- Швидке розуміння, чим займається клініка.
- Довіра до бренду (професійний дизайн, реальні лікарі, прозорий прайс).
- Зручний запис з мобільного телефону.
- Актуальні контакти та графік роботи.

### 3.3. Сценарії використання

1. **Пошук клініки** → перегляд головної → перегляд напрямків → запис.
2. **Пошук конкретного лікаря** → сторінка лікаря → запис до цього лікаря.
3. **Перевірка ціни** → прайс → запис на послугу.
4. **Потрібна адреса** → контакти → карта / схема проїзду.

---

## 4. Фірмовий стиль

### 4.1. Кольорова палітра

Референс: `assets/IMAGE_2026-06-30_11_02_04-2fafcddc-0dc6-402d-ba2f-7bfb53cd24b4.png`

| Назва | HEX | CSS-змінна | Роль на сайті |
|-------|-----|------------|---------------|
| **Deep Navy** | `#1F4A73` | `--color-navy` | Header, footer, заголовки H1–H2, primary-кнопки |
| **Sage Teal** | `#8AAFA8` | `--color-sage` | Акценти, посилання, secondary-кнопки, іконки |
| **Warm Ivory** | `#F4F0EB` | `--color-ivory` | Основний фон сторінок |
| **Graphite** | `#3F4954` | `--color-graphite` | Основний текст, підзаголовки |
| **Light Accent** | `#DDE7E3` | `--color-accent-light` | Фони секцій, hover-стани, розділювачі, card-background |

#### Правила використання кольорів

- Фон сторінки — Warm Ivory; не використовувати чистий білий `#FFFFFF` як основний фон.
- Текст на світлому фоні — Graphite; заголовки — Deep Navy.
- Primary CTA-кнопки — Deep Navy з білим текстом; hover — затемнення navy на 10%.
- Посилання та акценти — Sage Teal; hover — затемнення sage.
- Контраст тексту відповідає WCAG AA (мінімум 4.5:1 для body-тексту).

### 4.2. Логотип

Референс: `assets/IMAGE_2026-06-30_11_02_10-624ddfde-096f-412c-aa60-6d478bd265f8.png`

#### Композиція логотипу

| Елемент | Опис |
|---------|------|
| **TEN** | Великі sans-serif літери. Літера **E** стилізована як три горизонтальні риски: верхня та нижня — Deep Navy, середня — Sage Teal |
| **clinic** | Напис курсивом/script під «TEN», колір Sage Teal |
| **Розділювач** | Тонка горизонтальна лінія Sage Teal |
| **MEDICINE & SURGERY** | Uppercase sans-serif, Sage Teal, з letter-spacing |

#### Вимоги до web-версії логотипу

- Формати: SVG (пріоритет), PNG (fallback, @2x для Retina).
- Favicon: спрощена версія (літери TEN або символ E з трьох рисок).
- Alt-текст: `TEN clinic — Medicine & Surgery`.
- Мінімальна ширина на сайті: 120px (mobile), 160px (desktop).
- Зона безпеки: відступ не менше 16px від країв контейнера.

### 4.3. Типографіка

| Роль | Шрифт (рекомендація) | Розмір (desktop) | Розмір (mobile) |
|------|----------------------|------------------|-----------------|
| H1 | Manrope / Inter, 700 | 40–48px | 28–32px |
| H2 | Manrope / Inter, 600 | 32–36px | 24–28px |
| H3 | Manrope / Inter, 600 | 24px | 20px |
| Body | Manrope / Inter, 400 | 16–18px | 16px |
| Caption | Manrope / Inter, 400 | 14px | 14px |
| Brand accent «clinic» | Script-шрифт (лише в логотипі) | — | — |

- Script-шрифт використовується **виключно** в логотипі, не для body-тексту.
- Line-height для body: 1.6.
- Максимальна ширина текстового блоку: 720px.

### 4.4. Візуальний стиль

- Мінімалістичний, медичний, професійний.
- Багато «повітря» (whitespace), чітка сітка.
- Фото лікарів — реальні, однаковий стиль обробки (світлий нейтральний фон).
- Іконки — line-style, колір Sage Teal або Graphite.
- Тіні — м'які, `box-shadow` з низькою opacity; без агресивних 3D-ефектів.

---

## 5. Структура сайту

### 5.1. Карта сайту

```
/                          — Головна
/directions/               — Напрямки (список)
/directions/<slug>/        — Детальна сторінка напрямку
/doctors/                  — Лікарі (список)
/doctors/<slug>/           — Детальна сторінка лікаря
/services/                 — Послуги (список)
/services/<slug>/          — Детальна сторінка послуги
/price/                    — Прайс
/contacts/                 — Контакти
/booking/                  — Онлайн-запис
/privacy/                  — Політика конфіденційності
```

### 5.2. Основна навігація (header)

```
[Логотип]  Головна | Напрямки | Лікарі | Послуги | Прайс | Контакти  [Записатися]
```

- Кнопка **«Записатися»** — primary CTA, Deep Navy, завжди видима.
- На mobile — burger-меню + sticky CTA (bottom bar або FAB).

### 5.3. Footer

- Логотип (скорочений або повний).
- Дублювання навігації.
- Контакти: адреса, телефон, email.
- Скорочений графік роботи.
- Посилання на політику конфіденційності.
- © TEN clinic, рік.

---

## 6. Опис сторінок і блоків

### 6.1. Головна (`/`)

| Блок | Опис | Пріоритет |
|------|------|-----------|
| **Hero** | Логотип або слоган, короткий текст про клініку (2–3 речення), CTA «Записатися» | Високий |
| **Про клініку** | 1 абзац + 3–4 ключові переваги (іконка + текст) | Високий |
| **Напрямки** | 4–6 карток з назвою та коротким описом; посилання на `/directions/` | Високий |
| **Лікарі** | 3–6 карток (фото, ПІБ, спеціалізація); посилання на `/doctors/` | Середній |
| **CTA-блок** | «Запишіться на прийом онлайн» + кнопка | Високий |
| **Контакти (скорочено)** | Адреса, телефон, графік (сьогодні) | Середній |
| **Карта (превʼю)** | Embed карти з посиланням «Детальніше → Контакти» | Низький |

### 6.2. Напрямки (`/directions/`)

**Список:**

- Grid карток: назва, короткий опис (до 150 символів), іконка/зображення.
- Сортування за полем `order` (з admin).

**Детальна сторінка (`/directions/<slug>/`):**

- Назва напрямку (H1).
- Повний опис.
- Список повʼязаних послуг (посилання).
- Список лікарів цього напрямку (картки).
- CTA «Записатися на прийом».

### 6.3. Лікарі (`/doctors/`)

**Список:**

- Grid карток: фото, ПІБ, спеціалізація, напрямок, стаж.
- Фільтр за напрямком (опційно).

**Детальна сторінка (`/doctors/<slug>/`):**

- Фото (велике), ПІБ (H1), спеціалізація.
- Біографія, освіта, досвід.
- Список послуг, які надає лікар.
- CTA «Записатися до лікаря» (форма з pre-fill лікаря).

### 6.4. Послуги (`/services/`)

**Список:**

- Групування за напрямками (accordion або секції).
- Кожна послуга: назва, короткий опис, ціна (або «за прайсом»).

**Детальна сторінка (`/services/<slug>/`):**

- Назва (H1), напрямок (breadcrumb).
- Повний опис процедури.
- Тривалість (якщо є).
- Ціна.
- Лікарі, що надають послугу.
- CTA «Записатися».

### 6.5. Прайс (`/price/`)

- Таблиця або accordion: **Послуга — Ціна**.
- Групування за напрямками.
- Фільтр/пошук за назвою послуги.
- Примітка: «Ціни актуальні на [дата]. Уточнюйте у адміністратора.»
- CTA «Записатися» внизу сторінки.

### 6.6. Контакти (`/contacts/`)

| Блок | Зміст |
|------|-------|
| **Адреса** | Повна адреса клініки |
| **Телефони** | Кlik-to-call на mobile (`tel:`) |
| **Email** | `mailto:` посилання |
| **Месенджери** | Telegram, Viber (опційно) — іконки з посиланнями |
| **Графік роботи** | Таблиця по днях тижня (Пн–Нд, час відкриття/закриття) |
| **Схема проїзду** | Embed Google Maps / OpenStreetMap + текстова інструкція (громадський транспорт, парковка) |
| **Форма зворотного звʼязку** | Опційно: імʼя, телефон, повідомлення |

#### Графік роботи — формат відображення

```
Понеділок:    09:00 – 18:00
Вівторок:     09:00 – 18:00
...
Неділя:       Вихідний
```

- Поточний день виділяється візуально.
- Якщо сьогодні вихідний — відображати «Сьогодні не працюємо».

#### Схема проїзду — вимоги

- Інтерактивна карта (iframe embed).
- Кнопка «Прокласти маршрут» (посилання на Google Maps).
- Текстовий опис: як дістатися автомобілем та громадським транспортом.
- Інформація про парковку (якщо є).

### 6.7. Онлайн-запис (`/booking/`)

#### Поля форми

| Поле | Тип | Обовʼязкове | Валідація |
|------|-----|-------------|-----------|
| ПІБ | text | Так | Мін. 2 символи, кирилиця/латиниця |
| Телефон | tel | Так | Формат +380XXXXXXXXX або (0XX) XXX-XX-XX |
| Email | email | Ні | Стандартна email-валідація |
| Напрямок | select | Так | З БД (активні напрямки) |
| Послуга | select | Так | Залежить від напрямку (cascade) |
| Лікар | select | Ні | Фільтр за напрямком/послугою |
| Бажана дата | date | Так | Не раніше сьогодні |
| Бажаний час | select/text | Ні | Опційно: ранок / день / вечір |
| Коментар | textarea | Ні | Max 500 символів |
| Згода на обробку ПД | checkbox | Так | Посилання на `/privacy/` |

#### Поведінка форми

1. Client-side валідація (HTML5 + JS).
2. Server-side валідація (Django forms).
3. Honeypot-поле (приховане) для захисту від ботів.
4. Rate limit: не більше 3 заявок з одного IP за 10 хвилин.
5. CSRF-захист (Django middleware).
6. Після успішної відправки — redirect на success-сторінку або inline-повідомлення.
7. Заявка зберігається в БД + email/Telegram адміну.
8. Опційно: email-підтвердження пацієнту («Ми отримали вашу заявку»).

#### Pre-fill з інших сторінок

- Зі сторінки лікаря: `?doctor=<slug>`
- Зі сторінки послуги: `?service=<slug>`
- Зі сторінки напрямку: `?direction=<slug>`

---

## 7. Функціональні вимоги

### 7.1. Публічна частина

| ID | Вимога | Пріоритет |
|----|--------|-------------|
| F-01 | Відображення всіх сторінок з розділу 6 | Must |
| F-02 | Адаптивна верстка: desktop (≥1200px), tablet (768–1199px), mobile (<768px) | Must |
| F-03 | Коректна робота в iOS Safari (safe-area-inset, viewport-fit=cover, touch targets ≥44px) | Must |
| F-04 | Форма онлайн-запису з валідацією | Must |
| F-05 | SEO: унікальні title/description на кожній сторінці | Must |
| F-06 | Open Graph meta-теги для соцмереж | Should |
| F-07 | Schema.org розмітка: `MedicalClinic`, `Physician`, `MedicalProcedure` | Should |
| F-08 | Breadcrumbs на внутрішніх сторінках | Should |
| F-09 | 404 та 500 custom-сторінки в стилі бренду | Should |
| F-10 | Lazy loading зображень | Should |

### 7.2. Django Admin

| ID | Вимога | Пріоритет |
|----|--------|-------------|
| A-01 | CRUD для напрямків, лікарів, послуг | Must |
| A-02 | Управління цінами (поле price на Service або окрема модель) | Must |
| A-03 | Управління графіком роботи | Must |
| A-04 | Управління контактною інформацією | Must |
| A-05 | Перегляд та управління заявками на запис | Must |
| A-06 | Завантаження фото лікарів та зображень | Must |
| A-07 | Завантаження/заміна логотипу | Should |
| A-08 | Статуси заявок: Нова → В обробці → Підтверджена / Відхилена | Must |
| A-09 | Налаштування email/Telegram для сповіщень (SiteSettings) | Must |
| A-10 | Сортування елементів (поле order, drag-and-drop — опційно) | Should |

### 7.3. Сповіщення про нові заявки

#### Email

- Отримувач: email з SiteSettings.
- Тема: `[TEN clinic] Нова заявка на запис — {ПІБ}`.
- Тіло: всі поля форми + дата створення + посилання на заявку в Admin.
- Відправка через Django `send_mail` + SMTP (налаштування в `.env`).

#### Telegram (опційно)

- Telegram Bot API.
- Повідомлення в чат/групу адміністратора.
- Формат: structured text з emoji-маркерами (без надмірностей).
- Token та chat_id — в `.env`, не в коді.

### 7.4. Захист від спаму та безпека форм

- Honeypot-поле (приховане CSS, не `display:none` для accessibility bots).
- CSRF-токен на всіх POST-формах.
- Rate limiting по IP.
- Server-side sanitization введених даних.
- Не логувати повні номери телефонів у production-логах.

---

## 8. Моделі даних

### 8.1. Direction (Напрямок)

```python
class Direction(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='directions/', blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
```

### 8.2. Doctor (Лікар)

```python
class Doctor(models.Model):
    full_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(upload_to='doctors/')
    specialization = models.CharField(max_length=200)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='doctors')
    bio = models.TextField()
    education = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    services = models.ManyToManyField('Service', blank=True, related_name='doctors')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
```

### 8.3. Service (Послуга)

```python
class Service(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='services')
    description = models.TextField()
    short_description = models.CharField(max_length=200, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_note = models.CharField(max_length=200, blank=True)  # "від", "за консультацію"
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
```

### 8.4. WorkingHours (Графік роботи)

```python
class WorkingHours(models.Model):
    DAYS = [(0, 'Понеділок'), (1, 'Вівторок'), ..., (6, 'Неділя')]
    day_of_week = models.IntegerField(choices=DAYS, unique=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
```

### 8.5. ContactInfo (Контакти)

```python
class ContactInfo(models.Model):
    address = models.CharField(max_length=500)
    phone_primary = models.CharField(max_length=20)
    phone_secondary = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    telegram_url = models.URLField(blank=True)
    viber_url = models.URLField(blank=True)
    map_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    map_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    map_embed_url = models.URLField(blank=True)
    directions_text = models.TextField(blank=True)  # текстова схема проїзду
```

### 8.6. Appointment (Заявка на запис)

```python
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нова'),
        ('processing', 'В обробці'),
        ('confirmed', 'Підтверджена'),
        ('rejected', 'Відхилена'),
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=50, blank=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
```

### 8.7. SiteSettings (Налаштування сайту)

```python
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='TEN clinic')
    tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True)
    about_text = models.TextField(blank=True)
    notification_email = models.EmailField()
    telegram_bot_token = models.CharField(max_length=100, blank=True)
    telegram_chat_id = models.CharField(max_length=50, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = 'Налаштування сайту'

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton
        super().save(*args, **kwargs)
```

### 8.8. Звʼязки між моделями

```
Direction 1──N Doctor
Direction 1──N Service
Doctor    N──M Service
Appointment N──1 Direction
Appointment N──1 Service
Appointment N──1 Doctor (optional)
```

---

## 9. Нефункціональні вимоги

### 9.1. Продуктивність

| Метрика | Цільове значення |
|---------|------------------|
| LCP (Largest Contentful Paint) | < 2.5s |
| FID (First Input Delay) | < 100ms |
| CLS (Cumulative Layout Shift) | < 0.1 |
| Розмір сторінки (HTML+CSS+JS) | < 500KB (без зображень) |
| Зображення | WebP з fallback, max-width через CSS, lazy load |

### 9.2. Безпека

- HTTPS обовʼязково (production).
- Django CSRF middleware увімкнено.
- XSS-захист: auto-escaping в шаблонах, `|safe` лише для перевіреного контенту.
- Секрети (SECRET_KEY, SMTP, Telegram token) — в `.env`, `.env` в `.gitignore`.
- Django `DEBUG=False` на production.
- `ALLOWED_HOSTS` налаштовано.
- Регулярне оновлення залежностей.

### 9.3. Доступність (a11y)

- Контраст тексту: WCAG AA (4.5:1 body, 3:1 large text).
- Focus-visible стилі на всіх інтерактивних елементах.
- `aria-label` на кнопках без тексту (burger, close).
- Форми: `<label>` повʼязані з `<input>` через `for`/`id`.
- Alt-текст на всіх зображеннях.
- Навігація з клавіатури (Tab order).

### 9.4. Сумісність з браузерами

| Браузер | Версії |
|---------|--------|
| Chrome | Останні 2 |
| Firefox | Останні 2 |
| Safari (macOS) | Останні 2 |
| Safari (iOS) | 15+ |
| Edge | Останні 2 |
| Samsung Internet | Остання |

### 9.5. Адаптивність та iOS Safari

- Viewport meta: `width=device-width, initial-scale=1, viewport-fit=cover`.
- Safe area: `padding: env(safe-area-inset-*)` для fixed/sticky елементів.
- Touch targets: мінімум 44×44px.
- Font-size inputs: мінімум 16px (запобігання zoom на iOS).
- `-webkit-tap-highlight-color` налаштовано.
- Sticky header не перекриває контент при scroll.
- Форми: `inputmode="tel"` для телефону, `type="email"` для email.

---

## 10. Технічна архітектура

### 10.1. Стек технологій

| Компонент | Технологія |
|-----------|------------|
| Backend | Python 3.12+, Django 5.x |
| БД (production) | PostgreSQL 15+ |
| БД (development) | SQLite 3 |
| Web server | Gunicorn + Nginx |
| Static files | Django `collectstatic` + Nginx |
| Media files | File system / S3 (опційно) |
| Email | SMTP (SendGrid, Gmail, або локальний) |
| Telegram | Bot API via `requests` |
| CSS | Окремі `.css` файли, CSS Custom Properties |
| JS | Vanilla JS (без важких фреймворків) |

### 10.2. Структура проєкту

```
ten_clinic/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── clinic/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── urls.py
│   └── signals.py          # сповіщення при новій заявці
├── templates/
│   ├── base.html
│   ├── includes/
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── breadcrumbs.html
│   ├── pages/
│   │   ├── home.html
│   │   ├── directions/
│   │   ├── doctors/
│   │   ├── services/
│   │   ├── price.html
│   │   ├── contacts.html
│   │   └── booking.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── static/
│   ├── css/
│   │   ├── variables.css    # CSS-змінні з палітри
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   └── pages/
│   └── js/
│       ├── main.js
│       └── booking.js       # cascade selects, валідація
├── media/
├── .env.example
├── .gitignore
├── requirements.txt
├── manage.py
└── TZ.md
```

### 10.3. Змінні оточення (.env)

```
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=tenclinic.ua,www.tenclinic.ua
DATABASE_URL=postgres://user:pass@localhost:5432/ten_clinic

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@tenclinic.ua
NOTIFICATION_EMAIL=admin@tenclinic.ua

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

### 10.4. Деплой (рекомендації)

- VPS (Ubuntu 22.04+) або PaaS (Railway, Render).
- Nginx як reverse proxy + SSL (Let's Encrypt).
- Gunicorn як WSGI-server (3–4 workers).
- PostgreSQL на тому ж сервері або managed DB.
- Автоматичний deploy через Git push (опційно).
- Backup БД — щоденно.

---

## 11. UI/UX вимоги

### 11.1. Загальні принципи

- Мінімалізм, професійність, довіра.
- Warm Ivory фон, Deep Navy header/footer, Sage Teal акценти.
- Одна primary-дія на екран (CTA «Записатися»).
- Консистентність: однакові компоненти на всіх сторінках.

### 11.2. Header

- Fixed/sticky при scroll.
- Логотип зліва → клік на головну.
- Навігація по центру (desktop) або burger (mobile/tablet).
- CTA «Записатися» справа — Deep Navy button.
- При scroll: легка тінь, без зміни висоти (запобігання layout shift).

### 11.3. Mobile-специфіка

- Burger-меню: full-screen overlay або slide-in panel.
- Sticky bottom bar з CTA «Записатися» (Deep Navy, full-width).
- Safe-area padding для iPhone з notch.
- Карта: full-width, height 250px на mobile.
- Таблиця прайсу: horizontal scroll або accordion на mobile.

### 11.4. Компоненти

| Компонент | Опис |
|-----------|------|
| **Button Primary** | Deep Navy bg, white text, border-radius 8px, padding 12px 24px |
| **Button Secondary** | Transparent bg, Sage Teal border + text |
| **Card** | Light Accent bg, border-radius 12px, padding 24px, subtle shadow |
| **Input** | Border 1px Graphite 20%, border-radius 8px, focus: Sage Teal border |
| **Section** | Padding 64px vertical (desktop), 40px (mobile) |

### 11.5. CSS-обмеження

- Не використовувати `!important`.
- CSS Custom Properties для всіх кольорів бренду.
- Mobile-first media queries.
- Окремі CSS-файли за відповідальністю (не один monolith).

---

## 12. Контент від замовника

### 12.1. Чеклист матеріалів

| № | Матеріал | Статус | Примітка |
|---|----------|--------|----------|
| 1 | Текст «Про клініку» (1–2 абзаци) | ☐ | |
| 2 | Список напрямків з описами | ☐ | |
| 3 | Профілі лікарів (фото, біо, освіта, стаж) | ☐ | Фото: min 800×800px |
| 4 | Каталог послуг з описами | ☐ | |
| 5 | Повний прайс-лист | ☐ | |
| 6 | Адреса клініки | ☐ | |
| 7 | Телефони (основний + додатковий) | ☐ | |
| 8 | Email для контактів та заявок | ☐ | |
| 9 | Графік роботи (по днях) | ☐ | |
| 10 | Текст схеми проїзду | ☐ | |
| 11 | Координати для карти (lat/lng) | ☐ | |
| 12 | Логотип SVG або PNG @2x | ☐ | |
| 13 | Посилання на Telegram/Viber | ☐ | Опційно |
| 14 | Текст політики конфіденційності | ☐ | |
| 15 | Meta description для SEO | ☐ | |

### 12.2. Вимоги до фото лікарів

- Формат: JPG або WebP.
- Мінімальний розмір: 800×800px.
- Стиль: однаковий фон (світлий нейтральний або однотонний).
- Обрізка: портрет, обличчя в центрі.

---

## 13. Етапи розробки

### Етап 1: Фундамент

- [ ] Ініціалізація Django-проєкту (config, clinic app).
- [ ] Моделі даних (розділ 8).
- [ ] Django Admin для всіх моделей.
- [ ] CSS-змінні з бренд-палітри (`variables.css`).
- [ ] Base template (header, footer).
- [ ] `.env.example`, `requirements.txt`, `.gitignore`.

### Етап 2: Публічні сторінки

- [ ] Головна сторінка (всі блоки з 6.1).
- [ ] Напрямки: список + детальна.
- [ ] Лікарі: список + детальна.
- [ ] Послуги: список + детальна.
- [ ] Прайс.
- [ ] Контакти (графік, карта, схема проїзду).

### Етап 3: Онлайн-запис

- [ ] Форма запису з валідацією.
- [ ] Cascade selects (напрямок → послуга → лікар).
- [ ] Pre-fill з URL-параметрів.
- [ ] Збереження заявки в БД.
- [ ] Email-сповіщення адміну.
- [ ] Telegram-сповіщення (опційно).
- [ ] Success-сторінка.

### Етап 4: Якість

- [ ] Адаптивна верстка (tablet, mobile).
- [ ] iOS Safari тестування та фікси.
- [ ] SEO meta-теги, schema.org.
- [ ] 404/500 сторінки.
- [ ] Cross-browser тестування.
- [ ] Lighthouse audit (Performance, Accessibility, SEO).

### Етап 5: Запуск

- [ ] Наповнення контентом (з матеріалів замовника).
- [ ] Production-деплой (Nginx, Gunicorn, PostgreSQL, SSL).
- [ ] Фінальне тестування форми запису на production.
- [ ] Передача доступів до Admin замовнику.
- [ ] Приймальні випробування.

---

## 14. Критерії приймання

### 14.1. Функціональні

- [ ] Всі розділи (Напрямки, Лікарі, Послуги, Прайс, Контакти) доступні та відображають дані з Admin.
- [ ] Форма онлайн-запису приймає заявки; заявка зʼявляється в Django Admin.
- [ ] Email-сповіщення надходить адміністратору при новій заявці.
- [ ] Графік роботи відображається на сторінці Контактів та в footer.
- [ ] Карта та текстова схема проїзду працюють на сторінці Контактів.
- [ ] Pre-fill форми працює зі сторінок лікаря/послуги/напрямку.

### 14.2. Дизайн та UX

- [ ] Кольори відповідають бренд-палітрі (розділ 4.1).
- [ ] Логотип відображається коректно в header та footer.
- [ ] Сайт адаптивний: коректне відображення на desktop, tablet, mobile.
- [ ] iOS Safari: форми, sticky header, safe-area — без багів.
- [ ] Touch targets ≥ 44px на mobile.

### 14.3. Технічні

- [ ] Django Admin: CRUD для всіх сутностей без помилок.
- [ ] `DEBUG=False` на production; секрети в `.env`.
- [ ] HTTPS працює.
- [ ] Lighthouse Performance ≥ 80, Accessibility ≥ 90, SEO ≥ 90.
- [ ] Немає console errors на жодній сторінці.

### 14.4. Контент

- [ ] Сайт наповнений реальним контентом від замовника (не lorem ipsum).
- [ ] Політика конфіденційності опублікована.
- [ ] Всі зображення оптимізовані (WebP, lazy load).

---

## 15. Поза scope (фаза 2)

Наступний функціонал **не входить** до першої версії, але може бути реалізований пізніше:

| Функціонал | Опис |
|------------|------|
| Інтеграція з Helsi / Doc.ua | Зовнішній сервіс онлайн-запису |
| Календар вільних слотів | Вибір дати/часу з реальним розкладом лікаря |
| Особистий кабінет пацієнта | Історія візитів, результати аналізів |
| Онлайн-оплата | Оплата послуг через LiqPay / WayForPay |
| Багатомовність | UA / EN версії сайту |
| Блог / новини | Статті, акції, корисна інформація |
| PDF-прайс | Експорт прайсу в PDF для скачування |
| SMS-сповіщення | Підтвердження запису через SMS |
| Google Analytics / GTM | Аналітика відвідувань |
| Cookie consent banner | GDPR / Zakon про захист ПД |

---

## Додаток А. Референси брендингу

| Файл | Опис |
|------|------|
| `assets/IMAGE_2026-06-30_11_02_04-2fafcddc-0dc6-402d-ba2f-7bfb53cd24b4.png` | Кольорова палітра |
| `assets/IMAGE_2026-06-30_11_02_10-624ddfde-096f-412c-aa60-6d478bd265f8.png` | Логотип TEN clinic |

## Додаток Б. Приклад CSS-змінних

```css
:root {
  --color-navy: #1F4A73;
  --color-sage: #8AAFA8;
  --color-ivory: #F4F0EB;
  --color-graphite: #3F4954;
  --color-accent-light: #DDE7E3;
  --color-white: #FFFFFF;

  --font-primary: 'Manrope', 'Inter', sans-serif;

  --radius-sm: 8px;
  --radius-md: 12px;

  --shadow-card: 0 2px 8px rgba(63, 73, 84, 0.08);

  --header-height: 72px;
  --section-padding: 64px;
}

@media (max-width: 767px) {
  :root {
    --section-padding: 40px;
    --header-height: 60px;
  }
}
```

---

*Кінець документа. Версія 1.0 — 30.06.2026.*
