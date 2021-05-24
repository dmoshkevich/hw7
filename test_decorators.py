import pytest
import decorators


def test_potentially_unsafe_func():
    result = decorators.potentially_unsafe_func('name')
    assert result == 'test'


def test_potentially_unsafe_func_silented():
    result = decorators.potentially_unsafe_func('x')
    assert result == 'error is silented'


def test_potentially_unsafe_func_silented():
    with pytest.raises(TypeError):
        decorators.potentially_unsafe_func(True, True)


def test_sum_of_values():
    result = decorators.sum_of_values((1, 3, 5))
    assert result == 9


def test_sum_of_values_err():
    with pytest.raises(ValueError):
        decorators.sum_of_values((1, 3, 5, 7))


def test_sum_of_values_type_err():
    with pytest.raises(TypeError):
        decorators.sum_of_values(True)


def test_show_message():
    decorators.show_message('Avada Kedavra bruh')


def test_show_message_err():
    with pytest.raises(ValueError):
        decorators.show_message('test')


def test_process_text():
    result = decorators.process_text('the French revolution resulted in 3 concepts,./:; freedom,equality,fraternity')
    assert result == 'ThE FrencH RevolutioN ResulteD IN 3 ConceptS      FreedoM EqualitY FraternitY'


def test_another_process():
    result = decorators.another_process('the French revolution resulted in 3 concepts,./:; freedom,equality,fraternity')
    assert result == 'ThE FrencH RevolutioN ResulteD IN 3 Concepts      Freedom equality fraternitY'
