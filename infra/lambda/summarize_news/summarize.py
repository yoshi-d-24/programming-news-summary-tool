from data_access.api.generative_ai_api_data_access import GenerateAiApiDataAccess
from data_access.secrets_manager.generative_ai_secrets_data_access import GenerateAiSecretsDataAccess
from data_access.s3.pnst_bucket_data_access import PnstBucketDataAccess
from model.news_data import NewsData
from model.summary_data import SummaryData

# def run(content: str) -> str:
def run(search_date_list: list[str]) -> None:
    pnst_bucket_data_access = PnstBucketDataAccess()
    generative_ai_secrets_data_access = GenerateAiSecretsDataAccess()
    api_key = generative_ai_secrets_data_access.get_secret('API_KEY')

    generate_ai_data_access = GenerateAiApiDataAccess(api_key)

    news_dict: dict[str, list[NewsData]] = {}

    for d in search_date_list:
        news_data_list = pnst_bucket_data_access.get_news(d)
        news_dict[d] = news_data_list

    for k, v in news_dict.items():

        summaries: list[SummaryData] = []
        for n in v:
            summary = generate_ai_data_access.summarize(n.content)

            summaries.append(SummaryData(
                id=n.id,
                title=n.title,
                uri=f'https://codezine.jp{n.link}',
                date=n.date,
                summary=summary,
                tag_set=n.tag_set
            ))

        pnst_bucket_data_access.put_summary(search_date=k, data_list=summaries)

    pass
    # return summary

if __name__ == '__main__':
    search_date_list = ['2024/01/25']
    run(search_date_list=search_date_list)
    # content = '''
# 　私が小学校にあがる前まで住んでいた家の風呂は、薪で炊いていたことを覚えている。
# 　風呂の外に焚き口があって、そこに薪を入れて火を焚き、お湯をわかしていた。なにしろ幼いころのことなので詳細は覚えていないが、ガスや、もちろん現在のように自動の湯沸かし器で焚いていたのではなかった。
# 　いまになって気になるのは、風呂を焚くための薪はどうやって調達していたのか、ということだ。'''
    # print(run(content=content))