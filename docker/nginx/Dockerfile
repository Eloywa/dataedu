# nginx перед DataEdu.
#
# Конфигурация вшита в образ, а не подключается томом: образ, собранный один раз,
# везде поднимается одинаково, и на сервере нечему разъехаться с репозиторием.
#
# Статику nginx берёт из тома /var/www/static, который наполняет контейнер
# приложения при запуске (см. docker/entrypoint.sh), — копировать 18 МБ вендора
# во второй образ незачем.

FROM nginx:1.27-alpine

# Свой конфиг вместо стандартного: default.conf отдаёт приветственную страницу
# nginx на том же порту и перехватывал бы корень сайта.
RUN rm /etc/nginx/conf.d/default.conf
COPY dataedu.conf /etc/nginx/conf.d/dataedu.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=4s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://127.0.0.1/static/css/app.css || exit 1
