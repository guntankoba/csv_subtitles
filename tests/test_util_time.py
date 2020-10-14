# -*- coding: utf-8 -*-
import sys
import os
sys.path.append("..")
import util_time
import datetime


def test_has_duplicates_01():
    case = (1,2,3,4,5)
    assert(util_time.has_duplicates(case) == True)

def test_has_duplicates_02():
    case = (1,1,2,3,4)
    assert(util_time.has_duplicates(case) == False)

def test_get_h_m_s_01():
    case = datetime.timedelta(hours=int(1), minutes=int(2), seconds=int(3))
    print(util_time.get_h_m_s(case))
    assert(util_time.get_h_m_s(case) == ('01', '02', '03'))

def test_get_h_m_s_02():
    case = datetime.timedelta(hours=int(1), minutes=int(2), seconds=int(3))
    print(util_time.get_h_m_s(case))
    assert(util_time.get_h_m_s(case) != ('1', '2', '3'))

def test_get_times_01():
    start_date = datetime.datetime.strptime('2020/08/20 12:58:00', '%Y/%m/%d %H:%M:%S')
    check_date = datetime.datetime.strptime('2020/08/20 12:58:39', '%Y/%m/%d %H:%M:%S')
    current_date = datetime.datetime.strptime('2020/08/20 12:58:55', '%Y/%m/%d %H:%M:%S')
    length = 3
    word_nums = [24, 77, 49]
    times = util_time.get_times(start_date, check_date, current_date, length, word_nums)
    assert(times == ['00:00:39.000', '00:00:42.000', '00:00:50.000'])

def test_get_times_02():
    start_date = datetime.datetime.strptime('2020/08/20 12:58:00', '%Y/%m/%d %H:%M:%S')
    check_date = datetime.datetime.strptime('2020/08/20 12:58:55', '%Y/%m/%d %H:%M:%S')
    current_date = datetime.datetime.strptime('2020/08/20 12:59:10', '%Y/%m/%d %H:%M:%S')
    length = 1
    word_nums = [24]
    times = util_time.get_times(start_date, check_date, current_date, length, word_nums)
    assert(times == ['00:00:55.000'])

