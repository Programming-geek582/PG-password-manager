from quart import Quart
from tortoise import Tortoise
from views import general, auth, management


app = Quart(__name__)
app.secret_key = "werkzeugIsChad"

@app.before_serving
async def before_startup():
    await Tortoise.init(
        db_url="sqlite://passwords.sqlite",
        modules={
            'models' : ['models']
        }
    )
    await Tortoise.generate_schemas()
    await general.register(app)
    await auth.register(app)
    await management.register(app)

if __name__ == "__main__":
    app.run(debug=True)