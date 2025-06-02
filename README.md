# CientIA Artigos

Gere artigos científicos originais com IA multiagente!

## Descrição
Este aplicativo utiliza a biblioteca CrewAI para orquestrar múltiplos agentes inteligentes que pesquisam, analisam e redigem artigos científicos completos e inéditos sobre qualquer tema informado pelo usuário. A interface é feita em Streamlit para facilitar o uso.

## Funcionalidades
- Busca automática de referências e artigos recentes sobre o tema informado
- Análise dos conteúdos encontrados
- Geração de **5 artigos científicos originais** com introdução, desenvolvimento e conclusão (mínimo 1000 palavras cada)
- Revisão automática dos textos
- Download dos artigos em formato `.txt`

## Como usar
1. **Clone o repositório**
2. **Instale as dependências**:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. **Configure as variáveis de ambiente** em um arquivo `.env` (exemplo: chaves de API para busca web)
4. **Execute o app**:
   ```bash
   .\venv\Scripts\Activate.ps1
   streamlit run app_streamlit.py
   ```
5. **Informe o tema** e aguarde a geração dos artigos!

## Estrutura dos agentes
- **Pesquisador:** Busca referências confiáveis
- **Analista:** Extrai insights e organiza informações
- **Redator:** Cria os artigos originais, completos e estruturados
- **Revisor:** Refina o texto e garante qualidade acadêmica

## Requisitos
- Python 3.10+
- CrewAI
- Streamlit
- crewai-tools
- dotenv

## Licença
MIT

---

> Desenvolvido com 💡 por IA e colaboração humana.
