EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'myproject@gmail.com'  # Ваш email
EMAIL_HOST_PASSWORD = 'app_specific_password'  # Пароль приложения Gmail
DEFAULT_FROM_EMAIL = 'My Project <myproject@gmail.com>'
