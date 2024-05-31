from pyrk import driver


def test_name_from_path():
    assert driver.name_from_path("/Users/test/test.py") == "test"
    assert driver.name_from_path("/Users/test/test") == "test"
    assert driver.name_from_path("test.py") == "test"
    assert driver.name_from_path("~/test.py") == "test"
    assert driver.name_from_path("~/test") == "test"


def test_name_from_path_has_p():
    assert driver.name_from_path("/Users/test/testp.py") == "testp"
    assert driver.name_from_path("testp.py") == "testp"
    assert driver.name_from_path("~/testp.py") == "testp"
    assert driver.name_from_path("~/testp") == "testp"
