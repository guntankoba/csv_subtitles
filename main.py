# -*- coding:utf-8 -*-

import csv, datetime
import glob
import util_csv
import util_time
import editrow


def main():
    # データファイル一覧の読み込み
    files=glob.glob("./data/*.csv")

    for file_name in files:
        # 本番用test
        file_name_list = file_name.split('/')
        result_dir_name = './result/'
        result_file_name = result_dir_name + file_name_list[2]
        
        # ファイルのread
        file = util_csv.read_csv(file_name)

        # ファイルの分割、書き込み
        separate_file = editrow.separate_row(file, '。')
        print('ファイル名： '+ file_name)
        print('分割前： ' + str(len(file)))
        print('分割後： ' + str(len(separate_file)))

        # タイムスタンプ形式への更新
        next_times = util_time.get_next_times(separate_file)
        vtt_times = util_time.get_vtt_times(next_times)
        assert(len(separate_file)==len(vtt_times))

        # ファイルの書き込み
        with open(result_file_name, 'w')as o:
            writer = csv.writer(o, delimiter=',')
            for i, row in enumerate(separate_file):
                writer.writerow([vtt_times[i], row[1], row[2]])


if __name__ == '__main__':
    main()