# cors
import os

# Для development разрешить все origins
# В production закомментируйте эту строку и используйте CORS_ALLOWED_ORIGINS
DEBUG = os.getenv("DEBUG", "True") == "True"

if DEBUG:
    # В режиме разработки разрешаем все origins
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # В production используем белый список
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        # backend
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://finance.smarthouse.website:8000",
        "https://finance.smarthouse.website:8000",
        # frontend
        "https://finance.smarthouse.website",
        "http://finance.smarthouse.website",
        "http://103.88.243.13:4343",
        "https://103.88.243.13:4343",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # other
        "http://localhost",
        "http://127.0.0.1",
    ]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Важные заголовки для работы с токенами
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True

# CSRF trusted origins (только для production)
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
else:
    CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
