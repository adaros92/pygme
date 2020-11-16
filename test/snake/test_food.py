import random

from pygme.snake import food


def test_cricket():
    """ Tests snake.food.Cricket class """
    for i in range(100):
        x_coordinate = random.randint(0, 100)
        y_coordinate = random.randint(0, 100)
        cricket = food.Cricket(x_coordinate=x_coordinate, y_coordinate=y_coordinate)
        assert cricket.representation == "#"
        assert cricket.coordinates == (x_coordinate, y_coordinate)
        assert cricket.SPAWN_WEIGHT == food.Cricket.SPAWN_WEIGHT
        assert 1 <= cricket.growth_value <= 2


def test_mouse():
    """ Tests snake.food.Mouse class """
    for i in range(100):
        x_coordinate = random.randint(0, 100)
        y_coordinate = random.randint(0, 100)
        mouse = food.Mouse(x_coordinate=x_coordinate, y_coordinate=y_coordinate)
        assert mouse.representation == "&"
        assert mouse.coordinates == (x_coordinate, y_coordinate)
        assert mouse.SPAWN_WEIGHT == food.Mouse.SPAWN_WEIGHT
        assert 2 <= mouse.growth_value <= 3


def test_food_collection_init():
    """ Tests snake.food.FoodCollection construction """
    for i in range(25):
        grid_width = random.randint(1, 100)
        grid_length = random.randint(1, 100)
        collection = food.FoodCollection(grid_width=grid_width, grid_length=grid_length)
        collection_length = len(collection)
        assert collection_length == grid_width * grid_length and collection_length == collection.length


def test_food_generation():
    """ Tests snake.food.FoodCollection generate method """
    grid_width = 1
    grid_length = 2
    collection = food.FoodCollection(grid_width=grid_width, grid_length=grid_length)
    generated = collection.generate(count=2)
    assert collection.length == 0 and len(generated) == 2
    generated = collection.generate(count=1)
    assert collection.length == 1 and len(generated) == 1
    for i in range(25):
        grid_width = random.randint(1, 100)
        grid_length = random.randint(1, 100)
        count = random.randint(1, grid_width * grid_length)
        collection = food.FoodCollection(grid_width=grid_width, grid_length=grid_length)
        collection_before = len(collection)
        result = collection.generate(count=count)
        assert collection.length == collection_before - count
        assert len(result) == count
