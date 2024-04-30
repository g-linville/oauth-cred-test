LOGIN_MANAGER_ENDPOINT = "http://localhost:3000"  # TODO - change this to the actual endpoint

SERVICES = ["spotify"]

REFRESH_DOMAINS = {
    "spotify": "https://accounts.spotify.com/api/token",
}

SCOPES = {
    "spotify": [  # Source: https://developer.spotify.com/documentation/web-api/concepts/scopes
        "user-read-currently-playing",
        "playlist-read-private",
        "playlist-read-collaborative",
        "playlist-modify-private",
        "playlist-modify-public",
        "user-follow-modify",
        "user-follow-read",
        "user-top-read",
        "user-read-recently-played",
        "user-library-modify",
        "user-library-read",
        "user-read-email",
        "user-read-private",
    ]
}
