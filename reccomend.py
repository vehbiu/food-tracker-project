from db import User, FindBy, Recipe
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_recipes(target_recipe: Recipe, recipes: List[Recipe], amount: int = 5):
    # Preprocess the ingredients
    target_ingredients = [
        ingredient["name"].lower() for ingredient in target_recipe.ingredients]
    preprocessed_recipes = []
    for recipe in recipes:
        ingredients = [
            ingredient["name"].lower() for ingredient in recipe.ingredients]
        preprocessed_recipes.append(" ".join(ingredients))

    # Calculate the TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_recipes)

    # Calculate cosine similarity between target recipe and all recipes
    target_tfidf = vectorizer.transform([" ".join(target_ingredients)])
    similarities = cosine_similarity(target_tfidf, tfidf_matrix)

    # Sort and rank the recommendations
    sorted_indices = similarities.argsort()[0][::-1]  # Sort in descending order
    recommended_recipes = [recipes[i] for i in sorted_indices[:amount]]

    return recommended_recipes


if __name__ == "__main__":
    from json import dump, dumps
    user = User.find_by(FindBy.NAME, "vehbiu")
    recipes = Recipe.search("lasagna")

    with open("reccomendation.json", "w") as f:
        recco = recommend_recipes(recipes[0], Recipe.find_all(), amount=15)
        dump([iter.to_dict(convert=True) for iter in recco], f, indent=4)

    print("Done")
