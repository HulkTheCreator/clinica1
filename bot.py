import sqlite3
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from datetime import datetime, timedelta
import re

# ------------------------------
# Conectar ao banco de dados
# ------------------------------
conn = sqlite3.connect("nra_marilia.db", check_same_thread=False)
cursor = conn.cursor()

# ------------------------------
# Inicializar OllamaLLM
# ------------------------------
llm = OllamaLLM(model="tinyllama:latest")

prompt = """
Você é um assistente de agendamento muito educado e prestativo.
- Responda aos cumprimentos de forma amigável.
- Responda perguntas sobre disponibilidade de horários.
- Responda perguntas sobre os tipos de exames que você pode agendar.
- Não tente agendar ou alterar eventos a menos que eu peça.
- A mensagem do usuário é: {text}
"""
prompt_template = PromptTemplate(input_variables=["text"], template=prompt)

# ------------------------------
# Funções de banco de dados
# ------------------------------
def listar_exames():
    cursor.execute("SELECT id, nome FROM exames")
    return cursor.fetchall()

def listar_unidades():
    cursor.execute("SELECT id, nome FROM unidades")
    return cursor.fetchall()

def buscar_paciente_por_cpf(cpf):
    cursor.execute("SELECT id, nome FROM pacientes WHERE cpf=?", (cpf,))
    return cursor.fetchone()

def agendar_exame(paciente_id, exame_id, unidade_id, data_hora):
    cursor.execute("""
        INSERT INTO solicitacoes (paciente_id, exame_id, unidade_id, data_hora)
        VALUES (?, ?, ?, ?)
    """, (paciente_id, exame_id, unidade_id, data_hora))
    conn.commit()
    return f"Exame agendado com sucesso para {data_hora}!"

def consultar_solicitacoes(paciente_id):
    cursor.execute("""
        SELECT e.nome, s.data_hora, u.nome
        FROM solicitacoes s
        JOIN exames e ON s.exame_id = e.id
        JOIN unidades u ON s.unidade_id = u.id
        WHERE s.paciente_id = ?
        ORDER BY s.data_hora
    """, (paciente_id,))
    return cursor.fetchall()

# ------------------------------
# Funções do chatbot
# ------------------------------
def classify_intent(user_message):
    user_message = user_message.lower()
    greetings = ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'e aí']
    schedule_keywords = ['agendar', 'marcar', 'consulta', 'exame']
    change_keywords = ['alterar', 'mudar', 'remarcar']
    availability_keywords = ['disponibilidade', 'horários', 'disponível', 'tem vaga']
    exam_info_keywords = ['tipos de exame', 'quais exames', 'exames']
    consultas_keywords = ['meus exames', 'minhas consultas', 'agendamentos']

    if any(word in user_message for word in greetings):
        return 'greet'
    if any(word in user_message for word in schedule_keywords):
        return 'schedule'
    if any(word in user_message for word in change_keywords):
        return 'change'
    if any(word in user_message for word in availability_keywords):
        return 'availability_query'
    if any(word in user_message for word in exam_info_keywords):
        return 'exam_info_query'
    if any(word in user_message for word in consultas_keywords):
        return 'consultas'
    return 'unknown'

def interpret_datetime(user_message):
    today = datetime.today()
    if 'depois de amanhã' in user_message:
        event_date = today + timedelta(days=2)
    elif 'amanhã' in user_message:
        event_date = today + timedelta(days=1)
    elif 'hoje' in user_message:
        event_date = today
    else:
        day_match = re.search(r'\d{1,2}:\d{2}', user_message)
        if day_match:
            event_date = today
        else:
            event_date = today
    time_match = re.search(r'\d{1,2}:\d{2}', user_message)
    if time_match:
        hour, minute = map(int, time_match.group().split(':'))
        event_date = event_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return event_date

# ------------------------------
# Função para gerar resposta do LLM
# ------------------------------
def gerar_resposta(user_input):
    """
    Retorna a resposta do LLM para qualquer mensagem do usuário
    """
    return llm.invoke(prompt_template.format(text=user_input))
