# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import csv
import os

#locationName 
#prec_no 都道府県名
#block_no　市名
def takeDataByMonth(locationName,prec_no,block_no,year,month):
    #define url
    url_str = 'http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no={}&block_no={}&year={}&month={}&day=&view=p1'.format(str(prec_no),str(block_no),str(year),str(month))

    location = []
    date = []
    average_temp = []
    highest_temp = []
    lowest_temp = []
    day_status = []
    night_status = []



    #output folder declare
    output_path = "./output/"
    if os.path.exists(os.path.dirname(output_path)) is False:
        try:
            os.makedirs(os.path.dirname(output_path))
        except OSError as ex:  # Guard against race condition
            raise ValueError('Folder is not exist {}'.format(output_path))



    # 気象庁 福井 2016年1月データ
    # url = ('http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?'
    #     'prec_no=57&block_no=47616&year=2008&month=12&day=&view=p1')
    url = (url_str)
    #  pyquery
    query = pq(url, parser='html',encoding='utf-8')
    # title の取得
    title = query('title').text()
    # 日毎を取得
    day = query('.data_0_0')
    print(title)
    for i, item in enumerate(day):
        if i%20 == 0:
            date.append(int(i/20+1))
            location.append(locationName)
        if i % 20 == 5:
            if pq(item).text()=='':
                del date[-1]
                break
            average_temp.append(pq(item).text())
   
        if i%20 == 6:
            if pq(item).text()=='':
                del date[-1]
                break
            highest_temp.append(pq(item).text())
         
        if i%20 == 7:
            if pq(item).text()=='':
                del date[-1]
                break
            lowest_temp.append(pq(item).text())
       
        if i%20==18:
            if pq(item).text()=='':
                del date[-1]
                break
            day_status.append(pq(item).text())
         
        if i%20 == 19:
            if pq(item).text()=='':
                del date[-1]
                break
            night_status.append(pq(item).text())


    #end date
    endDate = date[-1]     

    #write to csv file
    output_name = 'weather_{:04}{:02d}01_{:04}{:02d}{:02d}'.format(year,month,year,month,endDate)
    print("Write to: {}".format(output_name))
    fieldnames = ['location','date','average_temp','highest_temp','lowest_temp','day_status','night_status']
    with open(output_path+output_name+".csv", 'w',encoding='UTF-8') as f:
        writer = csv.DictWriter(f, lineterminator='\n', fieldnames=fieldnames) # 改行コード（\n）を指定しておく
        writer.writeheader()
        for i in range(endDate):
            writer.writerow({'location':location[i],
            'date':date[i],
            'average_temp':average_temp[i],
            'highest_temp':highest_temp[i],
            'lowest_temp':lowest_temp[i],
            'day_status':day_status[i],
            'night_status':night_status[i]})


def takeData(locationName,prec_no,block_no,startYear,startMonth,endYear,endMonth):
    if endYear == startYear:
        if endMonth > startMonth:
            for i in range(startMonth,endMonth+1):
                takeDataByMonth(locationName,prec_no,block_no,startYear,i)
    elif endYear>startYear:
        for year in range(startYear,endYear+1):
            print("year={}".format(year))
            if year == startYear:
                for month in range(startMonth,13):
                    takeDataByMonth(locationName,prec_no,block_no,startYear,month)
            elif year == endYear:
                for month in range(1,endMonth+1):
                    takeDataByMonth(locationName,prec_no,block_no,endYear,month)
            else:
                for month in range(1,13):
                    takeDataByMonth(locationName,prec_no,block_no,year,month)
if __name__ == '__main__':
    locationName = "福井市"
    prec_no = 57
    block_no = 47616
    takeData(locationName,prec_no,block_no,2018,1,2018,12)
    