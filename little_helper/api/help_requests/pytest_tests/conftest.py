from django.core.management import call_command

import pytest


@pytest.fixture(scope="session", autouse=True)
def load_test_data(db, django_db_blocker):
    print("loading data....")
    with django_db_blocker.unblock():
        call_command("loaddata", "test.json", database="default")
