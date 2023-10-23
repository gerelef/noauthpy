#!/usr/bin/env -S python3.12 -i 
# FIXME remove interactive
from time import time
from typing import Any
import requests as req
import enum
import json 
import re

class _Fields(enum.StrEnum):
    TOKEN = "accessToken"
    TOKEN_EXPIRATION_TIME = "accessTokenExpirationTimestampMs"
    IS_ANONYMOUS = "isAnonymous"
    CLIENT_ID = "clientId"

type URL = str
type Token = dict[str, Any]
type AuthorizationHeader = dict[str, str]

def get_spotify_token(url: URL="https://open.spotify.com/search", timeout_seconds=1) -> Token:
    """
    Get an anonymous Spotify Token.
    :param url: url to get the token from
    :param timeout_seconds: timeout in seconds
    :returns Token: return a json (dict) which contains the anonymous Token
    :raises IndexError: when there's no match for the Spotify Token
    :raises requests.exceptions.ConnectionError: See Requests.ConnectionError documentation.
    :raises requests.exceptions.Timeout: See Requests.Timeout documentation.
    :raises requests.exceptions.HTTPError: See Requests.HTTPError documentation.
    """
    # this is a hack, but what saves it is probably the fact that this is going to be a unique string in the response  
    json_token_regex = '<script id="session" data-testid="session" type="application/json">({.*})</script>'
    res = req.get(url, timeout=timeout_seconds)
    # json.loads is needed to provide access to individual fields
    return json.loads(re.findall(json_token_regex, res.text)[0])

def token_has_expired(token: Token) -> bool:
    return token[_Fields.TOKEN_EXPIRATION_TIME.value] - int(time()*1000) <= 1

def token_as_header(token: Token) -> AuthorizationHeader:
    return { "Authorization": f"Bearer {token[_Fields.TOKEN.value]}" }

def token_as_valid_json(token: Token) -> str:
    # json.dumps is needed since python prints wrong quotes (single quotes, not double quotes) which are specified by RFC 8259
    return json.dumps({ "Authorization": f"Bearer {token[_Fields.TOKEN.value]}" })


if __name__ == "__main__":
    # Using this library is as simple as using the header token and inserting it on the GET request's header
    # Same restrictions as `noauth` apply; you can only make anonymous requests, 
    #  which means you can't access any user data or make POST requests. 
    tok = get_spotify_token()
    print(tok)
    print(token_as_header(tok))
    print(type(token_as_header(tok)))
    print(token_as_valid_json(tok))
    print(type(token_as_valid_json(tok)))
