import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# def dict_factory(cursor, row):
#     d = {}
#     for idx, col in enumerate(cursor.description):
#         d[col[0]] = row[idx]
#         print(d)
#     # print(d)
#     return d

def dict_factory(cursor, row):
    return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))

# conn = sqlite3.connect('/Users/afa/Desktop/python_100/api/books.db')
# cur = conn.cursor()

# cur.execute('''ALTER TABLE books
#             RENAME COLUMN ID TO id;
#             ''')

# cur.execute('''INSERT INTO books VALUES ("69","2021","molly","i am so cool","hello world!!!!")
#             ''')

# cur.execute('''SELECT rowid, * FROM books
#             ''')
# items = cur.fetchall()
# for item in items:
#     print(item)

# cur.execute("select * from books")
# results = cur.fetchall()
# for n in range(1, len(results)+1):
#     cur.execute(f"UPDATE books SET id = {n} WHERE rowid = {n}")
#     conn.commit()
# conn.close()

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('/Users/afa/Desktop/python_100/api/books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=(?) AND'
        to_filter.append(int(id))
    if published:
        query += ' published=(?) AND'
        to_filter.append(published)
    if author:
        query += ' author=(?) AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'
    
    conn = sqlite3.connect('/Users/afa/Desktop/python_100/api/books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    # results = cur.execute(query, to_filter).fetchall()
    
    return jsonify(cur.execute(query, to_filter).fetchall())

app.run()