from prettytable import PrettyTable
table_n = PrettyTable()
table = PrettyTable()


class Navigate:

    def __init__(self, page):
        self.page = page
        self.status = True
        self.keyword_list = (
            'qqq', 'ins', 'see', 'name',
            'next', 'back', 'srh', 'stop',
            'count', 'vac', 'avg', 'high', 'key')

    def allocation(self, old_num_comp):
        key = input()
        if key.isdigit():
            return self.int_navigate(int(key) - 1)
        else:
            return self.str_navigate(key, old_num_comp)

    def int_navigate(self, key):
        '''key - инт индекс страницы'''
        if key <= len(self.page):
            return key, True
        else:
            key = 0
            return key, True

    def str_navigate(self, key, old_num_comp):
        '''key - команда, old_num_comp - индекс страницы'''
        if key.lower() in self.keyword_list:
            if key.lower() in ('ins', 'see', 'count', 'vac', 'avg', 'high', 'key'):
                return old_num_comp, key.lower()
            else:
                return 0, key.lower()
        else:
            return old_num_comp, True


def get_company_name():
    table.field_names = ['HeadHunter Favorite Vacancies']
    table.add_row(['Укажите название компании для поиска'])
    table.add_row(['Для выход - qqq'])
    print(table)
    company_name = input('  ')
    return company_name


def table_menu():
    table_n.field_names = [
        'Вакансии', 'Другие компании', 'Добавить в бд', 'Поиск по тегу', 'Отмена поиска', 'Следующий список', 'Предыдущий список', 'Выход']
    table_n.add_row([
        'see', 'name', 'ins', 'srh',
        'stop', 'next', 'back', 'qqq'])

    return table_n


out_table_menu = table_menu()
