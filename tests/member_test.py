"""
Test Member class
"""

from datetime import datetime
import json

import pytest
import requests_mock

from habitica_helper.member import Member


@pytest.fixture
def member_data_from_api():
    """
    Return the interesting parts of a member dict as from Habitica API
    """
    return {
            "data": {
                '_id': '3c3858fb-8bd9-4119-ad50-e2f6fe3523c7',
                'auth': {'local': {'username': 'SomeUser'},
                         'timestamps': {
                             'created': '2020-01-04T21:11:35.201Z',
                             'loggedin': '2022-01-06T08:09:17.096Z',
                             'updated': '2022-01-06T08:10:50.754Z'}},
                'profile': {'blurb': 'I am a test user!\n'
                                     'There\'s nothing interesting about me',
                            'name': 'Some Üser'},
                }
            }


@pytest.fixture
def api_header():
    """
    Return a structurally valid API header
    """
    return {
        "x-client": "f687a6c7-860a-4c7c-8a07-9d0dcbb7c831-habot-testing",
        "x-api-user": "8415a003-ef41-4168-9f8e-50baa099d37e",
        "x-api-key": "4f1f9c07-0dab-4820-a80b-cf47a5f54ecf",
    }


# pylint doesn't understand fixtures
# pylint: disable=redefined-outer-name
@pytest.fixture
def mock_get_member(member_data_from_api):
    """
    Return a pre-defined member data as a response to API call
    """
    with requests_mock.Mocker() as mock:
        mock.register_uri(
            "GET",
            "https://habitica.com/api/v3/members/"
            "3c3858fb-8bd9-4119-ad50-e2f6fe3523c7",
            headers={"content-type": "text/json", "charset": "utf-8"},
            content=json.dumps(member_data_from_api).encode("utf-8"),
            )
        yield


@pytest.mark.usefixtures("mock_get_member")
def test_member_from_api(api_header):
    """
    Test getting member data from an API response
    """
    member = Member("3c3858fb-8bd9-4119-ad50-e2f6fe3523c7", header=api_header)
    assert member.id == "3c3858fb-8bd9-4119-ad50-e2f6fe3523c7"
    assert member.displayname == "Some Üser"
    assert member.login_name == "SomeUser"
    assert member.habitica_birthday == datetime(2020, 1, 4, 21, 11, 35, 201000)
    assert member.last_login == datetime(2022, 1, 6, 8, 9, 17, 96000)


def test_member_from_profile_data():
    """
    Test member creation based on profile data
    """
    uid = "3c3858fb-8bd9-4119-ad50-e2f6fe3523c7"
    displayname = "Some Üser"
    loginname = "SomeUser"
    birthday = datetime(2020, 1, 4, 21, 11, 35, 201000)
    last_login = datetime(2022, 1, 6, 8, 9, 17, 96000)
    profile_data = {
        "id": uid,
        "displayname": displayname,
        "loginname": loginname,
        "birthday": birthday,
        "last_login": last_login,
        }

    member = Member(user_id=uid, profile_data=profile_data)
    assert member.id == uid
    assert member.displayname == displayname
    assert member.login_name == loginname
    assert member.habitica_birthday == birthday
    assert member.last_login == last_login
