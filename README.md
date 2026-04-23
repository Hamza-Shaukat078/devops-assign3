# DevOps Assignment 3 — Containerization with Docker
<img width="975" height="145" alt="image" src="https://github.com/user-attachments/assets/af9cdcd0-fad7-4fa9-a66e-361dac8c0a58" />
<img width="975" height="378" alt="image" src="https://github.com/user-attachments/assets/8faf654f-ffbc-4e86-bb0f-cf3638760c27" />


Assignment 3 of the DevOps course series. Covers the fundamentals of containerizing an application with Docker — from writing an optimized Dockerfile to running, networking, and managing containers on a Linux host.

---

## Objectives

- Write a production-quality Dockerfile using multi-stage builds
- Minimize final image size by separating build and runtime stages
- Run containers with port mapping, volume mounts, and custom networks
- Manage the container lifecycle (build, run, inspect, stop, remove)
- Push the image to Docker Hub

---

## Project Structure

```
devops-assign3/
├── Dockerfile                   # Multi-stage container build definition
├── .dockerignore                # Files excluded from build context
├── app/
│   └── ...                      # Application source code
├── scripts/
│   └── run.sh                   # Helper script to build and run locally
└── README.md
```

---

## Dockerfile — Multi-Stage Build

Using multi-stage builds keeps the final image lean by discarding build tools, compilers, and dev dependencies that aren't needed at runtime.

```dockerfile
# ── Stage 1: Build ────────────────────────────────────────────
FROM node:18-alpine AS builder

WORKDIR /app

# Copy dependency manifests first (layer caching optimization)
COPY package*.json ./
RUN npm ci --only=production

# Copy source and build
COPY . .
RUN npm run build

# ── Stage 2: Runtime ──────────────────────────────────────────
FROM node:18-alpine AS runtime

# Create non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy only production artifacts from builder stage
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

USER appuser

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Why Multi-Stage?

| Metric | Single-Stage | Multi-Stage |
|--------|-------------|-------------|
| Image size | ~800 MB | ~120 MB |
| Attack surface | High (includes dev tools) | Low (runtime only) |
| Build tools in prod | Yes | No |

---

## .dockerignore

```
node_modules/
.git/
*.log
.env
coverage/
dist/
README.md
```

Excluding these from the build context speeds up `docker build` and prevents accidental secret leakage (e.g., `.env` files).

---

## Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/Hamza-Shaukat078/devops-assign3.git
cd devops-assign3
```

### 2. Build the Docker image
```bash
docker build -t hamzashaukat/assign3-app:v1 .
```

### 3. Run the container
```bash
# Basic run with port mapping
docker run -d \
  --name assign3_app \
  -p 3000:3000 \
  hamzashaukat/assign3-app:v1

# With environment variables and volume mount
docker run -d \
  --name assign3_app \
  -p 3000:3000 \
  -e NODE_ENV=production \
  -v $(pwd)/logs:/app/logs \
  hamzashaukat/assign3-app:v1
```

### 4. Verify the container
```bash
docker ps                             # Confirm running
docker logs assign3_app               # View output
docker exec -it assign3_app sh        # Open interactive shell
curl http://localhost:3000            # Test the app
```

### 5. Push to Docker Hub
```bash
docker login
docker push hamzashaukat/assign3-app:v1
```

### 6. Stop and clean up
```bash
docker stop assign3_app
docker rm assign3_app
docker rmi hamzashaukat/assign3-app:v1
```

---

## Container Networking

```bash
# Create a custom bridge network
docker network create assign3_net

# Run container on custom network
docker run -d --name assign3_app --network assign3_net -p 3000:3000 hamzashaukat/assign3-app:v1

# Containers on the same network resolve each other by name
docker run -it --network assign3_net alpine ping assign3_app
```

---

## Key Concepts Demonstrated

- **Layer caching** — `COPY package*.json` before source code so dependency install is cached unless `package.json` changes
- **Non-root user** — container runs as `appuser`, not root, reducing privilege escalation risk
- **Build context optimization** — `.dockerignore` reduces context size and prevents secret leakage
- **Port mapping** — `-p host:container` exposes the service without exposing the container directly
- **Volume mounts** — persistent or shared data without rebuilding the image

---

## Author

**Hamza Shaukat** — BS Cybersecurity, COMSATS University Islamabad  
[GitHub](https://github.com/Hamza-Shaukat078) · [LinkedIn](https://www.linkedin.com/in/hamza-shaukat-7185792b7/)
