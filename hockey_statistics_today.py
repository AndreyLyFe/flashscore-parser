import requests
import openpyxl
from openpyxl.styles import Font


input_shans = float(input('Введите первую цифру, которая указана в название файла: '))
input_izmen = float(input('Введите вторую цифру, которая указана в название файла: '))

book = openpyxl.open(f'hockey_today_{input_shans}_{input_izmen}.xlsx')
sheet = book.active

print("Работа программы началась.\nПожалуйста ожидайте.")

for i in range(sheet.max_row - 1):

  key = sheet[f'V{i+2}'].value
  url = f'https://d.flashscore.com/x/feed/dc_1_{key}'
  # url = f'https://d.flashscore.com/x/feed/dc_1_UqYeppwc'
  headers = {'x-fsign': 'SW9D1eZo',
             'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
  req = requests.get(url=url, headers=headers)
  text = req.text

  #Кол-во шайб первой команды в основное время
  a = text.find('DG÷') + 3
  b = text.find('¬DH')


  #
  c = text.find('DH÷') + 3
  d = text.find('¬DI')
  sheet[f'T{i+2}'].value = f'{text[a:b]}:{text[c:d]}'

  if '÷' in sheet[f'T{i+2}'].value:
    sheet[f'T{i + 2}'].value = 'Не начался'
  else:
    if sheet[f'U{i + 2}'].value == 'П1' and int(text[a:b]) > int(text[c:d]):
      cell = sheet[f'T{i + 2}']
      cell.font = Font(color="33cc33", italic=True)
    elif sheet[f'U{i + 2}'].value == 'П2' and int(text[a:b]) < int(text[c:d]):
      cell = sheet[f'T{i + 2}']
      cell.font = Font(color="33cc33", italic=True)
    elif sheet[f'U{i + 2}'].value == 'Ничья' and int(text[a:b]) == int(text[c:d]):
      cell = sheet[f'T{i + 2}']
      cell.font = Font(color="33cc33", italic=True)
    elif sheet[f'U{i + 2}'].value == '1X' and int(text[a:b]) >= int(text[c:d]):
      cell = sheet[f'T{i + 2}']
      cell.font = Font(color="33cc33", italic=True)
    elif sheet[f'U{i + 2}'].value == 'X2' and int(text[a:b]) <= int(text[c:d]):
      cell = sheet[f'T{i + 2}']
      cell.font = Font(color="33cc33", italic=True)
    elif sheet[f'U{i + 2}'].value == 'П1' and int(text[a:b]) <= int(text[c:d]):
      cell = sheet[f'T{i + 2}']
      cell.font = Font(color="ff0000", italic=True)
    elif sheet[f'U{i + 2}'].value == 'П2' and int(text[a:b]) >= int(text[c:d]):
      cell = sheet[f'T{i + 2}']
      cell.font = Font(color="ff0000", italic=True)
    elif sheet[f'U{i + 2}'].value == '1X' and int(text[a:b]) < int(text[c:d]):
      cell = sheet[f'T{i + 2}']
      cell.font = Font(color="ff0000", italic=True)
    elif sheet[f'U{i + 2}'].value == 'X2' and int(text[a:b]) > int(text[c:d]):
      cell = sheet[f'T{i + 2}']
      cell.font = Font(color="ff0000", italic=True)




sheet['T1'].value = 'Результат'
book.save(f'hockey_statistics_today_{input_shans}_{input_izmen}.xlsx')
