import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    # backup and restore participants lists
    original = {k: v["participants"][:] for k, v in app_module.activities.items()}
    yield
    for k, p in original.items():
        app_module.activities[k]["participants"] = p[:]


def test_get_activities_function():
    data = app_module.get_activities()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_functions():
    activity = "Chess Club"
    email = "teststudent@mergington.edu"

    # ensure not present
    assert email not in app_module.activities[activity]["participants"]

    # call signup function
    resp = app_module.signup_for_activity(activity, email)
    assert "Signed up" in resp["message"]
    assert email in app_module.activities[activity]["participants"]

    # signing up again should raise an HTTPException; simulate by calling and catching
    import pytest as _pytest
    from fastapi import HTTPException

    with _pytest.raises(HTTPException):
        app_module.signup_for_activity(activity, email)

    # unregister
    resp = app_module.unregister_participant(activity, email)
    assert "Removed" in resp["message"]
    assert email not in app_module.activities[activity]["participants"]


def test_unregister_nonexistent_participant_raises():
    activity = "Programming Class"
    email = "notfound@mergington.edu"
    import pytest as _pytest
    from fastapi import HTTPException

    with _pytest.raises(HTTPException):
        app_module.unregister_participant(activity, email)
