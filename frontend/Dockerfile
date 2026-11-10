# ============================================================
# BookVerse frontend - MULTI-STAGE build
# Stage 1 (builder): Node builds the React/Vite bundle
# Stage 2 (runtime): nginx serves the static files (~50 MB image)
# ============================================================

# ---------- Stage 1: builder ----------
# Version-specific tag (NOT latest)
FROM node:22.11.0-alpine3.20 AS builder

WORKDIR /build

# Dependency layer first: cached unless package.json changes
COPY package.json package-lock.json* ./
RUN npm install

# Source copied only after dependencies are installed
COPY . .
RUN npm run build

# ---------- Stage 2: runtime ----------
FROM nginx:1.27.2-alpine AS runtime

# Static bundle from the builder stage
COPY --from=builder /build/dist /usr/share/nginx/html

# nginx config: SPA routing + reverse proxy /api -> backend:8000
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Exec form: nginx stays in the foreground as PID 1
CMD ["nginx", "-g", "daemon off;"]
