Quero criar um sistema que busca na Internet artig9s mais atuais sobre um determinado assunto junta todos eles, faz uma análise e faz mais 10 outros artigos sobre o tema, com o que foi tirado dos outros e dando um toque a mais de inteligência .
Para criar um sistema que busca na internet artigos atuais sobre um determinado assunto, faz uma análise e gera outros 10 artigos originais com um toque de inteligência, podemos estruturar um fluxo utilizando o CrewAI. Aqui está uma abordagem eficiente para implementar isso:

Arquitetura do Sistema
O sistema contará com quatro agentes principais:

Agente Pesquisador: Utiliza ferramentas de busca para encontrar artigos recentes sobre o tema solicitado.
Agente Analista: Lê os artigos coletados, faz um resumo e identifica os principais insights e padrões.
Agente Redator: Com base nas análises, escreve 10 novos artigos originais sobre o tema, adicionando um toque criativo e aprofundando a discussão.
Agente Revisor: Ajusta a coerência, clareza e gramática dos artigos antes de armazená-los ou publicá-los.
Código de Implementação
Aqui está um exemplo de código utilizando CrewAI:

python
Copy
Edit
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Definir modelo de IA
llm = 'gpt-4o-mini'

# Ferramenta de busca na web
search_tool = SerperDevTool()
search_tool.n_results = 50  # Define o número de resultados

# ---------------------------
# AGENTES
# ---------------------------

# Agente Pesquisador
pesquisador = Agent(
    role="Pesquisador de Conteúdo",
    backstory=(
        "Você é um investigador digital altamente experiente, com acesso a bancos de dados "
        "avançados, periódicos científicos e repositórios de informações confiáveis. Seu trabalho "
        "consiste em garimpar a internet em busca dos artigos mais recentes e relevantes sobre um "
        "determinado tema, garantindo que apenas fontes confiáveis e de alta qualidade sejam incluídas "
        "no processo. Seu olhar crítico e metódico permite separar dados valiosos de informações "
        "irrelevantes, criando uma base sólida para análise."
    ),
    goal="Coletar e organizar artigos recentes sobre um tema específico, priorizando fontes confiáveis e de impacto.",
    tools=[search_tool],
    verbose=True,
    llm=llm,
    memory=True
)

# Agente Analista
analista = Agent(
    role="Analista de Conteúdo",
    backstory=(
        "Você é um analista de dados e informações com um olhar clínico para detectar padrões, tendências "
        "e insights ocultos em grandes volumes de texto. Seu trabalho é absorver o conteúdo coletado pelo "
        "pesquisador e identificar os pontos mais relevantes, separando fatos importantes de especulações "
        "e ruídos. Com habilidades refinadas em estruturação de informações, você transforma artigos brutos "
        "em relatórios organizados e prontos para serem utilizados na criação de novos conteúdos originais."
    ),
    goal="Analisar os artigos encontrados, extrair principais ideias e estruturar um relatório com insights estratégicos.",
    verbose=True,
    llm=llm,
    memory=True
)

# Agente Redator
redator = Agent(
    role="Criador de Conteúdo",
    backstory=(
        "Você é um escritor talentoso e criativo, especializado na geração de conteúdo original e envolvente. "
        "Com base nas análises detalhadas do agente analista, sua missão é transformar dados e insights em "
        "artigos bem estruturados, que sejam informativos, persuasivos e agradáveis de ler. Sua escrita flui "
        "com naturalidade, e você sabe como adaptar o tom e estilo conforme o público-alvo. Você não apenas "
        "reorganiza informações, mas adiciona valor ao texto, conectando ideias e proporcionando novas perspectivas."
    ),
    goal="Escrever 10 artigos originais baseados nos insights coletados pelo analista, garantindo criatividade e profundidade.",
    verbose=True,
    llm=llm,
    memory=True
)


# Agente Revisor
revisor = Agent(
    role="Revisor e Editor",
    backstory=(
        "Você é um especialista em refinamento textual, garantindo que cada artigo produzido tenha fluidez, coerência "
        "e impacto. Seu olhar atento identifica erros gramaticais, ambiguidades e inconsistências, aprimorando a clareza "
        "e o profissionalismo de cada texto. Além de corrigir erros técnicos, você melhora a estrutura, o ritmo e o tom "
        "do conteúdo para torná-lo mais envolvente e adequado ao propósito final. Sua missão é transformar bons textos "
        "em materiais impecáveis e prontos para publicação."
    ),
    goal="Revisar e aprimorar os artigos gerados pelo redator, garantindo precisão, fluidez e qualidade editorial.",
    verbose=True,
    llm=llm,
    memory=True
)

# ---------------------------
# TAREFAS
# ---------------------------

# Tarefa do Pesquisador
pesquisa_task = Task(
    agent=pesquisador,
    description="Busque e colete os artigos mais recentes sobre um tema específico.",
    expected_output="Lista de links e resumos de pelo menos 5 artigos atuais sobre o tema."
)

# Tarefa do Analista
analise_task = Task(
    agent=analista,
    description="Analise os artigos encontrados e extraia as principais ideias e padrões.",
    expected_output="Resumo detalhado dos artigos com insights relevantes e sugestões de abordagem."
)

# Tarefa do Redator
criacao_artigos_task = Task(
    agent=redator,
    description="Com base no relatório do analista, crie 10 artigos originais sobre o tema.",
    expected_output="10 artigos bem estruturados, únicos e coerentes com os insights levantados."
)

# Tarefa do Revisor
revisao_task = Task(
    agent=revisor,
    description="Revisar e ajustar os artigos criados pelo redator, garantindo qualidade e clareza.",
    expected_output="10 artigos revisados, prontos para publicação ou armazenamento."
)

# ---------------------------
# CREW
# ---------------------------

# Configurando o Crew
crew = Crew(
    agents=[pesquisador, analista, redator, revisor],
    tasks=[pesquisa_task, analise_task, criacao_artigos_task, revisao_task],
    process=Process.sequential,
    memory=True
)

# Executando o Crew
result = crew.kickoff(inputs={"tópico": "Inteligência Artificial e Impacto no Mercado de Trabalho"})
print(result)
Explicação do Fluxo
Pesquisador coleta os artigos mais recentes usando a ferramenta de busca na web.
Analista examina os artigos e resume os principais insights e tendências.
Redator escreve 10 artigos com base nos insights coletados.
Revisor refina e ajusta a escrita para garantir clareza e coerência.
Vantagens desta abordagem
✅ Automatização Completa: Todo o processo de busca, análise e escrita é feito sem intervenção humana.
✅ Geração de Conteúdo de Qualidade: O uso da IA garante textos bem estruturados e coerentes.
✅ Escalabilidade: Pode ser adaptado para diversas áreas, como tecnologia, saúde, finanças, etc.
✅ Personalização: O usuário pode definir temas específicos e ajustar o fluxo conforme necessário.

Possíveis Melhorias
Integração com APIs: Adicionar APIs para buscar artigos diretamente em fontes como Google Scholar ou arXiv.
Armazenamento e Publicação: Criar um sistema para salvar os artigos em um banco de dados ou publicá-los automaticamente em blogs.
Melhoria da Revisão: Incluir um agente crítico para validar se o conteúdo não repete informações desnecessárias.
Este fluxo garante que os artigos criados tenham embasamento e sejam coerentes, tornando-se uma excelente solução para geração de conteúdos automatizados!