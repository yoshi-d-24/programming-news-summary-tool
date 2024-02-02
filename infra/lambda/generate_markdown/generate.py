from data_access.s3.pnst_bucket_data_access import PnstBucketDataAccess
from const.codezine import CODEZINE_AGGREGATE_PHRASE
from enums.code import Code
from model.summary_data import Code, SummaryData
from datetime import datetime, timedelta
from collections import defaultdict


def run(code: Code, start_date: str, end_date:str) -> None:
    pnst_bucket_data_access = PnstBucketDataAccess()
    summary_dict: dict[str, list[SummaryData]] = {}
    search_date_list: list[str] = get_dates_in_range(start_date=start_date, end_date=end_date)

    for search_date in search_date_list:
        summary_data_list = pnst_bucket_data_access.get_summary(code=code, search_date=search_date)
        summary_dict[search_date] = summary_data_list


    aggregated_list: list[dict[str, list[SummaryData]]] = []
    for search_date, summary_data_list in summary_dict.items():
        aggregated = aggregate_day_summaries(code=code, summary_data_list=summary_data_list)
        aggregated_list.append(aggregated)

    merged: dict[str, list[SummaryData]] = merge_list_of_dicts(aggregated_list)

    markdown = f'# {start_date} - {end_date}\n\n'
    for lang, summary_data_list in merged.items():
        if len(summary_data_list) == 0:
            continue

        markdown += f'## {lang}\n'
        for summary_data in summary_data_list:
            # add indent
            summary = '\n'.join(list(map(lambda s: f'  {s}' , summary_data.summary.split('\n'))))
            markdown += f'* [{summary_data.title}]({summary_data.uri})\n'
            markdown += f'{summary}\n'
            markdown += '\n'
        
        markdown += '\n'

    current_date = datetime.now()
    today = current_date.strftime("%Y/%m/%d")

    pnst_bucket_data_access.put_markdown(code=code, today=today, start_date=start_date, end_date=end_date, markdown=markdown)

    pass
    # return summary

def aggregate_day_summaries(code: Code, summary_data_list: list[SummaryData]):
    aggregate_phase = []
    if code == Code.CODEZINE:
        aggregate_phase = CODEZINE_AGGREGATE_PHRASE

    aggregated: dict[str, list[SummaryData]] = dict(map(lambda x: (x, []), aggregate_phase))
    aggregated['Others'] = []

    for summary in summary_data_list:
        tag_set = summary.tag_set

        added = False
        for pharse in aggregated.keys():
            if pharse in tag_set:
                aggregated[pharse].append(summary)
                added = True
                break

        if added == False:
            aggregated['Others'].push(summary)

    return aggregated

def get_dates_in_range(start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y/%m/%d")
    end = datetime.strptime(end_date, "%Y/%m/%d")
    date_array = [(start + timedelta(days=x)).strftime("%Y/%m/%d") for x in range(0, (end-start).days+1)]
    return date_array

def merge_list_of_dicts(lst):
    merged = defaultdict(list)
    for dic in lst:
        for key, values in dic.items():
            merged[key].extend(values)
    return dict(merged)

if __name__ == '__main__':
    start_date = '2024/01/25'
    end_date = '2024/01/25'
    run(code=Code.CODEZINE, start_date=start_date, end_date=end_date)
    # content = '''
# 　私が小学校にあがる前まで住んでいた家の風呂は、薪で炊いていたことを覚えている。
# 　風呂の外に焚き口があって、そこに薪を入れて火を焚き、お湯をわかしていた。なにしろ幼いころのことなので詳細は覚えていないが、ガスや、もちろん現在のように自動の湯沸かし器で焚いていたのではなかった。
# 　いまになって気になるのは、風呂を焚くための薪はどうやって調達していたのか、ということだ。'''
    # print(run(content=content))