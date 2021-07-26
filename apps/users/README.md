## User API Rest

### Token Authentication
```json
POST /api/token/

payload:
{
    "username": "jf_superuser",
    "password": "Strong.1"
}

response:
200 OK
{
    "token": "a9dbb4f5d89fc661b716d5fd8bd1fd64e0fb6c9f"
}
```

### JWT Token

Obtener token

```json
POST /api/token-jwt/

payload:
{
    "username": "jf_superuser",
    "password": "Strong.1"
}

response:
200 OK
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNzM0NjQ5OSwianRpIjoiOTRiN2E0OWFiOTE0NDg5ZGE1NjViNjUxMDg4MmI3NzYiLCJ1c2VyX2lkIjozfQ.I2uUdwZBlamKhg_hS92AGMC8cWkZ1xdg_MmtUJT7oPc",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3MjYwMzk5LCJqdGkiOiI3NDUzNGM1YzQ1NmY0MDljYjA2NzMzMmY1MjVlZmJiNSIsInVzZXJfaWQiOjN9.2FYnxm7nxN7ZOS-vUeF3y47onqHXJWwZOUta5UNPVCQ"
}
```

Refrescar token

```json
POST /api/token-jwt/refresh/

payload:
{
    "refresh": "{refresh}"
}

response:
200 OK
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI3MjYxNTAxLCJqdGkiOiJiMjViNWI5YWQ2MDM0MWU0YjdiMzY0MTc2NTIwOGI4YSIsInVzZXJfaWQiOjN9.mqAjIAZ-yaZU4NAeMlfH-XJqRua6_3Nf1hpA3A73TZU"
}
```

### Create users

```json
POST /api/v1/users/

payload:
{
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@ine.test",
    "password": "SuperSecurePasswd",
    "repeat_password": "SuperSecurePasswd",
    "groups": [
        "sales",
        "support",
    ]
}

response:
201 CREATED
{
    "id": "3c9da6cb-e863-46c8-b3ad-f6a100f0a819",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@ine.test",
    "password": "********",
    "groups": [
        "sales",
        "support",
    ],
    "subscription": "active",
    "created": "2021-07-14T15:19:21.671962",
    "updated": "2021-07-14T15:19:21.671962"
}
```

### Update users

```json
PUT /api/v1/users/{id}/
PATCH /api/v1/users/{id}/

payload:
{
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@ine.test",
    "password": "SuperSecureNewPasswd",
    "old_password": "SuperSecurePasswd",
    "groups": [
        "sales",
        "support",
    ]
}

response:
200 OK
{
    "id": "3c9da6cb-e863-46c8-b3ad-f6a100f0a819",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@ine.test",
    "password": "********",
    "groups": [
        "sales",
        "support",
    ],
    "subscription": "active",
    "created": "2021-07-14T15:19:21.671962",
    "updated": "2021-07-14T15:19:21.671962"
}
```

### Retreive users
```json
GET /api/v1/users/{id}/

response for same user:
200 OK
{
    "id": "3c9da6cb-e863-46c8-b3ad-f6a100f0a819",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@ine.test",
    "password": "********",
    "groups": [
        "sales",
        "support",
    ],
    "subscription": "active",
    "created": "2021-07-14T15:19:21.671962",
    "updated": "2021-07-14T15:19:21.671962"
}

response for other users:
200 OK
{
    "id": "3c9da6cb-e863-46c8-b3ad-f6a100f0a819",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Delete users
```json
DELETE /api/v1/users/:uuid

response:
204 NO CONTENT
```
