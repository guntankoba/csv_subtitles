import unicodedata
import util_csv
import util_time
import csv

def check_zenkaku(text):
    for char in text:
        ret = unicodedata.east_asian_width(char)
        if (ret == 'W'):
            return True
        
    else:
        return False


def get_end_time(file):
    rows = util_csv.read_csv(file)
    print('rows_num : ' + str(len(rows)))
    new_rows = []
    num = 0
    count = 0
    n_c = 0
    flag = False
    for i, row in enumerate(rows):
        if(i == len(rows)-1):
            if(flag ==True):
                new_rows.append(rows[num])
                flag = False
            else:
                new_rows.append(row)
        else:
            if(rows[i+1][3] == ''):
                count += 1
                if flag == True:
                    rows[num][0] = rows[num][0].split(' ')[0] + ' --> ' + rows[i+1][0].split(' ')[2]
                    rows[num][2] = rows[num][2] + rows[i+1][2]
                else:                    
                    row[0] = row[0].split(' ')[0] + ' --> ' + rows[i+1][0].split(' ')[2]
                    row[2] = row[2] + rows[i+1][2]
                    flag = True
                    num = i
                    
            else:
                n_c +=1
                if(flag ==True):
                    new_rows.append(rows[num])
                    flag = False
                else:
                    new_rows.append(row)
        
    return new_rows   


def get_new_rows(file):
    rows = util_csv.read_csv(file)
    row_length = len(rows[0])

    if (row_length >= 4):
        new_rows = []
        for i, row in enumerate(rows):
            current_en = row[3]
            # 文字列に全角があるかチェック
            is_zenkaku = check_zenkaku(current_en)
            if is_zenkaku:
                limit_sentence = 32 * 3
                split_word = '、'
            else:
                limit_sentence = 64 * 3
                split_word = ' '
                        
            # 文字列の長さの判定
            if (len(current_en) < limit_sentence):
                new_rows.append(row)
            else:              
                split_sentences = get_split_sentences(current_en, split_word)
                
                split_times = get_split_times(row[0], split_sentences)
                assert(len(split_times) == len(split_sentences))
                for i, split_time in enumerate(split_times):
                    if(i==0):
                        new_rows.append([split_times[i], row[1], row[2], split_sentences[i]])
                    else:
                        new_rows.append([split_times[i], row[1], '★★★cut★★★', split_sentences[i]])

    return new_rows


def get_word_nums(sentences):
    word_nums = []
    for sentence in sentences:
        word_nums.append(len(sentence))
    return word_nums


def get_split_times(timestamp, sentences):
    """
    timestamp
    00:00:07.000 --> 00:00:15.000
    sentences
    ['aaa','bbb']
    """
    word_nums = get_word_nums(sentences)
    timestamps = timestamp.split(' ')
    zero_time = util_time.get_timedelta('00:00:00.000')
    start_time = util_time.get_timedelta(timestamps[0])
    end_time = util_time.get_timedelta(timestamps[2])

    new_times = util_time.get_times(zero_time, start_time, end_time, len(sentences), word_nums)
    new_vtt_times = get_new_vtt_times(new_times, end_time)

    return new_vtt_times


def get_new_vtt_times(new_times, end_time):
    new_vtt_times = []
    end_time = '0' + str(end_time) + '.000'
    for i, new_time in enumerate(new_times):
        if(i == (len(new_times) - 1)):
            vtt_time = new_time + ' --> ' + end_time
        else:
            vtt_time = new_time + ' --> ' + new_times[i+1]
        new_vtt_times.append(vtt_time)
        
    return new_vtt_times


def get_split_sentences(text, split_word):
    words = text.split(split_word)
    #print(words)
    split_sentences = []
    split_sentence = ''
    for word in words:
        length = len(split_sentence + word)
        if split_word == ' ':
            limit = 64*2
        else:
            limit = 32*2
        if(length > limit):
            split_sentences.append(split_sentence)
            split_sentence = word

        else:
            split_sentence = split_sentence +' '+ word
    
    else:
        split_sentences.append(split_sentence)
        
        
    if(len(split_sentences) != 0):
        if split_sentences[0][0] == ' ':
            split_sentences[0] = split_sentences[0][1:]
        if split_sentences[0] == ' ':
            split_sentences[0] = ''
            
    return split_sentences


def delete_star(file):
    rows = util_csv.read_csv(file)
    result_file = './checked_result/' + file.split('/')[2]
    print(result_file)
    with open(result_file, 'w') as o:
        writer = csv.writer(o)
        for i, row in enumerate(rows):
            if('★★' in row[2] and '★★' in row[3]):
                start_time = rows[i][0].split(' --> ')[0]
                end_time = rows[i+1][0].split(' --> ')[1]
                rows[i+1][0] = start_time + ' --> ' + end_time

            else:
                writer.writerow(row)
