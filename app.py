from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)
nombre = None
edad = None

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

with get_db_connection() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 task VARCHAR(100) NOT NULL)
                 
                 ''')
    
    conn.commit()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/datos', methods=['POST'])
def post_datos():
    global task

    task = request.form['task']

    with get_db_connection() as conn:
        conn.execute('INSERT INTO tasks (task) VALUES (?)', (task,))

    return redirect('/')


@app.route('/update_data', methods=['POST'])
def update_data():
    global task

    task = request.form['edit_task']
    id = request.form['edit_id']

    with get_db_connection() as conn:
        conn.execute('UPDATE tasks SET task = ? WHERE id = ?', (task, id))

    return redirect('/')

@app.get('/recuperar_datos')
def get_data_from_db():

    with get_db_connection() as conn:
        datos = conn.execute('SELECT id, task FROM tasks').fetchall()
        
        
    lista_datos = [{'id':row['id'],'task':row['task']} for row in datos]

    return jsonify(lista_datos)

    
@app.route('/eliminar_datos', methods=['POST'])
def eliminar_datos():
    id_to_delete = request.get_json()
    if not id_to_delete:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    id = id_to_delete.get('id')
    delete_by_id(id)
    return jsonify({"mensaje": "Datos recibidos correctamente", "id":id}), 200


def delete_by_id(id):
    with get_db_connection() as conn:
        conn.execute(f"DELETE FROM tasks WHERE id = {id}")
        conn.commit()


if __name__ == '__main__':
    app.run(debug=True)