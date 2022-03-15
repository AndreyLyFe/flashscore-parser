import requests
import openpyxl
from openpyxl.styles import Font



book = openpyxl.open('hockey_tomorrow.xlsx')
sheet = book.active



for i in range(sheet.max_row - 1):

  key = sheet[f'T{i+2}'].value
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
  sheet[f'R{i+2}'].value = f'{text[a:b]}:{text[c:d]}'

  if '÷' in sheet[f'R{i+2}'].value:
    sheet[f'R{i + 2}'].value = 'Не начался'
  else:
    if sheet[f'S{i + 2}'].value == 'П1' and int(text[a:b]) > int(text[c:d]):
      cell = sheet[f'R{i + 2}']
      cell.font = Font(color="33cc33", italic=True)
    elif sheet[f'S{i + 2}'].value == 'П2' and int(text[a:b]) < int(text[c:d]):
      cell = sheet[f'R{i + 2}']
      cell.font = Font(color="33cc33", italic=True)
    elif sheet[f'S{i + 2}'].value == 'Ничья' and int(text[a:b]) == int(text[c:d]):
      cell = sheet[f'R{i + 2}']
      cell.font = Font(color="33cc33", italic=True)
    elif sheet[f'R{i + 2}'].value != 'Не начался' and sheet[f'S{i + 2}'].value != 'Отсутствует' and sheet[f'S{i + 2}'].value != 'None' and type(sheet[f'S{i + 2}'].value) != 'NoneType':
      cell = sheet[f'R{i + 2}']
      cell.font = Font(color="ff0000", italic=True)



sheet['R1'].value = 'Результат'
book.save('hockey_statistics_tomorrow.xlsx')
