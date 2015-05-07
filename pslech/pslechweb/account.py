from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response, redirect
from django.template import Context, Template, RequestContext

def account_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user w/db
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Success, check permissions (user/admin)
                if user.is_staff:
                    # Staff redirected to control panel
                    return redirect('/control/')
                else:
                    # User redirected to practice homepage
                    return redirect('/home/')
            else:
                if user.last_login == user.date_joined:
                    # Not activated
                    return render(request, 'auth.login.html', {'error': 'inactive'})
                else:
                    # User account has been disabled
                    return render_to_response('auth.login.html', {'error': 'disabled'}, context_instance=RequestContext(request))
        else:
            # User account not found or password is incorrect
            return render_to_response('auth.login.html', {'error': 'incorrect'}, context_instance=RequestContext(request))
    else:
        if request.user.is_authenticated():
            if 'next' not in request.GET:
                # Why are you visiting my sign in page again?
                return redirect('/')
            else:
                return render(request, 'auth.login.html', {'error':'permission'})
        else:
            return render(request, 'auth.login.html')

def account_logout(request):
    # Logout for user
    logout(request)

    return render_to_response('auth.logout.html', {}, context_instance=RequestContext(request))

def account_register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST) # Bind to user submitted form
        if form.is_valid():
            # Process account registration
            user = User.objects.create_user(username=form.cleaned_data['email'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']
            user.is_active = False
            user.save()

            # Generate a activation key using existing salt for pwd
            algorithm, iterations, salt, hashed = user.password.split('$', 3)
            activation_key = make_password(user.email, salt, algorithm)
            algorithm, iterations, salt, activation_key = activation_key.split('$', 3)
            activation_key = activation_key[:-1]
            # Alternative char for + and /
            activation_key = activation_key.replace('+','-').replace('/','_')

            title = 'Account Activation'
            content = render_to_string('register.email', {'first_name': user.first_name, 'last_name': user.last_name, 'is_secure': request.is_secure(), 'host': request.get_host(), 'activation_key': activation_key, 'sender': settings.PROJECT_NAME})

            send_mail(title, content, settings.PROJECT_NAME + ' <' + settings.EMAIL_HOST_USER + '>', [user.email])

            return render(request, 'account.register.success.html')
    else:
        # Display new form for user to fill in
        form = forms.RegistrationForm()

    return render(request, 'account.register.form.html', {'form': form})

def account_activate(request):
    # Already activated
    if request.user.is_authenticated():
        return render(request, 'account.activate.success.html', {'error': 'activated'})

    if request.method == 'GET':
        # Get activation details
        activation_key = request.GET.get('key')

        # No activation key, throw to login page
        if activation_key is None:
            return redirect('/accounts/login/')

        # Keep activation key in session awaiting login
        request.session['activation_key'] = activation_key

        form = forms.ActivationForm()
    else:
        # Attempt to activate user using given user, password and key
        form = forms.ActivationForm(request.POST)
        if form.is_valid():
            # Try logging in
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is None:
                form.activation_error = 'incorrect'
            else:
                # Already active? error!
                if user.is_active:
                    form.activation_error = 'expired'
                else:
                    # Match activation key
                    algorithm, iterations, salt, hashed = user.password.split('$', 3)
                    activation_key = make_password(user.email, salt, algorithm)
                    algorithm, iterations, salt, activation_key = activation_key.split('$', 3)
                    activation_key = activation_key[:-1]
                    # Alternative char for + and /
                    activation_key = activation_key.replace('+','-').replace('/','_')

                    form.key1 = request.session['activation_key']
                    form.key2 = activation_key

                    # Match keys
                    if activation_key == request.session['activation_key']:
                        # Activated, login and proceed
                        user.is_active = True
                        user.save()
                        login(request, user)

                        return render(request, 'account.activate.success.html')
                    else:
                        # Key expired!
                        form.activation_error = 'expired'

    return render(request, 'account.activate.form.html', {'form': form})

def account_forgot(request):
    if request.method == 'POST':
        form = forms.PasswordForgetForm(request.POST) # Bind to user submitted form
        if form.is_valid():
            # Retrieve user from db
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
            except User.DoesNotExist:
                return redirect('/accounts/forgot/?error=nouser')

            # Generate a reset key using existing salt for pwd
            algorithm, iterations, salt, hashed = user.password.split('$', 3)
            reset_key = make_password(user.email, salt, algorithm)
            algorithm, iterations, salt, reset_key = reset_key.split('$', 3)
            reset_key = reset_key[:-1]
            # Alternative char for + and /
            reset_key = reset_key.replace('+','-').replace('/','_')

            title = 'Password Reset'
            content = render_to_string('passwordreset.email', {'first_name': user.first_name, 'last_name': user.last_name, 'host': request.get_host(), 'reset_key': reset_key, 'sender': settings.PROJECT_NAME, 'email': user.email})

            send_mail(title, content, settings.PROJECT_NAME + ' <' + settings.EMAIL_HOST_USER + '>', [user.email])

            return render(request, 'account.forgot.success.html')
    else:
        # Display new form for user to fill in
        form = forms.PasswordForgetForm()

    return render(request, 'account.forget.form.html', {'form': form})

def account_reset(request):
    if request.user.is_authenticated():
        pass
    else:
        if request.method == 'GET':
            # TODO: Error messages if key is not valid or email is wrong

            # Reset password for user who has forgotten it
            # Get user from request data
            user_email = request.GET.get('user')

            # Retrieve user from db
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                return redirect('/accounts/forgot/?error=nouser')

            # Get reset key from request data
            reset_key_input = request.GET.get('key')

            # No reset key, throw to login page
            if reset_key_input is None:
                return redirect('/accounts/forgot/?error=nokey')

            # Match reset key
            algorithm, iterations, salt, hashed = user.password.split('$', 3)
            reset_key = make_password(user.email, salt, algorithm)
            algorithm, iterations, salt, reset_key = reset_key.split('$', 3)
            reset_key = reset_key[:-1]
            # Alternative char for + and /
            reset_key = reset_key.replace('+','-').replace('/','_')

            # Match keys
            if reset_key == reset_key_input:
                # Reset keys match, render page for user to reset
                # Store reset email in session
                request.session['reset_email'] = user_email

                form = forms.PasswordResetForm(initial={'email': user_email})
            else:
                # Key expired!
                return redirect('/accounts/forgot/?error=keymismatch')
        elif request.method == 'POST':
            form = forms.PasswordResetForm(request.POST)
            if form.is_valid():
                # Perform real resetting of account
                # Check if emails from form and session matches
                if form.cleaned_data['email'] == request.session['reset_email']:
                    # Get user
                    try:
                        user = User.objects.get(email=request.session['reset_email'])
                    except User.DoesNotExist:
                        return redirect('/accounts/forgot/?error=nouser')

                    # Update password of user in system
                    user.set_password(form.cleaned_data['password'])
                    user.save()

                    # Success, login user and display success page
                    user = authenticate(username=user.username, password=form.cleaned_data['password'])
                    login(request, user)

                    return render(request, 'account.reset.success.html')
                else:
                    return redirect('/accounts/forgot/?error=email')

        return render(request, 'account.reset.form.html', {'form': form})


