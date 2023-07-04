from quart import Quart
from tortoise import Tortoise
from views import general, auth, management


app = Quart(__name__)
app.secret_key = "werkzeugIsChad"

@app.before_serving
async def before_startup():
    await Tortoise.init(
        db_url="postgres://pg:Qun72wh5L4lso1M6Kqa3Pq9HQM3fDh7N@dpg-cihsf8qip7vpelqibkog-a.oregon-postgres.render.com/passwordmanager_3dzy",
        modules={
            'models' : ['models']
        },
        config='connections': {
                          # Dict format for connection
                          'default': {
                              'engine': 'tortoise.backends.asyncpg',
                              'credentials': {
                                  'host': 'dpg-cihsf8qip7vpelqibkog-a',
                                  'port': '5432',
                                  'user': 'pg',
                                  'password': 'Qun72wh5L4lso1M6Kqa3Pq9HQM3fDh7N',
                                  'database': 'passwordmanager_3dzy',
                              },
                              'maxsize': 100
                          }
    )
    await Tortoise.generate_schemas()
    await general.register(app)
    await auth.register(app)
    await management.register(app)

if __name__ == "__main__":
    app.run(debug=True)
