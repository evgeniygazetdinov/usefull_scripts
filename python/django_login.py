from django.contrib.auth import (login as auth_login,  authenticate)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
...
def login(request):
    _message = 'Please sign in'
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                _message = 'Your account is not activated'
        else:
            _message = 'Invalid login, please try again.'
    context = {'message': _message}
    return render(request, 'myaccount/login.html', context)
...
