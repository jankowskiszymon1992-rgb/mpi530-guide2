# Instrukcja Wdrozenia - MPI-530 Przewodnik
## Na VPS Hostinger z CloudPanel (Ubuntu 24.04)

---

## KROK 0: Zapisz kod na GitHub

1. W interfejsie Emergent, kliknij przycisk **"Save to Github"** (przy polu czatu)
2. Zaloguj sie na swoje konto GitHub i utworz repozytorium (np. `mpi530-guide`)
3. Zapamietaj adres repozytorium, np: `https://github.com/TWOJ_USER/mpi530-guide.git`

---

## KROK 1: Polacz sie z VPS przez SSH

```bash
ssh root@62.72.32.149
```
Wpisz haslo roota z panelu Hostinger.

---

## KROK 2: Uruchom skrypt instalacyjny

Po polaczeniu z VPS, uruchom te komendy:

```bash
# Pobierz kod z GitHub (zamien URL na swoj!)
cd /home
git clone https://github.com/TWOJ_USER/mpi530-guide.git mpi530-app
cd mpi530-app

# Uruchom skrypt instalacyjny
chmod +x deployment/setup.sh
bash deployment/setup.sh
```

Skrypt automatycznie zainstaluje wszystkie wymagane komponenty.

---

## KROK 3: Skonfiguruj domene w CloudPanel

### Opcja A: Subdomena (ZALECANA - nie koliduje z WordPress)

1. Zaloguj sie do CloudPanel: `https://62.72.32.149:8443`
2. Przejdz do **"Sites"** -> **"Add Site"**
3. Wybierz **"Create a Reverse Proxy"** lub **"Static Site"**
4. Wpisz domene: `mpi530.elektryk.cloud`
5. W panelu Hostinger DNS, dodaj rekord A:
   - Typ: `A`
   - Host: `mpi530`
   - Wartosc: `62.72.32.149`
   - TTL: 3600

### Opcja B: Uzyj glownej domeny (zastapi WordPress)

Jesli nie potrzebujesz WordPress na `elektryk.cloud`, mozesz uzyc glownej domeny.

---

## KROK 4: Dodaj konfiguracje Nginx

### Jesli uzywasz CloudPanel:

W CloudPanel przejdz do strony -> **Vhost** i zastap konfiguracje:

```nginx
server {
    listen 80;
    server_name mpi530.elektryk.cloud;  # <- ZMIEN na swoja domene

    # Frontend - pliki statyczne React
    root /home/mpi530-app/frontend/build;
    index index.html;

    # Kompresja
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;

    # API - przekierowanie do FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # React Router - przekieruj wszystkie inne sciezki do index.html
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Jesli NIE uzywasz CloudPanel:

```bash
# Skopiuj konfiguracje Nginx
sudo cp /home/mpi530-app/deployment/nginx.conf /etc/nginx/sites-available/mpi530
sudo ln -s /etc/nginx/sites-available/mpi530 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## KROK 5: Wlacz SSL (HTTPS)

### W CloudPanel:
CloudPanel automatycznie generuje certyfikat Let's Encrypt - wlacz go w ustawieniach strony.

### Reczne (bez CloudPanel):
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d mpi530.elektryk.cloud
```

---

## KROK 6: Sprawdz czy wszystko dziala

```bash
# Sprawdz status backendu
sudo systemctl status mpi530-backend

# Sprawdz logi
sudo journalctl -u mpi530-backend -f

# Testuj API
curl http://localhost:8001/api/health

# Otworz w przegladarce
# http://mpi530.elektryk.cloud (lub Twoja domena)
```

---

## Przydatne komendy

```bash
# Restart backendu
sudo systemctl restart mpi530-backend

# Logi backendu
sudo journalctl -u mpi530-backend --no-pager -n 50

# Restart Nginx
sudo systemctl restart nginx

# Aktualizacja aplikacji (po zmianach na GitHub)
cd /home/mpi530-app
git pull
cd frontend && yarn install && yarn build
cd ../backend && source venv/bin/activate && pip install -r requirements.txt
sudo systemctl restart mpi530-backend
```

---

## Rozwiazywanie problemow

| Problem | Rozwiazanie |
|---------|-------------|
| Strona nie laduje sie | Sprawdz: `sudo systemctl status nginx` |
| API nie odpowiada | Sprawdz: `sudo systemctl status mpi530-backend` |
| Blad 502 Bad Gateway | Backend nie dziala - restart: `sudo systemctl restart mpi530-backend` |
| Blad DNS | Poczekaj 5-30 min na propagacje DNS |
| MongoDB blad | Sprawdz: `sudo systemctl status mongod` |
