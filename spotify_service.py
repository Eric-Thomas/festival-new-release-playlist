import os
import requests
import json


class SpotifyService:

    OAUTH_URL = "https://accounts.spotify.com/api/token"
    GET_PLAYLISTS_URL = "https://api.spotify.com/v1/me/playlists?limit=50"
    CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/user_id/playlists"
    GET_USER_PROFILE = "https://api.spotify.com/v1/me"

    def __init__(self) -> None:
        self.oauth_token = self._get_oauth_token()
        self.playlist_href = None
        self._initialize_playlist()

    def add_new_releases(self, releases):
        pass

    def _get_oauth_token(self):
        refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")

        payload = f"grant_type=refresh_token&refresh_token={refresh_token}"
        headers = {
            "Authorization": f'Basic {os.environ.get("BASIC_ENCODED_AUTHORIZATION")}',
            "Content-Type": "application/x-www-form-urlencoded",
        }

        print(f"Getting oauth token from {self.OAUTH_URL}")

        response = requests.request(
            "POST", self.OAUTH_URL, headers=headers, data=payload
        ).json()

        return response.get("access_token")

    def _initialize_playlist(self):
        playlist_name = os.environ.get("PLAYLIST_NAME")
        existsing_playlists = self._get_existing_playlists()
        for playlist in existsing_playlists:
            if playlist_name == playlist["name"]:
                print(f"Playlist already exists href - {playlist['href']}")
                self._set_playlist_href(playlist["href"])
                return

        self._set_playlist_href(self._create_playlist())

    def _get_playlist_href(self):
        return self.playlist_href

    def _set_playlist_href(self, href):
        self.playlist_href = href

    def _get_existing_playlists(self):
        existing_playlists = []
        current_url = self.GET_PLAYLISTS_URL
        while current_url:

            print(f"Getting current playlists at {current_url}")
            response = requests.request(
                "GET", current_url, headers=self._get_headers()
            ).json()
            for playlist in response["items"]:
                current_playlist = {}
                current_playlist["name"] = playlist["name"]
                current_playlist["href"] = playlist["href"]
                existing_playlists.append(current_playlist)

            current_url = response.get("next")

        return existing_playlists

    def _create_playlist(self):
        playlist_name = os.environ.get("PLAYLIST_NAME")
        playlist_description = os.environ.get("PLAYLIST_DESCRIPTION")
        print(f"Creating playlist {playlist_name}")

        user_id = self._get_user_id()
        url = self.CREATE_PLAYLIST_URL.replace("user_id", user_id)

        payload = json.dumps(
            {"name": playlist_name, "description": playlist_description}
        )

        print(f"Creating playlist at {url}")
        response = requests.request(
            "POST", url, headers=self._get_headers(), data=payload
        ).json()

        return response["href"]

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.oauth_token}",
            "Content-Type": "application/json",
        }

    def _get_user_id(self):
        print(f"Getting user profile at {self.GET_USER_PROFILE}")

        response = requests.request(
            "GET", self.GET_USER_PROFILE, headers=self._get_headers()
        ).json()

        return response["id"]
