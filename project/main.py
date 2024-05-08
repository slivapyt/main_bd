from utils import HeadHunter, HH_vacancy
from config import config
from bd import create_database, insert_company_data
from navigation import Navigate

'''создание БД'''
params = config()
db_name = "hh_vacancies"
create_database(db_name, params)


company_name = input(
    f"\n{'-' * 60}\n{' ' * 10}qqq - Выход\n{'-' * 60}\n{' ' * 10}Укажите название компании для поиска:\n{'-' * 60}\n{' ' * 10}")
num_comp = 0  # номер компании на странице
page = 0
link_company = HeadHunter()
name = False

while True:
    ins_com = False
    see = False
    '''проверка на выход'''
    if company_name.lower() != "qqq":
        try:
            if name == True:
                link_company = HeadHunter()
            list_companies = link_company.get_request(company_name)['items']
            page_of_companies = link_company.get_value(list_companies, page)
            company = link_company.get_company_and_url(
                page_of_companies, num_comp)
        except:
            link_company = HeadHunter()
            print(f"\n{'-' * 60}\n{' ' * 20}Некорректные данные\n{'-' * 60}")
            company_name = input(
                "Укажите название компании для поиска:\nqqq - что бы выйти\n")
            name = False
            continue
    else:
        break

    '''Данные компании'''
    str_company_value = company[0]
    dict_company_value = company[1]
    company_vacancies_url = dict_company_value['vacancies_url']

    print(f"{'*' * 60}{str_company_value}{'*' * 60}")
    '''Навигация по компаниям'''
    num_comp = input(
        f"{'-' * 60}\n{' ' * 10}Другой тег - name | Смотреть вакансии - see\n{'-' * 60}\n{' ' * 10}Выход - qqq {' ' * 6}| Другие варианты - (1, 2, 3...)\n{'-' * 60}\n{' ' * 20}Найдено компаний: {len(page_of_companies)}\n{'-' * 60}\n{' ' * 10}")

    num_comp, cont, company_name, page, name, ins_com = link_company.com_navigation(
        num_comp, page_of_companies, company_name, page)

    if ins_com:
        insert_company_data(db_name, params, dict_company_value)

    if cont:
        continue

    '''Запрос вакансий'''
    vacancies = HH_vacancy()
    '''в get_request можно добавить атрибут для выбора профессии'''
    list_vacancy = vacancies.get_request(company_vacancies_url)['items']

    '''в get_value можно добавить атрибут для выбора страницы '''
    page_of_vacancies = vacancies.get_value(list_vacancy)
    params_vacancies = vacancies.create_params_vacancy(page_of_vacancies)

    num_comp = 0

    '''Навигация вакансий'''
    navigate = -1
    while True:

        insert = False
        dict_vacancy_value = params_vacancies[navigate]
        dict_vacancy_value['company_id'] = dict_company_value['company_id']
        formatted_vac = vacancies.get_formatted_vacancy(dict_vacancy_value)

        print(f"{'*' * 180}{formatted_vac}{'*' * 180}")
        print(
            f"{'-' * 60}\n{' ' * 10}страница номер {navigate + 2} из {len(params_vacancies)}\n{'-' * 60}\n{' ' * 10}qqq - что бы выйти\n{'-' * 60}")
        navigate = vacancies.navigation_vacancies(
            range(len(params_vacancies)))

        if navigate == "qqq" or navigate is None:
            break

        if navigate == "ins":
            insert = True
            navigate = -1
        if insert:
            insert_company_data(
                db_name, params, dict_company_value, dict_vacancy_value)
