""" Make the tests pass to make the cities endpoint work"""

# pylint: disable=redefined-outer-name, unused-argument, line-too-long

from tests.helpers import print_json_to_data_view_log_nicely


def test_task1_home_route(client):  # <---Arrange the test with the fixture, you can add others
    """Testing the home route to see it returns 200 OK"""  # <---You need the comment to describe the tests
    response = client.get('/')  # <--Act Perform an action
    assert response.status_code == 200, "Homepage did not return 200 status code "  # <--Explain if something fails
    # in plain english.


def test_task1_get_wineries_data(client):  # <---Arrange the test with the fixture, you can add others
    """Testing the cities endpoint retrieves the correct data"""  # <---You need the comment to describe the tests
    response = client.get('/winery/')  # <--Act Perform an action
    assert response.status_code == 200, "Cites did not return 200 status code "  # <--Explain if something fails in
    # plain english.

    # Uncomment this to use this function to print to the data_view.log file to see the data you want to inspect.
    print_json_to_data_view_log_nicely(response.get_json())

    data = response.get_json()
    winery_name = data["data"][0]["attributes"]["name"]
    assert winery_name == "Heitz", "The first city is not Tokyo as expected"


def test_task1_post_wineries_data(client):
    """Testing a post to cities"""
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}

    response = client.post("/winery/", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 201
    assert response_data["data"]["attributes"]["name"] == "Heitz"


def test_task1_patch_cities_data(client):
    """Testing a patch / update to a city that is just inserted"""
    # first I have to make a city
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}

    response = client.post("/winery/", json={"data": data})
    # now i have to get the data
    response_data = response.get_json()
    # now i get the id of the new record
    winery_id = response_data["data"]["id"]
    print_json_to_data_view_log_nicely(response_data)
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery", "id": winery_id}

    response = client.patch(f"/winery/{winery_id}", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 200
    assert response_data["data"]["attributes"]["name"] == "Heitz"


def test_task1_patch_method_not_allowed_wineries_data(client):
    """Testing that this will make a method not allowed if i try to post to a new record"""
    # first I have to make a city
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}

    response = client.post("/winery/", json={"data": data})
    # now i have to get the data
    response_data = response.get_json()
    # now i get the id of the new record
    city_id = response_data["data"]["id"]

    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}

    response = client.post(f"/wonery/{city_id}", json={"data": data})
    response_data = response.get_json()
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 405


def test_task1_delete_city(client):
    """This will test deleting a winery"""
    # first I have to make a winery
    data = {"attributes": {"name": "Heitz", "country_id": 1}, "type": "Winery"}

    response = client.post("/winery/", json={"data": data})
    # now i have to get the data
    response_data = response.get_json()
    # now i get the id of the new record
    winery_id = response_data["data"]["id"]

    data = {"type": "Winery", "id": winery_id}

    response = client.delete(f"/winery/{winery_id}", json={"data": data})
    print_json_to_data_view_log_nicely(response_data)
    assert response.status_code == 204
