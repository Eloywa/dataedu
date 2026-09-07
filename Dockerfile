# Образ приложения DataEdu: Django под gunicorn.
#
# Статику отдаёт nginx (см. docker/nginx), а не приложение. Разница здесь не
# вкусовая: в static/vendor лежит движок PGlite на 18 МБ, и каждая его загрузка
# занимала бы рабочий процесс gunicorn целиком. На занятии, когда тренажёр
# открывает вся группа сразу, свободных процессов не осталось бы вовсе.
#
# Python 3.13 — не «посвежее», а обязательное требование: проект использует
# models.CompositePrimaryKey, появившийся в Django 5.2, а он требует 3.13.

FROM python:3.13-slim

# PYTHONDONTWRITEBYTECODE — .pyc в слоях образа не нужны; PYTHONUNBUFFERED —
# иначе логи Django копятся в буфере и не доходят до journald вовремя.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

# Зависимости отдельным слоем: правка кода не должна заставлять ставить их заново.
# psycopg[binary] везёт libpq внутри колеса, поэтому ни gcc, ни libpq-dev не нужны
# и образ остаётся slim.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Сборка статики на этапе сборки образа, а не при запуске: она занимает время
# (18 МБ вендора сжимаются и получают хеши в именах), и платить это время при
# каждом перезапуске контейнера незачем.
#
# Профиль prod намеренно отказывается стартовать без настоящего SECRET_KEY и
# параметров БД. collectstatic до базы не дотрагивается, но настройки читаются
# целиком, поэтому здесь подставляются заведомо временные значения — только на
# время этой команды. В образ они не попадают: переменные заданы внутри RUN.
RUN DJANGO_ENV=prod \
    SECRET_KEY=build-time-placeholder-not-used-at-runtime-0123456789 \
    DB_HOST=localhost \
    python manage.py collectstatic --noinput --clear

# Обычный пользователь: процесс в контейнере не должен быть root.
# Каталог тома статики создаётся заранее и отдаётся ему же — иначе entrypoint
# не сможет туда писать.
RUN useradd --system --create-home --uid 10001 dataedu \
    && mkdir -p /var/www/static \
    && chmod +x /app/docker/entrypoint.sh \
    && chown -R dataedu:dataedu /app /var/www/static
USER dataedu

EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]

# Проверка живости — по странице входа: она не требует ни сессии, ни базы курсов,
# но проходит через весь цикл Django, то есть отвечает «приложение работает»,
# а не «порт открыт».
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/login/', timeout=4).status == 200 else 1)"

# Воркеров — по числу ядер: WEB_CONCURRENCY читает сам gunicorn.
# Таймаут больше стандартных 30 с: отчёты преподавателя по большому потоку
# считаются дольше, и обрывать их на середине хуже, чем подождать.
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
