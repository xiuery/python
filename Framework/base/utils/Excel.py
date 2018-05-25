import xlrd


class Excel(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = xlrd.open_workbook(self.file_name, on_demand=True)
        self.sheet = None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.release_resources()
        return False

    def _check(self):
        if self.sheet is None:
            raise Exception("No sheet is open,Please call open_sheet.")

    # def __getattribute__(self, attr):
    #     try:
    #         if 'open_sheet' != attr:
    #             super(Excel, self).__getattribute__('_check')()
    #         return super(Excel, self).__getattribute__(attr)
    #     except KeyError:
    #         return 'Not the properties of the Excel class.'

    def open_sheet(self, sheet_name):
        self.sheet = self.file.sheet_by_name(sheet_name)

    def get_row_data(self, row_index):
        if row_index >= self.get_rows():
            raise IndexError("row_index  is out of range.")

        return self.sheet.row_values(row_index)

    def get_row_col_data(self, row_index, col_index):
        if row_index >= self.get_rows():
            raise IndexError("row_index  is out of range.")

        if col_index >= self.get_cols():
            raise IndexError("col_index  is out of range.")

        row = self.sheet.row_values(row_index)
        return row[col_index]

    def get_rows(self):
        return self.sheet.nrows

    def get_cols(self):
        return self.sheet.ncols


if __name__ == '__main__':
    from base.utils.DateTools import DateTools
    with Excel("d:\\SKU20026495_2018-05-04-13-49-48.xls") as excel:
        excel.open_sheet('sheet1')
        print(DateTools.excel_date_format(excel.get_row_col_data(1, 6)))
