# -*- coding: utf-8 -*-
# 医疗器械生产企业（许可）
import pickle
import re
from selenium import webdriver
from gjypjd.utils import *
import json
import time
def main():
    option=None
    mysql_db = DataBase()
    #配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')
    for i in range(1, 156):  # 遍历155个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=132&State=1&bcId=154209313929078698414236686309&State=1&curstart='+str(i)+'&State=1&tableName=TABLE132&State=1&viewtitleName=COLUMN1801&State=1&viewsubTitleName=COLUMN1802&State=1&tableView=%25E5%258C%25BB%25E7%2596%2597%25E5%2599%25A8%25E6%25A2%25B0%25E7%2594%259F%25E4%25BA%25A7%25E4%25BC%2581%25E4%25B8%259A%25EF%25BC%2588%25E8%25AE%25B8%25E5%258F%25AF%25EF%25BC%2589&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=132&tableName=TABLE132&tableView=医疗器械生产企业（许可）&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ylqxscqy_xk(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    """
    许可证编号xkzbh
    企业名称qymc
    法定代表人fddbr
    企业负责人qyfzr
    住所zs
    生产地址scdz
    生产范围scfw
    发证部门fzbm
    发证日期dzrq
    有效期限yxqx
    注z
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['xkzbh'] = r"许可证编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['qymc'] = r"企业名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fddbr'] = r"法定代表人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['qyfzr'] = r"企业负责人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zs'] = r"住所</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scdz'] = r"生产地址</td>\s*<td.*?>(.*)</td></tr>"
    reg_dict['scfw'] = r"生产范围</td>\s*<td.*?>(.*)</td></tr>"
    reg_dict['fzbm'] = r"发证部门</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dzrq'] = r"发证日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxqx'] = r"有效期限</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['z'] = r"注</td>\s*<td.*><span.*>(.*)</span></td></tr>"

    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)
if __name__ == '__main__':
    main()
