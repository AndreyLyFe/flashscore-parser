import requests
import Excel
import time
import datetime

def func(a: int, b: int, part_text: str, count: int, letter: str):
    new_text = part_text[a + 3:b]
    if '[u]' in new_text:
        a = float(new_text[:new_text.find('[u]')])
        b = float(new_text[new_text.find('[u]') + 3:])
        result = round(((a - b) / a) * -100, 2)
        Excel.ws[f"{letter}{count}"] = result
        return result, a, b
    elif '[d]' in new_text:
        a = float(new_text[:new_text.find('[d]')])
        b = float(new_text[new_text.find('[d]') + 3:])
        result = round(((a - b) / a) * -100, 2)
        Excel.ws[f"{letter}{count}"] = result
        return result, a, b
    else:
        result = 0
        Excel.ws[f"{letter}{count}"] = result
        a = b = float(new_text)
        return result, a, b


def function_for_totals(a: int, b: int, part_text: str) -> float:
    new_text = part_text[a:b]
    if '[u]' in new_text:
        a = float(new_text[:new_text.find('[u]')])
        b = float(new_text[new_text.find('[u]') + 3:])
        result = b - a
        return result
    elif '[d]' in new_text:
        a = float(new_text[:new_text.find('[d]')])
        b = float(new_text[new_text.find('[d]') + 3:])
        result = b - a
        return result
    else:
        return 0





input_shans = float(input('Введите шанс на победу: '))
input_izmen = float(input('Введите изменение(положительное число): '))
print()

input_shans_x = float(input('Введите максимальную вероятность аутсайдера(Максимально-возможная вероятность на то, что выиграет аутсайдер: '))
input_izmen_x = float(input('Введите максимальное изменение аутсайдера(Максимальное изменение коэффициентов на аутсайдера): '))

try:
    headers = {
        'x-fsign': 'SW9D1eZo'
    }

    url = 'https://d.flashscore.com/x/feed/f_4_1_3_ru_5'

    """
    Забираем с главной страницы названия лиг и составляем словарь из Ключ матча : лига
    """
    req = requests.get(url=url, headers=headers)
    text = req.text

    dict_name_liga = dict()
    count_ZA = text.count('ZA÷')
    for _ in range(count_ZA):
        start_find_name_liga = text.find('ZA÷')
        stop_find_name_liga = text.find('¬ZEE')
        name_liga = text[start_find_name_liga + 3: stop_find_name_liga]
        two_start_name_liga = text.find('ZA÷', start_find_name_liga + 1, len(text))
        count_AA = text[start_find_name_liga:two_start_name_liga].count('AA÷')
        text_name_liga_new = text[start_find_name_liga:two_start_name_liga]
        for i in range(count_AA):
            a = text_name_liga_new.find('AA÷')
            b = text_name_liga_new.find('¬AD÷')
            dict_name_liga[text_name_liga_new[a + 3: b]] = name_liga
            text_name_liga_new = text_name_liga_new[b + 3:]
        text = text[two_start_name_liga - 6:]






    headers = {
        'x-fsign': 'SW9D1eZo'
    }

    url = 'https://d.flashscore.com/x/feed/f_4_1_3_ru_5'

    """
    Тут мы просто парсим сайт и в куче текста находим нужные нам ссылки на конкретные матчи
    """
    req = requests.get(url=url, headers=headers)
    text = req.text

    """
    В фрагменте ниже, достаем все ссылки на матчи.
    Теперь они хранятся в словаре в переменной all_url
    """

    all_url = dict()
    index_find = 0
    count_AA = text.count('AA÷')

    count = 1
    for _ in range(count_AA):
        index_find = text.find('AA÷') + 3
        if not text[index_find:index_find + 7] in all_url:
            if text[index_find + 8:index_find + 11] == '¬AD':
                text = text[index_find:]
                a = text.find('FH÷') + 3
                b = text.find('¬JA')
                c = text.find('FK÷') + 3
                d = text.find('¬JB')
                q = text.find('¬ADE÷') + 5
                w = text.find('¬AB÷')
                all_url[text[:8]] = text[a:b], text[c:d], text[q:w]
        else:
            continue

    """
    Создадим список из ссылок на конкретный матч

    После того, как цикл отработает, у нас будут ссылки на все матчи по которым мы можем спарсить данные
    """
    math_hockey_all = list()
    for i in all_url.keys():
        math_hockey_all.append(f'https://d.flashscore.com/x/feed/df_od_1_{i}')

    count = 2
    for id in math_hockey_all:
        url = id

        req = requests.get(url=url, headers=headers)
        text = req.text
        if text == "":
            continue

        print(text)
        """
        Найдем тоталы и посчитаем их
        """
        positive_list = list()
        negative_list = list()
        start_index = text.find('¬~OA÷O/U¬')
        stop_index = text.find('¬~OB÷1st Period¬OBU÷1st-period¬OBI÷1per¬~OCT÷Total')
        try:
            new_text_from_total = text[start_index:stop_index]
            count_total = new_text_from_total.count('XB÷')
            for _ in range(count_total):
                positive_index_1 = new_text_from_total.find('XB÷') + 3
                positive_index_2 = new_text_from_total.find('¬XC')
                negative_index_1 = new_text_from_total.find('XC÷') + 3
                negative_index_2 = new_text_from_total.find('¬OG')
                positive_list.append(
                    function_for_totals(a=positive_index_1, b=positive_index_2, part_text=new_text_from_total))
                negative_list.append(
                    function_for_totals(a=negative_index_1, b=negative_index_2, part_text=new_text_from_total))
                new_text_from_total = new_text_from_total[negative_index_2 + 3:]
            if sum(positive_list) / count_total > sum(negative_list) / count_total:
                Excel.ws[f'W{count}'] = 'ТБ'
            elif sum(positive_list) / count_total < sum(negative_list) / count_total:
                Excel.ws[f'W{count}'] = 'ТМ'
            else:
                Excel.ws[f'W{count}'] = 'Т = 0'
        except:
            Excel.ws[f'W{count}'] = 'Ошибка'



        """
        Здесь мы нашли индекс той буквы, на котором заканчивается информация по поводу победы,поражения команд
        И отделили текст до этой буквы
        Теперь у нас информация только по П1 П2 и т.д
        """

        index_full_time = text.find('~OA÷O/U¬OAU')
        text = text[:index_full_time]

        key = url.split('_')[-1]
        Excel.ws[f"E{count}"] = all_url[key][1]
        Excel.ws[f"D{count}"] = all_url[key][0]

        Excel.ws[f"V{count}"] = f'{key}'

        data_match = datetime.datetime.fromtimestamp(int(f"{all_url[key][2]}")).strftime('%Y-%m-%d %H:%M:%S').split()
        Excel.ws[f"A{count}"] = data_match[0]
        Excel.ws[f"B{count}"] = data_match[1]

        for key2, value2 in dict_name_liga.items():
            if key == key2:
                Excel.ws[f'C{count}'] = value2

        try:
            one_part = text.find('¬~OE÷453')
            two_part = text.find('OG÷1¬')
            part_text = text[one_part:two_part]

            # Найдем данные для P1
            a = part_text.find('XA÷')
            b = part_text.find('¬XB')
            res_p1, a1, b1 = func(a, b, part_text, count, letter='H')
            Excel.ws[f"F{count}"] = a1
            Excel.ws[f"G{count}"] = b1

            # Найдем ничью
            a = part_text.find('XB÷')
            b = part_text.find('¬XC')
            res_x, a2, b2 = func(a, b, part_text, count, letter='M')
            Excel.ws[f"K{count}"] = a2
            Excel.ws[f"L{count}"] = b2

            # Найдем П2
            a = part_text.find('XC÷')
            b = len(part_text) - 1
            res_p2, a3, b3 = func(a, b, part_text, count, letter='R')
            Excel.ws[f"P{count}"] = a3
            Excel.ws[f"Q{count}"] = b3

            marja = (100 / b1 + 100 / b2 + 100 / b3) - 100
            c_p1 = round((100 / b1) * 100 / (100 + marja), 1)
            c_x = round((100 / b2) * 100 / (100 + marja), 1)
            c_p2 = round((100 / b3) * 100 / (100 + marja), 1)
            Excel.ws[f'I{count}'] = c_p1
            Excel.ws[f'N{count}'] = c_x
            Excel.ws[f'S{count}'] = c_p2

            """
            Создадим словарь для дальнейшего нахождения потенциального исхода
            """
            prediction_dict = dict()
            prediction_dict[res_p1] = 'П1'
            prediction_dict[res_x] = "Ничья"
            prediction_dict[res_p2] = "П2"
            min_num = min(prediction_dict)
            if prediction_dict[res_p1] == prediction_dict[res_x] == prediction_dict[res_p2]:
                Excel.ws[f"U{count}"] = 'None'
            elif c_p1 < input_shans_x and res_p1 > input_izmen_x:
                if c_p2 > input_shans and res_p2 < (input_izmen * -1):
                    Excel.ws[f"U{count}"] = 'П2'
                else:
                    Excel.ws[f"U{count}"] = 'X2'


            elif c_p2 < input_shans_x and res_p2 > input_izmen_x:
                if c_p1 > input_shans and res_p1 < (input_izmen * -1):
                    Excel.ws[f"U{count}"] = 'П1'
                else:
                    Excel.ws[f"U{count}"] = '1X'
            elif c_p2 > input_shans and res_p2 < (input_izmen * -1):
                Excel.ws[f"U{count}"] = 'П2'
            elif c_p1 > input_shans and res_p1 < (input_izmen * -1):
                Excel.ws[f"U{count}"] = 'П1'
            else:
                Excel.ws[f"U{count}"] = 'Отсутствует'

            count += 1
        except:
            count += 1
        finally:
            Excel.wb.save(f"hockey_tomorrow_{input_shans}_{input_izmen}.xlsx")
            print(f'Прошло итераций:{count - 2}')
except PermissionError:
    print("Пожалуйста закройте excel файл и запустите скрипт снова.")
finally:
    print('Работа программы завершена.\nОкно будет автоматически закрыто через 5 секунд.')
    time.sleep(5)
