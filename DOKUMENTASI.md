# 📘 DOKUMENTASI BELAJAR — BookVerse (UTS COMP6991031)

> **Tujuan file ini:** membantumu MEMAHAMI (bukan sekadar punya) project, agar
> kamu bisa menjelaskan setiap baris `Dockerfile` dan `docker-compose.yml`
> dengan bahasamu sendiri di video demo — sesuai aturan soal:
> *"bagian yang tidak dapat Anda jelaskan dianggap bukan hasil kerja Anda."*

---

## 0. Checklist Deliverable (samakan sebelum submit)

- [ ] Daftar topik ke dosen **≤ 3 jam** sejak soal rilis (judul, kategori AI, framework, deskripsi 1 kalimat)
- [ ] `docker compose up -d --build` jalan dari clone bersih (`git clone` → `cp .env.example .env` → up)
- [ ] Screenshot: `docker compose ps` (semua healthy), curl 200 & 201, uji persistensi, UI
- [ ] Git: repo **public**, ≥ 5 commit bermakna, **tanpa** `.env` (cek `git ls-files | grep .env` → hanya `.env.example`)
- [ ] Video YouTube **public** 3–5 menit, suara sendiri, link GitHub + artikel di deskripsi
- [ ] Artikel 500–800 kata (Medium/dev.to/Hashnode/LinkedIn), public
- [ ] PDF `UTS_COMP6991031_NIM_Nama.pdf`: identitas, judul, 3 link, jawaban Soal 1 & 2 + screenshot, AI Usage Declaration, pernyataan orisinalitas

---

## 1. Gambaran Besar Arsitektur

```
Browser ──HTTP──> frontend (nginx, host port 3000)
                     │  reverse proxy /api
                     ▼
                  backend (FastAPI, host port 8000)
                   │              │
                   ▼              ▼
             db (PostgreSQL)   redis (cache)
             volume: pgdata    volume: redisdata
             [adminer :8080 — hanya --profile tools]
```

- Semua container ada di **user-defined network `booknet`** → saling panggil
  dengan **nama service** (`db`, `redis`, `backend`), bukan `localhost`.
- Data PostgreSQL hidup di **named volume `pgdata`** → aman saat `docker compose down`.

---

## 2. backend/Dockerfile — penjelasan per blok

```dockerfile
FROM python:3.12.7-slim AS builder
```
- Base image **versi spesifik** (bukan `latest`) → build reproducible. `slim`
  = versi Debian kecil tanpa compiler/IDE. `AS builder` = nama stage 1.

```dockerfile
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1
WORKDIR /build
COPY requirements.txt .
```
- `ENV` = set environment variable saat build (hemat waktu & ukuran).
- `WORKDIR` = direktori kerja (dibuat otomatis bila belum ada).
- **Hanya `requirements.txt` yang dicopy lebih dulu** → layer "pip install"
  hanya di-build ulang kalau dependency berubah; kalau cuma kode aplikasi
  yang berubah, Docker pakai cache. Ini poin penilaian 2c(3).
- `COPY` dipakai, bukan `ADD`: `COPY` hanya menyalin file apa adanya;
  `ADD` punya behavior tambahan (auto-extract tar, unduh URL) yang bisa
  mengejutkan — jadi aturan praktis: pakai `COPY` kecuali butuh fitur itu.

```dockerfile
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt
```
- Dependency di-install ke **virtualenv terpisah** supaya stage runtime bisa
  menyalin *hanya* folder venv ini — inilah inti **multi-stage**.

```dockerfile
FROM python:3.12.7-slim AS runtime
RUN groupadd -r appuser && useradd -r -g appuser appuser
```
- Stage 2 mulai dari base **bersih** (tidak mewarisi pip cache dsb.).
- Buat user non-root → kalau app kemasukan, penyerang tidak langsung root.

```dockerfile
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app ./app
```
- `COPY --from=builder` = ambil artefak dari stage 1 (hanya venv), lalu
  source code aplikasi — urutan ini menjaga cache dependency.

```dockerfile
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
- `PYTHONUNBUFFERED=1` → log langsung muncul di `docker logs`.
- `USER appuser` → proses berjalan non-root.
- `EXPOSE` = **dokumentasi** port (tidak mem-publish; publishing ada di
  compose `ports`).
- `CMD` **exec form** (array JSON): uvicorn jadi PID 1, menerima sinyal
  SIGTERM langsung → `docker stop` shutdown dengan rapi. Shell form
  (`CMD uvicorn ...`) membungkus dengan `/bin/sh -c`, sinyal berhenti di
  shell → container lambat mati / kena `SIGKILL` setelah 10 detik.

### Kenapa multi-stage bikin image kecil?
Stage builder membawa pip + semua sampah build, tapi yang disalin ke runtime
**hanya venv jadi**. Bandingkan `docker images` — image backend jauh lebih
kecil daripada kalau install langsung di satu stage (tanpa compiler/cache).

---

## 3. frontend/Dockerfile — penjelasan per blok

```dockerfile
FROM node:22.11.0-alpine3.20 AS builder
WORKDIR /build
COPY package.json package-lock.json* ./
RUN npm install
```
- `package.json` dulu → layer `npm install` ter-cache.
- `node:…-alpine` = Linux mini (musl) sangat kecil, cukup untuk build React.

```dockerfile
COPY . .
RUN npm run build
```
- Source masuk setelah dependency; Vite menghasilkan folder `dist/` statis.

```dockerfile
FROM nginx:1.27.2-alpine AS runtime
COPY --from=builder /build/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
- Runtime **tidak ada Node sama sekali** — hanya nginx + file HTML/JS/CSS →
  image ± 50 MB. Ini contoh multi-stage paling dramatis: builder ratusan MB,
  runtime kecil.
- `daemon off;` = nginx jalan di foreground (wajib di container).

### nginx.conf (frontend)
- `location / { try_files $uri $uri/ /index.html; }` → SPA routing (React
  Router tidak 404 saat refresh).
- `location /api/ { proxy_pass http://backend:8000; }` → **reverse proxy**:
  browser hanya kenal `localhost:3000`; request `/api/...` diteruskan ke
  container `backend` (nama service, DNS dari Docker network). Bonus: tidak
  perlu setting CORS.

---

## 4. docker-compose.yml — penjelasan per blok

```yaml
services:
  db:
    image: postgres:16.4-alpine
```
- Tarik image resmi versi spesifik (bukan latest).

```yaml
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      ...
```
- `${VAR}` dibaca dari **file `.env`** di root project (yang di-commit hanya
  `.env.example`).

```yaml
    volumes:
      - pgdata:/var/lib/postgresql/data
```
- **Named volume** `pgdata` (dideklarasikan di bawah `volumes:`) → data DB
  hidup di luar container; `docker compose down` TIDAK menghapusnya
  (yang menghapus: `down -v`).

```yaml
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s  timeout: 5s  retries: 10
```
- Compose mengeksekusi `pg_isready` tiap 5 s; status jadi `healthy` kalau DB
  benar-benar siap menerima koneksi — bukan sekadar "proses jalan".

```yaml
  backend:
    build: ./backend
    depends_on:
      db:
        condition: service_healthy
```
- **Poin penilaian 2c(4):** backend menunggu sampai `db` **healthy**
  (bukan cuma started) baru start → tidak ada race condition "connection
  refused" saat boot.

```yaml
    ports:
      - "8000:8000"   # host:container — untuk curl/Swagger
```
- `db` dan `redis` sengaja TIDAK di-publish ke host → hanya bisa diakses
  dalam network (prinsip minimum exposure).

```yaml
  adminer:
    profiles: ["tools"]
```
- **Poin penilaian 2c(6):** service dengan profile tidak jalan dengan `up`
  biasa; jalankan eksplisit:
  `docker compose --profile tools up -d`.

```yaml
networks:
  booknet: { driver: bridge }
```
- **User-defined network** (bukan default) → Docker menyediakan DNS internal
  sehingga nama service bisa dipakai sebagai hostname.

---

## 5. Perintah Uji (untuk screenshot)

```bash
docker compose ps
# semua service "running", db & redis "(healthy)"

curl http://localhost:8000/health           # 200 {"status":"ok",...}

curl http://localhost:8000/api/books        # 200 daftar buku

curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"query":"The Hobbit","mode":"title"}'   # 201 + hasil rekomendasi

curl http://localhost:8000/api/history      # 200 riwayat dari DB
```

Tambah flag `-i` (mis. `curl -i ...`) supaya **status code terlihat** di
screenshot: `HTTP/1.1 200 OK` / `HTTP/1.1 201 Created`.

### Uji persistensi (Soal 2d)
```bash
curl -X POST http://localhost:8000/api/predict -H "Content-Type: application/json" \
  -d '{"query":"Dune","mode":"title"}'      # catat hasilnya
docker compose down                          # container & network dihapus
docker compose up -d                         # tanpa --build, cepat
curl http://localhost:8000/api/history      # data MASIH ADA ✅
```
**Bedanya `down` vs `down -v`:** `down` menghapus container & network saja;
named volume tetap. `down -v` juga menghapus volume → database kembali kosong
(buku seed ulang otomatis, riwayat hilang). Demonstrasikan keduanya di video.

---

## 6. Cara Kerja Fitur AI (untuk narasi video)

1. Saat startup, backend memuat 55 buku dari PostgreSQL dan membangun
   **TF-IDF matrix** dari gabungan `genre + deskripsi + penulis` tiap buku.
2. Mode **title**: buku pilihan dijadikan vektor pembanding → hitung
   **cosine similarity** terhadap semua buku lain → ambil 6 skor tertinggi.
3. Mode **text**: teks bebas di-vektorisasi dengan vocabulary yang sama →
   dicocokkan ke katalog.
4. Hasil di-**cache di Redis** (TTL 300 s) — request sama ditandai ⚡ di UI.
5. Setiap prediksi **ditulis ke tabel `recommendation_history`** → ini
   endpoint WRITE yang jadi bukti persistensi.

Kenapa TF-IDF cocok untuk ujian ini: ringan, murni CPU, tanpa download model
besar, dan tetap "AI" (bagian dari information retrieval / content-based
filtering) sesuai contoh soal.

---

## 7. Outline Video (3–5 menit)

1. **(0:00–0:30)** Perkenalan + alasan pilih topik (kaitkan karier).
2. **(0:30–1:15)** Arsitektur: tunjuk diagram, sebut 3 tier + network + volume.
3. **(1:15–2:30)** Buka `backend/Dockerfile` & `frontend/Dockerfile`:
   jelaskan multi-stage, tag versi, urutan COPY, exec form, .dockerignore.
4. **(2:30–3:30)** Buka `docker-compose.yml`: healthcheck + `service_healthy`,
   named volume, `.env`/`.env.example`, profile `tools`.
5. **(3:30–4:30)** Demo: `up -d --build`, `ps`, buka UI, minta rekomendasi,
   curl `-i` 200/201.
6. **(4:30–5:00)** Uji persistensi (`down` → `up` → history masih ada) +
   penutup.

---

## 8. Istilah Penting (bisa ditanya saat penilaian)

| Istilah | Arti singkat |
|---|---|
| Image vs container | Image = cetakan/template read-only; container = proses yang berjalan dari image. |
| Layer & cache | Tiap instruksi Dockerfile = layer; layer yang tidak berubah dipakai ulang dari cache. |
| Named volume | Penyimpanan dikelola Docker, terpisah dari hidup-matinya container. |
| Healthcheck | Perintah periodik untuk menandai container `healthy` — dasah `depends_on: condition`. |
| User-defined network | Network buatan sendiri + DNS internal (nama service = hostname). |
| Reverse proxy | Server (nginx) yang meneruskan request ke server lain (`/api` → backend). |
| Namespaces & cgroups | Teknologi Linux: isolasi "pandangan" sistem (namespaces) dan pembatasan CPU/RAM (cgroups) — alasan container jauh lebih ringan & cepat start dari VM. |
| Multi-stage build | Build di stage berat (compiler/Node), hasilnya disalin ke stage runtime minimal. |
