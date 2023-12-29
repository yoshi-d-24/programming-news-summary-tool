from data_access.api.generative_ai_api_data_access import GenerateAiApiDataAccess
from data_access.secrets_manager.generative_ai_secrets_data_access import GenerateAiSecretsDataAccess

def run(content: str) -> str:
    generative_ai_secrets_data_access = GenerateAiSecretsDataAccess()
    api_key = generative_ai_secrets_data_access.get_secret('API_KEY')

    generate_ai_data_access = GenerateAiApiDataAccess(api_key)

    summary = generate_ai_data_access.summarize(content)

    return summary

if __name__ == '__main__':
    content = '''
　私が小学校にあがる前まで住んでいた家の風呂は、薪で炊いていたことを覚えている。
　風呂の外に焚き口があって、そこに薪を入れて火を焚き、お湯をわかしていた。なにしろ幼いころのことなので詳細は覚えていないが、ガスや、もちろん現在のように自動の湯沸かし器で焚いていたのではなかった。
　いまになって気になるのは、風呂を焚くための薪はどうやって調達していたのか、ということだ。'''
    print(run(content=content))