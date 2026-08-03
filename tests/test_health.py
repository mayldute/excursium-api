import os

os.environ.setdefault("APP__APP_NAME", "Excursium API")
os.environ.setdefault("APP__DEBUG", "False")
os.environ.setdefault("APP__ENV", "test")
os.environ.setdefault("DATABASE__DB_LOGIN", "test")
os.environ.setdefault("DATABASE__DB_PASS", "test")
os.environ.setdefault("DATABASE__DB_HOST", "localhost")
os.environ.setdefault("DATABASE__DB_PORT", "5432")
os.environ.setdefault("DATABASE__DB_NAME", "test")
os.environ.setdefault(
    "DATABASE__DATABASE_URL",
    "postgresql+asyncpg://test:test@localhost:5432/test",
)
os.environ.setdefault("JWT__JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT__JWT_ALGORITHM", "HS256")
os.environ.setdefault("JWT__JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("JWT__JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7")
os.environ.setdefault("SMTP__SMTP_SERVER", "smtp.example.com")
os.environ.setdefault("SMTP__SMTP_PORT", "465")
os.environ.setdefault("SMTP__SMTP_USERNAME", "test")
os.environ.setdefault("SMTP__SMTP_PASSWORD", "test")
os.environ.setdefault("SMTP__FROM_EMAIL", "test@example.com")
os.environ.setdefault("MINIO__MINIO_ENDPOINT", "localhost:9000")
os.environ.setdefault("MINIO__MINIO_ACCESS_KEY", "test")
os.environ.setdefault("MINIO__MINIO_SECRET_KEY", "test")
os.environ.setdefault("MINIO__MINIO_BUCKET_NAME", "test")
os.environ.setdefault("MINIO__MINIO_SECURE", "False")
os.environ.setdefault("GOOGLE__GOOGLE_CLIENT_ID", "test")
os.environ.setdefault("GOOGLE__GOOGLE_CLIENT_SECRET", "test")
os.environ.setdefault(
    "GOOGLE__GOOGLE_REDIRECT_URI",
    "http://localhost/google",
)
os.environ.setdefault("YANDEX__YANDEX_CLIENT_ID", "test")
os.environ.setdefault("YANDEX__YANDEX_CLIENT_SECRET", "test")
os.environ.setdefault(
    "YANDEX__YANDEX_REDIRECT_URI",
    "http://localhost/yandex",
)

from fastapi.testclient import TestClient

from app.main import app


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
