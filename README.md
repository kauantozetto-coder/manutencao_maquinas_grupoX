1- Criação do grupo e das ferramentas utilizadas 

2- Escolha e implementação do modulo extra 

3- Estrutura
O núcleo do sistema utiliza duas estruturas principais:
maquinas: Uma lista de listas onde cada sub-lista representa uma máquina com os campos: Nome, Status, Temperatura, Última Manutenção.
historico: Um dicionário onde a chave é o nome da máquina e o valor é uma lista de strings

4- Funções
salvar_dados_maquinas() e carregar_dados_maquinas(): Gerenciam o arquivo dados_maquinas.txt.
salvar_historico() e carregar_historico(): Gerenciam o arquivo dados_historico.txt.
adicionar_manutencao(): Insere um registro no dicionário historico e atualiza a data da máquina na lista maquinas, utilizando o módulo datetime.
registrar_medicao(): Atualiza o status e a temperatura de uma máquina existente com base em uma entrada formatada do usuário.
gerar_relatorio(): Cria um arquivo relatorio_final.txt sumarizando as informações, incluindo a máquina com a maior temperatura registrada.
modulo_extra(): Demonstra funcionalidades de busca e filtro interativo por nome parcial ou status

5- Postagem do codigo no git 

6- organização do trello e do readme 
