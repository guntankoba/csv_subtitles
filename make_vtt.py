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

def write_vtt(file):
    rows = util_csv.read_csv(file)
    file_name = file.split('/')[2].replace('csv', 'vtt')
    vtt_jp = './vtt_jp/' + file_name
    vtt_en = './vtt_en/' + file_name
    print(vtt_jp, vtt_en)
    row_length = len(rows[0])
    print(row_length)
    with open(vtt_jp, 'w') as o:
        o.write('WEBVTT\n\n')
        for i, row in enumerate(rows):
            o.write(row[0] + '\n' + row[2] + '\n\n')
    
    
    if (row_length >= 4):
        with open(vtt_en, 'w') as o:
            o.write('WEBVTT\n\n')
            for i, row in enumerate(rows):
                current_en = row[3]
                print(len(current_en))
                #if(len(current_en) >= 64*3):
                #    print(current_en)
                #    split_sentences = get_split_sentences(current_en)
                
                
                #if (len(current_en)) == 0:
                    
                    
                o.write(row[0] + '\n' + row[3] + '\n\n')


def get_split_sentences(text):
    words = text.split(' ')
    split_sentences = []
    split_sentence = ''
    for word in words:
        length = len(split_sentence + word)
        if(length > 64):
            split_sentences.append(split_sentence)
            split_sentence = word
        else:
            split_sentence = split_sentence +' '+ word
    
    else:
        split_sentences.append(split_sentence)
    
    if split_sentences[0][0] == ' ':
        try:
            split_sentences[0] = split_sentences[0][1:]
        except:
            pass
    if split_sentences[0] == ' ':
        split_sentences[0] = ''

    return split_sentences



if __name__ == '__main__':
    main()