from data_access.api.generative_ai_api_data_access import GenerateAiApiDataAccess
from data_access.secrets_manager.generative_ai_secrets_data_access import GenerateAiSecretsDataAccess
from data_access.s3.pnst_bucket_data_access import PnstBucketDataAccess
from const.codezine import CODEZINE_FILTER_PHRASE
from enum.code import Code
from model.news_data import NewsData
from model.summary_data import SummaryData

def run(code: Code, search_date_list: list[str]) -> None:
    pnst_bucket_data_access = PnstBucketDataAccess()
    generative_ai_secrets_data_access = GenerateAiSecretsDataAccess()
    api_key = generative_ai_secrets_data_access.get_secret('API_KEY')

    generate_ai_data_access = GenerateAiApiDataAccess(api_key)

    news_dict = get_news_dict(code=code, search_date_list=search_date_list)

    for search_date, news_data_list in news_dict.items():

        summaries: list[SummaryData] = []
        for news in news_data_list:
            summary = generate_ai_data_access.summarize(news.content)

            summaries.append(SummaryData(
                code=news.code,
                id=news.id,
                title=news.title,
                uri=f'https://codezine.jp{news.link}',
                date=news.date,
                summary=summary,
                tag_set=news.tag_set
            ))

        pnst_bucket_data_access.put_summary(code=code, search_date=search_date, data_list=summaries)

    pass
    # return summary

def get_news_dict(code: Code, search_date_list: list[str]) -> dict[str, list[NewsData]]:
    pnst_bucket_data_access = PnstBucketDataAccess()
    news_dict: dict[str, list[NewsData]] = {}

    for search_date in search_date_list:
        exists_summary = pnst_bucket_data_access.exist_summary(code=code, search_date=search_date)

        if exists_summary:
            continue

        news_data_list = pnst_bucket_data_access.get_news(code=code, search_date=search_date)
        news_dict[search_date] = filter_news_by_tags(code=code, news_data_list=news_data_list)

    return news_dict

def filter_news_by_tags(code: Code, news_data_list: list[NewsData]) -> list[NewsData]:
    if code == Code.CODEZINE:
        filter_pharses = CODEZINE_FILTER_PHRASE

    ret = []
    for news in news_data_list:
        for pharse in filter_pharses:
            if pharse in news.tag_set:
                ret.append(news)
                continue

            if pharse in news.title:
                ret.append(news)
                continue

    return ret


if __name__ == '__main__':
    search_date_list = ['2024/01/25']
    run(search_date_list=search_date_list)
    # content = '''
# 　私が小学校にあがる前まで住んでいた家の風呂は、薪で炊いていたことを覚えている。
# 　風呂の外に焚き口があって、そこに薪を入れて火を焚き、お湯をわかしていた。なにしろ幼いころのことなので詳細は覚えていないが、ガスや、もちろん現在のように自動の湯沸かし器で焚いていたのではなかった。
# 　いまになって気になるのは、風呂を焚くための薪はどうやって調達していたのか、ということだ。'''
    # print(run(content=content))