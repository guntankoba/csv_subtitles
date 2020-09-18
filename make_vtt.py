# -*- coding:utf-8 -*-

import util_csv

def main():
    f = './result/33_sample.csv'
    file = util_csv.read_csv(f)
    csv_row = len(file[0])
   
    with open('./result/33_sample.vtt', 'w') as o:
        o.write('WEBVTT\n\n')
        for i, row in enumerate(file):
            o.write(row[0] + '\n' + row[2] + '\n\n')
    
    if (csv_row == 4):
        with open('./result/33_sample.vtt', 'w') as o:
            o.write('WEBVTT\n\n')
            for i, row in enumerate(file):
                o.write(row[0] + '\n' + row[3] + '\n\n')

if __name__ == '__main__':
    main()