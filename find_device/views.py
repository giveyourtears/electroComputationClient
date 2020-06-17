import json
from typing import List, Dict
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import logging
from accounts import views
from find_device.dbwork import db
from django.views.decorators.csrf import csrf_exempt
from accounts.databasework.dbwork import DatabaseLayerBase

db_work = DatabaseLayerBase()


@csrf_exempt
def get_render_select_data(request):
    result_dictionary = {}
    try:
        current_username = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        result_filter_db = db_work.read_user_filters(user)
        result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
        result = db.get_points_for_accounting(result_filter_db, result_inhibit_filter_db)
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


def accounting_view(request):
    if request.user.is_authenticated:
        logging.debug('Составление страницы Учёты электроэнергии')
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
        return render(request, 'accounting.html', {'dict': result_for_menu, 'dict_two': fes_dictionary,
                                                   'dict_three': ps_dictionary})
    else:
        return HttpResponseRedirect('/')