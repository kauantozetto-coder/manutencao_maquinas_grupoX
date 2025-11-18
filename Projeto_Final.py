import datetime
maquinas = [
    ["Torno CNC", "operando", 72.5, "05/11/2025"],
    ["Prensa Hidráulica", "parada", 30.0, "01/11/2025"],
    ["Compressor de Ar", "operando", 45.0, "04/11/2025"],
    ["Retífica", "operando", 60.0, "02/11/2025"],
]
historico = {
    "Torno CNC": ["Troca de óleo - 01/11/2025", "Limpeza - 03/11/2025"],
    "Prensa Hidráulica": ["Troca de mangueira - 02/11/2025"],
}
def adicionar_manutencao(nome_maquina, descricao):
    if nome_maquina not in historico:
        historico[nome_maquina] = []

    data_hoje = datetime.date.today().strftime("%d/%m/%Y")
    descricao_completa = f"{descricao} - {data_hoje}"
    historico[nome_maquina].append(descricao_completa)

    for m in maquinas:
        if m[0] == nome_maquina:
            m[3] = data_hoje
            print(f" Manutenção de '{nome_maquina}' registrada e data atualizada para {data_hoje}.")
            return
    print(f" Máquina '{nome_maquina}' não encontrada na lista principal.")


def registrar_medicao(linha):
    try:
        partes = linha.split(",")
        if len(partes) != 3:
            raise ValueError("Formato incorreto. Use: nome, temperatura, status")

        nome = partes[0].strip()
        temperatura = float(partes[1].strip())
        status = partes[2].strip().lower()  # Normaliza o status

        data_hoje = datetime.date.today().strftime("%d/%m/%Y")

        encontrada = False
        for m in maquinas:
            if m[0].lower() == nome.lower():
                m[1] = status
                m[2] = temperatura

                if status == "em manutenção":
                    pass

                print(f" Medição de '{nome}' atualizada: Status='{status}', Temp={temperatura}°C.")
                encontrada = True
                break

        if not encontrada:
            print(f" Máquina '{nome}' não encontrada para atualização.")

    except ValueError as e:
        print(f"🚨 Erro ao processar medição: {e}")

def salvar_dados_maquinas(lista_maquinas, nome_arquivo="dados_maquinas.txt"):
    try:
        with open(nome_arquivo, "w") as arq:
            for m in lista_maquinas:
                linha = f"{m[0]};{m[1]};{m[2]};{m[3]}\n"
                arq.write(linha)
        print(f" Dados das máquinas salvos em **{nome_arquivo}**")
    except IOError:
        print(f"🚨 Erro ao escrever no arquivo {nome_arquivo}.")


def carregar_dados_maquinas(nome_arquivo="dados_maquinas.txt"):
    maquinas_lidas = []
    try:
        with open(nome_arquivo, "r") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                if len(partes) == 4:
                    try:
                        nome = partes[0]
                        status = partes[1]
                        temperatura = float(partes[2])
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


def gerar_relatorio(nome_arquivo="relatorio_final.txt"):
    if not maquinas:
        print(" Não há máquinas cadastradas para gerar o relatório.")
        return
    maquina_quente = max(maquinas, key=lambda x: x[2])
    try:
        with open(nome_arquivo) as arq:
            arq.write("        RELATÓRIO DE MÁQUINAS           \n")

            arq.write(f"▶ Máquina mais quente: {maquina_quente[0]} ({maquina_quente[2]:.1f} °C)\n\n")

            arq.write("--- Máquinas que Requerem Atenção ---\n")
            encontrou_atencao = False
            for m in maquinas:
                if m[1].lower() in ["em manutenção", "parada"]:
                    arq.write(f"- {m[0]} (Status: {m[1]} | Última manutenção: {m[3]})\n")
                    encontrou_atencao = True
            if not encontrou_atencao:
                arq.write("- Nenhuma máquina requer atenção.\n")

            arq.write("\n--- Quantidade de Manutenções Registradas ---\n")
            for nome, eventos in historico.items():
                arq.write(f"- {nome}: {len(eventos)} registro(s)\n")

        print(f" Relatório gerado em **{nome_arquivo}**.")
    except IOError:
        print(f" Erro ao escrever no arquivo {nome_arquivo}.")

def buscar_maquina_por_nome_parcial(termo_busca):
    resultados = []
    termo = termo_busca.lower()

    for m in maquinas:
        if termo in m[0].lower():
            resultados.append(m)

    return resultados


def listar_maquinas_por_status(status_filtro):
    resultados = []
    status = status_filtro.lower()

    for m in maquinas:
        if m[1].lower() == status:
            resultados.append(m)

    return resultados


def modulo_extra():
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

def main():
    global maquinas

    dados_carregados = carregar_dados_maquinas()
    if dados_carregados:
        maquinas = dados_carregados

    while True:
        print("Sistema de Manutenção de Máquinas")
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
            modulo_extra()

        elif opc == "5":
            salvar_dados_maquinas(maquinas)
            salvar_historico(historico)

        elif opc == "0":
            print("Encerrando o sistema. Não se esqueça de salvar antes de sair.")
            break

        else:
            print("Opção inválida. Tente novamente.")

def salvar_historico(dict_historico, nome_arquivo="dados_historico.txt"):
    try:
        with open(nome_arquivo, "w") as arq:
            for maquina, eventos in dict_historico.items():
                linha = f"{maquina}|{'|'.join(eventos)}\n"
                arq.write(linha)
        print(f" Histórico de manutenções salvo em **{nome_arquivo}**")
    except IOError:
        print(f" Erro ao escrever no arquivo {nome_arquivo}.")


def carregar_historico(nome_arquivo="dados_historico.txt"):
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
        print(f"️ Arquivo de histórico '{nome_arquivo}' não encontrado. Iniciando com dados padrão.")
        return {}

historico = carregar_historico()

if __name__ == "__main__":
    main()