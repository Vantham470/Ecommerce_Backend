# E-commerce Backend

A Django REST Framework backend for an e-commerce platform, covering products, carts, orders, and payments — fully containerized with Docker and deployed via CI/CD.

## Features

- **Products** — categories, products, stock tracking
- **Carts** — per-user carts with quantity management
- **Orders** — cart-to-order checkout flow with price/name snapshotting and status tracking
- **Payments** — simulated payment processing with transaction IDs and automatic order status updates
- **REST API** — full DRF endpoints with authentication and user-scoped permissions
- **Dockerized** — runs locally via Docker Compose (Django + PostgreSQL)
- **CI/CD** — GitHub Actions automatically runs the test suite on every push
- **Live deployment** — hosted on Render.com

## Tech Stack

- Django 6.0 / Django REST Framework
- PostgreSQL (production/Docker) / SQLite (local dev fallback)
- Docker & Docker Compose
- GitHub Actions
- Gunicorn + WhiteNoise (production serving)
- Render.com (hosting)

## Local Development (without Docker)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:7777
```

## Local Development (with Docker)

```bash
docker compose build
docker compose up
```

Then, in a second terminal:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

App will be available at `http://localhost:8000`.

## API Endpoints

| Endpoint | Description |
|---|---|
| `/api/categories/` | List/create categories |
| `/api/products/` | List/create products |
| `/api/cart/` | View your cart |
| `/api/cart/add_item/` | Add item to cart |
| `/api/cart/remove_item/` | Remove item from cart |
| `/api/orders/` | View your orders |
| `/api/orders/checkout/` | Convert cart to an order |
| `/api/payments/` | View your payments |

## Running Tests

```bash
python manage.py test
```

## Deployment

This project auto-deploys to Render.com on every push to `main`, using the included `Dockerfile` and `entrypoint.sh`.