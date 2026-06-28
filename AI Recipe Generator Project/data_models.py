from abc import ABC, abstractmethod


# =========================
# DATA MODELS
# =========================
class FoodItem(ABC):
    def __init__(self, name):
        self._name = name.strip()

    def get_name(self):
        return self._name

    def set_name(self, name):
        if len(name.strip()) >= 2:
            self._name = name.strip()
        else:
            print("Name must have at least 2 characters.")

    @abstractmethod
    def display_summary(self):
        pass

    def __str__(self):
        return self._name.title()

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._name}')"


class Ingredient(FoodItem):
    default_category = "General"

    def __init__(self, name, category):
        super().__init__(name)
        self._name = self._name.lower()
        self.category = category

    def display_summary(self):
        return f"{self._name.title()} is in the {self.category} category."


class Recipe(FoodItem):
    recipe_type = "General Recipe"

    def __init__(self, name, ingredients, steps, meal_type, difficulty):
        super().__init__(name)

        self.__ingredients = [ingredient.lower().strip() for ingredient in ingredients]
        self.__steps = steps
        self.meal_type = meal_type
        self.difficulty = difficulty

    @property
    def name(self):
        return self._name

    @property
    def ingredients(self):
        return self.__ingredients

    @property
    def steps(self):
        return self.__steps

    def get_recipe_type(self):
        return self.recipe_type

    def display_summary(self):
        return f"{self.name} is a {self.difficulty.lower()} {self.meal_type} recipe."

    def get_available_ingredients(self, user_ingredients):
        return [item for item in self.__ingredients if item in user_ingredients]

    def get_missing_ingredients(self, user_ingredients):
        return [item for item in self.__ingredients if item not in user_ingredients]

    def match_percentage(self, user_ingredients):
        if not self.__ingredients:
            return 0

        available_count = len(self.get_available_ingredients(user_ingredients))
        return round((available_count / len(self.__ingredients)) * 100)

    def __len__(self):
        return len(self.__ingredients)

    def __eq__(self, other):
        if isinstance(other, Recipe):
            return self.name.lower() == other.name.lower()
        return False

    def __lt__(self, other):
        if isinstance(other, Recipe):
            return self.name.lower() < other.name.lower()
        return NotImplemented


class NigerianRecipe(Recipe):
    recipe_type = "Nigerian Dish"

    def get_recipe_type(self):
        return self.recipe_type

    def display_summary(self):
        return f"{self.name} is a Nigerian dish usually served as {self.meal_type}."


class QuickRecipe(Recipe):
    recipe_type = "Quick Meal"

    def get_recipe_type(self):
        return self.recipe_type

    def display_summary(self):
        return f"{self.name} is a quick {self.meal_type} meal."
