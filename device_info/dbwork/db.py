from typing import List
from pypika import Table, PostgreSQLQuery, Parameter, AliasedQuery, Order
from datetime import datetime
import logging
from accounts.create_engine.core import engine
from accounts.databasework.dbwork import DatabaseLayerBase
import pytz

db_work = DatabaseLayerBase()


def get_elements_for_device(department_filter: str, filters: List[str], inhibit_filters: List[str]) -> List:
    re_user_filters = []
    re_inhibit_user_filter = []
    result_filter: List[str]
    result_inhibit_filter: List[str]
    gg = department_filter.replace('/', '\\\\')
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
         .where(p.object_name == gg)
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
    logging.debug("get_elements_for_device() OK...")
    return result_elements


def get_id_device_elements(vl_url: str, filters: List[str], inhibit_filters: List[str]) -> List:
    re_user_filters = []
    re_inhibit_user_filter = []
    result_filter: List[str]
    result_inhibit_filter: List[str]
    gg = vl_url.replace('/', '\\\\')
    for inhibit in inhibit_filters:
        result_inhibit_filter = inhibit.split('\r\n')
        re_inhibit_user_filter = [w.replace('\\', '\\\\') for w in result_inhibit_filter]
        re_inhibit_user_filter = [w.replace('*', "%") for w in re_inhibit_user_filter]
    for filter_user in filters:
        result_filter = filter_user.split('\r\n')
        re_user_filters = [w.replace('\\', '\\\\') for w in result_filter]
        re_user_filters = [w.replace('*', "%") for w in re_user_filters]
    logging.debug('Получение таблицы балансов')
    p = Table('askue_rs_point', alias='p')
    q = (PostgreSQLQuery.from_(p)
         .select(p.id, p.object_name)
         .where(p.object_name == gg)
         )
    filter_sql = db_work.get_query_by_user_filter(q, result_filter, result_inhibit_filter)
    sql = filter_sql.get_sql()
    re_user_filters.extend(re_inhibit_user_filter)
    result_elements = []
    logging.debug(f'SQL: {sql}')
    try:
        result = engine.execute(sql, re_user_filters)
        for row in result:
            result_elements.append(row[0])
    except Exception as e:
        logging.error("Error is ", e)
    logging.debug("get_id_device_elements() OK...")
    return result_elements


def get_result_device_day_elements(list_id: List, start: str) -> float:
    logging.debug('Получение таблицы балансов')
    start_utc = datetime.strptime(start, '%Y-%m-%d').astimezone(pytz.UTC).replace(tzinfo=None)
    p = Table('calc_balance', alias='p')
    try:
        q = (PostgreSQLQuery.from_(p)
             .select(p.start_period)
             .where(
            (p.time_start_write == start_utc)
            & (p.id_tu.isin(list_id)))
             .orderby(p.dtp, order=Order.asc)
             )
        sql = q.get_sql()
    except Exception as e:
        logging.error("Error is ", e)
    result_elements = 0
    logging.debug(f'SQL: {sql}')
    try:
        result = engine.execute(sql)
        for row in result:
            result_elements = row[0]
    except Exception as e:
        logging.error("Error is ", e)
    logging.debug("get_result_device_day_elements() OK...")
    return result_elements


def get_result_day_by_day_elements(list_id: int, start: str, end: str) -> List:
    logging.debug('Получение таблицы балансов')
    start_utc = datetime.strptime(start, '%Y-%m-%d').astimezone(pytz.UTC).replace(tzinfo=None)
    end_utc = datetime.strptime(end, '%Y-%m-%d').astimezone(pytz.UTC).replace(tzinfo=None)
    p = Table('calc_balance', alias='p')
    try:
        q = (PostgreSQLQuery.from_(p)
             .select(p.start_period, p.time_start_write)
             .where(
            (p.time_start_write[start_utc:end_utc])
            & (p.id_tu == list_id[0])
             ).orderby(p.time_start_write, order=Order.asc))
        sql = q.get_sql()
    except Exception as e:
        logging.error("Error is ", e)
    result_elements = []
    logging.debug(f'SQL: {sql}')
    try:
        result = engine.execute(sql)
        for row in result:
            result_elements.append(row)
    except Exception as e:
        logging.error("Error is ", e)
    logging.debug("get_result_day_by_day_elements() OK...")
    return result_elements