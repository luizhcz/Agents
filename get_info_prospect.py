import json
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic # pip install langchain_anthropic
from dotenv import load_dotenv
load_dotenv()

def find_prospect_name(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except UnicodeDecodeError as e:
        return f"Erro ao ler o arquivo (problema de codificação): {e}"
    except Exception as e:
        return f"Erro ao ler o arquivo: {e}"


# Agente de leitura que encontra o nome do prospecto
reader_agent = Agent(
    role="File Reader",
    goal="Leia o texto e encontre o nome do prospecto.",
    verbose=True,
    memory=False,
    max_iter=1,
    backstory="Você é responsável por ler e encontrar informações importantes com base nas instruções.",
    llm=ChatOpenAI(model_name="gpt-4o", temperature=0.1)
)


# Tarefa de leitura
read_task = Task(
    description=""" 
    **Instruções:**

    Encontre e extraia os seguintes dados de um prospecto:

    1. **Nome do Fundo (nome_fundo)**: Extraia o nome do fundo conforme mencionado no prospecto.
    
    2. **CNPJ do Fundo (cnpj_fundo)**: Extraia o CNPJ do fundo como indicado no prospecto.

    3. **Classificação do Fundo (classificacao_fundo)**: Identifique a categoria ou tipo do fundo de acordo com as classificações abaixo:
    - Fundos de Renda Fixa -> renda fixa
    - Fundos de Ações -> acao
    - Fundos Multimercado -> multimercado
    - Fundos Cambiais -> cambio
    - Fundos de Investimento Imobiliário -> fii
    - Fundos de Índices -> etf
    - Fundos de Crédito Privado -> private equity
    - Fundos de Capital Estrangeiro -> capital estrangeiro
    - Fundos Referenciados -> referenciado
    - Fundos de Previdência -> previdência

    4. **Risco (risco)**: Informe o risco do fundo conforme as categorias a seguir:
    - Risco baixo -> baixo
    - Risco baixo a moderado -> baixoModerado
    - Risco médio -> medio
    - Risco moderado a médio -> medioModerado
    - Risco alto -> alto
    - Risco moderado a alto -> altoModerado
    - Risco variável -> variavel

    5. **Cota (cota)**: Informe a quantidade de cotas disponibilizadas pelo fundo.

    6. **Administrador (administrador)**: Identifique o administrador do fundo e seu CNPJ.

    7. **Valor da Cota (valorCota)**: Extraia o valor unitário da cota, conforme informado no prospecto.

    8. **Valor Inicial (valorInicial)**: Informe o valor inicial do fundo.

    9. **Objetivo do Fundo (objetivo)**: Extraia o objetivo principal do fundo conforme descrito no prospecto.
  
    10. **Código ISIN (codigo_ISIN)**: Extraia o código ISIN, que é um identificador único para o fundo negociado.

    11. **Código de Negociação (codigo_negociacao)**: Extraia o código de negociação do fundo, que é utilizado em bolsas de valores como a B3.

    12. **Segmento ANBIMA (segmento_ANBIMA)**: Identifique o segmento do fundo conforme classificação da ANBIMA (por exemplo, "Títulos e Valores Mobiliários").

    13. **Preço de Emissão (preco_emissao)**: Extraia o valor de emissão de cada cota, como informado no prospecto.

    14. **Montante Total da Oferta (montante_total_oferta)**: Informe o valor total da oferta pública de cotas.

    15. **Montante Mínimo da Oferta (montante_minimo_oferta)**: Informe o montante mínimo de investimento necessário para a participação na oferta.

    16. **Número de Cotas Disponíveis (num_cotas_disponiveis)**: Extraia a quantidade de cotas disponibilizadas para emissão ou venda na oferta pública.

    17. **Data de Início da Oferta (data_inicio_oferta)**: Extraia a data de início da oferta pública de cotas do fundo.

    18. **Prazo de Colocação (prazo_colocacao)**: Identifique o período durante o qual as cotas estarão disponíveis para subscrição.

    19. **Gestor do Fundo (gestor_fundo)**: Identifique a instituição gestora do fundo e seu CNPJ.

    20. **Taxa de Administração (taxa_administracao)**: Informe o valor da taxa de administração cobrada pelo fundo.

    21. **Taxa de Performance (taxa_performance)**: Extraia o valor da taxa de performance, se aplicável, cobrada sobre o rendimento do fundo.

    22. **Distribuidor (distribuidor)**: Informe o nome da corretora ou instituição responsável pela distribuição das cotas.

    23. **Regulamento do Fundo (regulamento_fundo)**: Extraia o link ou referência ao regulamento oficial do fundo.

    24. **Público-Alvo (publico_alvo)**: Descreva o público-alvo do fundo, conforme informado no prospecto (por exemplo, investidores institucionais, pessoas físicas, etc.).

    25. **Fatores de Risco (fatores_risco)**: Liste os principais riscos envolvidos no investimento no fundo, conforme descritos no prospecto.

    26. **Rentabilidade Passada (rentabilidade_passada)**: Informe se há detalhes sobre a rentabilidade passada do fundo, com a ressalva de que não garante resultados futuros.

    27. **Liquidez (liquidez)**: Informe a liquidez do fundo (por exemplo, diária, mensal, semestral), conforme indicado.

    28. **Tributação (tributacao)**: Extraia as informações sobre a tributação aplicável ao fundo e aos investidores.

    29. **Prazo de Resgate (prazo_resgate)**: Informe o prazo necessário para resgatar as cotas, se aplicável.
        
        
        {content}
    """,
    expected_output="""
        Sua resposta precisa ser em português no formato Json.

        Exemplo de resposta:

        {exemplo}
    """,
    agent=reader_agent
)


crew = Crew(
    agents=[reader_agent],
    tasks=[read_task],
    verbose=2,
)

# Caminho do arquivo TXT local
file_path = "C:/FundosNET/CrewAi/03683056000186-OPD06112017V02-000018672.txt"
output_file = "C:/FundosNET/CrewAi/nome_prospecto.txt"

exemplo = {
            "nome_fundo": "Fundo de Investimento Alpha",
            "cnpj_fundo": "12.345.678/0001-90",
            "classificacao_fundo": "renda fixa",
            "risco": "alto",
            "cota": "100.002",
            "administrador": {
                "nome": "Investimento Beta",
                "cnpj": "22.333.444/0001-90"
            },
            "valorCota": "100.01",
            "valorInicial": "100.000.000,00",
            "objetivo": "O fundo tem como objetivo fazer aplicações em títulos de renda fixa.",
            "codigo_ISIN": "BR1234567890",
            "codigo_negociacao": "FIA123",
            "segmento_ANBIMA": "Títulos e Valores Mobiliários",
            "preco_emissao": "98.37",
            "montante_total_oferta": "80.000.091,09",
            "montante_minimo_oferta": "10.000.097,46",
            "num_cotas_disponiveis": "813.257",
            "data_inicio_oferta": "2023-09-01",
            "prazo_colocacao": "2023-10-01",
            "gestor_fundo": {
                "nome": "RBR Gestão de Recursos Ltda.",
                "cnpj": "18.259.351/0001-87"
            },
            "taxa_administracao": "1.5%",
            "taxa_performance": "20% sobre o que exceder o CDI",
            "distribuidor": "XP Investimentos S.A.",
            "regulamento_fundo": "https://www.exemplo.com/regulamento.pdf",
            "publico_alvo": "Investidores institucionais e pessoas físicas qualificados",
            "fatores_risco": [
                "Risco de mercado",
                "Risco de liquidez",
                "Risco de crédito"
            ],
            "rentabilidade_passada": "A rentabilidade passada não garante resultados futuros.",
            "liquidez": "Mensal",
            "tributacao": "Imposto de Renda sobre ganho de capital",
            "prazo_resgate": "60 dias"
        }

content = find_prospect_name(file_path=file_path)
result = crew.kickoff(inputs={"content": content, "exemplo": exemplo })

# Exibe o resultado
print("Resultado:", result)
