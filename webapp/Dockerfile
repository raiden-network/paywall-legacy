FROM node:alpine
RUN npm install -g pnpm
WORKDIR .
COPY . . 
RUN pnpm install && pnpm run build

FROM flashspys/nginx-static
RUN apk update && apk upgrade
COPY --from=0 ./dist /static
