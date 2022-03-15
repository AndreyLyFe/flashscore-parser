import requests

headers = {
    'x-fsign': 'SW9D1eZo'
}

url = 'https://d.flashscore.com/x/feed/f_1_1_3_en_1'

"""
Тут мы просто парсим сайт и в куче текста находим нужные нам ссылки на конкретные матчи
"""
req = requests.get(url=url, headers=headers)
text = req.text


"""
В фрагменте ниже, достаем все ссылки на матчи.
Теперь они хранятся в списке в переменной all_url
"""
all_url = dict()
index_find = 0
count_AA = text.count('AA÷')

count = 1
for _ in range(0,count_AA):
    index_find = text.find('AA÷')+3
    if not text[index_find:index_find+7] in all_url:
        if text[index_find+8:index_find+11] == '¬AD':
            text = text[index_find:]
            a = text.find('FH÷') + 3
            b = text.find('¬JA')
            c = text.find('FK÷') + 3
            d = text.find('¬JB')
            all_url[text[:8]] = text[a:b], text[c:d]
    else:
        continue
print(all_url)
