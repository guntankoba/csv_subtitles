# -*- config:utf-8 -*-

def separate_row(file, delimiter):
    """
    日本語用
    ファイルから句点ごとに変更したリストを返す
    """
    new_file = []
    first_date = file[1][0] #1行目が項目名の想定
    
    for row_index, row in enumerate(file):
        if(row_index==0):
            continue
        current_date = row[0]
        # delimiteerごとに文章を分割
        sentences = row[2].split(delimiter)
        sentences_length = len(sentences)

        # 分割した文章数ごとの処理
        if (sentences_length == 1):
            new_sentence = check_quote(sentences[0]) + delimiter
            new_row = [row[0], row[1], new_sentence, row[3]]
            new_file.append(new_row)
        else:
            for index, sentence in enumerate(sentences):
                if (sentence == '' or sentence == '"' or sentence==' "'):
                    continue
                new_sentence = check_quote(sentence) + delimiter
                new_row = [row[0], row[1], new_sentence, row[3]]
                new_file.append(new_row)
    return new_file

def check_quote(sentence):
    """Meeting Assistの不要な文字列を削除"""
    if sentence[:1] == '"':
        sentence = sentence[1:]
    if sentence[:2] ==' "':
        sentence = sentence[2:]
    if sentence[-1] == '"':
        sentence = sentence [:-1]
    if sentence[-2:] == ' "':
        sentence = sentence [:-2]
    return sentence