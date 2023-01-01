from unittest.mock import Mock, patch

import pytest
from valid8 import ValidationError

from musics_library.menu import Entry, Key, Description, Menu


def test_empty_description_raises_exception():
    with pytest.raises(ValidationError):
        Description("")


def test_correct_descriptions():
    correct_values = ['Welcome in Music Library', 'Welcome_In_Music_Library', 'Welcome in Music Library!',
                      'Welcome: In, Music Library.', 'Description09']
    for correct in correct_values:
        assert Description(correct)


def test_empty_key_raises_exception():
    with pytest.raises(ValidationError):
        Key("")


def test_key_of_length_11_raises_exception():
    with pytest.raises(ValidationError):
        Key("A" * 11)


def test_correct_keys():
    correct_values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'A', 'B', 'C', 'A-B', 'a-b', 'a_c']
    for correct in correct_values:
        assert Key(correct)


def test_entry_on_selected():
    mocked_on_selected = Mock()
    entry = Entry(Key('1'), Description("Welcome in Music Library"), on_selected=lambda: mocked_on_selected())
    entry.on_selected()
    mocked_on_selected.assert_called_once()


@patch('builtins.print')
def test_entry_is_exit_on_selected(mocked_print):
    entry = Entry(Key('0'), Description('Exit'), on_selected=lambda: print('Goodbye, Music Library'), is_exit=True)
    entry.on_selected()
    mocked_print.assert_called_with('Goodbye, Music Library')


@patch('builtins.input', side_effect=['1', '0'])
@patch('builtins.print')
def test_menu_selection_call_on_selected(mocked_print, mocked_input):
    menu = Menu.Builder(Description('Test Menu')) \
        .with_entry(Entry.create('1', 'first_entry', on_selected=lambda: print('first entry selected'))) \
        .with_entry(Entry.create('0', 'exit', is_exit=True)) \
        .build()
    menu.run()
    mocked_print.assert_any_call('first entry selected')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['-1', '0'])
@patch('builtins.print')
def test_menu_selection_on_wrong_key(mocked_print, mocked_input):
    menu = Menu.Builder(Description('Test Menu')) \
        .with_entry(Entry.create('1', 'first_entry', on_selected=lambda: print('first entry selected'))) \
        .with_entry(Entry.create('0', 'exit', is_exit=True)) \
        .build()
    menu.run()
    mocked_print.assert_any_call('Invalid selection. Please, try again...')
    mocked_input.assert_called()


def test_stop_menu():
    menu = Menu.Builder(Description('Test Menu')) \
        .with_entry(Entry.create('1', 'first_entry', on_selected=lambda: print('first entry selected'))) \
        .with_entry(Entry.create('0', 'exit', is_exit=True)) \
        .build()
    menu.stop()
    assert not menu.is_running