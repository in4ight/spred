from tools.price_viewer.price_grabber import Price_Grabber
from prettytable import PrettyTable
import time
from tools.time_domain_list import TimeDomainList


if __name__ == '__main__':
    pg = Price_Grabber()
    stock_list = []
    with open('stock_list.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            stock_code = line
            stock_list.append(stock_code)

    index_list = []
    with open('index_list.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            index_code = line
            index_list.append(index_code)

    stock_tdl = []
    for stock_code in stock_list:
        tdl = TimeDomainList(element_cnt=12)
        stock_tdl.append(tdl)
    index_tdl = []
    for index_code in index_list:
        tdl = TimeDomainList(element_cnt=12)
        index_tdl.append(tdl)
    main_table = PrettyTable(['stock_code', ' stock_name ', ' price ', ' ratio ', 'volatility',
                              'today_low', 'today_high', 'time', 'ratio_f'])

    while (True):
        stock_table = main_table[:]
        for i, stock_code in enumerate(stock_list):
            res = pg.grab(stock_code)
            try:
                stock_tdl[i].push(float(res['ratio'][:-1]))
            except:
                print('Wrong value')
            volatility_s = ''
            if stock_tdl[i].list[0] is not None:
                volatility_ratio = stock_tdl[i].list[-1] - stock_tdl[i].list[0]
                if volatility_ratio > 0:
                    volatility_ratio = stock_tdl[i].list[-1] - min(stock_tdl[i].list)
                else:
                    volatility_ratio = stock_tdl[i].list[-1] - max(stock_tdl[i].list)
                volatility_s = "%.2f%%" % volatility_ratio
            ratio = res['ratio']
            rf = float(ratio[:-1])
            stock_table.add_row([stock_code, res['stock_name'],
                                   res['current_price'], ratio, volatility_s,
                                   res['today_low'], res['today_high'], res['current_time'], rf])
        index_table = main_table[:]
        for i, index_code in enumerate(index_list):
            res = pg.grab(index_code)
            try:
                index_tdl[i].push(float(res['ratio'][:-1]))
            except:
                print('Wrong value')
            volatility_s = ''
            if index_tdl[i].list[0] is not None:
                volatility_ratio = index_tdl[i].list[-1] - index_tdl[i].list[0]
                if volatility_ratio > 0:
                    volatility_ratio = index_tdl[i].list[-1] - min(index_tdl[i].list)
                else:
                    volatility_ratio = index_tdl[i].list[-1] - max(index_tdl[i].list)
                volatility_s = "%.2f%%" % volatility_ratio
            ratio = res['ratio']
            rf = float(ratio[:-1])
            index_table.add_row([index_code, res['stock_name'],
                                   res['current_price'], ratio, volatility_s,
                                   res['today_low'], res['today_high'], res['current_time'], rf])
        print(time.strftime('%H:%M:%S', time.localtime(time.time())))
        stock_table.align = "r"
        index_table.align = "r"
        print(index_table.get_string())
        print(stock_table.get_string(fields=['stock_code', ' stock_name ', ' price ', ' ratio ', 'volatility',
                              'today_low', 'today_high', 'time'], sortby="ratio_f"))
        time.sleep(10)
