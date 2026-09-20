# 🛒 Shop Portfolio

A **Django + Django Ninja** backend for an e‑commerce platform, built with an async‑first mindset and a clean separation between API, services, selectors, and schemas. Covers authentication via OTP, a product catalog, coupons, and a wallet/finance system powered by the Zibal payment gateway.

---

## ✨ Features

### 🔐 Authentication & User Management

- **Custom User model** keyed on `phone_number` (via `AbstractBaseUser`).
- **OTP login/register flow** using TOTP (`pyotp`) stored in cache with an expiring secret.
- **JWT access/refresh tokens** (custom `JWTService`, `sub` claim = user id).
- **Google OAuth callback** endpoint for social login (exchange code → userinfo → JWT).
- **Superuser creation** auto-provisions a `UserTOTP` record for 2FA.
- Custom **phone/email normalizers** and **password validators**.

### 🛍️ Catalog

- **Hierarchical categories** (self-referential `parent`).
- **Products** with slug, SKU, price, stock, tags (`django-taggit`), and availability.
- **Product images** with a unique-featured-image constraint per product.
- **Product attributes** as key/value pairs.

### 🎟️ Promotions

- **Coupons** with percent or fixed discounts.
- Start/end dates, minimum order amount, and max-usage tracking.
- **Per-product coupon** mapping (`ProductCoupon`).
- Verify endpoint that returns the computed discount.

### 💳 Finance & Wallets

- **Wallet model** supporting `PERSONAL`, `BUSINESS`, `ESCROW`, and `REVENUE` types.
- **Wallet transactions** with `DEPOSIT`, `WITHDRAWAL`, `BOOKING_PAYMENT`, `SYSTEM_PAYMENT`, and `REFUND` types and `PENDING`/`SUCCESSFUL`/`FAILED` statuses.
- **Atomic transfers** between wallets (`WalletTransfer`) using `select_for_update` and `F()` expressions.
- **Zibal gateway integration** for depositing into wallets:
    - Lazy request, verify, and inquiry endpoints.
    - Callback handler that locks the pending transaction and updates balances atomically.
    - Encrypted card/Sheba/account numbers via `EncryptedCharField` + HMAC lookup.
- **Pagination** on wallet and transaction listings via `django-ninja`'s `@paginate`.

### ⚙️ Infrastructure

- **Django Ninja** routers per domain, composed in `config/urls.py`.
- **Custom permission decorator** (`@permissions(...)`) with sync/async support.
- **Query logger middleware** for development (SQL + timing per request).
- **Dramatiq** worker for SMS tasks (MeliPayamak provider).
- **Seed command** (`python manage.py seed`) to populate the DB with realistic data.
- **Ruff** for linting, **pytest + pytest-django + pytest-asyncio** for tests.

---

## 🧱 Tech Stack

| Layer           | Tool                                  |
| --------------- | ------------------------------------- |
| Web framework   | Django                                |
| API layer       | Django Ninja                          |
| Auth            | Custom JWT + pyotp (TOTP)             |
| Async tasks     | Dramatiq (Redis broker)               |
| Payments        | Zibal                                 |
| SMS             | MeliPayamak                           |
| DB (dev)        | SQLite                                |
| DB (prod)       | PostgreSQL                            |
| Cache           | LocMem (dev), Redis (prod)            |
| Linting         | Ruff                                  |
| Testing         | pytest, pytest-django, pytest-asyncio |
| Package manager | uv                                    |

---

## 📁 Project Structure

```
src/
├── authentication/    # User model, OTP, JWT auth, social login
├── catalog/           # Categories, products, attributes, images
├── promotions/        # Coupons and product-coupon mapping
├── finance/           # Wallets, transactions, Zibal gateway
├── common/            # Shared utilities: JWT, OTP, validators,
│                      # normalizers, permissions, providers, seed
└── config/            # Settings (base/dev/prod), URLs, ASGI/WSGI,
                       # middlewares
```

Each domain app follows the same internal layout:

```
api/          # Ninja routers and views
schemas/      # Request/response pydantic schemas
selectors/    # Read-only query functions
services/     # Business logic (write side)
models.py     # Django models
apps.py       # App config
```

This separation keeps **read paths (selectors)** and **write paths (services)** distinct from the **transport layer (api)**, which makes the code easier to test and reason about.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.14+**
- [uv](https://github.com/astral-sh/uv) installed
- Redis (only needed if you run the Dramatiq worker)

### 1. Clone and install

```bash
git clone https://github.com/your-username/shop-portfolio.git
cd shop-portfolio
uv sync
```

### 2. Configure environment

Copy the template and adjust values:

```bash
cp template.env .env
```

Key variables:

| Variable                           | Description                             |
| ---------------------------------- | --------------------------------------- |
| `SECRET_KEY`                       | Django secret key                       |
| `DEBUG`                            | `True` in development                   |
| `ALLOWED_HOSTS`                    | Comma-separated list                    |
| `TIME_ZONE`                        | e.g. `Asia/Tehran`                      |
| `CACHE_BACKEND` / `CACHE_LOCATION` | Cache backend (Redis in prod)           |
| `DRAMATIQ_BROKER_URL`              | Redis URL for the worker                |
| `ZIBAL_MERCHANT_ID`                | Zibal merchant id (`zibal` in sandbox)  |
| `ZIBAL_CALLBACK_URL`               | Public URL for Zibal's callback         |
| `EMAIL_HOST_*`                     | SMTP credentials if you need real email |

### 3. Run migrations

```bash
cd src
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### 4. Seed sample data (optional)

```bash
uv run python manage.py seed
```

This creates:

- A test user (`09123456789`)
- Two categories, two products
- A `10%` coupon (`OFF10`)
- A personal wallet with `1,000,000` balance and one deposit transaction

### 5. Start the server

```bash
uv run python manage.py runserver
```

API is mounted at `/api/v1/`, docs at `/api/v1/docs/`.

### 6. Start the Dramatiq worker (optional)

```bash
uv run dramatiq authentication.tasks
```

---

## 📖 API Documentation

When `DEBUG=True`, an interactive OpenAPI UI is available at:

- **Swagger-like UI:** `/api/v1/docs/`
- **Raw OpenAPI schema:** `/api/v1/openapi.json`

Router prefixes:

| Prefix                | Domain                                                 |
| --------------------- | ------------------------------------------------------ |
| `/api/v1/auth/`       | Authentication (OTP, login, register, refresh, logout) |
| `/api/v1/catalog/`    | Products and categories                                |
| `/api/v1/promotions/` | Coupons                                                |
| `/api/v1/`            | Finance (wallets, deposits, Zibal callback)            |

---

## 🧪 Testing

```bash
uv run pytest
```

The project uses `pytest-django` with `pytest-asyncio` — most service and selector tests are written as `async def` tests using Django's async ORM methods (`acreate`, `aget_or_create`, `afirst`, etc.).

> **Note on Django 7.0 deprecation warnings:** Django has deprecated the `EMAIL_*` settings in favor of the new `MAILERS` setting. The warnings you see in test output come from pytest-django reading these settings. You can silence them for now or plan a migration before upgrading to Django 7.

To silence them in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
filterwarnings = [
    "ignore::django.utils.deprecation.RemovedInDjango70Warning",
]
```

---

## 🧹 Linting

```bash
uv run ruff check src
uv run ruff format src
```

Recommended `pyproject.toml` addition for Django projects (avoids false positives like `RUF012` on `Meta.indexes`):

```toml
[tool.ruff.lint]
ignore = ["RUF012"]
```

---

## 🔒 Security Notes

- JWT secret falls back to `SECRET_KEY` if `JWT_SETTINGS["JWT_SECRET_KEY"]` is unset — **always set a distinct value in production**.
- Card numbers, Sheba numbers, and account numbers are stored with `EncryptedCharField`; the HMAC column (`card_number_hmac`) enables lookups without decrypting.
- In production (`DEBUG=False`), the OpenAPI schema endpoint is disabled and HTTPS is enforced (`SECURE_SSL_REDIRECT`, secure cookies).
- Zibal callback signature is validated by re-verifying the payment with Zibal before crediting the wallet.

---

## 🗺️ Roadmap

- [ ] Cart and order modules
- [ ] Reviews (1–5 stars, images)
- [ ] Additional payment gateways
- [ ] Rate limiting on OTP endpoints
- [ ] Migrate to Django's `MAILERS` setting

---

## 📜 License

MIT — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Abolfazl Fallahkar**
Telegram: [@AbolfazlFa7](https://t.me/AbolfazlFa7)
