import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о канале и видео"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f'CREATE DATABASE {database_name}')
    except:
        pass
    finally:
        cur.close()
        conn.close()

    try:
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE companies (
                    company_id serial,
                    company_name VARCHAR,
                    company_url VARCHAR,
                    open_vacancies integer,
                    vacancies_url VARCHAR,
                    CONSTRAINT pk_companies_company_id PRIMARY KEY (company_id)

                        )
                        """)
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancies_id serial,
                    profession VARCHAR,
                    payment_from VARCHAR,
                    payment_to VARCHAR,
                    currency VARCHAR,                    
                    link VARCHAR,
                    address VARCHAR,
                    town VARCHAR,
                    schedule VARCHAR,
                    requirement VARCHAR,
                    responsibility VARCHAR,
                    company_id serial,
                    CONSTRAINT pk_vacancies_vacancies_id PRIMARY KEY (vacancies_id),
                    CONSTRAINT fk_vacancies_companies FOREIGN KEY(company_id) REFERENCES companies(company_id)
                        )
                        """)
    except:
        pass
    finally:
        conn.commit()
        conn.close()


def insert_company_data(db_name, params, dict_company_value, dict_vacancy_value=None):
    try:
        conn = psycopg2.connect(dbname=db_name, **params)
        with conn.cursor() as cur:
            cur.execute(f"""
                        INSERT INTO companies (company_id, company_name, company_url, open_vacancies, vacancies_url)
                        VALUES (%s, %s, %s, %s, %s)
                        """, (
                dict_company_value['company_id'],
                dict_company_value['name'],
                dict_company_value['url'],
                dict_company_value['open_vacancies'],
                dict_company_value['vacancies_url']
            )
            )
    except:
        pass
    finally:
        conn.commit()
        conn.close()
        if dict_vacancy_value:
            try:
                conn = psycopg2.connect(dbname=db_name, **params)
                with conn.cursor() as cur:
                    cur.execute(f"""
                                INSERT INTO vacancies (profession, payment_from, payment_to, currency, link, address, town, schedule, requirement, responsibility, company_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (
                        dict_vacancy_value['profession'],
                        dict_vacancy_value['payment_from'],
                        dict_vacancy_value['payment_to'],
                        dict_vacancy_value['currency'],
                        dict_vacancy_value['link'],
                        dict_vacancy_value['address'],
                        dict_vacancy_value['town'],
                        dict_vacancy_value['schedule'],
                        dict_vacancy_value['requirement'],
                        dict_vacancy_value['responsibility'],
                        dict_vacancy_value['company_id']
                    )
                    )
            except:
                pass
            finally:
                conn.commit()
                conn.close()
