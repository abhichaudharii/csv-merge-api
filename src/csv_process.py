from datetime import datetime, timedelta
from heapq import heappush, heappop
from custom_exceptions import InvalidUsage


class MergeCSV(object):
    def __init__(self, daily_csv, companies_csv, start_date, end_date, n):
        """Initializes a new object.

        :param self.daily_csv: Contents of  'daily.csv' file
        :param self.companies_csv: Contents of 'companies.csv' file
        :param self.start_date: The starting date for the data frame
        :param self.end_date: The end date of the data frame
        :param self.n: The number of lag periods
        :type self.daily_csv: csv.reader
        :type self.companies_csv: csv.reader
        :type self.start_date: String
        :type self.end_date: String
        :type self.n: integer
        """
        self.daily_csv = daily_csv
        self.companies_csv = companies_csv
        self.start_date = start_date
        self.end_date = end_date
        self.n = n
        self.companies = self._parse_and_validate_input()
        self._heapify_inputs()

    def _parse_and_validate_input(self):
        try:
            companies = {row[0]: dict(name=row[1], heap=[], data_frame=[]) for row in self.companies_csv}
            self.start_date = datetime.strptime(self.start_date, "%m/%d/%y")
            self.end_date = datetime.strptime(self.end_date, "%m/%d/%y")
            assert self.start_date <= self.end_date, "self.start_date must be earlier than self.end_date"
            self.n = abs(int(self.n))
        except Exception as e:
            # TODO: Make exception handling more specific
            raise InvalidUsage("Please verify input data : {}".format(str(e)))
        return companies

    def _heapify_inputs(self):
        """Separates CSV entries by company ID and writes them to a heap."""
        index = 0
        while index < len(self.daily_csv):
            curr_date = datetime.strptime(self.daily_csv[index][1], "%m/%d/%y")
            curr_company_id = self.daily_csv[index][0]
            if curr_date < self.start_date:
                self.daily_csv.pop(index)
            elif curr_date > self.end_date:
                self.daily_csv.pop(index)
            else:
                heappush(self.companies[curr_company_id]['heap'],
                         ((curr_date - self.start_date).days, list(self.daily_csv[index])))
                index += 1

    def _build_data_frame(self, company_id):
        """Build data_frame for each company ID and adds missing entries, if needed."""
        company = self.companies[company_id]
        heap = company['heap']
        data_frame = company['data_frame']
        for day in xrange((self.end_date - self.start_date).days + 1):
            next_date = self.start_date + timedelta(days=day)
            date_stamp = "{}/{}/{}".format(next_date.month, next_date.day, next_date.year % 1000)

            # Assuming '0' value for auto-filled entries.
            if heap:
                next_row = heappop(heap)[1] if heap[0][0] == (next_date - self.start_date).days else \
                    [company_id, date_stamp, 0]
            else:
                next_row = [company_id, date_stamp, 0]

            n_val = None if day < self.n else int(next_row[2]) - int(data_frame[day - self.n][2])
            next_row.append(n_val)
            next_row[0] = self.companies[company_id]['name']
            data_frame.append(next_row)

    def get_merged_file(self):
        """Returns a single merged file from the other two files.

        :return: Merged list of records
        :rtype: List of List
        """
        company_ids = []
        for company_id in self.companies.keys():
            company_ids.append(company_id)
            self._build_data_frame(company_id)
        company_ids.sort()

        merged_file = []
        for company_id in company_ids:
            merged_file += list(self.companies[company_id]['data_frame'])
        return merged_file
