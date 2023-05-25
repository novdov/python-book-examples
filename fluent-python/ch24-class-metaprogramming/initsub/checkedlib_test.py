import pytest

from .checkedlib import Checked


def test_field_validation_type_error():
    class Cat(Checked):
        name: str
        weight: float

    with pytest.raises(TypeError) as e:
        Cat(name="Felix", weight=None)

    assert str(e.value) == "None is not compatible with weight:float"
