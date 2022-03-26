from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.db.models import  F

from datetime import datetime


from mtaa_app.models import Users, Restaurants, Bookings


dbs_psswd = "helloworld" #password for authorization



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