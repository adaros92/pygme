import pytest

import pygme.__main__ as cli


def test_load_config():
    """ Tests pygme.__main__._load_config function """
    config_dict = cli._load_config()
    assert isinstance(config_dict, dict) and len(config_dict) > 0
    required_games_to_check = [key for key in cli.SUPPORTED_GAMES]
    for game in required_games_to_check:
        assert game in config_dict


def test_validate_config():
    """ Tests pygme.__main__._validate_config function """
    dummy_config = {"some_other_game": {}}
    with pytest.raises(ValueError):
        cli._validate_config(dummy_config)
    actual_config = cli._load_config()
    cli._validate_config(actual_config)


