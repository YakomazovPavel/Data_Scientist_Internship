import sqlite3


def sumchar(item):
    out = 0
    string = str(item)
    for simbol in string:
        out += int(simbol)
    return out


def main():
    """Функции func1 и func2 возвращают кортеж, состоящий их кортежей типа (Номер_группы, число покупателей)

        func1 выполнгяется для n_customers первых строк,
        func2 выполнятестся для n_customers от указанного id (n_first_id)

        Лирическое отступление:
        Была созданана тестовая БД. Не зная структуры основной бд, я мог не учесть некоторые особенности
        например: мои ID это значения INTEGER. в то время как в настоящей базе они могли быть VARCHAR и тогда
         ID 00001, 000001, 0000001 - это были бы три разных ID =), В то время как у меня все они равны 1.
         Так же непонятно упорядочены ли записи по ID, нужно ли применять сортировку перед тем как достать записи из БД?
         В общем все эти вопросы я было задал перед тем как приступать к работе, но так как спращивать не у кого
    """
    def func1(n_customers):
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()

            query = """SELECT id FROM customers LIMIT %(n_customers)d""" % {'n_customers': n_customers}
            ids = list(cursor.execute(query))
            for i in range(0, len(ids)):
                item = list(ids[i])
                item.append(sumchar(item[0]))
                ids[i] = tuple(item)

            query = """
                   DROP TABLE IF EXISTS temp;
                   """
            cursor.execute(query)

            query = """
                    CREATE TABLE temp (
                    ID INTEGER UNIQUE NOT NULL,
                    NumGroup INTEGER NOT NULL,
                    PRIMARY KEY(ID))
                    """
            cursor.execute(query)

            query = """
                    INSERT INTO temp (ID, NumGroup)
                    VALUES (?,?);
                    """
            cursor.executemany(query, ids)

            query = """
                    SELECT temp.NumGroup, COUNT(customers.ID)
                    FROM customers
                    LEFT JOIN temp
                    ON customers.ID = temp.ID
                    WHERE temp.NumGroup <> 'None'
                    GROUP BY NumGroup
                    """

            out = tuple(cursor.execute(query))

            query = """
                   DROP TABLE IF EXISTS temp;
                   """

            cursor.execute(query)

            return out

    def func2(n_first_id, n_customers):
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()
            query = """SELECT id FROM 
            (SELECT id FROM customers WHERE id >= %(n_first_id)d)
             LIMIT %(n_customers)d""" % {'n_customers': n_customers, 'n_first_id': n_first_id}

            ids = list(cursor.execute(query))
            for i in range(0, len(ids)):
                item = list(ids[i])
                item.append(sumchar(item[0]))
                ids[i] = tuple(item)

            query = """
                    DROP TABLE IF EXISTS temp;
                    """
            cursor.execute(query)

            query = """
                    CREATE TABLE temp (
                    ID INTEGER UNIQUE NOT NULL,
                    NumGroup INTEGER NOT NULL,
                    PRIMARY KEY(ID))
                    """
            cursor.execute(query)

            query = """
                    INSERT INTO temp (ID, NumGroup)
                    VALUES (?,?);
                    """
            cursor.executemany(query, ids)

            query = """
                    SELECT temp.NumGroup, COUNT(customers.ID)
                    FROM customers
                    LEFT JOIN temp
                    ON customers.ID = temp.ID
                    WHERE temp.NumGroup <> 'None'
                    GROUP BY NumGroup
                    """
            out = tuple(cursor.execute(query))

            query = """
                   DROP TABLE IF EXISTS temp;
                   """
            cursor.execute(query)

            return out


    print(func1(n_customers=2))
    print(func2(n_first_id=11, n_customers=2))

if __name__ == '__main__':
    main()
