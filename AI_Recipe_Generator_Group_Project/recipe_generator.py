from recipe_data import SubstituteFinder, create_recipe_database


# =========================
# AI RECOMMENDATION LOGIC
# =========================
class RecipeGenerator:
    def __init__(self):
        self.substitute_finder = SubstituteFinder()
        self.recipes = create_recipe_database()

    def clean_user_ingredients(self, ingredient_text):
        return {
            ingredient.lower().strip()
            for ingredient in ingredient_text.split(",")
            if ingredient.strip()
        }

    def suggest_recipes(self, ingredient_text):
        user_ingredients = self.clean_user_ingredients(ingredient_text)
        suggestions = []

        for recipe in self.recipes:
            score = recipe.match_percentage(user_ingredients)

            if score > 0:
                suggestions.append(
                    {
                        "recipe": recipe,
                        "score": score,
                        "available": recipe.get_available_ingredients(user_ingredients),
                        "missing": recipe.get_missing_ingredients(user_ingredients),
                    }
                )

        suggestions.sort(key=lambda item: item["score"], reverse=True)
        return suggestions

    def format_recipe_suggestions(self, ingredient_text):
        user_ingredients = self.clean_user_ingredients(ingredient_text)

        if not user_ingredients:
            return "Please enter at least one ingredient, separated by commas."

        suggestions = self.suggest_recipes(ingredient_text)

        if not suggestions:
            return (
                "No recipe match was found.\n\n"
                "Try entering common ingredients like rice, tomato, egg, bread, pasta, "
                "chicken, beans, or onion."
            )

        output = []

        for number, suggestion in enumerate(suggestions, start=1):
            recipe = suggestion["recipe"]
            missing = suggestion["missing"]

            output.append(f"{number}. {recipe.name}")
            output.append(f"Recipe Type: {recipe.get_recipe_type()}")
            output.append(f"Meal Type: {recipe.meal_type}")
            output.append(f"Difficulty: {recipe.difficulty}")
            output.append(f"Number of Ingredients: {len(recipe)}")
            output.append(f"Summary: {recipe.display_summary()}")
            output.append(f"Match: {suggestion['score']}%")
            output.append(
                "Ingredients You Have: "
                + self.format_list(suggestion["available"])
            )
            output.append("Missing Ingredients: " + self.format_list(missing))

            if missing:
                output.append("Substitute Suggestions:")
                for ingredient in missing:
                    substitutes = self.substitute_finder.find_substitutes(ingredient)
                    output.append(
                        f"  - {ingredient.title()}: {self.format_list(substitutes)}"
                    )
            else:
                output.append("Substitute Suggestions: None needed")

            output.append("Cooking Steps:")
            for step_number, step in enumerate(recipe.steps, start=1):
                output.append(f"  {step_number}. {step}")

            output.append("-" * 60)

        return "\n".join(output)

    def format_all_recipes(self):
        output = []

        for number, recipe in enumerate(self.recipes, start=1):
            output.append(f"{number}. {recipe.name}")
            output.append(f"Recipe Type: {recipe.get_recipe_type()}")
            output.append(f"Meal Type: {recipe.meal_type}")
            output.append(f"Difficulty: {recipe.difficulty}")
            output.append(f"Number of Ingredients: {len(recipe)}")
            output.append("Ingredients: " + self.format_list(recipe.ingredients))
            output.append("-" * 60)

        return "\n".join(output)

    def format_substitutes(self, ingredient_text):
        ingredient_name = ingredient_text.lower().strip()

        if not ingredient_name:
            return "Enter one ingredient first, then click Find Substitute."

        substitutes = self.substitute_finder.find_substitutes(ingredient_name)
        return f"Substitutes for {ingredient_name.title()}: {self.format_list(substitutes)}"

    @staticmethod
    def format_list(items):
        if not items:
            return "None"

        return ", ".join(item.title() for item in items)
