from custom_exceptions import InvalidUsage

REQUIRED_KEYS = [('start_date', str), ('end_date', str), ('n', int)]


class Record:
    """This class is an abstraction containing the user input and outputs."""
    def __init__(self, daily_vals, companies, start_date, end_date, n):
        self.daily_vals = [row for row in daily_vals]
        self.companies = [row for row in companies]
        self.start_date = start_date
        self.end_date = end_date
        self.n = n


def get_form_parameters(form):
    """Extracts and validates all parameters from the request form.
    :param form: Contains the form keys and values sent by the user.
    :type form: Dict (see flask.request.form)

    :return: An array containing the type-converted form parameters in same order as the constant REQUIRED_KEYS
    """
    try:
        args = [key_type(form[key_name]) for key_name, key_type in REQUIRED_KEYS]
    except KeyError as k:
        raise InvalidUsage("Missing key in request. {}".format(k))
    except ValueError as v:
        raise InvalidUsage("Invalid value found in request. {}".format(v))
    return args
