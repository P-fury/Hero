import pytest
from Hero_app.models import Day

@pytest.fixture
def day_fix():
    test_day = Day.objects.create(date='2021-01-10', mood=4,fatigue=2,note='test note')
    return test_day