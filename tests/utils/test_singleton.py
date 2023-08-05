from src.utils.singleton import singleton


@singleton
class SingletonClass:

    def __init__(self):
        self.value = "Singleton Value"


def test_singleton():
    s1 = SingletonClass()
    s2 = SingletonClass()

    assert s1 == s2

    s1.value = "New Value"
    assert s2.value == "New Value"
