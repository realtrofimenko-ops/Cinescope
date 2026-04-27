import pytest
import sys


@pytest.mark.skip(reason="Пока не реализовано")
def test_skip_example():
    assert False
@pytest.mark.skipif(sys.platform == "win32", reason="Не работает на Windows")
def test_skipif_example():
    assert True
@pytest.mark.xfail(reason="Известный баг")
def test_xfail_example():
    assert False
@pytest.mark.smoke
def test_smoke():
    assert True