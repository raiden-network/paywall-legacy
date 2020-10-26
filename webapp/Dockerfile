FROM node:alpine
RUN npm install -g pnpm
WORKDIR .
COPY . . 
ARG VUE_APP_CONTENT_BASE_URL
ARG VUE_APP_LIGHTCLIENT_URL
RUN pnpm install && pnpm run build

FROM flashspys/nginx-static
RUN apk update && apk upgrade
COPY --from=0 ./dist /static
