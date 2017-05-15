"""Creates custom in-memory database using thread-safe dictionaries."""
import abc
import datetime
from multiprocessing import Manager
from multiprocessing.managers import SyncManager
from custom_exceptions import InvalidUsage
from record import Record


class _DataBase(object):
    """Abstract class for database access. All new database wrappers must be derived from this class."""
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """Make necessary initializations (one-time)"""
        pass

    @abc.abstractmethod
    def get_new_id(self, record, request):
        """Inserts a user request into DB.

        :param request: The request object corresponding to the requesting user
        :type request: instance of flask.Request
        :param record: New user input to be inserted in DB.
        :type record: Record

        :return: A unique ID corresponding to the record (Usually a key in a K-V database)."""
        pass

    @abc.abstractmethod
    def is_valid_id(self, request_id):
        """Checks if a given ID exists in DB.

        :param request_id: Request ID
        :type request_id: Integer
        :returns: True, if request_id exists in DB else False.
        :rtype: Boolean
        """
        pass

    @abc.abstractmethod
    def delete_id(self, request_id):
        """Deletes a given ID from DB.

        :param request_id: Request ID whose result is needed.
        :type request_id: Integer

        :raise ValueError: If request_id is invalid.
        """
        pass

    @abc.abstractmethod
    def get_record_by_id(self, request_id):
        pass


class MyDictDB(_DataBase):
    """Implements a custom database using a process & thread safe python dict."""
    def __init__(self, *args, **kwargs):
        SyncManager.register("merged file", list)
        self._manager = Manager()
        self._db = self._manager.dict()
        self._db['next_usable_id'] = 0

    def get_new_id(self, record, request):
        log_dict = dict(record.__dict__)
        log_dict.update(dict(sender_ip=request.remote_addr, created_at=str(datetime.datetime.now())))
        while self._db['next_usable_id'] in self._db:
            self._db['next_usable_id'] += 1
        self._db[self._db['next_usable_id']] = self._manager.dict(log_dict)
        return self._db['next_usable_id']

    def get_record_by_id(self, request_id):
        if self.is_valid_id(request_id):
            return self._db[request_id]
        else:
            raise InvalidUsage("Request ID : {} not found".format(request_id), status_code=404)

    def delete_id(self, request_id):
        if self.is_valid_id(request_id):
            return self._db.pop(request_id, None)
        else:
            raise InvalidUsage("Request ID : {} not found".format(request_id), status_code=404)

    def is_valid_id(self, request_id):
        return True if request_id in self._db else False
