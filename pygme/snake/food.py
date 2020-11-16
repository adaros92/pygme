import random
import uuid

from abc import ABC, abstractmethod

from pygme.utils import space


class Food(ABC):

    def __init__(self,
                 food_type: str, representation: str, x_coordinate: int, y_coordinate: int,
                 food_id: uuid.UUID = uuid.uuid1()) -> None:
        self.food_type = food_type
        self.representation = representation
        self.food_id = str(food_id)
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    @property
    def coordinates(self) -> tuple:
        return self.x_coordinate, self.y_coordinate

    @abstractmethod
    def growth_value(self) -> int:
        """ Defines how much consumers of the food grow by after eating it """
        pass

    def __repr__(self) -> str:
        return self.representation

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other) -> bool:
        return self.food_type == other.food_type and self.food_id == other.food_id \
               and self.representation == other.representation


class Cricket(Food):

    SPAWN_WEIGHT = 3

    def __init__(self, representation: str = "#", x_coordinate: int = None, y_coordinate: int = None) -> None:
        super().__init__(
            food_type="crickets", x_coordinate=x_coordinate, y_coordinate=y_coordinate, representation=representation)

    @property
    def growth_value(self) -> int:
        return random.randint(1, 2)


class Mouse(Food):

    SPAWN_WEIGHT = 1

    def __init__(self, representation: str = "&", x_coordinate: int = None, y_coordinate: int = None):
        super().__init__(
            food_type="mouse", x_coordinate=x_coordinate, y_coordinate=y_coordinate, representation=representation)

    @property
    def growth_value(self) -> int:
        return random.randint(2, 3)


class FoodCollection(list):

    def __init__(self, grid_width: int, grid_length: int) -> None:
        super().__init__()
        self.grid_width = grid_width
        self.grid_length = grid_length
        self.length = 0
        self._refresh()

    @property
    def max_length(self) -> int:
        return self.grid_width * self.grid_length

    def _reset(self) -> None:
        self.extend([None] * self.max_length)
        self.length = self.max_length

    def _refresh(self) -> None:
        self._reset()
        eligible_types = [Mouse, Cricket]
        weights = [Mouse.SPAWN_WEIGHT, Cricket.SPAWN_WEIGHT]
        assert len(eligible_types) == len(weights)
        random_type_choices = random.choices(eligible_types, weights=weights, k=self.max_length)
        for idx, food_type in enumerate(random_type_choices):
            random_coordinates = space.get_coordinates_between_limits(self.grid_width, self.grid_length)
            self[idx] = food_type(x_coordinate=random_coordinates[0], y_coordinate=random_coordinates[1])

    def generate(self, count: int = 1) -> list:
        assert count > 0
        return_foods = []
        for _ in range(count):
            if self.length == 0:
                self._refresh()
            return_foods.append(self.pop())
            self.length -= 1
        return return_foods
