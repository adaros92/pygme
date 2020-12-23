import pytest

from pygme.game import player


def test_player_uniqueness():
    """ Tests player.Player.player_id generation """
    for i in range(pytest.very_large_iteration_count):
        player_obj1 = player.Player()
        player_obj2 = player.Player()
        assert player_obj1.player_id != player_obj2.player_id
