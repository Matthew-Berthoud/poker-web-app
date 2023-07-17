from functools import wraps  # https://docs.python.org/3/library/functools.html#functools.wraps

def login_required(f):  # https://flask.palletsprojects.com/en/2.3.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def admin_only(f):  # make this a thing if I ever add any ways to manage stuff from the backend
                    # for example if I want to add money to people's accounts or whatever
    pass