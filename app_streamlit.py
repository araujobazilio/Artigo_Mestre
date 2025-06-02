import streamlit as st
from crew_logic import create_crew, save_articles
import os
import time
from pathlib import Path

def criar_diretorios():
    """Cria os diretórios necessários para a aplicação"""
    Path("static/artigos").mkdir(parents=True, exist_ok=True)

def salvar_resultado(topico, result):
    """Salva o resultado em arquivo e retorna o caminho"""
    try:
        filename = save_articles(topico, result)
        filepath = os.path.join('static', 'artigos', filename)
        return filepath
    except Exception as e:
        st.error(f"Erro ao salvar artigos: {str(e)}")
        return None

def main():
    # Criar diretórios necessários
    criar_diretorios()

    st.set_page_config(
        page_title="Gerador de Artigos com CrewAI",
        page_icon="📝",
        layout="wide"
    )

    # Container principal
    with st.container():
        st.title("🤖 Gerador de Artigos Científicos com CrewAI")
        st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Área de entrada
    with st.sidebar:
        st.header("📋 Configurações")
        topico = st.text_input(
            "Tópico para pesquisa:",
            placeholder="Ex: Inteligência Artificial e Sociedade",
            help="Digite o tema sobre o qual deseja gerar artigos"
        )
        
        num_artigos = st.slider(
            "Número de Artigos", 
            min_value=3, 
            max_value=7, 
            value=5,
            help="Escolha quantos artigos deseja gerar"
        )

        gerar = st.button("🚀 Gerar Artigos", type="primary", use_container_width=True)

    # Área principal
    if gerar:
        if not topico:
            st.warning("⚠️ Por favor, insira um tópico para gerar artigos.")
            return

        try:
            with st.spinner("Inicializando agentes..."):
                # Container para o progresso
                progress_container = st.container()
                
                with progress_container:
                    progress_bar = st.progress(0)
                    status = st.empty()
                    
                    # Etapas do processo
                    etapas = {
                        "Pesquisador": "🔍 Pesquisando conteúdo relevante...",
                        "Analista": "📊 Analisando informações coletadas...",
                        "Redator": "✍️ Criando artigos científicos...",
                        "Revisor": "📝 Revisando e refinando conteúdo..."
                    }
                    
                    # Criar e executar o crew
                    crew = create_crew(topico)
                    
                    # Iniciar processamento
                    for i, (agente, mensagem) in enumerate(etapas.items()):
                        status.write(mensagem)
                        progress_bar.progress((i + 1) * 25)
                        if i < len(etapas) - 1:
                            time.sleep(1)
                    
                    result = crew.kickoff(inputs={"tópico": topico})
                    
                    # Salvar resultado
                    filepath = salvar_resultado(topico, result)
                    
                    if filepath and os.path.exists(filepath):
                        progress_bar.progress(100)
                        status.success("✅ Artigos gerados com sucesso!")
                        
                        # Exibir resultados
                        with open(filepath, 'r', encoding='utf-8') as f:
                            artigos = f.read()
                        
                        st.download_button(
                            label="📥 Baixar Artigos",
                            data=artigos,
                            file_name=os.path.basename(filepath),
                            mime='text/plain',
                            key='download_button'
                        )
                        
                        # Mostrar prévia
                        with st.expander("👀 Ver prévia dos artigos", expanded=True):
                            st.markdown(artigos)
                    else:
                        st.error("❌ Erro ao gerar artigos. Tente novamente.")
                        
        except Exception as e:
            st.error(f"❌ Ocorreu um erro: {str(e)}")
            st.info("🔄 Por favor, tente novamente ou escolha um tópico diferente.")

    # Rodapé
    st.sidebar.markdown("---")
    st.sidebar.info(
        """
        ### ℹ️ Sobre
        Este aplicativo usa CrewAI para gerar artigos científicos de alta qualidade.
        
        **Agentes:**
        - 🔍 Pesquisador
        - 📊 Analista
        - ✍️ Redator
        - 📝 Revisor
        """
    )

if __name__ == "__main__":
    main()
