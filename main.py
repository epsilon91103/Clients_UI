import os

from basic_functions import work_with_files
import db
from db import work_with_db


def main(**kwargs):
    """
    The main entry point of the application
    """
    # проверка таблиц в бд
    with db.Query() as query:
        query.base_check()

    if not ('update' in kwargs and not kwargs['update']):
        # получение данных из Excel
        clients_info = work_with_files.read_excel(
            'Test_study.xlsx',
            'Лист1',
            header=True,
            # integer_fields=[1, 2],
            # date_fields=[8, 9]
        )
        # запись данных в таблице
        work_with_db.add_data_in_db(*clients_info, db.TABLE_CLIENTS)

    # 3.1 получение агрегированных данных и запись в таблицу
    (aggregate_data, fields) = work_with_db.get_aggregate_data()
    work_with_db.add_data_in_db(fields, aggregate_data, db.TABLE_AGGREGATED)

    # 3.2 получение количества людей с не менее 3 действующими кредитами и запись в таблицу
    (clients, fields) = work_with_db.get_count_valid_clients()
    work_with_db.add_data_in_db(fields, clients, db.TABLE_CLIENTS_VALID)

    # 3.3 получение количества людей с не менее 3 действующими кредитами в одном банке и запись в таблицу
    (clients, fields) = work_with_db.get_count_clients_one_bank()
    work_with_db.add_data_in_db(fields, clients, db.TABLE_CLIENTS_ONE_BANK)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
    print('Done!')
