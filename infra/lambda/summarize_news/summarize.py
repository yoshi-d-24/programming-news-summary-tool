from data_access.api.generative_ai_api_data_access import GenerateAiApiDataAccess
from data_access.secrets_manager.generative_ai_secrets_data_access import GenerateAiSecretsDataAccess

def run(content: str) -> str:
    generative_ai_secrets_data_access = GenerateAiSecretsDataAccess()
    api_key = generative_ai_secrets_data_access.get_secret('API_KEY')

    generate_ai_data_access = GenerateAiApiDataAccess(api_key)

    summary = generate_ai_data_access.summarize(content)

    return summary

if __name__ == '__main__':
    content =     content = '''Yahoo!ニュース（ヤフーニュース）は、日本の企業LINEヤフー[注 1]が運営するポータルサイト『Yahoo! JAPAN』のニュースサイト。日本国内や海外のニュース・話題を多岐にわたり提供するウェブサイトである。1996年7月サービス開始[1]。iOS・Androidスマートフォン用の専用アプリ「Yahoo!ニュースアプリ」もある[2][3]。

    契約パートナーは約300社・約500媒体[1]、個人ニュースオーサーは約500名[1]。1日約4,000本のニュースを配信する[4]。2020年4月の時点で月間PV（ページビュー）は約225億[5]、1日のPVは約5億[4]と、日本国内のニュースサイトではトップシェアである[4]。

    契約パートナーは大手新聞社から小さな会社までさまざまで、見出し(タイトル)には契約パートナー(ニュースのソース)を表示する方針を取っている。個人ニュースの著者も見出しに表示される。

    ロイター・ジャーナリズム研究所の「デジタル・ニュース・レポート」2018年版の調査によれば、日本国内でのニュース利用は「新聞・テレビ・ラジオ」ではNHKが1位だが、インターネットではYahoo!ニュースが1位で、2位のNHKを大きく引き離している[4]。'''
    print(run(content=content))