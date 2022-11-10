# Science Fiction Novel API - Quart Edition
#
# Adapted from "Creating Web APIs with Python and Flask"
# <https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask>.
#

import collections
import dataclasses
import sqlite3
import textwrap

import databases
import toml

from quart import Quart, g, request, abort
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)

app.config.from_file(f"./etc/{__name__}.toml", toml.load)


@dataclasses.dataclass
class Quote:
    genre: str
    author: str
    title: str
    text: str


# Database connections on demand
#   See <https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/>
#   and <https://www.encode.io/databases/connections_and_transactions/>


async def _get_db():
    db = getattr(g, "_sqlite_db", None)
    if db is None:
        db = g._sqlite_db = databases.Database(app.config["DATABASES"]["URL"])
        await db.connect()
    return db


@app.teardown_appcontext
async def close_connection(exception):
    db = getattr(g, "_sqlite_db", None)
    if db is not None:
        await db.disconnect()


@app.route("/", methods=["GET"])
def index():
    return textwrap.dedent(
        """
        <h1>Fantasy Quote of the Day!</h1>
        <p>A prototype API for a new Fantasy or Science Fiction quote for each day!.</p>\n
        """
    )


@app.route("/quotes/all", methods=["GET"])
async def all_quotes():
    db = await _get_db()
    all_quotes = await db.fetch_all("SELECT * FROM quotes;")

    return list(map(dict, all_quotes))


@app.route("/quotes/<int:id>", methods=["GET"])
async def one_quote(id):
    db = await _get_db()
    quote = await db.fetch_one("SELECT * FROM quotes WHERE id = :id", values={"id": id})
    if quote:
        return dict(quote)
    else:
        abort(404)


@app.errorhandler(404)
def not_found(e):
    return {"error": "The resource could not be found"}, 404


@app.route("/quotes/", methods=["POST"])
@validate_request(Quote)
async def create_quote(data):
    db = await _get_db()
    quote = dataclasses.asdict(data)
    try:
        id = await db.execute(
            """
            INSERT INTO quotes(genre, author, title, text)
            VALUES(:genre, :author, :title, :text)
            """,
            quote,
        )
    except sqlite3.IntegrityError as e:
        abort(409, e)

    quote["id"] = id
    return quote, 201, {"Location": f"/quotes/{id}"}


@app.errorhandler(RequestSchemaValidationError)
def bad_request(e):
    return {"error": str(e.validation_error)}, 400


@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409


SearchParam = collections.namedtuple("SearchParam", ["name", "operator"])
SEARCH_PARAMS = [
    SearchParam(
        "author",
        "LIKE",
    ),
    SearchParam(
        "genre",
        "LIKE",
    ),
    SearchParam(
        "title",
        "LIKE",
    ),
    SearchParam(
        "text",
        "LIKE",
    ),
]


@app.route("/quote/search", methods=["GET"])
async def search():
    query_parameters = request.args

    sql = "SELECT * FROM quotes"
    conditions = []
    values = {}

    for param in SEARCH_PARAMS:
        if query_parameters.get(param.name):
            if param.operator == "=":
                conditions.append(f"{param.name} = :{param.name}")
                values[param.name] = query_parameters[param.name]
            else:
                conditions.append(f"{param.name} LIKE :{param.name}")
                values[param.name] = f"%{query_parameters[param.name]}%"

    if conditions:
        sql += " WHERE "
        sql += " AND ".join(conditions)

    app.logger.debug(sql)

    db = await _get_db()
    results = await db.fetch_all(sql, values)

    return list(map(dict, results))
