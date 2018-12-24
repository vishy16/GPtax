import json
import urlparse
import os
from django import http
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth as contrib_auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.shortcuts import render

LOGIN_REDIRECT_URL = '/'

from django.contrib import messages
from accounts.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from accounts import forms as account_forms
from accounts import models as account_models


@csrf_protect
def auth(request):
  """
  The combined authentication and registration form page
  """
  if request.user.is_authenticated():
    return http.HttpResponseRedirect(LOGIN_REDIRECT_URL)

  if request.method == "POST":
    redirect_to = request.POST.get('next', LOGIN_REDIRECT_URL)
    form_type = request.POST.get('user-formtype') if request.POST.get(
      'user-formtype', False) else request.POST['formtype']

    # Login form submission.
    if form_type == "login":
      login_form = account_forms.LoginForm(data=request.POST)
      if login_form.is_valid():
        netloc = urlparse.urlparse(redirect_to)[1]

        # Heavier security check -- don't allow redirection to a different host.
        if netloc and netloc != request.get_host():
          redirect_to = LOGIN_REDIRECT_URL

        # Okay, security checks complete. Log the user in.
        contrib_auth.login(request, login_form.get_user())
        if request.session.test_cookie_worked():
          request.session.delete_test_cookie()

        if request.POST.get('keep-login', False):
          request.session[settings.KEEP_LOGGED_KEY] = True
        return http.HttpResponse(
          json.dumps(dict(success=True, redirect_to=redirect_to)))
      else:
        return http.HttpResponse(
          json.dumps(dict(msg='The email and password don\'t match',
                          success=False,
                          title='Wrong ID or Password')))

      # Unbound registration form to show in case of invalidation.
      user_form = account_forms.RegistrationForm(prefix="user")

    # Registration form submission.
    elif form_type == "registration":
      user_form = account_forms.RegistrationForm(data=request.POST, prefix="user")
      if user_form.is_valid():
        registered_user = user_form.save()
        password = user_form.cleaned_data['password1']
        email = user_form.cleaned_data['email']
        if registered_user.userprofile.email_verified:
          token = signup_models.OneTimeLoginToken.get_token(email)
          direct_login_rel_url = 'email=%s&token=%s' % (email, token)
          dm_utils.send_welcome_note.delay(
            email, password, direct_login_rel_url)

        # After registration, login the user and redirect to account for
        # filling in other details.
        new_user = contrib_auth.authenticate(username=email, password=password)
        contrib_auth.login(request, new_user)
        return http.HttpResponse(
          json.dumps(dict(success=True, redirect_to=LOGIN_REDIRECT_URL)))
      else:
        error_msg = ' '.join(
          [str(value[0]) for _, value in user_form.errors.iteritems()])
        return http.HttpResponse(
          json.dumps(dict(msg=error_msg, title='Error')))

      # Unbound login form to show in case of invalidation.
      login_form = account_forms.LoginForm(request)
      pass
    else:
      assert False, "should not be coming here"
  else:
    login_form = account_forms.LoginForm(request)
    user_form = account_forms.RegistrationForm(prefix="user")
    redirect_to = request.GET.get('next', LOGIN_REDIRECT_URL)

  context = {
    'loginform': login_form,
    'userform': user_form,
    'next': redirect_to,
    'login_page': True
  }
  return render_to_response('signup/combo.html',
                            context,
                            context_instance=RequestContext(request))


@login_required
def logout_user(request):
    contrib_auth.logout(request)
    return HttpResponseRedirect('/')
    
