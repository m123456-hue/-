import re

def reg_search(text, regex_list):
    results = []
    for regex_dict in regex_list:
        result = {}
        for key, pattern in regex_dict.items():
            # 查找所有匹配
            matches = re.findall(pattern, text)
            # 展平元组
            matches = [m if isinstance(m, str) else m[0] for m in matches]
            # 去重
            matches = list(dict.fromkeys(matches))
            # 只返回有内容的
            if matches:
                # 如果是日期，尝试格式化为 yyyy-mm-dd
                if key == '换股期限':
                    # 只保留前两个日期
                    dates = []
                    for m in matches:
                        # 统一格式 yyyy-mm-dd
                        m = m.replace('年', '-').replace('月', '-').replace('日', '').replace(' ', '')
                        if re.match(r'\d{4}-\d{1,2}-\d{1,2}', m):
                            parts = m.split('-')
                            y = parts[0]
                            mth = parts[1].zfill(2)
                            d = parts[2].zfill(2)
                            m = f"{y}-{mth}-{d}"
                        dates.append(m)
                    result[key] = dates[:2]
                else:
                    result[key] = matches[0] if len(matches) == 1 else matches
        if result:
            results.append(result)
    return results

# 示例用法
text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债
券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
'''
regex_list = [{
    '标的证券': r'(\d{6}\.SH)',
    '换股期限': r'(\d{4} 年 \d{1,2} 月 \d{1,2} 日|\d{4}-\d{1,2}-\d{1,2})'
}]
print(reg_search(text, regex_list))
