import sqlite3

# INFO TABLES
TABLE_CLIENTS = 't_bank'
TABLE_AGGREGATED = 't_aggregated'
TABLE_CLIENTS_VALID = 't_clients_valid'
TABLE_CLIENTS_ONE_BANK = 't_clients_one_bank'

QUERY_CREATE_TABLE = {
    TABLE_CLIENTS: 'create_t_bank.sql',
    TABLE_AGGREGATED: 'create_t_aggregated.sql',
    TABLE_CLIENTS_VALID: 'create_t_clients_valid.sql',
    TABLE_CLIENTS_ONE_BANK: 'create_t_clients_one_bank.sql'
}
# END INFO TABLES

SELECT_QUERY = 'sources/sql_query/SELECT/'
CREATE_QUERY = 'sources/sql_query/CREATE/'

# шаблон для подстановки параметров в запрос
SYMBOL_SUBSTITUTION = '?'

# название БД
NAME_DATABASE = 'my_database.db'

# запрос для получения всех имеющихся в бд пользовательских таблиц
FILE_QUERY_TABLES = 'query_all_tables.sql'


class Query(object):
    def __init__(self):
        self.connect = sqlite3.connect(NAME_DATABASE)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # коммит
    def commit(self):
        """
        Run commit
        :return:
        """
        self.connect.commit()

    # закрытие соединения
    def close(self):
        """
        Close connections
        :return:
        """
        self.connect.close()

    # выполнение запроса без возврата данных
    def execute(self, sql, params):
        """
        Executing a query without returning data
        :param sql: Текст запроса
        :param params: Параметры для подстановки в запрос
        :return:
        """
        try:
            cur = self.connect.cursor()
            cur.execute(sql, params)
            cur.close()
            self.commit()

            result = True
        except Exception as error:
            print(error)
            self.connect.rollback()
            self.connect.close()
            result = False

        return result

    # выполнение запроса и возврат результата
    def execute_description(self, sql, params=None):
        """
        Executing a query and return the result
        :param sql: Текст запроса
        :param params: Параметры для подстановки в запрос
        :return:
        """
        data, desc = None, None
        if params is None:
            params = []
        try:
            cur = self.connect.cursor()
            cur.execute(sql, params)
            data = cur.fetchall()
            desc = [item[0] for item in cur.description]
            cur.close()
            self.commit()
        except Exception as error:
            print(error)
            self.connect.rollback()
            self.connect.close()

        return data, desc

    # выполнение запроса для записи данных большого объема
    def insert_into(self, sql_ins, sql_val, data):
        """
        Query execution to write large data
        :param sql_ins: Текст запроса
        :param sql_val: Маска для подстановки
        :param data: Данные для добавления в БД
        :return:
        """
        try:
            cursor = self.connect.cursor()
            sql = sql_ins + sql_val
            cursor.executemany(sql, data)
            cursor.close()
            self.commit()

            result = True
        except Exception as error:
            print(error)
            self.connect.rollback()
            self.connect.close()
            result = False

        return result

    # выполнение очистки таблицы
    def clear_table(self, table_name):
        """
        Performing table cleaning
        :param table_name: Название таблицы для очистки
        :return:
        """
        sql = 'DELETE FROM %s' % table_name
        return self.execute(sql, '')

    # удаление таблицы
    def delete_table(self, table_name):
        """
        Delete table
        :param table_name: Название таблицы для удаления
        :return:
        """
        sql = 'DROP TABLE IF EXISTS %s;' % table_name
        return self.execute(sql, '')

    # проверка всех ключевых таблиц в БД и их создание при необходимости
    def base_check(self, recreate_table=None):
        """
        Checking all key tables in the database and creating them if necessary
        :param recreate_table: Названия таблиц, которые нужно пересоздать
        :return:
        """
        if recreate_table is None:
            recreate_table = []
        with open(SELECT_QUERY + FILE_QUERY_TABLES, 'r') as f:
            sql = f.read()
        schema_tables = frozenset(item[0] for item in self.execute_description(sql)[0])
        for table, file_name in QUERY_CREATE_TABLE.items():
            if table not in schema_tables:
                pass
            elif table in recreate_table:
                self.delete_table(table)
            else:
                continue

            with open(CREATE_QUERY + file_name, 'r') as f:
                sql = f.read()
            self.execute(sql, '')
