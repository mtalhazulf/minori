FROM node:18-alpine3.16 as builder
WORKDIR /app
COPY . .

RUN yarn --immutable
RUN npx eslint --fix src/
RUN yarn build

RUN chmod +x ./dist/spa/set-env.sh

FROM caddy:2.6.2-alpine
WORKDIR /app

COPY --from=builder /app/dist/spa ./

COPY ./docker/Caddyfile /

EXPOSE 8080

CMD ["/bin/sh", "-c", "./set-env.sh; caddy run --config /Caddyfile"]
