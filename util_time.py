# -*- coding:utf-8 -*-

import datetime
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

def get_times2(start_date, check_date, current_date, length, word_nums):
    # 差分から推定時間をリストにして返却
    diff_time = current_date - check_date #差分時間
    # TODO : 一度secondsで計算後、mm:ssに戻す
    diff_seconds = diff_time.seconds # 時間、分含めた総合秒数
    diff_time = int(get_h_m_s(diff_time)[2])
    check_date_ss = check_date.second # 
    print(diff_seconds, check_date_ss)
    
    # args: ex 01:30:00 , 01:30:20, 3
    # return : [01:30:00, 01:30:05, 01:30:15]
    percentages = list(map(lambda i:i/sum(word_nums), word_nums))
    time_percentages = list(map(lambda i:i*diff_seconds, percentages))
    # 整数への切り上げ
    time_percentages = list(map(lambda i:int(Decimal(str(i)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)),time_percentages))
    if (sum(time_percentages) != diff_seconds):
        time_percentages[-1] = diff_seconds - sum(time_percentages[:-1])
    print(time_percentages)
    assert sum(time_percentages) == diff_seconds
    
    # total_time = 0
    # [24, 77, 49]
    # ーー＞ [00:00:00, 00:00:24, 00:00:101]
    # 初期値は１つ前の時間（＝check_date)
    total_time = 0
    times = []
    for i, time in enumerate(time_percentages):
        if (i==0):
            # 初期値＝check_timeが入る
            pass
        else:
            # 合計した値の秒数となる
            total_time += time_percentages[i-1]
        
        # check_dateにtotal_timeを足した日付が発話開始時間
        # 開始日付からの経過時間を算出してvtt形式対応する
        td = (check_date + datetime.timedelta(seconds=total_time)) - start_date
        print(type(td), td)
        hh, mm, ss = get_h_m_s(td)
        print(hh,mm,ss)
        print(type(hh), type(mm), type(ss))
        time = hh +':'+ mm +':'+ ss +'.000'
        times.append(time)

    return times



def get_times(mm, length, word_nums):
    """
    文字列長に合わせて１分間のn秒ずつのリストを求める
    [str, str,str...]
    """
    percentages = list(map(lambda i:i/sum(word_nums), word_nums))
    time_percentages = list(map(lambda i:i*60, percentages))
    time_percentages = list(map(lambda i:int(Decimal(str(i)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)),time_percentages))
    
    if (sum(time_percentages) != 60):
        time_percentages[-1] = 60 - sum(time_percentages[:-1])
    assert sum(time_percentages) == 60
    total_time = 0
    times = []
    for i, time in enumerate(time_percentages):
        total_time += time
        ss = '0'+str(total_time) if len(str(total_time))==1 else str(total_time)
        if(ss == '60'):
            minitutes = '0'+str(int(mm[1])+1) if len(str(int(mm[1])+1))==1 else str(int(mm[1])+1)
            t = mm[0] + ':' + minitutes + ':00.000'
        else:
            t = mm[0] + ':' + mm[1] + ':' + ss +'.000'
        times.append(t)
    
    return times


def get_next_times(file):
    """推定字幕表示時間を抽出する
    TODO: 仕様変更で秒数が出力されることに、同一SSまでを判断してから
          その60 - SSを文字数ごとに分割する
    """
    first_date = datetime.datetime.strptime(file[1][0], '%Y/%m/%d %H:%M:%S')
    print('first_date: ' + str(first_date))
    same_minitutes_count = 0
    same_minitutes_word_num = [] # 同一時間帯の文字数一覧
    check_date = first_date
    new_times = []
    check_total = 0
    for row in file:
        current_date = datetime.datetime.strptime(row[0], '%Y/%m/%d %H:%M:%S')
        word_num = len(row[2])
        if current_date == check_date:
            same_minitutes_count += 1
            same_minitutes_word_num.append(word_num)
        else:
            # 日付変更
            #date = current_date - first_date - datetime.timedelta(minutes=1)
            date = current_date - first_date # 経過時間
            #print(date)
            #mm = get_h_m_s(date)
            check_total += same_minitutes_count
            # 値の算出
            #print(same_minitutes_count)
            # same_minitutes_count ==1
            if same_minitutes_count == 1:
                new_times.extend([str(date)+'.000'])
                check_date = current_date
                same_minitutes_word_num = [word_num]
            else:
                print(check_date, current_date, same_minitutes_count)
                # current_date = 次の時間帯
                # chekck_date = その前の時間
                #date_diff = current_date - check_date
                #print(date_diff)
                times = get_times2(first_date, check_date, current_date, same_minitutes_count, same_minitutes_word_num)
                #times = get_times(mm, same_minitutes_count, same_minitutes_word_num)
                #print(type(times), times)
                assert (len(times)==same_minitutes_count)
                # 値の更新
                check_date = current_date
                same_minitutes_count = 1
                same_minitutes_word_num = [word_num]
                new_times.extend(times)
    else:
        #date = current_date - first_date 
        #mm = get_h_m_s(date)
        check_total += same_minitutes_count
        times = get_times2(first_date, check_date, current_date, same_minitutes_count, same_minitutes_word_num)
        #times = get_times(mm, same_minitutes_count, same_minitutes_word_num)
        if new_times[-1] != times[-1]:
            new_times.extend(times)

    print(len(new_times))
    print(new_times)
    return new_times


def get_vtt_times(new_times):

    vtt_times = []
    for i, new in enumerate(new_times):
        if (i==0):
            vtt_time = '00:00:00.000 --> '+ new
        else:
            try:
                vtt_time = new_times[i-1] + ' --> ' + new
            except:
                #next_minites = get_next_minites(new)
                vtt_time = new_times[i-1] + ' --> ' + new
        vtt_times.append(vtt_time)
    return vtt_times


def get_next_minites(time):
    current_minites = int(time[3:5])+1
    next_minites = '0'+str(current_minites) if len(str(current_minites))==1 else str(current_minites)
    next_time = time[:3] + next_minites + time[5:]
    return next_time


def get_h_m_s(td):
    m, s = divmod(td.seconds, 60)
    h, m = divmod(m, 60)
    if len(str(h))==1:
        h = '0'+str(h)
    else:
        h = str(h)

    if len(str(m))==1:
        m = '0'+str(m)
    else:
        m = str(m)
        
    if len(str(s))==1:
        s = '0'+str(s)
    else:
        s = str(s)
    return h, m, s