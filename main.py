import sqlite3


def sumchar(item):
    out = 0
    string = str(item)
    for simbol in string:
        out += int(simbol)
    return out


"""
    Функции func1 и func2 возвращают список, состоящий их кортежей типа (Номер_группы, число покупателей)

    func1 выполнгяется для n_customers первых строк,
    func2 выполнятестся для n_customers от указанного id (n_first_id)

    Лирическое отступление:
    Была созданана тестовая БД. Не зная структуры основной бд, я мог не учесть некоторые особенности
    например: мои ID это значения INTEGER. в то время как в настоящей базе они могли быть VARCHAR и тогда
     ID 00001, 000001, 0000001 - это были бы три разных ID =), В то время как у меня все они равны 1.
     Так же непонятно упорядочены ли записи по ID, нужно ли применять сортировку перед тем как достать записи из БД?
     В общем все эти вопросы я бы задал перед тем как приступать к работе, но так как спращивать не у кого - работаем
"""


def func1(n_customers):
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()

        db.create_function('sumchar_all', 1, sumchar)

        query_values = {
            'n_customers': n_customers
        }

        query = """
                SELECT temp1.num_group, count(customers.id) FROM customers
                LEFT JOIN (
                    SELECT customers.id, sumchar_all(customers.id) AS num_group FROM (
                        SELECT id FROM customers LIMIT :n_customers) AS customers) AS temp1
                ON customers.id = temp1.id
                WHERE num_group <> 'None'
                GROUP BY num_group
                """

        return cursor.execute(query, {'n_customers': n_customers}).fetchall()


def func2(n_first_id, n_customers):
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()

        db.create_function('sumchar_all', 1, sumchar)

        query_values = {
            'n_first_id': n_first_id,
            'n_customers': n_customers
        }

        query = """
        SELECT temp1.num_group, count(customers.id) FROM customers
        LEFT JOIN (
            SELECT customers.id, sumchar_all(customers.id) as num_group FROM (
                SELECT id FROM (SELECT id FROM customers WHERE id >= :n_first_id)
            LIMIT :n_customers) as customers) AS temp1
        ON customers.id = temp1.id
        WHERE num_group <> 'None'
        GROUP BY num_group
        """

        return cursor.execute(query, query_values).fetchall()


if __name__ == '__main__':
    print(func1(6))
    print(func2(120, 3))
