import json
from typing import List, Dict
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserLoginForm
import logging
from datetime import date, timedelta
from accounts.databasework.dbwork import DatabaseLayerBase
from django.views.decorators.csrf import csrf_exempt


def login_view(request, *args, **kwargs):
    """
    Страница авторизации
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect('/menu')
    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            request.session['username'] = user_obj.username
            login(request, user_obj)
            return HttpResponseRedirect("/menu")
        return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def create_dict_fes_description() -> Dict[str, str]:
    point_description: Dict[str, str] = dict()
    data_result = DatabaseLayerBase()
    try:
        dm_elements: List[str] = data_result.read_fes_name()
        for i in dm_elements:
            point_description[i] = ""
    except Exception as e:
        logging.error("error is " + e)
    return point_description


def create_dict_ps_description() -> Dict[str, str]:
    point_description: Dict[str, str] = dict()
    data_result = DatabaseLayerBase()
    try:
        dm_elements: List[str] = data_result.read_ps_name()
        for i in dm_elements:
            point_description[i] = ""
    except Exception as e:
        logging.error("error is " + e)
    return point_description


def menu_items_dict(request) -> Dict:
    common_dictionary = {}
    if 'username' in request.session:
        current_username = request.session['username']
        user = str(current_username)
        data_result = DatabaseLayerBase()
        result_filter_db = data_result.read_user_filters(user)
        array_list = []
        for filter_user in result_filter_db:
            person_filter = filter_user.split('\r\n')
            data_layer = data_result.get_all_string_by_filter(person_filter)
            for elem in data_layer:
                elem = str(elem).lstrip("('").rstrip("',)")
                array_list.append(elem.split('\\\\'))
            for item in array_list:
                end_part = ""
                for id_item, val in enumerate(item):
                    if id_item < 3:
                        continue
                    end_part += val + "\\"
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
    return common_dictionary


def index_view(request):
    """
    Выполняет составление меню для главной страницы
    """
    data_result = DatabaseLayerBase()
    if request.user.is_authenticated:
        logging.debug('Составление главного меню')
        common_dictionary = {}
        if 'username' in request.session:
            current_username = request.session['username']
            user = str(current_username)
            logging.info(f'Пользователь {user}')
            fes_dictionary = {}
            ps_dictionary = {}
            fes_name_dictionary = create_dict_fes_description()
            ps_name_dictionary = create_dict_ps_description()
            for fes in fes_name_dictionary.keys():
                fes_value = data_result.read_fes_value(fes)
                fes_dictionary[fes] = fes_value

            for ps in ps_name_dictionary.keys():
                ps_value = data_result.read_ps_value(ps)
                ps_dictionary[ps] = ps_value

            result_for_menu = menu_items_dict(request)
            print('her')
    else:
        return HttpResponseRedirect('/')
    logging.debug('index_view() OK...')
    return render(request, "home.html", {'dict': result_for_menu, 'dict_two': fes_dictionary,
                                         'dict_three': ps_dictionary})


@csrf_exempt
def get_fes_dic(request):
    try:
        current_username = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        data_result = DatabaseLayerBase()
        fes_dictionary = {}
        fes_name_dictionary = create_dict_fes_description()
        for fes in fes_name_dictionary.keys():
            fes_value = data_result.read_fes_value(fes)
            fes_dictionary[fes] = fes_value
        return HttpResponse(json.dumps(fes_dictionary))
    except Exception as error_req:
        return HttpResponse("Bad Request " + str(error_req))


@csrf_exempt
def get_ps_dic(request):
    try:
        current_username = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        data_result = DatabaseLayerBase()
        ps_dictionary = {}
        ps_name_dictionary = create_dict_ps_description()
        for ps in ps_name_dictionary.keys():
            ps_value = data_result.read_ps_value(ps)
            ps_dictionary[ps] = ps_value
        return HttpResponse(json.dumps(ps_dictionary))
    except Exception as error_req:
        return HttpResponse("Bad Request " + str(error_req))