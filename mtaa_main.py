from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.db.models import  F

from datetime import datetime


from mtaa_app.models import Users, Restaurants, Bookings


dbs_psswd = "helloworld" #password for authorization

def for_key_const(col, val):
    if col == "id_bookings":
        q = Bookings.objects.values("id_bookings")
        q = q.filter(Q(id_bookings=val))
        if q:

            pass
        else:
            err = {"errors": col, "reasons": "booking does not exist"}
            return err, 2
    return {}, 1

def book_insert_rest(i, val):
    id_r = 0
    try:
        id_r = int(val)
    except:
        err = {"errors": i, "reasons": "needs to be a number"}
        return 0, err, 422
    q = Restaurants.objects.values("id_restaurants")
    q = q.filter(Q(id_restaurants=val))
    if q:
        return id_r, {}, 200
    else:
        err = {"errors": i, "reasons": "restaurant does not exist"}
        return 0, err, 422

def book_insert_usr(i, val):
    id_u = 0
    try:
        id_u = int(val)
    except:
        err = {"errors": i, "reasons": "needs to be a number"}
        return 0, err, 422
    q = Users.objects.values("id_users")
    q = q.filter(Q(id_users=val))
    if q:
        return id_u, {}, 200
    else:
        err = {"errors": i, "reasons": "user does not exist"}
        return 0, err, 422

def book_insert_ppl(i, val):

    try:
        a = int(val)
    except:
        err = {"errors": i, "reasons": "needs to be a number"}
        return 0, err, 422
    if a <= 0:
        err = {"errors": i, "reasons": "needs to be more than 0"}
        return 0, err, 422
    return a, {}, 200


def book_insert_date(i, val):

    try:
        val = val.split("-")
        val_1 = val[2].split(" ")
        val_2 = val_1[1].split(":")
        d = datetime(int(val[0]), int(val[1]), int(val_1[0]), int(val_2[0]), int(val_2[1]), int(val_2[2]))  # transformations into datetime

    except:
        err = {"errors": i, "reasons": "wrong format try: YYYY-MM-DD HH:MM:SS"}
        return 0, err, 422

    return d, {}, 200

@csrf_exempt
def user_reg(request): #register a new users
    if request.method == 'POST':
        if request.POST.get("dbs_psswd") != dbs_psswd: #check auhorization
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        arr_of_cols = ["user_name", "password", "email"]
        try:
            img = request.FILES["user_image"]
        except:
            err = {"errors": "image", "reasons": "missing"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
        for i in arr_of_cols:

            val = request.POST.get(i)
            if i == "email":
                q = Users.objects.values("email")
                q = q.filter(Q(email=val))

                if q:
                    err = {"errors": val, "reasons": "email must be unique"}
                    return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
            if val is None:  # requires all values
                err = {"errors": i, "reasons": "required"}
                return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
        f = img.read()  # transforming the image
        b = bytearray(f)
        par = Users(user_name=request.POST.get("user_name"), password=request.POST.get("password"),
                    email=request.POST.get("email"), user_image=b)
        par.save()
        order_by = "id_users"
        p = Users.objects.values("id_users").order_by((F(order_by)).desc(nulls_last=True)).first()
        dictionary = {}
        dictionary['items'] = p

        return JsonResponse(dictionary, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=405)


@csrf_exempt
def user_log(request): #login user
    if request.method == 'GET':
        if request.GET.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        arr_of_cols = ["password", "email"]
        for i in arr_of_cols:

            val = request.GET.get(i)
            if val is None:
                err = {"errors": val, "reasons": "required"}
                return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)

        psswd = request.GET.get("password")
        mail = request.GET.get("email")
        q = Users.objects.values("id_users", "user_name", "email", "user_image")
        q = q.filter(Q(password=psswd) & Q(email=mail))
        to_dict = []
        for i in q: #picture to string
            a = i["user_image"].tobytes()
            i["user_image"] = str(a)
            to_dict.append(i)
            break
        dictionary = {}
        dictionary['items'] = to_dict
        return JsonResponse(dictionary, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=405)

@csrf_exempt
def rest_insert(request): #create new restaurant
    if request.method == 'POST':
        if request.POST.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        arr_of_cols = ["restaurant_name", "description"]
        try:
            img = request.FILES["restaurant_image"]
        except:
            err = {"errors": "image", "reasons": "missing"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
        for i in arr_of_cols:

            val = request.POST.get(i)
            if val is None:
                err = {"errors": i, "reasons": "required"}
                return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
        f = img.read()
        b = bytearray(f)
        par = Restaurants(restaurant_name=request.POST.get("restaurant_name"),
                          description=request.POST.get("description"), restaurant_image=b)  # POST and PUT

        par.save()
        order_by = "id_restaurants"
        p = Restaurants.objects.values("id_restaurants").order_by((F(order_by)).desc(nulls_last=True)).first()
        dictionary = {}
        dictionary['items'] = p
        return JsonResponse(dictionary, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=405)


@csrf_exempt
def rest_list(request): #get all restaurants
    if request.method == 'GET':
        if request.GET.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        q = Restaurants.objects.values("id_restaurants", "restaurant_name", "description", "restaurant_image")
        to_dict = []
        for i in q:
            a = i["restaurant_image"].tobytes()
            i["restaurant_image"] = str(a)
            to_dict.append(i)
        dictionary = {}
        dictionary['items'] = to_dict
        return JsonResponse(dictionary, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=405)

@csrf_exempt
def rest_det(request, rest_id): #get info about a chosen restaurant
    if request.method == 'GET':
        if request.GET.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        val = rest_id
        q = Restaurants.objects.values("id_restaurants", "restaurant_name", "description", "restaurant_image")
        q = q.filter(Q(id_restaurants=val))
        to_dict = []
        for i in q:
            a = i["restaurant_image"].tobytes()
            i["restaurant_image"] = str(a)
            to_dict.append(i)
            break
        dictionary = {}
        dictionary['items'] = to_dict
        return JsonResponse(dictionary, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=405)


@csrf_exempt
def book_create(request): #user creates a new booking
    if request.method == 'POST':
        if request.POST.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        arr_of_cols = ["user_id", "rest_id", "date_time", "num_ppl"]
        val = ""
        id_r = 0
        id_u = 0
        d = 0
        num_ppl = 1
        for i in arr_of_cols:

            val = request.POST.get(i)

            if val is None:
                err = {"errors": i, "reasons": "required"}
                return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
            #catching incorrect values
            if i == "user_id":
                id_u, err, code = book_insert_usr(i, val)
            elif i == "rest_id":
                id_r, err, code = book_insert_rest(i, val)
            elif i == "date_time":
                d, err, code = book_insert_date(i, val)
            else:
                num_ppl, err, code = book_insert_ppl(i, val)
            if err:
                return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=code)

        par = Bookings(user_id=Users.objects.get(id_users=id_u), rest_id=Restaurants.objects.get(id_restaurants=id_r),
                       date_time=d, num_ppl=num_ppl)
        par.save()
        order_by = "id_bookings"
        p = Bookings.objects.values("id_bookings").order_by((F(order_by)).desc(nulls_last=True)).first()
        dictionary = {}
        dictionary['items'] = p

        return JsonResponse(dictionary, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=405)

@csrf_exempt
def book_edit(request, book_id): #edit a booking
    if request.method == 'PUT':
        if request.GET.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        arr_of_cols = ["date_time", "num_ppl", "rest_id", "user_id"]
        val = book_id
        for c in arr_of_cols:
            to_update = request.GET.get(c)
            if to_update is not None:

                if c == "user_id":
                    id_u, err, code = book_insert_usr(c, to_update)
                elif c == "rest_id":
                    id_r, err, code = book_insert_rest(c, to_update)
                elif c == "date_time":
                    d, err, code = book_insert_date(c, to_update)
                else:
                    num_ppl, err, code = book_insert_ppl(c, to_update)
                if err:
                    return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=code)

                a = {c: to_update}
                Bookings.objects.filter(id_bookings=val).update(**a)
        return JsonResponse({}, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=405)


@csrf_exempt
def book_del(request, book_id): #delete a booking
    if request.method == 'DELETE':
        if request.GET.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        err, err_code = for_key_const("id_bookings", book_id)
        if err_code == 2:
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
        Bookings.objects.get(id_bookings=book_id).delete()
        return JsonResponse({}, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)


@csrf_exempt
def book_get(request, user_id): #list all users bookings
    if request.method == 'GET':
        if request.GET.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        q = Bookings.objects.values("id_bookings", "date_time", "num_ppl", 'rest_id__restaurant_name').filter(user_id=user_id)
        to_dict = []
        for i in q:
            to_dict.append(i)

        dictionary = {}
        dictionary['items'] = to_dict

        return JsonResponse(dictionary, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)



@csrf_exempt
def book_det(request, book_id): #get info about a booking
    if request.method == 'GET':
        if request.GET.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        p = Bookings.objects.values("id_bookings", "date_time", "num_ppl", 'rest_id__restaurant_name').filter(id_bookings=book_id).first()

        dictionary = {}
        dictionary['items'] = p

        return JsonResponse(dictionary, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)
    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
@csrf_exempt
def book_delall(request): #delete all bookings of a user before a specified date
    if request.method == 'DELETE':
        if request.GET.get("dbs_psswd") != dbs_psswd:
            err = {"errors": "dbs_psswd", "reasons": "incorrect"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=401)
        arr_of_cols = ["user_id", "date_time"]
        val1 = ""
        val2 = ""
        for i in arr_of_cols:

            val = request.GET.get(i)
            if val is None:
                err = {"errors": i, "reasons": "required"}
                return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
            if i == "user_id":
                val1 = val
            if i == "date_time":
                val2 = val
        try:
            Bookings.objects.filter(user_id=val1, date_time__lte=val2).delete()

        except:
            err = {"errors": "bookings", "reasons": "no such bookings"}
            return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)

        return JsonResponse({}, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=200)


    else:
        err = {"errors": "method", "reasons": "unrecognized"}
        return JsonResponse(err, json_dumps_params={'ensure_ascii': False, "indent": 4}, status=422)
