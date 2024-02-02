from data_access.s3.pnst_bucket_data_access import PnstBucketDataAccess
from model.summary_data import SummaryData

# def run(content: str) -> str:
def run(search_date_list: list[str]) -> None:
    pnst_bucket_data_access = PnstBucketDataAccess()
    summary_dict: dict[str, list[SummaryData]] = {}

    for d in search_date_list:
        summary_data_list = pnst_bucket_data_access.get_summary(d)
        summary_dict[d] = summary_data_list

    for k, v in summary_dict.items():
        aggregated = aggregate(v)

        for l, sdl in aggregated:
            
            pnst_bucket_data_access.put_summary(search_date=k, data_list=summaries)

    pass
    # return summary

def aggregate(summary_data_list: list[SummaryData]):
    a: dict[str, list[SummaryData]] = {
        'Python': [],
        'Java': [],
        'JavaScript': [],
        'TypeScript': [],
        'C#': [],
        '.NET': [],
    }

    for s in summary_data_list:
        ts = s.tag_set

        for l in a.keys():
            if l in ts:
                a[l].append(s)

    return a

if __name__ == '__main__':
    search_date_list = ['2024/01/25']
    run(search_date_list=search_date_list)
    # content = '''
# 　私が小学校にあがる前まで住んでいた家の風呂は、薪で炊いていたことを覚えている。
# 　風呂の外に焚き口があって、そこに薪を入れて火を焚き、お湯をわかしていた。なにしろ幼いころのことなので詳細は覚えていないが、ガスや、もちろん現在のように自動の湯沸かし器で焚いていたのではなかった。
# 　いまになって気になるのは、風呂を焚くための薪はどうやって調達していたのか、ということだ。'''
    # print(run(content=content))