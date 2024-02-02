import requests
import json


class GenerateAiApiDataAccess:
    def __init__(self, api_key: str) -> None:
        self.url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
        pass

    def summarize(self, content: str) -> str:
        prompt = f'''以下の文章の要点をマークダウン形式の箇条書きにしてください。箇条書きの記号には * を用いてください。
        ${content}
'''
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # ヘッダー
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
        }

        # POSTリクエストの送信
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        res_dict = json.loads(response.text)

        text_list = []

        for candidate in res_dict['candidates']:
            parts = candidate['content']['parts']

            parts_text_list = []

            for part in parts:
                parts_text_list.append(part['text'])
            
            text_list.append('\n'.join(parts_text_list))

        joined = '\n\n'.join(text_list)
        return joined
