import requests
import json


def get_iam_token(oauth_token):
    r = requests.request(
        'POST',
        'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        headers={'Content-type': 'application/json'},
        data=json.dumps({'yandexPassportOauthToken': oauth_token})

    )
    iam_token = r.json()['iamToken']

    return iam_token


def synthesize(text, iam_token, folder_id, lang='ru-RU', voice='oksana', emotion='neutral', speed=1.0, form='oggopus',
               sample_rate=48000):
    r = requests.request(
        'POST',
        'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
        headers={
            'Authorization': 'Bearer ' + iam_token
        },
        data={
            'text': text,
            'lang': lang,
            'voice': voice,
            'emotion': emotion,
            'speed': speed,
            'format': form,
            'sampleRateHertz': sample_rate,
            'folderId': folder_id
        },
        stream=True
    )

    return r
