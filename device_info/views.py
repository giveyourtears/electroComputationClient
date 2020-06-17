from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import logging
from accounts import views
from calendar import monthrange
import pytz
import datetime
from datetime import date, timedelta
from device_info.dbwork import db
from accounts.databasework.dbwork import DatabaseLayerBase

db_work = DatabaseLayerBase()


def device_view(request):
    if request.user.is_authenticated:
        logging.debug('Составление страницы Информация о приборе')
        url_param = request.GET['name']
        result_url_string = url_param.split('\\')
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        result_filter_db = db_work.read_user_filters(user)
        result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
        description = []
        result = db.get_elements_for_device(url_param, result_filter_db, result_inhibit_filter_db)
        for res in result:
            description.append(res['driver'])
            description.append(res['ktt'])
            description.append(res['number_point'])
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
        array_ids = db.get_id_device_elements(url_param, result_filter_db, result_inhibit_filter_db)
        start_date = date.today()
        start_date_month = date.today().replace(day=1)
        result_data_day = (db.get_result_device_day_elements(array_ids, str(start_date)))
        result_date_month = (db.get_result_device_day_elements(array_ids, str(start_date_month)))
    else:
        return HttpResponseRedirect('/')
    logging.debug('device_view() OK...')
    return render(request, 'device.html', {"ps": result_url_string[2], "vl": result_url_string[3],
                                                "tp": result_url_string[4], "tu": result_url_string[5],
                                                'description_array': description, "day_start": result_data_day,
                                                "day_start_month": result_date_month,
                                                "dict": result_for_menu, "dict_two": fes_dictionary,
                                                "dict_three": ps_dictionary})


def archive_day_view(request):
    if request.user.is_authenticated:
        logging.debug('Составление страницы "Архив по дню"')
        today = datetime.datetime.today()

        if len(str(today.month)) < 2:
            month = '0' + str(today.month)

        result_date = str(today.year) + "-" + month
        url_param = request.GET.get('driver_name')
        result_url_string = url_param.split('\\')
        try:
            date_param_one = request.GET['date_one']
            date_param_second = request.GET['date_second']
        except Exception as e:
            date_param_one = ''
            date_param_second = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        result_filter_db = db_work.read_user_filters(user)
        result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
        description = []
        result = db.get_elements_for_device(url_param, result_filter_db, result_inhibit_filter_db)
        for res in result:
            description.append(res['driver'])
            description.append(res['ktt'])
            description.append(res['number_point'])
        data_by_day_dict = {}
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
        if date_param_one == '' and date_param_second == '':
            date_param_one = date.today().replace(day=1)
            last_day = monthrange(date_param_one.year, date_param_one.month)
            date_param_second = f"{date_param_one.year}-{date_param_one.month}-{last_day[1]}"
        array_ids = db.get_id_device_elements(url_param, result_filter_db, result_inhibit_filter_db)
        result_data_by_day = db.get_result_day_by_day_elements(array_ids, str(date_param_one), str(date_param_second))
        minsk = pytz.timezone('Europe/Minsk')
        for elem_result in result_data_by_day:
            formatedDate = elem_result[1].replace(tzinfo=pytz.UTC).astimezone(minsk).replace(tzinfo=None).strftime("%d.%m.%Y")
            data_by_day_dict[formatedDate] = elem_result[0]
        return_button = '\\'.join(result_url_string)
        logging.debug('archive_day_view() OK...')
        return render(request, 'archive_day.html', {"ps": result_url_string[2], "vl": result_url_string[3],
                                                    "ktp": result_url_string[4], "description": description,
                                                    "data_by_date": data_by_day_dict, "return": return_button,
                                                    "dict": result_for_menu, "dict_two": fes_dictionary,
                                                    "dict_three": ps_dictionary, "date_result": result_date})
    else:
        return HttpResponseRedirect('/')


def archive_month_view(request):
    if request.user.is_authenticated:
        logging.debug('Составление страницы "Архив по месяцу"')
        url_param = request.GET['name']
        result_url_string = url_param.split('\\')
        try:
            year = request.GET['year']
        except Exception as e:
            year = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        result_filter_db = db_work.read_user_filters(user)
        result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
        description = []
        result = db.get_elements_for_device(url_param, result_filter_db, result_inhibit_filter_db)
        for res in result:
            description.append(res['driver'])
            description.append(res['ktt'])
            description.append(res['number_point'])
        array_ids = db.get_id_device_elements(url_param, result_filter_db, result_inhibit_filter_db)
        data_by_day_dict = {}
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
        if year == '':
            result_data_by_day = []
            today = date.today()
            now_year = today.year
            for i in range(1, 13):
                date_start = f"{now_year}-{i}-{1}"
                date_end = f"{now_year}-{i}-{2}"
                result_data_by_day.extend(db_work.get_result_elements(array_ids, str(date_start), str(date_end)))
        else:
            result_data_by_day = []
            for i in range(1, 13):
                date_start = f"{year}-{i}-{1}"
                date_end = f"{year}-{i}-{2}"
                result_data_by_day.extend(db_work.get_result_elements(array_ids, str(date_start), str(date_end)))
        minsk = pytz.timezone('Europe/Minsk')
        for elem_result in result_data_by_day:
            formatedDate = elem_result['time_start_write'].replace(tzinfo=pytz.UTC).astimezone(minsk).replace(tzinfo=None).strftime(
                "%d.%m.%Y")
            data_by_day_dict[formatedDate] = elem_result['start_period']
        return_button = '\\'.join(result_url_string)
    else:
        return HttpResponseRedirect('/')
    logging.debug('archive_month_view() OK...')
    return render(request, 'archive_month.html', {"ps": result_url_string[2], "vl": result_url_string[3],
                                                          "ktp": result_url_string[4], "description": description,
                                                          "data_by_date": data_by_day_dict, "return": return_button,
                                                          "dict": result_for_menu, "dict_two": fes_dictionary,
                                                          "dict_three": ps_dictionary
                                                          })


def rashod_day_view(request):
    if request.user.is_authenticated:
        logging.debug('Составление страницы "Расход по дню"')
        url_param = request.GET['name']
        result_url_string = url_param.split('\\')
        try:
            date_param_one = request.GET['date_one']
            date_param_second = request.GET['date_second']
        except Exception as e:
            date_param_one = ''
            date_param_second = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
        result_filter_db = db_work.read_user_filters(user)
        result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
        description = []
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
        result = db.get_elements_for_device(url_param, result_filter_db, result_inhibit_filter_db)
        for res in result:
            description.append(res['driver'])
            description.append(res['ktt'])
            description.append(res['number_point'])
        data_by_day_dict = {}
        array_ids = db.get_id_device_elements(url_param, result_filter_db, result_inhibit_filter_db)
        if date_param_one == '' and date_param_second == '':
            date_param_one = date.today().replace(day=1)
            last_day = monthrange(date_param_one.year, date_param_one.month)
            result_data_by_day = []
            for i in range(1, last_day[1]):
                date_start = f"{date_param_one.year}-{date_param_one.month}-{i}"
                date_end = f"{date_param_one.year}-{date_param_one.month}-{i+1}"
                result_data_by_day.extend(db_work.get_result_elements(array_ids, str(date_start), str(date_end)))
        else:
            splited_param = date_param_one.split('-')
            if splited_param[1][0] == '0':
                splited_param[1] = splited_param[1][1:]
            result_data_by_day = []
            last_day = monthrange(int(splited_param[0]), int(splited_param[1]))
            for i in range(1, last_day[1]):
                date_start = f"{splited_param[0]}-{splited_param[1]}-{i}"
                date_end = f"{splited_param[0]}-{splited_param[1]}-{i + 1}"
                result_data_by_day.extend(db_work.get_result_elements(array_ids, str(date_start), str(date_end)))

        minsk = pytz.timezone('Europe/Minsk')
        for elem_result in result_data_by_day:
            formatedDate = elem_result['time_start_write'].replace(tzinfo=pytz.UTC).astimezone(minsk).replace(tzinfo=None).strftime(
                "%d.%m.%Y")
            data_by_day_dict[formatedDate] = "{:10.3f}".format((elem_result['end_period'] - elem_result['start_period']) * elem_result['ktt'])
        return_button = '\\'.join(result_url_string)
    else:
        return HttpResponseRedirect('/')
    logging.debug('rashod_day_view() OK...')
    return render(request, 'rashod_day.html', {"ps": result_url_string[2], "vl": result_url_string[3],
                                                      "ktp": result_url_string[4], "description": description,
                                                      "data_by_date": data_by_day_dict, "return": return_button,
                                                      "dict": result_for_menu, "dict_two": fes_dictionary,
                                                      "dict_three": ps_dictionary
                                                      })


def rashod_month_view(request):
    if request.user.is_authenticated:
        logging.debug('Составление страницы "Расход по месяцу"')
        url_param = request.GET['name']
        result_url_string = url_param.split('\\')
        try:
            year = request.GET['year']
        except Exception as e:
            year = ''
        if 'username' in request.session:
            current_username = request.session['username']
        user = str(current_username)
        logging.info(f'Пользователь {user}')
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
        result_filter_db = db_work.read_user_filters(user)
        result_inhibit_filter_db = db_work.read_user_inhibit_filters(user)
        description = []
        result = db.get_elements_for_device(url_param, result_filter_db, result_inhibit_filter_db)
        for res in result:
            description.append(res['driver'])
            description.append(res['ktt'])
            description.append(res['number_point'])
        array_ids = db.get_id_device_elements(url_param, result_filter_db, result_inhibit_filter_db)
        data_by_day_dict = {}
        if year == '':
            result_data_by_day = []
            today = date.today()
            for i in range(1, 13):
                if i == 12:
                    continue
                if i == today.month:
                    date_start = f"{today.year}-{i}-{1}"
                    date_end = f"{today.year}-{i}-{today.day}"
                    result_data_by_day.extend(db_work.get_result_elements(array_ids, str(date_start), str(date_end)))
                else:
                    date_start = f"{today.year}-{i}-{1}"
                    date_end = f"{today.year}-{i + 1}-{1}"
                    result_data_by_day.extend(db_work.get_result_elements(array_ids, str(date_start), str(date_end)))
        else:
            result_data_by_day = []
            today = date.today()
            for i in range(1, 13):
                if i == 12:
                    continue
                if i == today.month:
                    date_start = f"{year}-{i}-{1}"
                    date_end = f"{year}-{i}-{today.day}"
                    result_data_by_day.extend(db_work.get_result_elements(array_ids, str(date_start), str(date_end)))
                else:
                    date_start = f"{year}-{i}-{1}"
                    date_end = f"{year}-{i + 1}-{1}"
                    result_data_by_day.extend(db_work.get_result_elements(array_ids, str(date_start), str(date_end)))
                date_start = f"{year}-{i}-{1}"
                date_end = f"{year}-{i+1}-{1}"
                result_data_by_day.extend(db_work.get_result_elements(array_ids, str(date_start), str(date_end)))
        minsk = pytz.timezone('Europe/Minsk')
        for elem_result in result_data_by_day:
            formatedDate = elem_result['time_start_write'].replace(tzinfo=pytz.UTC).astimezone(minsk).replace(
                tzinfo=None).strftime(
                "%d.%m.%Y")
            data_by_day_dict[formatedDate] = "{:10.3f}".format((elem_result['end_period'] - elem_result['start_period']) * elem_result['ktt'])
        return_button = '\\'.join(result_url_string)
    else:
        return HttpResponseRedirect('/')
    logging.debug('rashod_month_view() OK...')
    return render(request, 'rashod_month.html', {"ps": result_url_string[2], "vl": result_url_string[3],
                                                        "ktp": result_url_string[4], "description": description,
                                                        "data_by_date": data_by_day_dict, "return": return_button,
                                                        "dict": result_for_menu, "dict_two": fes_dictionary,
                                                        "dict_three": ps_dictionary
                                                        })
