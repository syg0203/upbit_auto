import json
import requests


def send_msg(balance_li):
    bal = "\n".join(balance_li)
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    with open("kakao_token.json", "r") as fp:
        kakaotoken = json.load(fp)
    # 사용자 토큰
    headers = {
        "Authorization": "Bearer " + kakaotoken['access_token']
    }

    data = {
        "template_object": json.dumps({"object_type": "text",
                                       "text": bal,
                                       "link": {
                                           "web_url": "https://www.instagram.com/syg_null/"
                                       }
                                       })
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

send_msg(["hello","world"])
