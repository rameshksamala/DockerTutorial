# Multi-stage Dockerfile — Node.js Application
# -----------------------------------------------
# Multi-stage builds keep the final image lean by
# separating the build environment from the runtime.

# ── Stage 1: Build ──────────────────────────────
FROM node:18-alpine AS builder

WORKDIR /app

# Copy dependency manifests first (leverages Docker layer cache)
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# ── Stage 2: Production Runtime ─────────────────
FROM node:18-alpine AS production

# Create a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy only what's needed from the builder stage
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/src ./src
COPY --from=builder /app/package.json .

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# Start the application
CMD ["node", "src/index.js"]
