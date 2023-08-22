import requests
import json

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": "client_id",
    "redirect_uri": "https://localhost.com",
    "code": "code"

}
response = requests.post(url, data=data)

tokens = response.json()

print(tokens)
with open("kakao_token.json", "w") as fp:
    json.dump(tokens, fp)
