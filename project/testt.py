from db_manager import db_manager
from config import config

params = config()
db_name = "hh_vacancies"

test_bd = db_manager(db_name, params)

comp1 = test_bd.get_companies_and_vacancies_count()
# print(comp1)
comp2 = test_bd.get_all_vacancies()
# print(comp2)
comp3 = test_bd.get_avg_salary()
# print(comp3)


# cur.fetchall()
comp4 = test_bd.get_vacancies_with_higher_salary()
print(comp4)

comp5 = test_bd.get_vacancies_with_keyword("Специалист")
print(comp5)
