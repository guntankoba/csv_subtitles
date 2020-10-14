# -*- coding:utf-8 -*-

import datetime
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

import util_csv

def get_times(start_date, check_date, current_date, length, word_nums):
    """
    重複時間の列の文字数から推定時間を算出および、開始からの経過時間に変更

    """
    # 差分から推定時間をリストにして返却
    diff_time = current_date - check_date #差分時間
    diff_seconds = diff_time.seconds # 時間、分含めた総合秒数
    diff_time = int(get_h_m_s(diff_time)[2])
    # 差分文字数に対する割合を算出
    percentages = list(map(lambda i:i/sum(word_nums), word_nums))
    time_percentages = list(map(lambda i:i*diff_seconds, percentages))
    # 整数への切り上げ
    time_percentages = list(map(lambda i:int(Decimal(str(i)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)),time_percentages))
    if (sum(time_percentages) != diff_seconds):
        time_percentages[-1] = diff_seconds - sum(time_percentages[:-1])
    assert sum(time_percentages) == diff_seconds

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
        hh, mm, ss = get_h_m_s(td)
        time = hh +':'+ mm +':'+ ss +'.000'
        times.append(time)

    assert(len(times)==length)
    return times


def get_next_times(file):
    """
    推定字幕表示時間を抽出する
    """
    first_date = datetime.datetime.strptime(file[1][0], '%Y/%m/%d %H:%M:%S')
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
            date = check_date - first_date # 経過時間

            check_total += same_minitutes_count
            # 値の算出
            if same_minitutes_count == 1:
                new_times.extend(['0'+str(date)+'.000'])
                check_date = current_date
                same_minitutes_word_num = [word_num]

            else:               
                times = get_times(first_date, check_date, current_date, same_minitutes_count, same_minitutes_word_num)
                assert (len(times)==same_minitutes_count)
                try:
                    assert (has_duplicates(times))
                except:
                    print(times, row)

                assert (times[-1] != current_date)
                # 値の更新
                check_date = current_date
                same_minitutes_count = 1
                same_minitutes_word_num = [word_num]
                new_times.extend(times)
    else:
        next_minitutes = current_date.minute + 2
        if next_minitutes >= 60:
            next_hours = current_date.hour + 1
            next_minitutes = next_minitutes - 60
            str_next_time = str(current_date)[:11] + str(next_hours) + ':' + str(next_minitutes) + ':00'
        else:
            str_next_time = str(current_date)[:14] + str(next_minitutes) + ':00'

        current_date = datetime.datetime.strptime(str_next_time, '%Y-%m-%d %H:%M:%S')
        times = get_times(first_date, check_date, current_date, same_minitutes_count, same_minitutes_word_num)
        print(times)
        if new_times[-1] != times[-1]:
            new_times.extend(times)
    
    if(len(file)!=len(new_times)):
        next_minitutes = current_date.minute + 2
        if next_minitutes >= 60:
            next_hours = current_date.hour + 1
            next_minitutes = next_minitutes - 60
            str_next_time = str(current_date)[:11] + str(next_hours) + ':' + str(next_minitutes) + ':00'
        else:
            str_next_time = str(current_date)[:14] + str(next_minitutes) + ':00'

        current_date = datetime.datetime.strptime(str_next_time, '%Y-%m-%d %H:%M:%S')
        times = get_times(first_date, check_date, current_date, same_minitutes_count, same_minitutes_word_num)
        new_times.extend(times)

    return new_times

def has_duplicates(seq):
    return len(seq) == len(set(seq))

def get_vtt_times(new_times):
    vtt_times = []
    for i, new_time in enumerate(new_times):
        if (i+1 == len(new_times)):
            next_minitutes = get_next_minitutes(new_time)
            vtt_time = new_time + ' --> ' + next_minitutes
        else:
            vtt_time = new_time + ' --> ' + new_times[i+1]
            print(vtt_time, new_times[i+1])
        vtt_times.append(vtt_time)
        
    return vtt_times


def get_next_minitutes(time):
    current_minitutes = int(time[3:5])+1
    next_minitutes = '0'+str(current_minitutes) if len(str(current_minitutes))==1 else str(current_minitutes)
    next_time = time[:3] + next_minitutes + ':00.000' 
    return next_time


def get_h_m_s(td):
    """
    datetime.timedelta形式から時間、分、秒を算出する
    """
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

def get_timedelta(time):
    hours, minutes, seconds = time.split(':')
    seconds = seconds.split('.')[0]
    timedelta = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    return timedelta

def add_time(default_time, start_time):
    """
    timedelta同士の加算
    default_time : datetime.timedelta
    start_time : datetime.timedelta                                          
    added_time : datetime.timedelta
    """
    added_time = default_time + start_time
    
    return added_time

def add_start_time(file_name, start_time):
    """
    各行の値を加算する
    return : new_rows
    
    """
    start_timedelta = get_timedelta(start_time)
    # 予めメモしていた開始推定時間を全秒数に追加する
    rows = util_csv.read_csv(file_name)

    for row in rows:
        first_timedelta = get_timedelta(row[0].split(' ')[0])
        second_timedelta = get_timedelta(row[0].split(' ')[2])
        # 加算
        first_time = add_time(first_timedelta, start_timedelta)
        second_time = add_time(second_timedelta, start_timedelta)
        
        new_vtt_time = '0' + str(first_time) + '.000 --> 0' + str(second_time) + '.000'
        assert(new_vtt_time != row[0])
        row[0] = new_vtt_time
        
    return rows