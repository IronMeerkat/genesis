FROM node:16 as starter

WORKDIR /usr/src/app

COPY ./ ./

RUN yarn install

FROM starter as intermediate

RUN yarn build

FROM nginx:1.21.3 as prod

COPY --from=intermediate /usr/src/app/build /home/nginx/build

COPY --from=intermediate /usr/src/app/nginx /etc/nginx/conf.d
