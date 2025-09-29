# Chatbot de Agendamento de Exames (Flask + SQLite + OllamaLLM)

Este projeto é um app  agendamento de exames médicos, desenvolvido com **Flask**, **SQLite** e **OllamaLLM**.

---

## Estrutura do Projeto

chat/
├── app.py
├── bot.py
├── templates/index.html
├── static/style.css
├── requirements.txt
└── README.md

---

## Como rodar no Windows

1. **Clonar o repositório**

Abra o **Prompt de Comando** ou **PowerShell**:

```powershell
git clone https://github.com/USERNAME/REPO.git
cd REPO
Substitua USERNAME e REPO pelo seu usuário e repositório do GitHub.
no powershell:
python -m venv venv
.\venv\Scripts\Activate.ps1
Se der erro de execução de scripts no PowerShell, rode:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Instalar dependências
pip install -r requirements.txt

Rodar o servidor Flask
python app.py

O Flask iniciará e mostrará algo como:
Running on http://127.0.0.1:5000



Observações

O banco nra_marilia.db será criado automaticamente se não existir.

Sempre use o venv para evitar conflitos de dependências.

Para sair do chatbot ou do servidor Flask, use CTRL + C.


Estrutura do Chatbot

app.py → Flask + rotas para o chatbot.

bot.py → Lógica do chatbot, conexão SQLite e OllamaLLM.

templates/index.html → Interface do usuário (HTML).

static/style.css → Estilo da interface.


Licença
Este projeto é open-source e pode ser usado livremente.
