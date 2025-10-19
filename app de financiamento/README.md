FinanControl - Deploy Ready (Netlify frontend + Render backend)
================================================================

Contents:
- frontend/  -> Netlify-ready static site (drop to Netlify)
- backend/   -> Render-ready backend (FastAPI, Alembic migration included)

How to deploy frontend (Netlify):
1. Zip or upload the `frontend` folder to Netlify (or connect GitHub repo).
2. Netlify will serve files from `static/`. netlify.toml included for redirects to API.
3. Configure domain and set environment variable for API if you want to override.

How to deploy backend (Render):
1. Push repo to GitHub with both `frontend/` and `backend/` folders.
2. Create a Web Service on Render using Docker (render.yaml included as example).
3. Create a Postgres managed DB on Render with credentials matching the config (or set DATABASE_URL env var).
4. In Render shell, run: `alembic upgrade head` to apply migrations (the migration file is in backend/alembic/versions/).
5. Set CORS origins in backend if you have a custom Netlify domain.

Important notes:
- DATABASE_URL default in backend/config.py uses `postgresql+psycopg2://finan_user:finan_pass@db:5432/financontrol` — update it with your Render DB host and credentials.
- After deployment, use the admin credentials seeded (admin@financontrol.local / admin123) or re-seed with secure password.
