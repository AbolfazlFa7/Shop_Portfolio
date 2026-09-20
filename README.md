# 🛒 Shop Portfolio

A **Django + DRF** based e-commerce backend API that provides full authentication, user management, product catalog, cart, orders, payments, and coupon system with documentation and background tasks.

---

## 🚀 Features

### 🔐 Authentication & User Management

* **Custom User Model** with email login, phone, birthday, gender, and secret key.
* **JWT Authentication** using `access` and `refresh` tokens (SimpleJWT).
* **User CRUD APIs** (register, profile, update, delete).
* **Logout with Blacklist** for refresh tokens.
* **OTP System**:

  * Account activation via email OTP.
  * Password reset with OTP.
  * Phone number verification & set with OTP.
* **Custom Password Validation** with serializer-level validation.

---

### 🛍️ Product & Category

* Category hierarchy with parent-child relationships.
* Product model with:

  * Unique **Slug** and **SKU** auto-generation.
  * Stock, availability, and price management.
  * Tagging system (`django-taggit`).
  * Attributes (key-value pairs).
* Product images with **unique featured image constraint**.
* Optimized queries using `select_related`, `prefetch_related`, and annotations.
* Public product listing with filters (via `django-filters`).
* Admin CRUD endpoints for product & category management.

---

### 🎟️ Coupon System

* Coupon features:

  * Unique code (auto-generated if empty).
  * Percentage or fixed amount discounts.
  * Min order amount requirement.
  * Usage count & max usage limit.
  * Start & end date.
* Coupon relations:

  * Assign to **specific products**.
  * Assign to **categories**.
  * Assign to **users**.
* API endpoint for verifying coupon validity and returning final price.

---

### 🛒 Cart

* One-to-one cart per user.
* Add/remove/update cart items.
* Prevent duplicate products in cart.
* Auto-adjust item quantity if it exceeds product stock.
* Prefetch featured product images for faster responses.

---

### 📦 Orders

* Create orders directly from cart items.
* Auto-generate **tracking codes**.
* Order status flow: `pending → paid → shipped → completed / canceled`.
* Store total amount, discount amount, and final amount.
* Order items snapshot product, quantity, and price at purchase time.

---

### 💳 Payments

* Integrated with **Zarinpal Gateway** (sandbox & real).
* API for initiating payments, returning payment URL.
* Callback endpoint for verifying payments.
* Tracks transaction IDs and reference IDs.
* Auto-clear user cart after successful payment.
* Coupon usage count updated after successful payment.
* Payment status tracking: `pending`, `success`, `failed`.

---

### ⭐ Reviews

* Users can leave product reviews (1–5 stars).
* Each user can only review a product once.
* Reviews support images (max 5 per review).
* Update and delete review endpoints.
* Admin management of reviews and review images.

---

### ⚙️ Tech Stack

* **Django 5.2** & **Django REST Framework**.
* **JWT Authentication** with SimpleJWT.
* **Celery + Redis** for async tasks (emails & SMS).
* **Kavenegar API** for OTP SMS.
* **drf-spectacular** for OpenAPI schema & Swagger/Redoc UI.
* **Django Debug Toolbar**, **Django Extensions**, **Django Filters**, **Taggit**.

---

### 🧩 Admin Panel

* Django admin customization for all models:

  * Users with filters and search.
  * Products with inline attributes and images.
  * Categories, Coupons, Orders, Payments.
* Prepopulated slugs and list filters for better UX.

---

## 📖 API Documentation

* **Swagger UI**: `/api/schema/ui/`
* **Redoc**: `/api/schema/redoc/`
* **Raw Schema**: `/api/schema/`

---

## ⚡ Installation & Setup

```bash
# Clone repository
git clone https://github.com/your-username/shop-portfolio.git
cd shop-portfolio

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp template.env .env
# Edit .env file with your configs

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
```

---

## 📦 Celery & Redis

Start Redis server and run Celery worker:

```bash
celery -A config worker -l info
```

---

## 🧪 Testing

Run all tests:

```bash
python manage.py test
```

## 📊 Seeding
Populates the database with realistic fake data:

```bash
python manage.py seed
```

---

## 📜 Author:
### 👤 Abolfazl Fallahkar
#### 💻 Telegram 🆔: [@AbolfazlFa7](https://t.me/AbolfazlFa7)
---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.