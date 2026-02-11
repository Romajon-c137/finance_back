# cors
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOWED_ORIGINS = [
    # beck
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # front
    "https://finance.smarthouse.website",
    "http://finance.smarthouse.website",
    "http://103.88.243.13:4343",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # other
    "http://localhost",
    "http://127.0.0.1",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
