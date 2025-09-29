# Chatbot de Agendamento de Exames (Flask + SQLite + OllamaLLM)

Este projeto é um **app de agendamento de exames médicos**, desenvolvido com **Flask**, **SQLite** e **OllamaLLM**. O chatbot permite interagir, consultar pacientes, agendar exames e obter informações sobre exames e unidades.
1)
Preparação do Projeto
a) Clonar o repositório
Abra o Prompt de Comando (Windows) ou Terminal (Linux/macOS) e rode
git clone https://github.com/HulkTheCreator/clinica1.git
cd REPO

b)Estrutura do projeto
Após clonar, você deve ter algo assim:
__pycache__
templates
/index.html
>venv
>.gitignore
>app.py
>bot.py
>nra_marilia.db
>readme.md
>requirements.txt
>sistemas_regulacao

2)Configurar o ambiente virtual
Ambiente virtual ajuda a isolar as dependências do projeto.
Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

Se aparecer erro de execução de scripts, rode:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

3)Instalar dependências
Com o ambiente virtual ativado, rode:
pip install -r requirements.txt
Isso instalará Flask, langchain, SQLite, OllamaLLM e outras bibliotecas necessárias.

4)Configurar o OllamaLLM
O projeto usa OllamaLLM, que requer:
Instalar a CLI do Ollama:
Windows/macOS: baixe e instale de https://ollama.com/download

(no cmd)Baixar o modelo TinyLlama:
ollama pull tinyllama:latest
Isso baixa o modelo localmente, necessário para que o chatbot funcione offline.

5)Executar o servidor Flask
Com o venv ativado:
python app.py
Você verá algo como:
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Abra seu navegador e acesse:
http://127.0.0.1:5000
Você verá a interface do Assistente de Agendamento.

6)Usando o Chatbot
Digite mensagens no chat para interagir.
Para agendar exames, siga as instruções do bot.
Para consultar exames agendados, informe o CPF do paciente.
Para parar o servidor, pressione CTRL + C

7)
Observações Importantes
O banco nra_marilia.db será criado automaticamente na primeira execução.
Sempre use o ambiente virtual (venv) para evitar conflitos de pacotes.
As dependências do Python estão listadas em requirements.txt.
O modelo OllamaLLM precisa ser baixado via ollama pull tinyllama:latest para funcionar.

Licença
Este projeto é open-source e pode ser usado livremente para fins educacionais ou profissionais.
