from db_manager import db_manager
from config import config
from prettytable import PrettyTable
params = config()
db_name = "hh_vacancies"
bd = db_manager(db_name, params)


def com_and_vac_count():
    table1 = PrettyTable()
    bd_counter = bd.get_companies_and_vacancies_count()
    table1.field_names = ['Компании', 'Количество актуальных вакансий']
    for i in bd_counter:
        table1.add_row([i[0], i[1]])
    return table1


def str_all_vac():
    table2 = PrettyTable()
    all_vac = bd.get_all_vacancies()
    table2.field_names = [
        'Вакансии', 'Компания',
        'Заработная плата', 'Валюта', 'Url']
    for i in all_vac:
        table2.add_row([i[0], i[1], f'{i[2]} - {i[3]}', i[4], i[5]])
    return table2


def str_avg_payment():
    table3 = PrettyTable()
    avg_payment = bd.get_avg_salary()
    table3.field_names = ['средняя зарплата по избранным вакансиям']
    table3.add_row([round(avg_payment[0][0])])
    return table3


def str_higher_salary():
    table4 = PrettyTable()
    higher_salary = bd.get_vacancies_with_higher_salary()
    table4.field_names = [
        'Вакансии', 'Компания',
        'Заработная плата', 'Валюта', 'Url']
    for i in higher_salary:
        table4.add_row([i[0], i[1], f'{i[2]} - {i[3]}', i[4], i[5]])
    return table4


def str_key_search():
    table5 = PrettyTable()
    key = input('Ключевое слово для поиска')
    key_search = bd.get_vacancies_with_keyword(key)
    table5.field_names = [
        'Вакансии', 'Компания',
        'Заработная плата', 'Валюта', 'Url']
    for i in key_search:
        table5.add_row([i[0], i[1], f'{i[2]} - {i[3]}', i[4], i[5]])
    return table5


def table_num_com(num_comp, page_of_com, page):
    table6 = PrettyTable()
    table6.field_names = [
        'Текущая компания',
        'Найдено компаний',
        'Номер списка']
    try:
        table6.del_row(0)
    except:
        pass
    finally:
        table6.add_row([num_comp + 1, len(page_of_com), page + 1])
    return table6


def table_num_vac(num_v, params_vacancies, page_v):
    table7 = PrettyTable()
    table7.field_names = [
        'Текущая вакансия',
        'Найдено вакансий',
        'Номер списка']
    try:
        table7.del_row(0)
    except:
        pass
    finally:
        table7.add_row([num_v + 1, len(params_vacancies), page_v + 1])
    return table7
