import pathlib
import textwrap

import google.generativeai as genai

class GenerateAiApiDataAccess:
    def __init__(self, api_key: str) -> None:
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        pass

    def summarize(self, content: str) -> str:
        prompt = f'''以下の文章の要点をまとめ、箇条書きにしてください。
        ${content}
'''
        response = self.model.generate_content(prompt)
        return response.text
