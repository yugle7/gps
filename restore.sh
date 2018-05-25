#!/bin/bash

echo "==> Removing all data from the database..."
python manage.py flush --noinput

echo "==> Loading user fixtures..."
python manage.py loaddata debt/fixtures/user.json

echo "==> Loading debt fixtures..."
python manage.py loaddata debt/fixtures/debt.json

echo "==> Done!"
