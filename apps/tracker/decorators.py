from django.shortcuts import redirect


def unauthenticated_user(view_func):
    # Redirects unregistered users to the sign-up page, otherwise redirects
    # registered users to the home page.
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            # return to the view function
            return view_func(request, *args, **kwargs)

    return wrapper_func
