import time

import jwt


# Can be used to easily generate a encoded JWT token given the client_id and secret
def generate_jwt_token(client_id: str, secret: str, user_representation: str = "") -> str:
    payload = {
        # standard claims
        "iss": "testsuite",
        "iat": int(time.time()),
        # custom
        "client_id": client_id,
        "user_id": client_id,
        "user_representation": user_representation,
    }

    encoded = jwt.encode(payload, secret, algorithm="HS256")
    return str(encoded)
