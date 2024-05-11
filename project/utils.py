import requests
from prettytable import PrettyTable

table = PrettyTable()
table_v = PrettyTable()
table_v2 = PrettyTable()


class Base:
    def __init__(self):
        self.__header = {
            "User-Agent": "Brave/1.64 (platform:rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"}
        self.__params = {
            "text": None,
            "page": 0,
            "per_page": 100
        }
        self.__page_values = []

    def get_request(self, company_link, page=0, keyword=None,):
        '''keyword - Ключевое слово для поиска компании'''
        self.__params['text'] = keyword
        self.__params['page'] = page
        response = requests.get(
            company_link,
            headers=self.__header,
            params=self.__params
        )
        js_response = response.json()
        return js_response


def get_company_and_url(page_of_companies, num_company):
    '''СПИСОК:
        1.ТАБЛИЦА ВЫВОДА КОМПАНИЙ
        2.СЛОВАРЬ КОМПАНИИ ДЛЯ БД '''
    formatted_company = {}
    formatted_company["company_id"] = page_of_companies[num_company]["id"]
    formatted_company["name"] = page_of_companies[num_company]["name"]
    formatted_company["url"] = page_of_companies[num_company]["url"]
    formatted_company["open_vacancies"] = page_of_companies[num_company]["open_vacancies"]
    formatted_company["vacancies_url"] = page_of_companies[num_company]["vacancies_url"]

    table.field_names = [
        'Компания',
        'Url профиля компании', 'Актуально вакансий:']
    try:
        table.del_row(0)
    except:
        pass
    finally:
        table.add_row([
            page_of_companies[num_company]["name"],
            page_of_companies[num_company]["url"],
            page_of_companies[num_company]["open_vacancies"]])

    return (table, formatted_company)


class HH_vacancy(Base):

    def create_params_vacancy(self, page_of_vacancies):
        vacancy_list = []
        vacancies = page_of_vacancies
        for vacancy in vacancies:
            """------------------Название вакансии----------------------------"""
            try:
                profession = vacancy["name"]
            except KeyError:
                profession = "нет данных"

            """---------------------Зарплата----------------------------------"""
            try:
                currency = vacancy["salary"]["currency"]
            except TypeError:
                currency = ""

            try:
                payment_to = vacancy["salary"]["to"]
                if payment_to == None:
                    payment_to = "не указана"
            except TypeError:
                payment_to = "не указана"

            try:
                payment_from = vacancy["salary"]["from"]
                if payment_from == None:
                    payment_from = "не указана"
            except TypeError:
                payment_from = "не указана"

            """-----------------------Адрес-----------------------------------"""
            """Адрес: улица"""
            try:
                address = vacancy["address"]["street"]
            except TypeError:
                address = "нет данных"

            """Адрес: город"""
            try:
                town = vacancy["address"]["city"]
            except TypeError:
                town = "нет данных"

            """Адрес: дом"""
            try:
                building = vacancy["address"]["building"]
            except TypeError:
                building = ""
            address_build = f'{address} {building}'

            """Адрес: ссылка"""
            try:
                link = vacancy["alternate_url"]
            except KeyError:
                link = "нет данных"

            """-------------Условия и требования------------------------------"""
            """Режим работы"""
            try:
                schedule = vacancy["schedule"]["name"]
            except TypeError:
                schedule = "нет данных"

            """Требования"""
            try:
                requirement = vacancy["snippet"]["requirement"]
                if "<highlighttext>" in requirement:
                    requirement = requirement.replace(
                        "<highlighttext>", "</highlighttext>", "")
            except TypeError:
                requirement = "нет данных"

            """Обязанности"""
            try:
                responsibility = vacancy["snippet"]["responsibility"]
                if "<highlighttext>" in responsibility:
                    responsibility = responsibility.replace(
                        "<highlighttext>", "</highlighttext>", "")
            except TypeError:
                responsibility = "нет данных"
            """---------------------------------------------------------------"""
            vacancy_list.append(
                {
                    "profession": profession,
                    "payment_from": payment_from,
                    "payment_to": payment_to,
                    "currency": currency,
                    "link": link,
                    "address": address_build,
                    "town": town,
                    "schedule": schedule,
                    "requirement": requirement,
                    "responsibility": responsibility
                })
        return vacancy_list

    @staticmethod
    def get_formatted_vacancy(dict_vacancy_value):

        table_v.field_names = [
            'Вакансия', 'Минимальная з.п.', 'Максимальная з.п.', 'Валюта', 'Url', 'Город', 'Адрес', 'График занятости']

        table_v2.field_names = [dict_vacancy_value["requirement"]]
        try:
            table_v.del_row(0)
            table_v2.del_row(0)
        except:
            pass
        finally:
            table_v.add_row([
                dict_vacancy_value['profession'],
                dict_vacancy_value['payment_from'],
                dict_vacancy_value['payment_to'],
                dict_vacancy_value['currency'],
                dict_vacancy_value['link'],
                dict_vacancy_value['town'],
                dict_vacancy_value['address'],
                dict_vacancy_value['schedule']])
            table_v2.add_row([dict_vacancy_value["responsibility"]])
        return table_v, table_v2
