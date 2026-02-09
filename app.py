from flask import Flask, render_template, request, jsonify
from db import get_db
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("agendar.html")

@app.route("/agendar", methods=["POST"])
def agendar():
    data = request.json

    nome = data["nome"]
    servico = data["servico"]
    dia = data["data"]
    hora = data["hora"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM agendamentos WHERE data=%s AND hora=%s",
        (dia, hora)
    )

    if cur.fetchone():
        return jsonify({"erro": "Horário indisponível"}), 400

    cur.execute(
        "INSERT INTO agendamentos (nome, servico, data, hora) VALUES (%s,%s,%s,%s)",
        (nome, servico, dia, hora)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Agendamento criado 💈"})

if __name__ == "__main__":
    app.run()
