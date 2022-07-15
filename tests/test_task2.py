"""Testing all Wine models, endpoints, home route"""

# pylint: disable=redefined-outer-name, unused-argument, unspecified-encoding
# pylint: disable=redefined-outer-name, unused-argument, line-too-long
# pylint: disable=unused-argument, unused-import, duplicate-code, comparison-with-itself, singleton-comparison
import csv
import os
from os.path import exists

from pandas.io.common import file_exists
from pylint.testutils.functional import test_file

from app import app, config
from tests.helpers import print_json_to_data_view_log_nicely


    # Testing HOME ROUTE and RECORDS routes
def test_task2_home_route(client):
    """Testing the home route to see it returns 200 OK"""
    response = client.get('/')
    assert response.status_code == 200, "Homepage did return 200 status code"

def test_task2_routes():
    """Testing the routes to list records"""
    response = app.test_client().get('/')
    assert response.status_code == 200
    response = app.test_client().get('/countries/')
    assert response.status_code == 200
    response = app.test_client().get('/winery/')
    assert response.status_code == 200

def test_task2_province_route():
    """Testing the routes to list provinces"""
    response = app.test_client().get('/province/')
    assert response.status_code == 200


    #  testing "GET" endpoints

def test_task2_get_wineries_data(client):
    """Testing the wineries endpoint retrieves the correct data"""
    response = client.get('/winery/')
    assert response.status_code == 200, "Wineries did return 200 status code"
    print_json_to_data_view_log_nicely(response.get_json())
    data = response.get_json()
    winery_name = data["data"][0]["attributes"]["name"]
    assert winery_name == "Heitz", "The first winery is Heitz as expected"

def test_task2_get_countries_data(client):
    """Testing the countries endpoint retrieves the correct data"""
    response = client.get('/countries/')
    assert response.status_code == 200
    print_json_to_data_view_log_nicely(response.get_json())
    data = response.get_json()
    country_name = data["data"][0]["attributes"]["name"]
    assert country_name == "US", "The first country is US as expected"

def test_task2_get_province_data(client):
    """Testing the province/state endpoint retrieves the correct data"""
    response = client.get('/province/')
    assert response.status_code == 200
    print_json_to_data_view_log_nicely(response.get_json())
    data = response.get_json()
    province_name = data["data"][0]["attributes"]["name"]
    assert province_name == "California", "The first province/state is California as expected"


    #  Testing "POST" endpoints

def test_task2_post_wineries_data(client):
    """Testing a post to wineries"""
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}
    response = client.post("/winery/", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 201
    assert response_data["data"]["attributes"]["name"] == "Heitz"

def test_task2_post_countries_data(client):
    """Testing a post to countries"""
    data = {"attributes": {"name": "US", "country_id": 1}, "type": "Country"}
    response = client.post("/countries/", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 201
    assert response_data["data"]["attributes"]["name"] == "US"

def test_task2_post_province_data(client):
    """Testing a post to province/state"""
    data = {"attributes": {"name": "California", "country_id": 1}, "type": "Province"}
    response = client.post("/province/", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 201
    assert response_data["data"]["attributes"]["name"] == "California"


    # Testing "PATCH" endpoints

def test_task2_patch_wineries_data(client):
    """Testing a patch / update to a city that is just inserted"""
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}
    response = client.post("/winery/", json={"data": data})
    response_data = response.get_json()
    winery_id = response_data["data"]["id"]
    print_json_to_data_view_log_nicely(response_data)
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery", "id": winery_id}
    response = client.patch(f"/winery/{winery_id}", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 200
    assert response_data["data"]["attributes"]["name"] == "Heitz"

def test_task2_patch_countries_data(client):
    """Testing a patch / update to a country that is just inserted"""
    data = {"attributes": {"name": "US", "country_id": 1}, "type": "Country"}
    response = client.post("/countries/", json={"data": data})
    response_data = response.get_json()
    country_id = response_data["data"]["id"]
    print_json_to_data_view_log_nicely(response_data)
    data = {"attributes": {"name": "US", "country_id": 1}, "type": "Country", "id": country_id}
    response = client.patch(f"/countries/{country_id}", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 200
    assert response_data["data"]["attributes"]["name"] == "US"

def test_task2_patch_province_data(client):
    """Testing a patch / update to a province that is just inserted"""
    data = {"attributes": {"name": "California", "country_id": 1}, "type": "Province"}
    response = client.post("/province/", json={"data": data})
    response_data = response.get_json()
    province_id = response_data["data"]["id"]
    print_json_to_data_view_log_nicely(response_data)
    data = {"attributes": {"name": "California", "country_id": 1}, "type": "Province", "id": province_id}
    response = client.patch(f"/province/{province_id}", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 200
    assert response_data["data"]["attributes"]["name"] == "California"


    # Testing "METHOD NOT ALLOWED" endpoints

def test_task2_patch_method_not_allowed_wineries_data(client):
    """Testing that this will make a method not allowed if i try to post to a new record"""
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}
    response = client.post("/winery/", json={"data": data})
    response_data = response.get_json()
    city_id = response_data["data"]["id"]
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}
    response = client.post(f"/wonery/{city_id}", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 405


    # Testing "DELETE' endpoints

def test_task2_delete_winery(client):
    """This will test deleting a winery"""
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}
    response = client.post("/winery/", json={"data": data})
    response_data = response.get_json()
    winery_id = response_data["data"]["id"]
    data = {"type": "Winery", "id": winery_id}
    response = client.delete(f"/winery/{winery_id}", json={"data": data})
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 204


 # Testing CSV file
"""Testing Csv"""
BASE_DIR = config.Config.BASE_DIR
uploaddir = os.path.join(BASE_DIR, '../data')
test_file = os.path.join(uploaddir, 'test.csv')


def test_task2_upload_dir():
    """Tests for existence of upload directory"""
    if not os.path.exists(uploaddir):
        os.mkdir(uploaddir)
    assert os.path.exists(uploaddir)


def test_task2_csv_existence():
    """Tests for csv file existence"""
    fields = ['country', 'designation', 'points', 'price', 'province', 'region_1', 'region_2', 'variety', 'winery']
    rows = [['US', 'Reserve', '96', '65', 'Oregon', 'Willamette Valley', 'Willamette Valley', 'Pinot Noir', 'Ponzi']]
    with open(test_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
    assert os.path.exists(test_file)
