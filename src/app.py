import csv
from cStringIO import StringIO
from flask import Flask, jsonify, request, send_file, make_response
from database import MyDictDB
from custom_exceptions import InvalidUsage
from csv_process import MergeCSV
from record import Record, get_form_parameters

__version__ = '1.0.0'
_api_name = 'csvmerge'
_api_path = "{}/api/{}".format(_api_name, __version__)

app = Flask(__name__)
_db_conn = None
logger = None


@app.before_first_request
def init_global_db():
    global _db_conn
    _db_conn = MyDictDB()


@app.route('/{}/files'.format(_api_path), methods=['POST'])
def create_file():

    try:
        args = get_form_parameters(request.form)
        daily = csv.reader(request.files['daily.csv'])
        companies = csv.reader(request.files['companies.csv'])
        new_record = Record(daily, companies, *args)
        merge_csv = MergeCSV(new_record.daily_vals, new_record.companies, *args)
        merged_file = merge_csv.get_merged_file()
    except Exception as e:
        # TODO : Implement more-specific error handling
        raise InvalidUsage(e.message, status_code=400)

    new_id = _db_conn.get_new_id(new_record, request)

    file_as_str = ""
    for row in merged_file:
        row_str = ",".join(str(item) for item in row)
        file_as_str += "{}\n".format(row_str)

    sender = StringIO(file_as_str[:-1])
    resp = make_response(send_file(sender, attachment_filename='merged_file.csv', as_attachment=True))
    resp.headers['Id'] = new_id
    return resp


@app.route('/{}/files/<int:request_id>'.format(_api_path), methods=['POST'])
def get_record(request_id):
    return jsonify(_db_conn.get_record_by_id(request_id))


@app.route('/{}/files/<int:request_id>'.format(_api_path), methods=['DELETE'])
def delete_record(request_id):
    return jsonify(_db_conn.delete_id(request_id))


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    app.logger.error("IP : {} Error Code : {} Message : {}".format(request.remote_addr, error.status_code,
                                                                   error.message))
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run()
