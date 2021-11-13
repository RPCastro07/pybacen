from pybacen.bacen.bacen_data import Bacen_data as bd

def read_bacen_complaints(year: int, periodicity: str, period: str):
    return bd().read_bacen_complaints(year, periodicity, period)


"""
def read_list_reports():
    return bd().read_list_reports()

def read_registration_inst(limit: int = 100, filter: str = None, select: str = None):
    return bd().read_registration_inst(limit, filter, select)

def read_report_inst(year_month: str, type_inst: int, num_report: str, limit: int = 100, filter: str = None, select: str = None):
    return bd().read_report_inst(year_month, type_inst, num_report, limit, filter, select)
"""