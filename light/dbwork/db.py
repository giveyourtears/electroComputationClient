from typing import List
from pypika import Table, PostgreSQLQuery, Parameter, AliasedQuery, Order
from datetime import datetime
import logging
import pytz
from accounts.create_engine.core import engine
from accounts.databasework.dbwork import DatabaseLayerBase

db_work = DatabaseLayerBase()


def get_points_for_uo(filters: List[str], inhibit_filters: List[str]) -> List:
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
            if row[0].rfind('УО') != -1:
                result_elements.append(row)
    except Exception as e:
        logging.error("Error is ", e)
    logging.debug("get_points_for_uo() OK...")
    return result_elements


def get_uo_id_elements(vl_url: str) -> List:
    logging.debug('Получение списка УО точек учета')
    p = Table('askue_rs_point', alias='p')
    gg = vl_url.replace('/', '\\\\')
    q = (PostgreSQLQuery.from_(p)
         .select(p.id)
         .where(p.object_name == gg)
         )
    sql = q.get_sql()
    result_elements = []
    logging.debug(f'SQL: {sql}')
    try:
        result = engine.execute(sql)
        for row in result:
            result_elements = row[0]
    except Exception as e:
        logging.error("Error is ", e)
    logging.debug("get_uo_id_elements() OK...")
    return result_elements


def get_elements_for_light(list_id: List, start: str, end: str) -> List:
    logging.debug('Получение данных для таблицы УО')
    start_utc = datetime.strptime(str(start), '%Y-%m-%d').astimezone(pytz.UTC).replace(tzinfo=None)
    end_utc = datetime.strptime(str(end), '%Y-%m-%d').astimezone(pytz.UTC).replace(tzinfo=None)
    p = Table('calc_balance', alias='p')
    pp = Table('calc_balance', alias='pp')
    try:
        q = (PostgreSQLQuery.from_(p).join(pp).on(p.id_tu == pp.id_tu)
             .select(p.id_tu, p.dtp, p.locality, p.name_of_accounting_point, p.str_ra, p.pxx, p.loss_xx,
                     p.ktt, p.head_of_counter, p.start_period, pp.start_period.as_("end_period"),
                     p.q_slim, p.time_start_write, p.country, p.driver)
             .where(
            (p.time_start_write == start_utc)
            & (pp.time_start_write == end_utc)
            & (p.id_tu.isin(list_id)))
             )
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
    logging.debug("get_elements_for_light() OK...")
    return result_elements