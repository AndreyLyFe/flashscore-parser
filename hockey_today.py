import requests
import Excel
import time


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



try:
    headers = {
        'x-fsign': 'SW9D1eZo'
    }

    url = 'https://d.flashscore.com/x/feed/f_4_0_3_ru_5'

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
                all_url[text[:8]] = text[a:b], text[c:d]
        else:
            continue

    """
    Создадим список из ссылок на конкретный матч

    После того, как цикл отработает, у нас будут ссылки на все матчи по которым мы можем спарсить данные
    """
    math_hockey_all = list()
    for i in all_url.keys():
        math_hockey_all.append(f'https://d.flashscore.ua/x/feed/df_od_1_{i}')

    count = 2
    for id in math_hockey_all:
        url = id

        req = requests.get(url=url, headers=headers)
        text = req.text
        if text == "":
            continue

        """
        Здесь мы нашли индекс той буквы, на котором заканчивается информация по поводу победы,поражения команд
        И отделили текст до этой буквы
        Теперь у нас информация только по П1 П2 и т.д
        """

        index_full_time = text.find('~OA÷O/U¬OAU')
        text = text[:index_full_time]

        key = url.split('_')[-1]
        Excel.ws[f"A{count}"] = all_url[key][0]
        Excel.ws[f"B{count}"] = all_url[key][1]
        Excel.ws[f"T{count}"] = f'{key}'
        try:
            one_part = text.find('¬~OE÷453')
            two_part = text.find('OG÷1¬')
            part_text = text[one_part:two_part]

            # Найдем данные для P1
            a = part_text.find('XA÷')
            b = part_text.find('¬XB')
            res_p1, a1, b1 = func(a, b, part_text, count, letter='D')
            Excel.ws[f"E{count}"] = a1
            Excel.ws[f"F{count}"] = b1



            # Найдем ничью
            a = part_text.find('XB÷')
            b = part_text.find('¬XC')
            res_x, a2, b2 = func(a, b, part_text, count, letter='I')
            Excel.ws[f"J{count}"] = a2
            Excel.ws[f"K{count}"] = b2



            # Найдем П2
            a = part_text.find('XC÷')
            b = len(part_text) - 1
            res_p2, a3, b3 = func(a, b, part_text, count, letter='N')
            Excel.ws[f"O{count}"] = a3
            Excel.ws[f"P{count}"] = b3




            marja = (100/b1 + 100/b2 + 100/b3) - 100
            c_p1 = round((100 / b1) * 100 / (100+marja), 1)
            c_x = round((100 / b2) * 100 / (100 + marja), 1)
            c_p2 = round((100 / b3) * 100 / (100+marja), 1)
            Excel.ws[f'G{count}'] = c_p1
            Excel.ws[f'L{count}'] = c_x
            Excel.ws[f'Q{count}'] = c_p2

            """
            Создадим словарь для дальнейшего нахождения потенциального исхода
            """
            prediction_dict = dict()
            prediction_dict[res_p1] = 'П1'
            prediction_dict[res_x] = "Ничья"
            prediction_dict[res_p2] = "П2"
            min_num = min(prediction_dict)
            if prediction_dict[res_p1] == prediction_dict[res_x] == prediction_dict[res_p2]:
                Excel.ws[f"S{count}"] = 'None'
            elif c_p1 > 42 and res_p1 < -4:
                Excel.ws[f"S{count}"] = 'П1'
            elif c_x > 42 and res_x < -4:
                Excel.ws[f"S{count}"] = 'Ничья'
            elif c_p2 > 42 and res_p2 < -4:
                Excel.ws[f"S{count}"] = 'П2'
            else:
                Excel.ws[f"S{count}"] = 'Отсутствует'

            count += 1
        except:
            count += 1
        finally:
            Excel.wb.save("hockey_today.xlsx")
            print(f'Прошло итераций:{count - 2}')
except:
    print("Пожалуйста закройте excel файл и запустите скрипт снова.")
finally:
    print('Работа программы завершена.\nОкно будет автоматически закрыто через 5 секунд.')
    time.sleep(5)
