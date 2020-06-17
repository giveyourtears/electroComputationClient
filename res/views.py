from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
import logging
import json
from accounts import views
from datetime import date, timedelta
from django.views.decorators.csrf import csrf_exempt
from accounts.databasework.dbwork import DatabaseLayerBase
from substation_info.dbwork import db

db_work = DatabaseLayerBase()


def res_view(request):
    if request.user.is_authenticated:
        logging.debug('Составление страницы РЭС')
        url_param = request.GET['res']
        result_url_string = url_param.split('/')
        current_username = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        result_filter_db = db_work.read_user_filters(user)
        result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
        result = db.get_elements_for_table(url_param, result_filter_db, result_inhibit_filter_db)
        array_list = []
        common_dictionary = {}
        data_layer = db_work.get_all_points_by_res(url_param, result_filter_db, result_inhibit_filter_db)
        for elem in data_layer:
            elem = str(elem).lstrip("('").rstrip("',)")
            array_list.append(elem.split('\\\\'))
        result_for_menu = views.menu_items_dict(request)
        fes_dictionary = {}
        ps_dictionary = {}
        fes_name_dictionary = views.create_dict_fes_description()
        ps_name_dictionary = views.create_dict_ps_description()
        for fes in fes_name_dictionary.keys():
            fes_value = db_work.read_fes_value(fes)
            fes_dictionary[fes] = fes_value

        for ps in ps_name_dictionary.keys():
            ps_value = db_work.read_ps_value(ps)
            ps_dictionary[ps] = ps_value
        for item in array_list:
            end_part = ""
            for id_item, val in enumerate(item):
                if id_item == 3:
                    end_part = val
            if item[0] in common_dictionary:
                if item[1] in common_dictionary[item[0]]:
                    if item[2] in common_dictionary[item[0]][item[1]]:
                        common_dictionary[item[0]][item[1]][item[2]].append(end_part)
                    else:
                        common_dictionary[item[0]][item[1]][item[2]] = []
                        common_dictionary[item[0]][item[1]][item[2]].append(end_part)
                else:
                    common_dictionary[item[0]][item[1]] = {}
                    common_dictionary[item[0]][item[1]][item[2]] = []
                    common_dictionary[item[0]][item[1]][item[2]].append(end_part)
            else:
                common_dictionary[item[0]] = {}
                common_dictionary[item[0]][item[1]] = {}
                common_dictionary[item[0]][item[1]][item[2]] = []
                common_dictionary[item[0]][item[1]][item[2]].append(end_part)
            agas_array = sorted(set(common_dictionary[item[0]][item[1]][item[2]]))
            common_dictionary[item[0]][item[1]][item[2]] = agas_array
    else:
        return HttpResponseRedirect('/')
    logging.debug('res_view() OK...')
    return render(request, 'res.html', {"name": result_url_string[1], "table_elems": common_dictionary,
                                        "ps": ps_dictionary, "dict": result_for_menu, "dict_two": fes_dictionary,
                                        "dict_three": ps_dictionary})


@csrf_exempt
def get_render_table_data(request):
    points = request.POST.getlist('points[]')
    start_date = date.today()
    sub_day: int = 0
    sub_month: int = 0
    if 'username' in request.session:
        current_username = request.session['username']
    user = str(current_username)
    logging.info(f'Пользователь {user}')
    result_filter_db = db_work.read_user_filters(user)
    result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
    result_dictionary = {}
    end_date_day = date.today() - timedelta(days=1)
    end_date_month = date.today() - timedelta(days=30)
    try:
        for point in points:
            array_ids = db_work.get_id_elements(point, result_filter_db, result_inhibit_filter_db)
            array_reg_ids = db_work.get_reg_id_elements(point.replace('/', r'\\'))
            result_points_data = []
            result_data_day = []
            result_data_day.extend(db_work.get_result_elements(array_ids, str(end_date_day), str(start_date)))
            result_data_reg_day = (
                db_work.get_reg_result_elements(array_reg_ids, str(end_date_day), str(start_date)))
            if len(result_data_reg_day) != 0:
                leng = len(result_data_reg_day)
                second = result_data_reg_day[leng - 1].start_period
                first = result_data_reg_day[0].start_period
                sub_day = second - first

            rashod_day = 0
            for day_elem in result_data_day:
                rashod_day += (day_elem.end_period - day_elem.start_period) * day_elem.ktt
            summ_losses_day = sub_day - rashod_day

            result_data_month = []
            result_data_month.extend(db_work.get_result_elements(array_ids, str(end_date_month), str(start_date)))
            result_data_reg_month = (db_work.get_reg_result_elements(array_reg_ids, str(end_date_month), str(start_date)))
            if len(result_data_reg_month) != 0:
                leng = len(result_data_reg_month)
                second = result_data_reg_month[leng - 1].start_period
                first = result_data_reg_month[0].start_period
                sub_month = second - first
            result_points_data.append(sub_month)
            result_points_data.append(sub_day)
            rashod_month = 0
            for day_elem in result_data_month:
                rashod_month += (day_elem.end_period - day_elem.start_period) * day_elem.ktt
            summ_losses_month = sub_month - rashod_month
            balance_percent_month = (summ_losses_month / sub_month) * 100
            balance_percent_day = (summ_losses_day / sub_day) * 100
            result_points_data.append(balance_percent_month)
            result_points_data.append(balance_percent_day)
            result_dictionary[point] = result_points_data
    except Exception as error_req:
        return HttpResponse("Bad Request " + str(error_req))
    return HttpResponse(json.dumps(result_dictionary))