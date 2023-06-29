from decouple import Config, RepositoryEnv

PROJECT_ENV = 0  # 0 for DEVELOPMENT, 1 for PRODUCTION

if PROJECT_ENV == 1:
    config = Config(RepositoryEnv('.env/.env.prod'))
else:
    config = Config(RepositoryEnv('.env/.env.dev'))

PROJECT_SECRET_KEY = config('PROJECT_SECRET_KEY')
DB_NAME=config('DB_NAME')
EMAIL_BACKEND=config('EMAIL_BACKEND')
EMAIL_HOST=config('EMAIL_HOST')
EMAIL_USE_TLS=config('EMAIL_USE_TLS', cast=bool)
EMAIL_PORT=config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER=config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')