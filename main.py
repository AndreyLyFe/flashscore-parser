if __name__ == '__main__':
    print("Началась работа программы. Не закрывайте данное окно.")
    vid = input("Выберите вид спорта.\n1 - Хоккей\n2 - Футбол\n")
    if vid == '1':
        print("Вы перешли в ХОККЕЙ")
        answer = input('Введите число\n1 - выгрузка на завтрашний день\n2 - Выгрузка на сегодняшний день\n3 - Выгрузка на предыдущий день с файла "tomorrow"\n4 - Выгрузка на предыдущий день с файла "today"\n')
        if answer == '1':
            import hockey_tomorrow
        elif answer == '2':
            import hockey_today
        elif answer == '3':
            import hockey_statistics_tomorrow
        elif answer == '4':
            import hockey_statistics_today
        else:
            print("Вы ввели что-то не то.")
    elif vid == '2':
        print("Вы перешли в ФУТБОЛ")
        answer = input('Введите число\n1 - выгрузка на завтрашний день\n2 - Выгрузка на сегодняшний день\n3 - Выгрузка на предыдущий день с файла "tomorrow"\n4 - Выгрузка на предыдущий день с файла "today"\n')
        if answer == '1':
            import football_tomorrow
        elif answer == '2':
            import football_today
        elif answer == '3':
            import football_statistics_tomorrow
        elif answer == '4':
            import football_statistics_today
        else:
            print("Вы ввели что-то не то.")
    else:
        print("Вы ввели что-то не то.")












