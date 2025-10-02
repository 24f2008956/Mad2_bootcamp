class LocalDevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///my_db.sqlite3"
    SECURITY_PASSWORD_SALT = "mysecretsalt"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECRET_KEY = "mysecretkey"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_TOKEN_MAX_AGE = 7200  # 2 hour