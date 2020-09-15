import datetime
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

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
    """
    first_date = datetime.datetime.strptime(file[1][0], '%Y/%m/%d %H:%M')
    same_minitutes_count = 0
    same_minitutes_word_num = [] # 同一時間帯の文字数一覧
    check_date = first_date
    new_times = []
    check_total = 0
    for row in file:
        current_date = datetime.datetime.strptime(row[0], '%Y/%m/%d %H:%M')
        word_num = len(row[2])
        if current_date == check_date:
            same_minitutes_count += 1
            same_minitutes_word_num.append(word_num)
        else:
            # 日付変更
            date = current_date - first_date - datetime.timedelta(minutes=1)
            mm = get_h_m_s(date)
            check_total += same_minitutes_count
            # 値の算出
            times = get_times(mm, same_minitutes_count, same_minitutes_word_num)
            assert (len(times)==same_minitutes_count)
            # 値の更新
            check_date = current_date
            same_minitutes_count = 1
            same_minitutes_word_num = [word_num]
            new_times.extend(times)
    else:
        date = current_date - first_date 
        mm = get_h_m_s(date)
        check_total += same_minitutes_count
        times = get_times(mm, same_minitutes_count, same_minitutes_word_num)
        if new_times[-1] != times[-1]:
            new_times.extend(times)

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
    return h, m