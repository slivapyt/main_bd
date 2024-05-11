from utils import HH_vacancy, get_company_and_url, Base
from config import config
from bd import create_database, insert_company_data
from navigation import Navigate, get_company_name, out_table_menu

from str_manager import table_num_com, table_num_vac, com_and_vac_count, str_all_vac, str_avg_payment, str_higher_salary, str_key_search

'''создание БД'''
params = config()
db_name = "hh_vacancies"
create_database(db_name, params)

'''первичные атрибуты компании'''
num_comp, page, command = 0, 0, False
key_commands = (
    'qqq', 'ins', 'see',
    'name', 'next', 'back',
    'srh', 'stop', 'count',
    'vac', 'avg', 'high', 'key')
'''генерация request запроса '''
directory = Base()
company_link = "https://api.hh.ru/employers"
company_name = get_company_name()

while True:
    '''---------проверка на смену компании и выход--------'''
    if command == 'name':
        command = False
        company_name = input(f"Введите название другой компании:\n")
    elif company_name == 'qqq':
        break

    '''--------------получаем request------------------'''
    try:
        page_of_companies = directory.get_request(
            company_link, page, company_name)['items']

        '''----------проверка page---------------------'''
        if page_of_companies == []:
            page = 0
            command = False
            print(f'   Некорректные данные\n   Введите название компании')
            company_name = input()
            continue
    except KeyError:
        page = 0
        continue

    '''-------------------Данные компании------------------'''
    company = get_company_and_url(page_of_companies, num_comp)
    table_company_value = company[0]
    dict_company_value = company[1]
    company_vacancies_url = dict_company_value['vacancies_url']

    '''-------------------Таблицы интерфейса------------'''
    print('\n'*10)
    print(f'{"-"*40}ИНФОРМАЦИЯ О КОМПАНИИ{"-"*70}')
    print(table_company_value)
    print(f'{"-"*40}КОМАНДНОЕ МЕНЮ{"-"*77}')
    print(out_table_menu)
    print(table_num_com(num_comp, page_of_companies, page))
    print(f'{"-"*130}')
    '''-------------------Навигация по компаниям------------'''
    old_num_comp = num_comp
    navigate = Navigate(page_of_companies)
    num_comp, command = navigate.allocation(old_num_comp)

    if command in key_commands:
        if command == 'qqq':
            command = False
            break
        elif command == 'next':
            command = False
            page += 1
            continue
        elif command == 'back':
            command = False
            page -= 1
            continue
        elif command == "ins":
            command = False
            insert_company_data(db_name, params, dict_company_value)
            continue
        elif command == 'see':
            command = False
        elif command == 'name':
            continue
        elif command_v in ('srh', 'stop'):
            continue
        elif command_v in ('count', 'vac', 'avg', 'high', 'key'):
            if command_v == 'count':
                print(com_and_vac_count())
            elif command_v == 'vac':
                print(str_all_vac())
            elif command_v == 'avg':
                print(str_avg_payment())
            elif command_v == 'high':
                print(str_higher_salary())
            elif command_v == 'key':
                print(str_key_search())
            command_v = False
            input('продолжить')
    else:
        continue
    '''первичные атрибуты вакансии'''
    page_v, num_v, old_num_v = 0, 0, 0
    command_v = False

    '''------------------Запрос вакансий--------------------'''
    vacancies = HH_vacancy()
    page_of_vacancies = vacancies.get_request(
        company_vacancies_url, page_v)['items']
    params_vacancies = vacancies.create_params_vacancy(page_of_vacancies)

    while True:
        '''поиск вакансии по ключевому слову'''
        if command_v in ['srh', 'stop']:
            if command_v == 'srh':
                keyword = input()
            else:
                keyword = None
            command_v = False

            page_of_vacancies = vacancies.get_request(
                company_vacancies_url, page_v, keyword)['items']
            params_vacancies = vacancies.create_params_vacancy(
                page_of_vacancies)

        '''-----------------Составление  данных вакансии-----------------'''
        dict_vacancy_value = params_vacancies[num_v]
        dict_vacancy_value['company_id'] = dict_company_value['company_id']
        table_formatted_vac = vacancies.get_formatted_vacancy(
            dict_vacancy_value)

        '''-----------------Интерфейс------------------------------------'''
        print('\n'*10)
        print(f'{"-"*40}ИНФОРМАЦИЯ О ВАКАНСИИ{"-"*70}')
        print(f'{table_formatted_vac[0]} \n{table_formatted_vac[1]}')
        print(f'\n{"-"*40}КОМАНДНОЕ МЕНЮ{"-"*77}')
        print(table_num_vac(num_v, params_vacancies, page_v))
        print(f'{"-"*130}')

        '''-----------------Навигация------------------------------------'''
        navigate_v = Navigate(params_vacancies)
        num_v, command_v = navigate_v.allocation(old_num_v)

        if command_v in key_commands:
            if command_v == 'qqq':
                command = 'qqq'
                break
            elif command_v == 'next':
                command_v = False
                page_v += 1
                continue
            elif command_v == 'back':
                command_v = False
                page_v -= 1
                continue
            elif command_v == "ins":
                command_v = False
                insert_company_data(
                    db_name, params, dict_company_value, dict_vacancy_value)
                continue
            elif command_v == 'name':
                command = 'name'
                break
            elif command_v in ('srh', 'stop'):
                continue
            elif command_v in ('count', 'vac', 'avg', 'high', 'key'):
                if command_v == 'count':
                    print(com_and_vac_count())
                elif command_v == 'vac':
                    print(str_all_vac())
                elif command_v == 'avg':
                    print(str_avg_payment())
                elif command_v == 'high':
                    print(str_higher_salary())
                elif command_v == 'key':
                    print(str_key_search())
                command_v = False
                input('продолжить')
        else:
            continue
