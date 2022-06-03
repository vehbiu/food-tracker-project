import time, os
from db import User, FindBy, Recipe
from functools import wraps
from quart import Quart, render_template as render, g, request, session, redirect, url_for
from reccomend import recommend_recipes

app = Quart(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = os.urandom(32)


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not "user" in g:
            return redirect(url_for("login") + "?next=" + request.path)
        return await func(*args, **kwargs)
    return wrapper


@app.before_request
async def before_request():
    print(dict(session))
    if "uname" in session:
        user = User.find_by(FindBy.NAME, session["uname"])
        if user and not user.verify_pw(session["passw"]):
            g.user = None
            print("(!) User password changed, logging out...")
            session.clear()
        if user:
            g.user = user
    if "exp" in session and session["exp"] < time.time():
        print("(!) User session expired, logging out...")
        session.clear()
        g.user = None


@app.route("/")
async def index():
    return await render("index.html")


@app.get("/auth/login")
async def login():
    if "user" in g:
        return redirect(url_for("me"))
    return await render("auth/login.html")


@app.get("/auth/logout")
@login_required
async def logout():
    session.clear()
    return redirect(url_for("login"))


@app.post("/auth/login")
async def login_POST():
    data = await request.json
    user = User.find_by(FindBy.EMAIL, data["email"])
    if user is None:
        return {"status": "USER_NOT_FOUND", "msg": "User not found"}, 404
    if not user.verify_pw(data["password"]):
        return {"status": "WRONG_PASSWORD", "msg": "Password incorrect"}, 401
    session.update({
        "uname": user.uname,
        "passw": data["password"],
        "exp": (time.time() + 60 * 60 * 24 * 7) if data.get("remember") else (time.time() + 60 * 60)
    })
    return {"status": "OK"}, 200


@app.get("/auth/signup")
async def signup():
    return await render("auth/signup.html")


@app.post("/auth/signup")
async def signup_POST():
    data = await request.json
    uname, email, password = data.get(
        "uname"), data.get("email"), data.get("password")
    if not uname or not email or not password:
        return {"status": "MISSING_DATA", "msg": "Missing data"}, 400
    if len(uname) < 3 or len(uname) > 32:
        return {"status": "INVALID_USERNAME", "msg": "Username must be between 3 and 32 characters"}, 400
    if User.find_by(FindBy.EMAIL, email):
        return {"status": "EMAIL_EXISTS", "msg": "Email already exists"}, 409
    if User.find_by(FindBy.NAME, uname):
        return {"status": "USERNAME_EXISTS", "msg": "Username already exists"}, 409
    if len(password) < 8 or len(password) > 32:
        return {"status": "INVALID_PASSWORD", "msg": "Password must be between 8 and 32 characters"}, 400
    user = User.create_new(
        uname=uname,
        email=email,
        passw=password
    )
    session.update({
        "uname": user.uname,
        "passw": password,
        "exp": (time.time() + 60 * 60 * 24 * 7) if data.get("remember") else (time.time() + 60 * 60)
    })
    return {"status": "OK"}, 200


@app.get("/@user")
@login_required
async def me():
    return await render("user/index.html")


@app.get("/@user/recipes/create")
@login_required
async def create():
    new_recipe = Recipe.create_new(g.user._id, "New Recipe", "New Recipe Description", ingredients=[
    ], steps=["Step 1", "Step 2", "Step 3"])
    return redirect(url_for("recipe", recipe_id=new_recipe._id))


@app.get("/@user/recipes/browse")
@login_required
async def browse():
    if request.args.get("term"):
        return await render("user/browse.html", recipes=Recipe.search(request.args.get("term")))
    return await render("user/browse.html")


@app.get("/@user/recipes/<recipe_id>")
@app.get("/@user/recipes/<recipe_id>/view")
@login_required
async def view_recipe(recipe_id: str):
    return await render("user/recipe.html", recipe=Recipe.find(recipe_id))


@app.get("/@user/recipes/<recipe_id>/recommendations")
@login_required
async def recommend_recipe(recipe_id: str):
    recipe: Recipe = Recipe.find(recipe_id)
    return await render("user/recommend.html", recipe=recipe, recipes=recommend_recipes(
        recipe, Recipe.find_all(), 50
    ))


@app.get("/@user/recipes/<recipe_id>/edit")
@login_required
async def edit_recipe(recipe_id: str):
    return await render("user/edit.html", recipe=Recipe.find(recipe_id))


@app.post("/@user/recipes/<recipe_id>/edit/general")
@login_required
async def recipe_POST(recipe_id: str):
    data = await request.json
    recipe = Recipe.find(recipe_id)
    if recipe is None:
        return {"status": "NOT_FOUND", "msg": "Recipe not found"}, 404
    elif recipe.owner != g.user._id:
        return {"status": "FORBIDDEN", "msg": "You can't edit this recipe"}, 403
    recipe.name = data["name"]
    recipe.desc = data["desc"]
    recipe.update()
    return {"status": "OK"}, 200


@app.post("/@user/recipes/<recipe_id>/edit/data")
@login_required
async def recipe_edit_POST(recipe_id: str):
    data = await request.json
    recipe = Recipe.find(recipe_id)
    if recipe is None:
        return {"status": "NOT_FOUND", "msg": "Recipe not found"}, 404
    elif recipe.owner != g.user._id:
        return {"status": "FORBIDDEN", "msg": "You can't edit this recipe"}, 403
    recipe.ingredients = data["ingredients"]
    recipe.steps = data["steps"]
    recipe.update()
    return {"status": "OK"}, 200

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
