from flask import Flask, render_template, request, jsonify, session
from bot import gerar_resposta, classify_intent, buscar_paciente_por_cpf, listar_exames, listar_unidades, agendar_exame, consultar_solicitacoes, interpret_datetime

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

def processar_mensagem(user_input):
    if "estado" not in session:
        session["estado"] = {}
    estado = session["estado"]

    # ---------------------------
    # Fluxo de agendamento
    # ---------------------------
    if estado.get("fase") == "aguardando_cpf":
        paciente = buscar_paciente_por_cpf(user_input)
        if not paciente:
            return "Paciente não encontrado. Informe um CPF válido."
        estado["paciente_id"] = paciente[0]
        estado["fase"] = "aguardando_exame"
        session["estado"] = estado
        exames = listar_exames()
        msg = "Paciente encontrado. Escolha o exame:\n"
        msg += "\n".join([f"{ex[0]} - {ex[1]}" for ex in exames])
        return msg

    elif estado.get("fase") == "aguardando_exame":
        try:
            exame_id = int(user_input)
        except:
            return "Informe o ID do exame corretamente."
        estado["exame_id"] = exame_id
        estado["fase"] = "aguardando_unidade"
        session["estado"] = estado
        unidades = listar_unidades()
        msg = "Escolha a unidade:\n"
        msg += "\n".join([f"{u[0]} - {u[1]}" for u in unidades])
        return msg

    elif estado.get("fase") == "aguardando_unidade":
        try:
            unidade_id = int(user_input)
        except:
            return "Informe o ID da unidade corretamente."
        estado["unidade_id"] = unidade_id
        estado["fase"] = "aguardando_data"
        session["estado"] = estado
        return "Informe a data e hora do exame (ex: 2025-09-29 14:00)."

    elif estado.get("fase") == "aguardando_data":
        data_hora = user_input
        resultado = agendar_exame(estado["paciente_id"], estado["exame_id"], estado["unidade_id"], data_hora)
        session.pop("estado")
        return resultado

    # ---------------------------
    # Fluxo de consulta de exames
    # ---------------------------
    if estado.get("fase") == "aguardando_cpf_consulta":
        paciente = buscar_paciente_por_cpf(user_input)
        if not paciente:
            return "Paciente não encontrado. Informe um CPF válido."
        paciente_id, paciente_nome = paciente
        consultas = consultar_solicitacoes(paciente_id)
        session.pop("estado")  # reset
        if consultas:
            msg = f"Exames agendados para {paciente_nome}:\n"
            for c in consultas:
                msg += f"- {c[0]} em {c[2]} na data/hora {c[1]}\n"
            return msg
        else:
            return f"Nenhum exame agendado para {paciente_nome}."

    # ---------------------------
    # Detecção de intenção
    # ---------------------------
    intent = classify_intent(user_input)
    if intent in ["schedule", "change"]:
        estado["fase"] = "aguardando_cpf"
        session["estado"] = estado
        return "Vamos agendar seu exame. Informe o CPF do paciente."
    elif intent == "consultas":
        estado["fase"] = "aguardando_cpf_consulta"
        session["estado"] = estado
        return "Informe o CPF do paciente para verificar exames agendados."
    else:
        return gerar_resposta(user_input)

# -------------------
# Rotas Flask
# -------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["message"]
    resposta = processar_mensagem(user_input)
    return jsonify({"response": resposta})

if __name__ == "__main__":
    app.run(debug=True)
