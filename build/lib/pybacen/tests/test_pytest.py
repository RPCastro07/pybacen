from pytest import mark

from pybacen.utils.requests import Request


# Step 1: Tests - Result Success
@mark.parametrize(
    'url,content_type',
    [('http://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json', 'application/json; charset=utf-8'), 
    ('http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv', 'text/csv')]
)
def test_request_status_code(url,content_type):

    request = Request()

    response = request.get(url)

    assert response.headers['content-type'] == content_type


# Step 2: Tests - Result Error