import requests


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

    def get_value(self, req_values, page=0):
        '''Получаем данные после реквеста и номер страницы
            Возвращаем список по заданной странице'''
        self.__params["page"] = page
        pages_count = page + 1
        while self.__params["page"] < pages_count:
            try:
                values = req_values
            except Exception:
                print("ошибка при парсинге")
                break
            self.__page_values.extend(values)
            self.__params["page"] += 1
        # self.__params["page"] = 0
        return self.__page_values


class HeadHunter(Base):

    def __init__(self):
        super().__init__()
        self.__header = self._Base__header
        self.__params = self._Base__params
        self.__page_values = self._Base__page_values

    def get_request(self, keyword=None):
        '''keyword - Ключевое слово для поиска компании'''
        self.__params['text'] = keyword
        response = requests.get(
            "https://api.hh.ru/employers",
            headers=self.__header,
            params=self.__params,
        )
        js_response = response.json()
        return js_response

    def get_company_and_url(self, page_of_companies, num_company):
        '''СПИСОК:
            1.СТРОКА ДЛЯ ВЫВОДА
            2.СЛОВАРЬ КОМПАНИИ ДЛЯ БД '''
        formatted_company = {}
        formatted_company["company_id"] = page_of_companies[num_company]["id"]
        formatted_company["name"] = page_of_companies[num_company]["name"]
        formatted_company["url"] = page_of_companies[num_company]["url"]
        formatted_company["open_vacancies"] = page_of_companies[num_company]["open_vacancies"]

        formatted_company["vacancies_url"] = page_of_companies[num_company]["vacancies_url"]

        f_string = f'''
Компания: {page_of_companies[num_company]["name"]}
Url профиля компании: {page_of_companies[num_company]["url"]}
Актуально вакансий: {page_of_companies[num_company]["open_vacancies"]}
'''
        return (f_string, formatted_company)

    def com_navigation(self, num_comp, page_of_companies, company_name, page):
        cont = False
        name = False
        ins_com = False
        try:
            num_comp = int(num_comp)
        except:
            if num_comp.lower() == "name":
                company_name = input(
                    "Укажите название компании для поиска:\n")
                num_comp = 0
                name = True
                cont = True

            elif num_comp.lower() == "qqq":
                company_name = num_comp
                cont = True

            elif num_comp.lower() == "ins":
                num_comp = 0
                ins_com = True
                cont = True

            elif num_comp.lower() == "see":
                pass
            elif num_comp.lower() == "next":
                if page <= len(page_of_companies):
                    page += 1
                    print(f'{page + 1} сотня')
                    num_comp = 0
                    cont = True
                else:
                    print('список отсутствует')
                    num_comp = 0
                    cont = True
            elif num_comp.lower() == "back":
                if page > 0:
                    page -= 1
                    print(f'{page + 1} сотня')
                    num_comp = 0
                    cont = True
                else:
                    print('список отсутствует')
                    num_comp = 0
                    cont = True
            else:
                num_comp = 0
                cont = True
        else:
            if int(num_comp) >= 100:
                num_comp = input(
                    f'выберите в диапазоне {len(page_of_companies)}')
                cont = True
            else:
                cont = True
        return num_comp, cont, company_name, page, name, ins_com


class HH_vacancy(Base):

    def __init__(self):
        super().__init__()
        self.__header = self._Base__header
        self.__params = self._Base__params
        self.__page_values = self._Base__page_values

    def get_request(self, link):
        response = requests.get(
            link,
            headers=self.__header,
            params=self.__params,
        )
        js_response = response.json()
        return js_response

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

    def navigation_vacancies(self, range_vac):
        for i in range_vac:
            num_vac = input(
                f"{' ' * 10}Введите номер стр\n{'-' * 60}\n{' ' * 10}")
            try:
                num_vac = int(num_vac) - 1

            except:
                if num_vac.lower() == "qqq":
                    print(
                        f"\n{'-' * 60}\n{' ' * 10}Просмотр компаний\n{'-' * 60}\n{' ' * 10}")
                    return "qqq"
                if num_vac.lower() == "ins":
                    print('сохранено в бд')

                    return "ins"
                else:
                    print(
                        f'укажите номер заново номер вакансии в пределах \n{len(range_vac)} некорректный ввод')
                    continue

            else:
                if num_vac in range_vac:
                    return num_vac - 1
                elif num_vac not in range_vac:
                    print(f"\nЗа пределами списка")
                    continue

    @staticmethod
    def get_formatted_vacancy(dict_vacancy_value):
        str_vacancy_value = f'''\nВакансия: {dict_vacancy_value['profession']}
Минимальная заработная плата: {dict_vacancy_value['payment_from']} {dict_vacancy_value['currency']}
Максимальная заработная плата: {dict_vacancy_value['payment_to']} {dict_vacancy_value['currency']}
Ссылка на вакансию: {dict_vacancy_value['link']}
Город: {dict_vacancy_value['town']}
Адрес: {dict_vacancy_value['address']}
График занятости: {dict_vacancy_value['schedule']}
Требования: {dict_vacancy_value['requirement']}
Обязанности: {dict_vacancy_value['responsibility']}
'''
        return str_vacancy_value
