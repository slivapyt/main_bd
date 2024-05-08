import psycopg2


class db_manager:

    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании'''
        comp_tally_vac = None
        try:
            conn = psycopg2.connect(dbname=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT company_name, COUNT(vacancies.profession)
                            FROM companies
                            LEFT JOIN vacancies USING(company_id)
                            GROUP BY company_name
                            ORDER BY COUNT(vacancies.profession) DESC""")
                comp_tally_vac = cur.fetchall()
        except:
            print("ошибка при внесение get_companies_and_vacancies_count")
        finally:
            conn.commit()
            conn.close()
            return comp_tally_vac

    def get_all_vacancies(self):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.'''
        all_vac = None
        try:
            conn = psycopg2.connect(dbname=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT profession, companies.company_name, payment_from, payment_to, currency, link 
                            FROM vacancies
                            JOIN companies USING(company_id)""")
                all_vac = cur.fetchall()
        except:
            print("ошибка при внесение get_all_vacancies")
        finally:
            conn.commit()
            conn.close()
            return all_vac

    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям.'''
        avg_payment = None
        try:
            conn = psycopg2.connect(dbname=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute("""
                SELECT AVG(val)
                FROM (
                    SELECT AVG((payment_to)::int) as val
                    FROM vacancies
                    WHERE payment_to NOT LIKE 'не указана'
                    UNION
                    SELECT AVG((payment_from)::int) as val
                    FROM vacancies
                    WHERE payment_from NOT LIKE 'не указана'
                    )
                    subquery""")
                avg_payment = cur.fetchall()
        except:
            print("ошибка при внесение get_companies_and_vacancies_count")
        finally:
            conn.commit()
            conn.close()
            return avg_payment

    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''
        list_plus_avg = None
        try:
            conn = psycopg2.connect(dbname=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT profession,companies.company_name, payment_from, payment_to, currency, link
                    FROM vacancies
                    JOIN companies USING(company_id)
                    WHERE payment_from NOT LIKE 'не указана' AND ((payment_from)::int) > (
                        SELECT AVG(val)
                        FROM (
                            SELECT AVG((payment_to)::int) as val
                            FROM vacancies
                            WHERE payment_to NOT LIKE 'не указана'
                            UNION
                            SELECT AVG((payment_from)::int) as val
                            FROM vacancies
                            WHERE payment_from NOT LIKE 'не указана'
                            )subquery)
                            OR payment_to NOT LIKE 'не указана' AND  ((payment_from)::int) > (
                                SELECT AVG(val)
                                FROM (
                                    SELECT AVG((payment_to)::int) as val
                                    FROM vacancies
                                    WHERE payment_to NOT LIKE 'не указана'
                                    UNION
                                    SELECT AVG((payment_from)::int) as val
                                    FROM vacancies
                                    WHERE payment_from NOT LIKE 'не указана'
                                    )subquery)""")
                list_plus_avg = cur.fetchall()
        except:
            print("ошибка при внесение get_companies_and_vacancies_count")
        finally:
            conn.commit()
            conn.close()
            return list_plus_avg

    def get_vacancies_with_keyword(self, keyword):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.'''
        word_search = None
        try:
            conn = psycopg2.connect(dbname=self.database_name, **self.params,)
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT profession,companies.company_name, payment_from, payment_to, currency, link
                            FROM vacancies
                            JOIN companies USING(company_id)
                            WHERE profession ILIKE '%{keyword}%' OR requirement ILIKE '%{keyword}%' OR responsibility LIKE '%{keyword}%'""")
                word_search = cur.fetchall()
        except:
            print("ошибка при внесение get_vacancies_with_keyword")
        finally:
            conn.commit()
            conn.close()
            return word_search
