from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import webbrowser
from urllib.parse import urlencode, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
import time
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "https://localhost:3000",
    "scope": "user-library-read"
}

driver.get("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

def get_token(token_data):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    result = post(url, headers=headers, data=token_data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_top(token):
    url = "https://api.spotify.com/v1/me/top/artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=AU"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def search_for_user(token, user_name):
    url = "https://api.spotify.com/v1/me"
    headers = get_auth_header(token)
    query = f"?q={user_name}"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result
while driver.current_url[8:13] != "local":
    time.sleep(1)
code = driver.current_url.split("=")[1]
token_data = {"grant_type": "authorization_code", "code": code, "redirect_uri": "https://localhost:3000"}
token = get_token(token_data)
print(search_for_top(token))
