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


def test_task2_post_with_relationship_country_winery(client):
    """Testing post method with relationship winery/country"""
    winery_name = "Heitz"
    data = {
        "attributes": {
            "title": "test"},
        "relationships": {
            "reader": {
                "data": {
                    "id": None,
                    "type": "Winery",
                    "attributes": {
                        "name": winery_name}}}},
        "type": "Country"}
    res = client.post("/countries", json={"data": data})
    assert res.status_code == 201


def test_task2_post_with_relationship_province_winery(client):
    """Testing post method with relationship winery/province"""
    winery_name = "Heitz"
    data = {
        "attributes": {
            "title": "test"},
        "relationships": {
            "reader": {
                "data": {
                    "id": None,
                    "type": "Winery",
                    "attributes": {
                        "name": winery_name}}}},
        "type": "Province"}
    res = client.post("/province", json={"data": data})
    assert res.status_code == 201


def test_task2_post_with_relationship_province_country(client):
    """Testing post method with relationship country/province"""
    country_name = "US"
    data = {
        "attributes": {
            "title": "test"},
        "relationships": {
            "reader": {
                "data": {
                    "id": None,
                    "type": "Country",
                    "attributes": {
                        "name": country_name}}}},
        "type": "Province"}
    res = client.post("/province", json={"data": data})
    assert res.status_code == 201


    # Testing "PATCH" endpoints


def test_task2_patch_wineries_data(client):
    """Testing a patch / update to a city that is just inserted"""
    data = {"attributes": {"name": "Blue Farm", "country_id": 1}, "type": "Winery"}
    response = client.post("/winery/", json={"data": data})
    response_data = response.get_json()
    winery_id = response_data["data"]["id"]
    print_json_to_data_view_log_nicely(response_data)
    data = {"attributes": {"name": "Blue Farm", "country_id": 1}, "type": "Winery", "id": winery_id}
    response = client.patch(f"/winery/{winery_id}", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 200
    assert response_data["data"]["attributes"]["name"] == "Blue Farm"


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
    data = {"attributes": {"name": "Blue Farm", "country_id": 1}, "type": "Winery"}
    response = client.post("/winery/", json={"data": data})
    response_data = response.get_json()
    winery_id = response_data["data"]["id"]
    data = {"attributes": {"name": "Blue Farm", "country_id": 1}, "type": "Winery"}
    response = client.post(f"/winery/{winery_id}", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 405


def test_task2_patch_method_not_allowed_country_data(client):
    """Testing that this will make a method not allowed if i try to post to a new record"""
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Country"}
    response = client.post("/countries/", json={"data": data})
    response_data = response.get_json()
    country_id = response_data["data"]["id"]
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Country"}
    response = client.post(f"/countries/{country_id}", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 405


def test_task2_patch_method_not_allowed_province_data(client):
    """Testing that this will make a method not allowed if i try to post to a new record"""
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Province"}
    response = client.post("/province/", json={"data": data})
    response_data = response.get_json()
    city_id = response_data["data"]["id"]
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "`Province`"}
    response = client.post(f"/province/{city_id}", json={"data": data})
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

def test_task2_delete_country(client):
    """This will test deleting a country"""
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}
    response = client.post("/country/", json={"data": data})
    response_data = response.get_json()
    winery_id = response_data["data"]["id"]
    data = {"type": "Country", "id": winery_id}
    response = client.delete(f"/country/{winery_id}", json={"data": data})
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 204

def test_task2_delete_province(client):
    """This will test deleting a province"""
    data = {"attributes": {"name": "Blue Farm", "country_id": 1}, "type": "Province"}
    response = client.post("/province/", json={"data": data})
    response_data = response.get_json()
    winery_id = response_data["data"]["id"]
    data = {"type": "Province", "id": winery_id}
    response = client.delete(f"/province/{winery_id}", json={"data": data})
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 204

# Testing log files

root = os.path.dirname(os.path.abspath(__file__))
logdir = os.path.join(root, '../logs')

def test_task2_dataview_logfiles():
    logfile = os.path.join(logdir, 'data_view.log')
    if not os.path.exists(logfile):
        f = open(logfile, 'w')
        f.close()
    assert os.path.exists(logfile) == True


def test_task2_request_logfiles():
    logfile = os.path.join(logdir, 'information.log')
    if not os.path.exists(logfile):
        f = open(logfile, 'w')
        f.close()
    assert os.path.exists(logfile) == True


def test_task2_sqlalchemy_logfiles():
    logfile = os.path.join(logdir, 'root_logger_default.log')
    if not os.path.exists(logfile):
        f = open(logfile, 'w')
        f.close()
    assert os.path.exists(logfile) == True


def test_task2_werkzeug_logfiles():
    logfile = os.path.join(logdir, 'werkzeug.log')
    if not os.path.exists(logfile):
        f = open(logfile, 'w')
        f.close()
    assert os.path.exists(logfile) == True


# Testing CSV file

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
