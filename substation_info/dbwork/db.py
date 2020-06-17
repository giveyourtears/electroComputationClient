from typing import List
from pypika import Table, PostgreSQLQuery, Parameter, AliasedQuery, Order
import logging
from accounts.create_engine.core import engine
from accounts.databasework.dbwork import DatabaseLayerBase
from pypika import functions as fn

db_work = DatabaseLayerBase()


def get_elements_for_table(department_filter: str, filters: List[str], inhibit_filters: List[str]) -> List:
    re_user_filters = []
    re_inhibit_user_filter = []
    result_filter: List[str]
    result_inhibit_filter: List[str]
    gg = department_filter.replace('/', '\\\\') + "\\\\%%"
    for inhibit in inhibit_filters:
        result_inhibit_filter = inhibit.split('\r\n')
        re_inhibit_user_filter = [w.replace('\\', '\\\\') for w in result_inhibit_filter]
        re_inhibit_user_filter = [w.replace('*', "%") for w in re_inhibit_user_filter]
    for filter_user in filters:
        result_filter = filter_user.split('\r\n')
        re_user_filters = [w.replace('\\', '\\\\') for w in result_filter]
        re_user_filters = [w.replace('*', "%") for w in re_user_filters]
    logging.debug('Получение подстанций, присоединений для таблицы балансов')
    p = Table('askue_rs_point', alias='p')
    q = (PostgreSQLQuery.from_(p)
         .select('*')
         .where(p.object_name.like(gg))
         )
    filter_sql = db_work.get_query_by_user_filter(q, result_filter, result_inhibit_filter)
    sql = filter_sql.get_sql()
    result_elements = []
    logging.debug(f'SQL: {sql}')
    re_user_filters.extend(re_inhibit_user_filter)
    try:
        result = engine.execute(sql, re_user_filters)
        for row in result:
            result_elements.append(row)
    except Exception as e:
        logging.error("Error is ", e)
    logging.debug("get_elements_for_table() OK...")
    return result_elements


def get_start_data_res() -> str:
    logging.debug('Получение начальной даты')
    p = Table('calc_reg_balance', alias='p')
    q = (PostgreSQLQuery.from_(p)
         .select(fn.Min(p.time_start_write)))
    result_elements = ''
    sql = q.get_sql()
    logging.debug(f'SQL: {sql}')
    try:
        result = engine.execute(sql)
        for row in result:
            result_elements = row
    except Exception as e:
        logging.error("Error is ", e)
    logging.debug("get_start_data_res() OK...")
    return result_elements