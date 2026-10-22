import secrets

TOKEN_BYTES = 12


def new_token():
    return secrets.token_hex(TOKEN_BYTES)
