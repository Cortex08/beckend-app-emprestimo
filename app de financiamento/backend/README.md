
Render deployment (quick):
1. Push this repo to GitHub.
2. In Render dashboard, create a new Web Service from this repo; select Docker; set start command: `gunicorn -c gunicorn_conf.py backend.main:app`
3. Create a new Postgres managed DB in Render; copy host / credentials and set DATABASE_URL as: `postgresql+psycopg2://finan_user:finan_pass@<HOST>:5432/financontrol`
4. After deploy, run: `alembic upgrade head` on the instance (via Render's shell or during startup) to create tables.
