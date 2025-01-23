class ConfigAPP:
    APP_TITLE = "Блог"
    APP_DESCRIPTION = "Базовые функции блога. CRUD для юзера и постов"
    APP_VERSION = "0.0.1"
    OPENAPI_TAGS = [
        {
            "name": "Users",
            "description": "Operations with users: create, read, update, delete."
        },
        {
            "name": "Posts",
            "description": "Operations with posts: create, read, delete."
        }
    ]
