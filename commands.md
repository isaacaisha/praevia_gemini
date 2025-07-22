# praevia_gemini commands eg.:

python manage.py collectstatic
sudo systemctl daemon-reload
sudo systemctl restart praevia_gemini.service
sudo systemctl status praevia_gemini.service

sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx

python manage.py makemigrations
python manage.py migrate

sudo journalctl -u praevia_gemini.service -f

source venv/bin/activate
export DATABASE_URL=postgresql://postgres:Toure7Medina@localhost:5432/praevi_gemini_db
python manage.py runserver 0.0.0.0:8079

# CONNECT POSTGRES
sudo -i -u postgres
sudo nano /var/lib/pgsql/data/postgresql.conf

# systemd
sudo nano /etc/systemd/system/praevia_gemini.service

# nginx
sudo nano /etc/nginx/sites-available/praevia_gemini.conf

# CREATE SSL CERTIFICATE
sudo dnf install certbot python-certbot-nginx
sudo certbot --nginx

# link the configuration to enable it
sudo ln -s /etc/nginx/sites-available/praevia_gemini.conf /etc/nginx/sites-enabled/

sudo certbot certificates
sudo certbot --nginx -d praevia-gemini.siisi.online -d www.praevia-gemini.siisi.online

sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

sudo systemctl enable certbot.timer
sudo certbot renew --dry-run

# kill all port runing
sudo lsof -t -iTCP:8001 -sTCP:LISTEN | xargs sudo kill

# Find Your Computer's Local IP Address
ifconfig | grep inet

# Testing
python -m gunicorn --workers 3 --bind unix:/home/siisi/praevia_gemini/praevia_gemini.sock siisi.wsgi:application

## Docker
# Start services

# Start DB + Django runserver
# Rebuild static assets & restart
<!-- prod -->
docker compose -f docker-compose.prod.yml -p praevia_gemini_prod run praevia_gemini python manage.py collectstatic
<!-- Collect static files INSIDE the container -->
docker compose -f docker-compose.prod.yml -p praevia_gemini_prod run --rm praevia_gemini \
  python manage.py collectstatic --noinput

docker-compose -f docker-compose.prod.yml -p praevia_gemini_prod down --volumes --remove-orphans
docker system prune -a --volumes
docker-compose -f docker-compose.prod.yml -p praevia_gemini_prod down -v
docker-compose -f docker-compose.prod.yml -p praevia_gemini_prod up -d --build --remove-orphans
docker-compose -f docker-compose.prod.yml -p praevia_gemini_prod ps
docker-compose -f docker-compose.prod.yml -p praevia_gemini_prod down
docker-compose -f docker-compose.prod.yml -p praevia_gemini_prod up -d --remove-orphans --build
docker-compose -f docker-compose.prod.yml -p praevia_gemini_prod logs -f nginx
docker-compose -f docker-compose.prod.yml -p praevia_gemini_prod logs -f

<!-- dev -->
docker compose -f docker-compose.dev.yml -p praevia_gemini_dev run praevia_gemini python manage.py collectstatic
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
docker system prune -a --volumes
docker-compose -f docker-compose.dev.yml -p praevia_gemini_dev down -v
docker-compose -f docker-compose.dev.yml -p praevia_gemini_dev up -d --remove-orphans --build
docker-compose -f docker-compose.dev.yml -p praevia_gemini_dev ps
docker-compose -f docker-compose.dev.yml -p praevia_gemini_dev down
docker-compose -f docker-compose.dev.yml -p praevia_gemini_dev up -d --remove-orphans --build
docker-compose -f docker-compose.dev.yml -p praevia_gemini_dev logs -f nginx
docker-compose -f docker-compose.dev.yml -p praevia_gemini_dev logs -f

# Apply migrations or create superuser
<!-- prod -->
docker exec -it praevia_gemini_prod-praevia_gemini_prod-1 python manage.py makemigrations
docker exec -it praevia_gemini_prod-praevia_gemini_prod-1 python manage.py migrate
docker exec -it praevia_gemini_prod-praevia_gemini_prod-1 python manage.py createsuperuser
docker exec -it praevia_gemini_prod-praevia_gemini_prod-1 python manage.py shell
docker exec -it praevia_gemini_prod-praevia_gemini_prod-1 bash

<!-- dev -->
docker exec -it praevia_gemini_dev-praevia_gemini_dev-1 python manage.py makemigrations
docker exec -it praevia_gemini_dev-praevia_gemini_dev-1 python manage.py migrate
docker exec -it praevia_gemini_dev-praevia_gemini_dev-1 python manage.py createsuperuser
docker exec -it praevia_gemini_dev-praevia_gemini_dev-1 python manage.py shell
docker exec -it praevia_gemini_dev-praevia_gemini_dev-1 bash

# ex. create a folder and set the permission
mkdir -p media/profile_img
# Change owner to siisi:siisi
sudo chown -R siisi:siisi media/profile_img
# Give user and group write permissions, others only read/execute
chmod -R 755 media/profile_img

# Siret: 918 881 913 00019
