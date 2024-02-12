import os

import gspread
import openpyxl

file = os.path.join(os.path.curdir, 'admin', 'Menu.xlsx')


async def gsheets_to_rows() -> list[list[str | int | float]]:
    """Получение всех строк из Google Sheets"""

    def to_int(val: str) -> int | str:
        try:
            res = int(val)
        except ValueError:
            return val
        return res

    def to_float(val: str) -> float | str:
        val = val.replace(',', '.')
        try:
            res = float(val)
        except ValueError:
            return val
        return res

    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('Menu')
    data = sh.sheet1.get_all_values()
    for row in data:
        row[:3] = list(map(to_int, row[:3]))
        row[-2:] = list(map(to_float, row[-2:]))

    return data


async def local_xlsx_to_rows() -> list[list[str | int | float]]:
    """Получение всех строк из локального файла Menu"""
    data = []
    wb = openpyxl.load_workbook(file).worksheets[0]
    for row in wb.iter_rows(values_only=True):
        data.append(list(row))
    return data


async def rows_to_dict(rows: list[list]) -> tuple:
    """Парсит строки полученные и источников в словарь"""

    menus = {}
    submenus = {}
    dishes = {}

    menu_num = None
    submenu_num = None

    for row in rows:
        if all(row[:3]):
            menu = {
                row[0]: {
                    'data': {'title': row[1], 'description': row[2]},
                    'id': None,
                }
            }
            menu_num = row[0]
            menus.update(menu)

        elif all(row[1:4]):
            submenu = {
                (menu_num, row[1]): {
                    'data': {'title': row[2], 'description': row[3]},
                    'parent_num': menu_num,
                    'id': None,
                    'parent_menu': None,
                }
            }
            submenu_num = row[1]
            submenus.update(submenu)

        elif all(row[3:6]):
            dish = {
                (menu_num, submenu_num, row[2]): {
                    'data': {
                        'title': row[3],
                        'description': row[4],
                        'price': row[5],
                    },
                    'parent_num': (menu_num, submenu_num),
                    'id': None,
                    'parent_submenu': None,
                    'discont': row[6],
                },
            }
            dishes.update(dish)
    return menus, submenus, dishes
