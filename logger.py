import abc
from time import strftime, gmtime


class _Logger(object):
    def __init__(self, *args, **kwargs):
        # Over ride this method for one-time initialization code (optional)
        pass

    @abc.abstractmethod
    def log(self, message):
        # type: (object) -> object
        pass

    @staticmethod
    def get_time_stamp():
        """Generates time stamp in a human readable form.
        :return: The current time, in a human readable format
        :rtype: String
        """
        return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())


class PrintLogger(_Logger):
    """Simple logger that prints to Standard Output."""
    def log(self, message):
        print ("{} : {}".format(_Logger.get_time_stamp(), message))
