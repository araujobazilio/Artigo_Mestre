from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pathlib import Path
import unicodedata
import re
import requests

def sanitize_filename(text):
    # Remove acentos
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Remove caracteres especiais
    text = re.sub(r'[^\w\-_\. ]', '', text)
    # Troca espaços por underline
    text = text.replace(' ', '_')
    return text

def save_articles(topico, result):
    """
    Salva os artigos em um arquivo e retorna o nome do arquivo
    """
    # Criar diretório para salvar artigos
    output_dir = Path('static/artigos')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Nome do arquivo baseado no tópico e timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topico = sanitize_filename(topico)
    filename = f"{safe_topico}_{timestamp}.txt"
    filepath = output_dir / filename
    
    # Salvar artigos
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(result))
    
    return filename

def search_web(query, api_key):
    """Função para buscar na web usando a API do Serper"""
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "q": query,
        "num": 5  # Número de resultados
    })
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Erro na busca: {str(e)}"

def create_crew(topico):
    """
    Cria e configura o crew de agentes
    """
    # Carregar variáveis de ambiente
    load_dotenv()
    serper_api_key = os.getenv('SERPER_API_KEY')

    # Definir modelo de IA
    llm = 'gpt-4o-mini'

    @tool("Web Search Tool")
    def web_search_tool(query: str) -> str:
        """
        Busca informações na internet usando a API do Google Serper.
        Use esta ferramenta para encontrar artigos, notícias e informações gerais sobre um tópico.
        Input: uma string de consulta para a busca.
        Output: uma string JSON com os resultados da busca ou uma mensagem de erro.
        """
        return search_web(query, serper_api_key)

    # Agente Pesquisador
    pesquisador = Agent(
        role="Pesquisador de Conteúdo",
        backstory=(
            "Você é um investigador digital altamente experiente, com acesso a bancos de dados "
            "avançados, periódicos científicos e repositórios de informações confiáveis."
        ),
        goal="Coletar e organizar artigos recentes sobre um tema específico.",
        tools=[web_search_tool],
        verbose=True,
        llm=llm
    )

    # Agente Analista
    analista = Agent(
        role="Analista de Conteúdo",
        backstory=(
            "Você é um analista de dados e informações com um olhar clínico para detectar padrões."
        ),
        goal="Analisar os artigos encontrados e extrair insights.",
        verbose=True,
        llm=llm,
        
    )

    # Agente Redator
    redator = Agent(
        role="Criador de Conteúdo",
        backstory=(
            "Você é um escritor talentoso e criativo, especializado em artigos científicos."
        ),
        goal="Escrever 5 artigos científicos profundos baseados nos insights.",
        verbose=True,
        llm=llm,
        
    )

    # Agente Revisor
    revisor = Agent(
        role="Revisor e Editor",
        backstory=(
            "Você é um especialista em refinamento textual e rigor acadêmico."
        ),
        goal="Revisar e aprimorar os artigos científicos.",
        verbose=True,
        llm=llm,
        
    )

    # Tarefas
    pesquisa_task = Task(
        agent=pesquisador,
        description=f"Busque e colete os artigos mais recentes sobre {topico}.",
        expected_output=f"Lista de links e resumos de artigos sobre {topico}."
    )

    analise_task = Task(
        agent=analista,
        description=f"Analise os artigos encontrados sobre {topico}.",
        expected_output=f"Resumo detalhado com insights sobre {topico}."
    )

    criacao_artigos_task = Task(
        agent=redator,
        description=(
            f"Com base apenas nos insights e informações analisadas pelo agente anterior, "
            f"escreva 5 artigos científicos originais e completos sobre {topico}. "
            f"Cada artigo deve conter introdução, desenvolvimento e conclusão, "
            f"com no mínimo 1000 palavras cada. "
            f"Não copie listas de links, títulos ou resumos dos artigos encontrados. "
            f"Use as referências apenas como base de conhecimento para criar textos inéditos. "
            f"Se possível, cite as referências utilizadas ao final de cada artigo."
        ),
        expected_output=f"5 artigos científicos originais e completos sobre {topico}."
    )

    revisao_task = Task(
        agent=revisor,
        description=f"Revise os 5 artigos científicos sobre {topico}.",
        expected_output=f"5 artigos científicos revisados sobre {topico}."
    )

    # Configurando o Crew
    crew = Crew(
        agents=[pesquisador, analista, redator, revisor],
        tasks=[pesquisa_task, analise_task, criacao_artigos_task, revisao_task],
        process=Process.sequential,
        
    )

    return crew
