import datetime
import os  # Necessário para carregar o histórico de forma robusta

# --- 1. VARIÁVEIS DE DADOS GLOBAIS ---

# Lista principal que armazena os dados de todas as máquinas.
# Formato: [Nome (str), Status (str), Temperatura (°C) (float), Última Manutenção (str)]
maquinas = [
    ["Torno CNC", "operando", 72.5, "05/11/2025"],
    ["Prensa Hidráulica", "parada", 30.0, "01/11/2025"],
    ["Compressor de Ar", "operando", 45.0, "04/11/2025"],
    ["Retífica", "operando", 60.0, "02/11/2025"],
]

# Dicionário que armazena o histórico detalhado de manutenções.
# Inicializado como vazio para ser preenchido pela função carregar_historico().
historico = {}


# --- 2. FUNÇÕES DE PERSISTÊNCIA (SALVAR/CARREGAR) ---

def salvar_dados_maquinas(lista_maquinas, nome_arquivo="dados_maquinas.txt"):
    """Salva os dados da lista 'maquinas' em um arquivo de texto, usando ';' como separador."""
    try:
        with open(nome_arquivo, "w") as arq:
            for m in lista_maquinas:
                # Formato: Nome;Status;Temperatura;Data\n
                linha = f"{m[0]};{m[1]};{m[2]};{m[3]}\n"
                arq.write(linha)
        print(f" Dados das máquinas salvos em **{nome_arquivo}**")
    except IOError:
        print(f" Erro ao escrever no arquivo {nome_arquivo}.")


def carregar_dados_maquinas(nome_arquivo="dados_maquinas.txt"):
    """Carrega os dados das máquinas de um arquivo de texto, usando ';' como separador."""
    maquinas_lidas = []
    try:
        with open(nome_arquivo, "r") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                if len(partes) == 4:
                    try:
                        nome = partes[0]
                        status = partes[1]
                        temperatura = float(partes[2])  # Tenta converter para float
                        ultima = partes[3]
                        maquinas_lidas.append([nome, status, temperatura, ultima])
                    except ValueError:
                        print(f" Erro de conversão de dados na linha: {linha.strip()}")
                else:
                    print(f"Linha ignorada por formato incorreto: {linha.strip()}")
        print(f" Dados carregados com sucesso de **{nome_arquivo}**.")
        return maquinas_lidas
    except FileNotFoundError:
        print(f" Arquivo '{nome_arquivo}' não encontrado. Iniciando com dados padrão.")
        return []


def salvar_historico(dict_historico, nome_arquivo="dados_historico.txt"):
    """Salva o dicionário de histórico em um arquivo, usando '|' como separador entre eventos."""
    try:
        with open(nome_arquivo, "w") as arq:
            for maquina, eventos in dict_historico.items():
                # Formato: Maquina|Evento1|Evento2|...
                linha = f"{maquina}|{'|'.join(eventos)}\n"
                arq.write(linha)
        print(f" Histórico de manutenções salvo em **{nome_arquivo}**")
    except IOError:
        print(f" Erro ao escrever no arquivo {nome_arquivo}.")


def carregar_historico(nome_arquivo="dados_historico.txt"):
    """Carrega o dicionário de histórico de um arquivo, usando '|' como separador."""
    historico_lido = {}
    try:
        with open(nome_arquivo, "r") as arq:
            for linha in arq:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split("|")
                if len(partes) >= 1:
                    maquina = partes[0]
                    eventos = partes[1:]
                    historico_lido[maquina] = eventos
        print(f" Histórico carregado com sucesso de **{nome_arquivo}**.")
        return historico_lido
    except FileNotFoundError:
        print(f" Arquivo de histórico '{nome_arquivo}' não encontrado. Iniciando com dados padrão.")
        return {}


# --- 3. FUNÇÕES DE OPERAÇÃO E ATUALIZAÇÃO ---

def adicionar_manutencao(nome_maquina, descricao):
    """Adiciona um registro de manutenção ao histórico e atualiza a data na lista de máquinas."""
    global historico

    if nome_maquina not in historico:
        historico[nome_maquina] = []

    # Obtém e formata a data atual
    data_hoje = datetime.date.today().strftime("%d/%m/%Y")
    descricao_completa = f"{descricao} - {data_hoje}"
    historico[nome_maquina].append(descricao_completa)

    # Atualiza a data da última manutenção na lista 'maquinas' (índice 3)
    for m in maquinas:
        if m[0] == nome_maquina:
            m[3] = data_hoje
            print(f" Manutenção de '{nome_maquina}' registrada e data atualizada para {data_hoje}.")
            return
    print(f" Máquina '{nome_maquina}' não encontrada na lista principal.")


def registrar_medicao(linha):
    """Atualiza o status e a temperatura de uma máquina a partir de uma string de entrada."""
    global maquinas
    try:
        partes = linha.split(",")
        if len(partes) != 3:
            raise ValueError("Formato incorreto. Use: nome, temperatura, status")

        nome = partes[0].strip()
        temperatura = float(partes[1].strip())  # Converte para float
        status = partes[2].strip().lower()  # Normaliza o status

        encontrada = False
        # Percorre a lista para encontrar a máquina pelo nome (case-insensitive)
        for m in maquinas:
            if m[0].lower() == nome.lower():
                m[1] = status  # Atualiza Status
                m[2] = temperatura  # Atualiza Temperatura

                print(f" Medição de '{m[0]}' atualizada: Status='{status}', Temp={temperatura}°C.")
                encontrada = True
                break

        if not encontrada:
            print(f" Máquina '{nome}' não encontrada para atualização.")

    except ValueError as e:
        print(f" Erro ao processar medição: {e}")


# --- 4. FUNÇÃO DE RELATÓRIO ---

def gerar_relatorio(nome_arquivo="relatorio_final.txt"):
    """Gera um arquivo de texto com o resumo das máquinas, a mais quente e o histórico."""
    global maquinas, historico
    if not maquinas:
        print(" Não há máquinas cadastradas para gerar o relatório.")
        return

    # Encontra a máquina com a maior temperatura (m[2])
    maquina_quente = max(maquinas, key=lambda x: x[2])

    try:
        # Modo 'w' para sobrescrever o arquivo
        with open(nome_arquivo, "w") as arq:
            arq.write("        RELATÓRIO DE MÁQUINAS           \n")
            arq.write("=" * 40 + "\n")

            # Máquina mais quente
            arq.write(f"▶ Máquina mais quente: {maquina_quente[0]} ({maquina_quente[2]:.1f} °C)\n\n")

            # Máquinas que requerem atenção
            arq.write("--- Máquinas que Requerem Atenção ---\n")
            encontrou_atencao = False
            for m in maquinas:
                if m[1].lower() in ["em manutenção", "parada"]:
                    arq.write(f"- {m[0]} (Status: {m[1]} | Última manutenção: {m[3]})\n")
                    encontrou_atencao = True
            if not encontrou_atencao:
                arq.write("- Nenhuma máquina requer atenção.\n")

            # Quantidade de manutenções
            arq.write("\n--- Quantidade de Manutenções Registradas ---\n")
            for nome, eventos in historico.items():
                arq.write(f"- {nome}: {len(eventos)} registro(s)\n")

        print(f" Relatório gerado em **{nome_arquivo}**.")
    except IOError:
        print(f" Erro ao escrever no arquivo {nome_arquivo}.")


# --- 5. MÓDULO EXTRA 4: BUSCA/FILTRO (IMPLEMENTAÇÃO) ---

def buscar_maquina_por_nome_parcial(termo_busca):
    """Busca máquinas cujo nome contenha o termo de busca (case-insensitive)."""
    resultados = []
    termo = termo_busca.lower()

    for m in maquinas:
        if termo in m[0].lower():
            resultados.append(m)

    return resultados


def listar_maquinas_por_status(status_filtro):
    """Filtra máquinas que possuem um status de operação específico."""
    resultados = []
    status = status_filtro.lower()

    for m in maquinas:
        if m[1].lower() == status:
            resultados.append(m)

    return resultados


def modulo_extra():
    """Interface para o Módulo 4: Busca e Filtro, integrada ao menu principal."""
    print("\n--- Módulo Extra 4: Busca e Filtro ---")
    print("1 - Buscar máquina por nome parcial")
    print("2 - Filtrar máquinas por status")

    opc = input("Escolha uma opção: ")

    if opc == "1":
        termo = input("Digite o termo de busca (ex: 'torno' ou 'pressor'): ")
        resultados = buscar_maquina_por_nome_parcial(termo)

        if resultados:
            print(f"\nResultados da busca por '{termo}':")
            for m in resultados:
                print(f"  - {m[0]} | Status: {m[1]} | Temp: {m[2]} °C | Última Manut: {m[3]}")
        else:
            print(f" Nenhuma máquina encontrada com o termo '{termo}'.")

    elif opc == "2":
        status_filtro = input("Digite o status para filtrar (ex: 'operando', 'parada', 'em manutenção'): ")
        resultados = listar_maquinas_por_status(status_filtro)

        if resultados:
            print(f"\nMáquinas com status '{status_filtro.upper()}':")
            for m in resultados:
                print(f"  - {m[0]} | Temp: {m[2]} °C | Última Manut: {m[3]}")
        else:
            print(f" Nenhuma máquina encontrada com o status '{status_filtro}'.")

    else:
        print("Opção inválida do Módulo Extra.")


# --- 6. FLUXO PRINCIPAL (MENU) ---

def main():
    global maquinas, historico

    # 1. Carregamento Inicial de Dados

    # Carrega o histórico (necessário antes de carregar as máquinas para ter o dado global)
    historico_carregado = carregar_historico()
    if historico_carregado:
        historico = historico_carregado

    # Tenta carregar os dados das máquinas. Se houver dados salvos, substitui os dados iniciais.
    dados_carregados = carregar_dados_maquinas()
    if dados_carregados:
        maquinas = dados_carregados

    # 2. Loop do Menu
    while True:
        print("\n=== Sistema de Manutenção de Máquinas ===")
        print("1 - Registrar medição (Atualizar status/temp)")
        print("2 - Adicionar registro de manutenção")
        print("3 - Gerar relatório final (.txt)")
        print("4 - Rodar Módulo Extra (Busca/Filtro)")
        print("5 - Salvar dados e histórico")
        print("0 - Sair")

        opc = input("Escolha uma opção: ")

        if opc == "1":
            linha = input("Digite: Nome, Temperatura, Status (ex: Torno CNC, 78.5, operando): ")
            registrar_medicao(linha)

        elif opc == "2":
            nome = input("Nome da máquina: ")
            desc = input("Descrição da manutenção: ")
            adicionar_manutencao(nome, desc)

        elif opc == "3":
            gerar_relatorio()

        elif opc == "4":
            # Chama o Módulo Extra
            modulo_extra()

        elif opc == "5":
            # Salva ambos os conjuntos de dados
            salvar_dados_maquinas(maquinas)
            salvar_historico(historico)

        elif opc == "0":
            print("Encerrando o sistema. Não se esqueça de salvar antes de sair.")
            break

        else:
            print("Opção inválida. Tente novamente.")


# 3. Execução
if __name__ == "__main__":
    main()