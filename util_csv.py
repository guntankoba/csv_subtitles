# -*- coding:utf-8 -*-

import csv

def read_csv(file_name):
    """ [row, row, row]の形式の２次元リストを返す"""
    file = []
    with open(file_name) as f:
        for row in csv.reader(f):
            file.append(row)
    return file
