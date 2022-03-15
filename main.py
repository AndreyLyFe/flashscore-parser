if __name__ == '__main__':
    print("Началась работа программы. Не закрывайте данное окно.")
    answer = input('Введите число\n1 - выгрузка на завтрашний день\n2 - Выгрузка на сегодняшний день\n3 - Выгрузка на предыдущий день\n4 - Выгрузка на предыдущий день с файла "today"\n')
    if answer == '1':
        import hockey_tomorrow
    elif answer == '2':
        import hockey_today
    elif answer == '3':
        import hockey_statistics_today
    elif answer == '4':
        import hockey_statistics_tomorrow
    else:
        print("Вы ввели что-то не то.")
