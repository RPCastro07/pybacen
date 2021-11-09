from pybacen.bacen.bacen_data import Bacen_data as bd

def read_bacen_complaints(year: int, periodicity: str, period: str):
    return bd().read_bacen_complaints(year, periodicity, period)