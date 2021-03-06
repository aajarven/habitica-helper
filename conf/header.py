"""
The static header info Habitica requires.
"""
from conf.secrets.habitica_credentials import PLAYER_USER_ID, PLAYER_API_TOKEN

HEADER = {
    "x-client":
        "f687a6c7-860a-4c7c-8a07-9d0dcbb7c831-habitica-challenge-helper",
    "x-api-user": PLAYER_USER_ID,
    "x-api-key":  PLAYER_API_TOKEN,
}
