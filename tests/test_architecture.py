from pathlib import Path


def test_vertical_slice_modules_exist() -> None:
    root = Path(__file__).resolve().parents[1]

    expected = [
        root / "app/modules/auth/router.py",
        root / "app/modules/auth/service.py",
        root / "app/modules/auth/schemas.py",
        root / "app/modules/clients/router.py",
        root / "app/modules/carriers/router.py",
        root / "app/modules/transports/router.py",
        root / "app/infrastructure/database/session.py",
        root / "app/infrastructure/storage/minio.py",
        root / "app/infrastructure/email/smtp.py",
    ]

    assert all(path.exists() for path in expected)
