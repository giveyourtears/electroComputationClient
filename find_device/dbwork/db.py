from typing import List
from pypika import Table, PostgreSQLQuery, Parameter, AliasedQuery, Order
import logging
from accounts.create_engine.core import engine
from accounts.databasework.dbwork import DatabaseLayerBase

db_work = DatabaseLayerBase()

def get_points_for_accounting(filters: List[str], inhibit_filters: List[str]) -> List:
    re_user_filters = []
    re_inhibit_user_filter = []
    result_filter: List[str]
    result_inhibit_filter: List[str]
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
    q = (PostgreSQLQuery.from_(p).select(p.object_name))
    filter_sql = db_work.get_query_by_user_filter(q, result_filter, result_inhibit_filter)
    sql = filter_sql.get_sql()
    result_elements = []
    re_user_filters.extend(re_inhibit_user_filter)
    logging.debug(f'SQL: {sql}')
    try:
        result = engine.execute(sql, re_user_filters)
        for row in result:
            result_elements.append(row)
    except Exception as e:
        logging.error("Error is ", e)
    logging.debug("get_points_for_accounting() OK...")
    return result_elements