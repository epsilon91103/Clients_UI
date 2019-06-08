import db


# возвращает запрос из файла по его названию
def get_select_query(name_file):
    """
    Returns the query from the file by its name
    :param name_file: Название файла с запросом
    :return:
    """
    with open(db.SELECT_QUERY + name_file, 'r') as f:
        return f.read()


# добавление новых данных в бд
def add_data_in_db(name_fields, items, name_table, clear_table=True):
    """
    Adding new data to database
    :param name_fields: Наименование полей
    :param items: Итерируемая последовательность для записи в бд
    :param name_table: Название таблицы
    :param clear_table: Необходимость очистки таблицы перед записью
    :return:
    """
    table = name_table

    with db.Query() as query:
        if clear_table:
            query.clear_table(table)

        sql_ins = 'INSERT INTO {} ({}) VALUES '.format(table, ', '.join(name_fields))
        sql_val = '({})'.format(', '.join(item for item in [db.SYMBOL_SUBSTITUTION] * len(name_fields)))
        query.insert_into(sql_ins, sql_val, items)


# возвращает данные из бд в агрегированном виде
def get_aggregate_data():
    """
    Returns data from the database in aggregated form
    :return:
    """
    with db.Query() as query:
        sql = get_select_query('query_aggregated_data.sql')
        data = query.execute_description(sql)

    return data


# возвращает количество действующих клиентов, которые имеют не менее указанного кол-ва кредитов
def get_count_valid_clients(amount_of_credits=3):
    """
    Returns the number of active clients who have at least a specified number of credits
    :param amount_of_credits: Минимальное количество кредитов у человека
    :return:
    """
    with db.Query() as query:
        sql = get_select_query('query_clients_valid_loan.sql')
        (items, name_fields) = query.execute_description(sql, params=(amount_of_credits,))

    return items, name_fields


# возвращает количество действующих клиентов одного банка, которые имеют не менее указанного кол-ва кредитов
def get_count_clients_one_bank(amount_of_credits=3):
    """
    Returns the number of active clients of one bank who have at least a specified number of credits
    :param amount_of_credits: Минимальное количество кредитов у человека
    :return:
    """
    with db.Query() as query:
        sql = get_select_query('query_clients_one_bank.sql')
        (items, name_fields) = query.execute_description(sql, params=(amount_of_credits,))

    return items, name_fields


# возвращает количество всех клиентов
def get_count_clients():
    """
    Returns the number of all clients
    :return:
    """
    with db.Query() as query:
        sql = get_select_query('query_cnt_clients.sql')
        (items, name_fields) = query.execute_description(sql)

    return items, name_fields
