from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
@never_cache
@csrf_exempt
def login(request):
#    return HttpResponse("Got json data")
    if request.method == "POST":
        json_data = simplejson.loads(request.raw_post_data)
        try:
            form = AuthenticationForm(data=json_data)
            username = json_data['username']
            password = json_data['password']
            if form.is_valid():
                auth_login(request, form.get_user())
                return HttpResponse(form.get_user().username)
            return HttpResponse(username)
        except KeyError:
            return HttpResponseServerError()
        return HttpResponse(json_data)
    else:
        return HttpResponse("1111111111111Got json data")
#        json_data = simplejson.loads(request.raw_post_data)
#        try:
#            data = json_data['data']
#        except KeyError:
#            return HttpResponse("Got damn")#HttpResponseServerError("Malformed data!")
#        return HttpResponse("Got json data")
