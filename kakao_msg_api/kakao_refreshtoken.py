import requests
import json
import schedule


def refresh():
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": "id",
        "refresh_token": "token"
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    # print(response.json())

    with open("kakao_token.json", "w") as fp:
        json.dump(tokens, fp)


# schedule.every().monday.do(refresh)

# while True:
#     schedule.run_pending()
