from typing import List
from pypika import Table, PostgreSQLQuery, Parameter, AliasedQuery, Order
from datetime import datetime
import logging
import pytz
from accounts.create_engine.core import engine


class DatabaseLayerBase:
    @staticmethod
    def read_user_filters(user: str) -> List:
        """
        Выполняет чтение всех фильтров пользоватлея
        :return: массив фильтров
        """
        logging.debug('Получение фильтров пользователя')
        p = Table('accounts_askueuser', alias='p')
        q = (PostgreSQLQuery.from_(p)
             .select(p.filter_department)
             .where(p.username == user)
             )
        sql = q.get_sql()
        ret_value = []
        logging.debug(f'SQL: {sql}')
        try:
            result = engine.execute(sql)
            for element in result:
                ret_value.append(element[0])
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("read_user_filters() OK...")
        return ret_value

    @staticmethod
    def read_fes_value(fes_name: str) -> str:
        """
        Выполняет чтение всех значений по имени
        :return: массив значений
        """
        logging.debug('Получение полного именования филиала')
        p = Table('accounts_filialmodel', alias='p')
        q = (PostgreSQLQuery.from_(p)
             .select(p.full_name)
             .where(p.short_name == fes_name)
             )
        sql = q.get_sql()
        ret_value = ""
        logging.debug(f'SQL: {sql}')
        try:
            result = engine.execute(sql)
            for element in result:
                ret_value = str(element).lstrip("('").rstrip("',)")
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("read_fes_value() OK...")
        return ret_value

    @staticmethod
    def read_ps_value(ps_name: str) -> str:
        """
        Выполняет чтение всех значений по имени
        :return: массив значений
        """
        logging.debug('Получение полного именования подстанции')
        p = Table('accounts_psmodel', alias='p')
        q = (PostgreSQLQuery.from_(p)
             .select(p.full_name)
             .where(p.short_name == ps_name)
             )
        sql = q.get_sql()
        ret_value = ""
        logging.debug(f'SQL: {sql}')
        try:
            result = engine.execute(sql)
            for element in result:
                ret_value = str(element).lstrip("('").rstrip("',)")
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("read_ps_value() OK...")
        return ret_value

    @staticmethod
    def read_fes_name() -> List:
        """
        Выполняет чтение всех сокращенных имен филиаолв
        :return: массив имен
        """
        logging.debug('Получение сокращенных имен филиалов')
        p = Table('accounts_filialmodel', alias='p')
        q = (PostgreSQLQuery.from_(p)
             .select(p.short_name)
             )
        sql = q.get_sql()
        ret_value = []
        logging.debug(f'SQL: {sql}')
        try:
            result = engine.execute(sql)
            for element in result:
                ret_value.extend(element)
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("read_fes_name() OK...")
        return ret_value

    @staticmethod
    def read_ps_name() -> List:
        """
        Выполняет чтение всех сокращенных имен филиаолв
        :return: массив имен
        """
        logging.debug('Получение сокращенных имен подстанций')
        p = Table('accounts_psmodel', alias='p')
        q = (PostgreSQLQuery.from_(p)
             .select(p.short_name)
             )
        sql = q.get_sql()
        ret_value = []
        logging.debug(f'SQL: {sql}')
        try:
            result = engine.execute(sql)
            for element in result:
                ret_value.extend(element)
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("read_ps_name() OK...")
        return ret_value

    @staticmethod
    def read_user_inhibit_filters(user: str) -> List:
        """
        Выполняет чтение всех фильтров пользоватлея
        :return: массив фильтров
        """
        logging.debug('Получение запрещающих фильтров пользователя')
        p = Table('accounts_askueuser', alias='p')
        q = (PostgreSQLQuery.from_(p)
             .select(p.inhibit_filter)
             .where(p.username == user)
             )
        sql = q.get_sql()
        ret_value = []
        logging.debug(f'SQL: {sql}')
        try:
            result = engine.execute(sql)
            for element in result:
                ret_value.extend(element)
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("read_user_inhibit_filters() OK...")
        return ret_value

    @staticmethod
    def get_all_string_by_filter(user_filters: List[str]) -> List[str]:
        """
        Получение всех объектов по фильтру пользоватлея
        :return: массив строк объектов
        """
        data_res = []
        re_user_filters = []
        logging.debug('Получение объектов по фильтрам пользователя')
        p = Table('askue_rs_point', alias='p')
        q = PostgreSQLQuery.from_(p).select(p.object_name)
        for filter_user in user_filters:
            q = q.where(p.object_name.like(Parameter('%s')))
            user_filter = filter_user.replace('\\', '\\\\')
            re_user_filters.append(user_filter.replace('*', "%"))
        sql = q.get_sql()
        logging.debug(f'SQL: {sql}')
        try:
            result_data = engine.execute(sql, re_user_filters)
            for element in result_data:
                data_res.append(element)
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("get_all_string_by_filter() OK...")
        return data_res

    @staticmethod
    def get_all_points_by_res(res: str, filters: List[str], inhibit_filters: List[str]) -> List:
        """
        Получение всех объектов по фильтру пользоватлея
        :return: массив строк объектов
        """
        db = DatabaseLayerBase()
        re_user_filters = []
        re_inhibit_user_filter = []
        result_filter: List[str]
        result_inhibit_filter: List[str]
        res_param = res.replace('/', '\\\\') + "\\\\%%"
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
             .select(p.object_name)
             .where(p.object_name.like(res_param))
             )
        filter_sql = db.get_query_by_user_filter(q, result_filter, result_inhibit_filter)
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
        logging.debug("get_all_points_by_res() OK...")
        return result_elements

    @staticmethod
    def get_query_by_user_filter(query: PostgreSQLQuery, filters: List[str],
                                 inhibit_filters: List[str]) -> PostgreSQLQuery:
        try:
            logging.debug('Получение запроса по критериям пользователя')
            t = Table('an_alias')
            test_query = (PostgreSQLQuery
                          .with_(query, "an_alias")
                          .from_(AliasedQuery("an_alias"))
                          .select('*'))
            for filter in filters:
                test_query = test_query.where(t.object_name.like(Parameter('%s')))
            for filter in inhibit_filters:
                test_query = test_query.where(t.object_name.not_like(Parameter('%s')))
        except Exception as e:
            logging.error("Error is ", e)
        return test_query


    @staticmethod
    def get_elements_reg_for_table(aga: str) -> List:
        logging.debug('Получение подстанций, присоединений для таблицы балансов')
        p = Table('askue_reg_point', alias='p')
        q = (PostgreSQLQuery.from_(p)
             .select(p.object_name)
             .where(p.object_name.like(f'{aga}%'))
             )
        sql = q.get_sql()
        result_elements = []
        logging.debug(f'SQL: {sql}')
        try:
            result = engine.execute(sql)
            for row in result:
                result_elements.append(row)
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("get_elements_reg_for_table() OK...")
        return result_elements

    @staticmethod
    def get_id_elements(vl_url: str, filters: List[str], inhibit_filters: List[str]) -> List:
        db = DatabaseLayerBase()
        re_user_filters = []
        re_inhibit_user_filter = []
        result_filter: List[str]
        result_inhibit_filter: List[str]
        gg = vl_url.replace('/', '\\\\') + "\\\\%%"
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
             .where(p.object_name.like(gg))
             )
        filter_sql = db.get_query_by_user_filter(q, result_filter, result_inhibit_filter)
        sql = filter_sql.get_sql()
        re_user_filters.extend(re_inhibit_user_filter)
        result_elements = []
        logging.debug(f'SQL: {sql}')
        try:
            result = engine.execute(sql, re_user_filters)
            for row in result:
                if row[1].rfind('УО') != -1:
                    continue
                result_elements.append(row[0])
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("get_id_elements() OK...")
        return result_elements


    @staticmethod
    def get_reg_id_elements(vl_url: str) -> List:
        logging.debug('Получение таблицы балансов')
        p = Table('askue_reg_point', alias='p')
        q = (PostgreSQLQuery.from_(p)
             .select(p.id)
             .where(p.object_name.like(f'{vl_url}%%'))
             )
        sql = q.get_sql()
        result_elements = []
        logging.debug(f'SQL: {sql}')
        try:
            result = engine.execute(sql)
            for row in result:
                result_elements.append(row[0])
        except Exception as e:
            logging.error("Error is ", e)
        logging.debug("get_reg_id_elements() OK...")
        return result_elements


    @staticmethod
    def get_result_elements(list_id: List, start: str, end: str) -> List:
        logging.debug('Получение таблицы балансов')
        start_utc = datetime.strptime(start, '%Y-%m-%d').astimezone(pytz.UTC).replace(tzinfo=None)
        end_utc = datetime.strptime(end, '%Y-%m-%d').astimezone(pytz.UTC).replace(tzinfo=None)
        p = Table('calc_balance', alias='p')
        pp = Table('calc_balance', alias='pp')
        try:
            q = (PostgreSQLQuery.from_(p).join(pp).on(p.id_tu == pp.id_tu)
                 .select(p.id_tu, p.dtp, p.locality, p.name_of_accounting_point, p.str_ra, p.pxx, p.loss_xx,
                         p.ktt, p.head_of_counter, p.start_period, pp.start_period.as_("end_period"),
                         p.q_slim, p.time_start_write)
                 .where(
                (p.time_start_write == start_utc)
                & (pp.time_start_write == end_utc)
                & (p.id_tu.isin(list_id)))
                 .orderby(p.dtp, order=Order.asc)
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
        logging.debug("get_result_elements() OK...")
        return result_elements


    @staticmethod
    def get_reg_result_elements(list_id: List, start: str, end: str) -> List:
        logging.debug('Получение таблицы балансов')
        start_utc = datetime.strptime(start, '%Y-%m-%d').astimezone(pytz.UTC).replace(tzinfo=None)
        end_utc = datetime.strptime(end, '%Y-%m-%d').astimezone(pytz.UTC).replace(tzinfo=None)
        p = Table('calc_reg_balance', alias='p')
        try:
            q = (PostgreSQLQuery.from_(p)
                 .select(p.id_tu, p.start_period, p.time_start_write)
                 .where(p.time_start_write.between(start_utc, end_utc) & (p.id_tu.isin(list_id)))
                 .orderby(p.time_start_write))
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
        logging.debug("get_reg_result_elements() OK...")
        return result_elements
