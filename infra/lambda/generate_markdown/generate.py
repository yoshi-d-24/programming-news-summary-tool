from data_access.s3.pnst_bucket_data_access import PnstBucketDataAccess
from generate_markdown.const.codezine import CODEZINE_AGGREGATE_PHRASE
from enum.code import Code
from model.summary_data import Code, SummaryData

# def run(content: str) -> str:
def run(code: Code, search_date_list: list[str]) -> None:
    pnst_bucket_data_access = PnstBucketDataAccess()
    summary_dict: dict[str, list[SummaryData]] = {}

    for search_date in search_date_list:
        summary_data_list = pnst_bucket_data_access.get_summary(code=code, search_date=search_date)
        summary_dict[search_date] = summary_data_list

    for search_date, summary_data_list in summary_dict.items():
        aggregated = aggregate(code=code, summary_data_list=summary_data_list)

        markdown = f'# {search_date}\n'
        for lang, inner_summary_data_list in aggregated:

            markdown += f'## {lang}\n'
            for summary in inner_summary_data_list:
                markdown += f'* {summary.title}\n'
                markdown += f'{summary.link}\n'
                markdown += f'{summary.content}\n'
                markdown += '\n'

        pnst_bucket_data_access.put_markdown(code=code, search_date=search_date, markdown=markdown)

    pass
    # return summary

def aggregate(code: Code, summary_data_list: list[SummaryData]):
    aggregate_phase = []
    if code == Code.CODEZINE:
        aggregate_phase = CODEZINE_AGGREGATE_PHRASE

    aggreagated: dict[str, list[SummaryData]] = dict(map(lambda x: (x, []), aggregate_phase))

    for summary in summary_data_list:
        tag_set = summary.tag_set

        for pharse in aggregate.keys():
            if pharse in tag_set:
                aggreagated[pharse].append(summary)
                continue

            if pharse in summary.title:
                aggreagated[pharse].append(summary)
                continue

    return aggreagated

if __name__ == '__main__':
    search_date_list = ['2024/01/25']
    run(search_date_list=search_date_list)
    # content = '''
# 　私が小学校にあがる前まで住んでいた家の風呂は、薪で炊いていたことを覚えている。
# 　風呂の外に焚き口があって、そこに薪を入れて火を焚き、お湯をわかしていた。なにしろ幼いころのことなので詳細は覚えていないが、ガスや、もちろん現在のように自動の湯沸かし器で焚いていたのではなかった。
# 　いまになって気になるのは、風呂を焚くための薪はどうやって調達していたのか、ということだ。'''
    # print(run(content=content))