from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import logging
from datetime import date, timedelta
from substation_info.dbwork import db
from accounts import views
from accounts.databasework.dbwork import DatabaseLayerBase

db_work = DatabaseLayerBase()


def first_words(input, words):
    for i in range(0, len(input)):
        if input[i] == '\\':
            words -= 1
        if words == 0:
            return input[0:i]
    return ""


class my_dictionary(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


def table_view(request):
    """
    Выполняет составление таблицы балансов распределений,
    основываясь на пути, взятом из меню пользователя
    """
    if request.user.is_authenticated:
        logging.debug('Составление таблицы балансов')
        url_param = request.GET.get('balans')
        try:
            vl_param = request.GET['vl']
            start_date = request.GET['start']
            end_date = request.GET['end']
            time_dif = request.GET['time_diff']
        except Exception as e:
            vl_param = ''
            start_date = ''
            end_date = ''
            time_dif = ''
        try:
            result_url_string = url_param.split('/')
            current_username = request.session['username']
            user = str(current_username)
            logging.info(f'Пользователь {user}')
            ps_dictionary = {}
            ps_name_dictionary = views.create_dict_ps_description()
            for ps in ps_name_dictionary.keys():
                ps_value = db_work.read_ps_value(ps)
                ps_dictionary[ps] = ps_value
            result_filter_db = db_work.read_user_filters(user)
            result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
            result = db.get_elements_for_table(url_param, result_filter_db, result_inhibit_filter_db)
            array_elements = []
            res_name = result_url_string[0] + "/" + result_url_string[1]
            res_res = result_url_string[1]
            menu_table_dictionary = my_dictionary()
            result_for_menu = views.menu_items_dict(request)
            fes_dictionary = {}
            pss_dictionary = {}
            fes_name_dictionary = views.create_dict_fes_description()
            ps_name_dictionary = views.create_dict_ps_description()
            for fes in fes_name_dictionary.keys():
                fes_value = db_work.read_fes_value(fes)
                fes_dictionary[fes] = fes_value
            for ps in ps_name_dictionary.keys():
                ps_value = db_work.read_ps_value(ps)
                pss_dictionary[ps] = ps_value
            name_ps = pss_dictionary[result_url_string[2]]
            for db_data in result:
                db_data = str(db_data).lstrip("('").rstrip("',)")
                left_join = db_data.find(result_url_string[-1])
                db_data = db_data[left_join:]
                right_join = db_data.find('\\\\')
                db_data = db_data[right_join + 2:]
                array_elements.append(first_words(db_data, 1))
                menu_table_dictionary.add(result_url_string[-1], set(array_elements))

            if vl_param == '':
                vl_param = array_elements[0]

            if start_date == '' and end_date == '':
                start_date = date.today()
                end_date = date.today() - timedelta(days=1)

            result_array_aga = []
            for elem in menu_table_dictionary.get(result_url_string[-1]):
                result_array_aga.append(elem)

            all_path = url_param + '/' + vl_param
            array_ids = db_work.get_id_elements(all_path, result_filter_db, result_inhibit_filter_db)
            array_reg_ids = db_work.get_reg_id_elements(all_path.replace('/', r'\\'))

            result_data = []
            result_data_reg = []
            result_data.extend(db_work.get_result_elements(array_ids, str(start_date), str(end_date)))
            result_data_reg.extend(db_work.get_reg_result_elements(array_reg_ids, str(start_date), str(end_date)))
            sub = 0
            hidden_start_date = db.get_start_data_res()
            year = hidden_start_date._row[0].year
            month = hidden_start_date._row[0].month
            day = hidden_start_date._row[0].day
            if len(result_data_reg) != 0:
                leng = len(result_data_reg)
                second = result_data_reg[leng - 1].start_period
                first = result_data_reg[0].start_period
                sub = second - first
            sub = abs(round(sub, 1))
            finish_data_str = str(year) + '-' + str(month) + '-' + str(day + 1)
        except Exception as e:
            fdsh = e
            print(e)
    else:
        return HttpResponseRedirect('/')
    logging.debug('table_view() OK...')
    return render(request, 'substation_info.html', {"table_elements": result_data, "menu_table": menu_table_dictionary,
                                               "time_dif": time_dif, "reg_consumption": sub,
                                               "hidden_date": finish_data_str, "ps": ps_dictionary,
                                               "dict": result_for_menu, "dict_two": fes_dictionary,
                                               "dict_three": pss_dictionary, "res_name": res_name, "res": res_res,
                                               "ps_name": name_ps
                                               })