from .server import PROJECT_ENV

if PROJECT_ENV == 1:
    PASSWORD_RESET_LINK_EXPIRY_MINS=30
    SITE_URL="https://a9f1-2401-4900-1f3f-6f37-11e4-9052-9305-815b.ngrok-free.app"
else:
    PASSWORD_RESET_LINK_EXPIRY_MINS=10
    SITE_URL="https://a9f1-2401-4900-1f3f-6f37-11e4-9052-9305-815b.ngrok-free.app"
    