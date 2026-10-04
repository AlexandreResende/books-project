from pytest import fixture

from Entities.todoEntity import TodoEntity

def test_equal_or_not_equal():
    assert 3 == 3

def test_validate_boolean():
    validated = True
    assert validated == True

def test_is_instance():
    assert isinstance('this is a string', str)

def test_type():
    assert type('this is a string' is str)
    assert type('this is a string' is not int)

@fixture
def default_todo():
    return TodoEntity('read eragon', 1, 1, 1, 'The dragon rider book')

def test_todo_class(default_todo):
    assert isinstance(default_todo, TodoEntity)
    assert default_todo.title == 'read eragon'
    assert default_todo.description == 'The dragon rider book'

