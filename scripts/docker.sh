#!/use/bin/env bash

if [ ! -e /venv/bin/activate ]; then
  python -m venv /venv
fi

source /venv/bin/activate

pip install -r /requirements.txt
python /manage.py migrate
python /manage.py collectstatic
daphne -b 0.0.0.0 -p 8080 vercel_app.asgi:application