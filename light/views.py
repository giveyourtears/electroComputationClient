import json
from typing import List, Dict
from django.shortcuts import render
from accounts import views
from django.http import HttpResponseRedirect, HttpResponse
import logging
from datetime import date, timedelta
from accounts.databasework.dbwork import DatabaseLayerBase
from django.views.decorators.csrf import csrf_exempt
from calendar import monthrange
from light.dbwork import db
from accounts.databasework.dbwork import DatabaseLayerBase

db_work = DatabaseLayerBase()

@csrf_exempt
def get_render_uo(request):
    result_dictionary = {}
    try:
        current_username = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        result_filter_db = db_work.read_user_filters(user)
        result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
        result = db.get_points_for_uo(result_filter_db, result_inhibit_filter_db)
        list_converted_items = []
        for elem in result:
            elem = str(elem).lstrip("('").rstrip("',)")
            list_converted_items.append(elem.split('\\\\'))
        for item in list_converted_items:
            end_part = ""
            for id_item, val in enumerate(item):
                if id_item == 5:
                    end_part = val
            if item[0] in result_dictionary:
                if item[1] in result_dictionary[item[0]]:
                    if item[2] in result_dictionary[item[0]][item[1]]:
                        if item[3] in result_dictionary[item[0]][item[1]][item[2]]:
                            if item[4] in result_dictionary[item[0]][item[1]][item[2]][item[3]]:
                                result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]].append(end_part)
                            else:
                                result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]] = []
                                result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]].append(end_part)
                        else:
                            result_dictionary[item[0]][item[1]][item[2]][item[3]] = {}
                            result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]] = []
                            result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]].append(end_part)
                    else:
                        result_dictionary[item[0]][item[1]][item[2]] = {}
                        result_dictionary[item[0]][item[1]][item[2]][item[3]] = {}
                        result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]] = []
                        result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]].append(end_part)
                else:
                    result_dictionary[item[0]][item[1]] = {}
                    result_dictionary[item[0]][item[1]][item[2]] = {}
                    result_dictionary[item[0]][item[1]][item[2]][item[3]] = {}
                    result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]] = []
                    result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]].append(end_part)
            else:
                result_dictionary[item[0]] = {}
                result_dictionary[item[0]][item[1]] = {}
                result_dictionary[item[0]][item[1]][item[2]] = {}
                result_dictionary[item[0]][item[1]][item[2]][item[3]] = {}
                result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]] = []
                result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]].append(end_part)
            sorted_array = sorted(set(result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]]))
            result_dictionary[item[0]][item[1]][item[2]][item[3]][item[4]] = sorted_array
        return HttpResponse(json.dumps(result_dictionary))
    except Exception as error_req:
        return HttpResponse("Bad Request " + str(error_req))


def light_view(request):
    if request.user.is_authenticated:
        logging.debug('Составление страницы Уличное Освещение')
        current_username = ''
        try:
            date_start = request.GET['date_one']
        except Exception as e:
            date_start = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        result_filter_db = db_work.read_user_filters(user)
        result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
        result_final = db.get_points_for_uo(result_filter_db, result_inhibit_filter_db)
        list_converted_items = []
        result_id = []
        res_res = []
        for elem in result_final:
            elem = str(elem).lstrip("('").rstrip("',)")
            list_converted_items.append(elem)
        for elem in list_converted_items:
            result_id.append(db.get_uo_id_elements(elem.replace('\\\\','\\')))
        res_res = None
        selsovet_select = []
        sum = 0
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
        if date_start == '':
            date_param_one = date.today().replace(day=1)
            date_param_now = date.today()
            res_res = db.get_elements_for_light(result_id, date_param_one, date_param_now)
            for elem in res_res:
                selsovet_select.append(elem['country'])
                re_sum = (elem['end_period'] - elem['start_period']) * elem['ktt']
                sum += re_sum
            selsovet_select = sorted(set(selsovet_select))
        else:
            splitted_date_one = date_start.split('-')
            if splitted_date_one[1][1:] == '0':
                splitted_date_one[1] = splitted_date_one[1][1:]

            last_day = monthrange(int(splitted_date_one[0]), int(splitted_date_one[1]))
            date_param_now = date.today()
            splitted_now_date = str(date_param_now).split('-')
            now_month = splitted_now_date[1][1:]
            if now_month == splitted_date_one[1][1:]:
                date_start = f"{splitted_date_one[0]}-{splitted_date_one[1]}-{1}"
                date_end = f"{splitted_date_one[0]}-{splitted_date_one[1]}-{splitted_now_date[2]}"
                res_res = db.get_elements_for_light(result_id, str(date_start), str(date_end))
            else:
                date_start = f"{splitted_date_one[0]}-{splitted_date_one[1]}-{1}"
                date_end = f"{splitted_date_one[0]}-{int(splitted_date_one[1]) + 1}-{1}"
                res_res = db.get_elements_for_light(result_id, str(date_start), str(date_end))
            for elem in res_res:
                selsovet_select.append(elem['country'])
                re_sum = (elem['end_period'] - elem['start_period']) * elem['ktt']
                sum += re_sum
            selsovet_select = sorted(set(selsovet_select))
        return render(request, 'light.html', {"table_elements": res_res, "select_data": selsovet_select,
                                                     "sum_all": sum, 'dict': result_for_menu, 'dict_two': fes_dictionary,
                                                     'dict_three': ps_dictionary})