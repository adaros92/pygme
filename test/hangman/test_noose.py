import pytest

from pygme.game.board import GameBoard
from pygme.hangman import noose


def test_noose_construction():
    """ Tests noose.Noose constructor and noose_components class attribute """
    test_board = GameBoard(10, 10, " ")
    noose_object = noose.Noose(test_board)
    required_parts = ["base", "pole", "top", "rope", "head", "body", "left_leg", "right_leg", "left_arm", "right_arm"]
    expected_representations = ["_", "|", "_", "|", "O", "|", "/", "\\", "-", "-"]
    # Test that all required parts are present
    for part, representation in zip(required_parts, expected_representations):
        found = False
        for component in noose_object.noose_components:
            component_part = component["part"]
            if part == component_part.part:
                # Ensure the matching part has the expected character representation
                assert repr(component_part) == representation and str(component_part) == representation
                found = True
        assert found


def test_draw():
    """ Tests noose.Noose.draw method """
    empty_char = " "
    test_board = GameBoard(10, 10, empty_char)
    noose_object = noose.Noose(test_board)
    noose_object.draw()
    components_on_grid = set()
    for component in noose_object.noose_components:
        if component["displayed"]:
            components_on_grid.add(repr(component["part"]))
            # Ensure that if a component is supposed to be displayed that the board has been refreshed with it
            assert test_board.board[component["x_index"]][component["y_index"]] == repr(component["part"])
    for column in test_board.board:
        for element in column:
            # Ensure that no other elements beyond the displayed parts and the empty square character are on the board
            assert element == empty_char or element in components_on_grid


def test_is_complete():
    """ Tests noose.Noose.is_complete method """
    test_board = GameBoard(10, 10, " ")
    noose_object = noose.Noose(test_board)
    # Initially not all components will be displayed so ensure that the noose is not complete
    assert not noose_object.is_complete()
    for component in noose_object.noose_components:
        component["displayed"] = True
    # After forcefully displaying all components though, the noose should be complete
    assert noose_object.is_complete()


def test_last_displayed():
    """ Tests noose.Noose.get_last_displayed method """
    test_board = GameBoard(10, 10, " ")
    noose_object = noose.Noose(test_board)
    # When first created the noose object should have a pointer to the element right after the last displayed
    assert noose_object.get_last_displayed() == noose_object.next_piece - 1
    idx = 0
    for component in noose_object.noose_components:
        if component["displayed"]:
            idx += 1
        else:
            break
    assert noose_object.get_last_displayed() == idx - 1


def test_update():
    """ Tests noose.Noose.update method """
    test_board = GameBoard(10, 10, " ")
    noose_object = noose.Noose(test_board)
    previous_pointer = noose_object.next_piece
    assert not noose_object.is_complete()
    for i in range(pytest.large_iteration_count):
        noose_object.update()
        current_pointer = noose_object.next_piece
        if current_pointer < len(noose_object.noose_components):
            assert current_pointer == previous_pointer + 1
        previous_pointer = current_pointer
    assert previous_pointer == current_pointer and noose_object.is_complete()
