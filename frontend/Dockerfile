FROM node:20-slim AS base

WORKDIR /app

FROM base AS deps

COPY package.json package-lock.json ./
RUN npm ci

FROM deps AS builder

COPY . .
RUN npm run build

FROM deps AS dev

COPY . .

EXPOSE 15173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "15173"]

FROM base AS runtime

ENV NODE_ENV=production

COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY --from=builder /app/build ./build

EXPOSE 15173

CMD ["node", "build"]
