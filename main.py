from service.corrida_service import CorridaService  # importa do arquivo corridaservice


def pegar_numero(piloto):
    # devolve o número do piloto (ou 0 se não tiver) para ordenar a lista
    return piloto.get("driver_number") or 0


def main():
    service = CorridaService()  # Cria uma instância do serviço de corrida

    # Escolha o Grande Prêmio - ano e país para consultar
    ano = 2023
    pais = "Brazil"

    try:
        dados = service.buscar_dados_corrida(ano, pais)

        if dados is None:
            print("Nenhuma corrida encontrada.")
            return

        corrida = dados["corrida"]
        gp = dados["gp"]
        pilotos = dados["pilotos"]
        voltas = dados["voltas"]

        if gp:
            nome_gp = gp.get("meeting_name", "Nome indisponível")
        else:
            nome_gp = "Nome indisponível"

        print("\n=== DADOS DA CORRIDA ===")
        print(f"Grande Prêmio: {nome_gp}")
        print(f"Ano: {ano}")
        print(f"Sessão: {corrida.get('session_name')}")
        print(f"Session key: {corrida.get('session_key')}")

        print(f"\nTotal de pilotos: {len(pilotos)}")
        print(f"Registros de voltas: {len(voltas)}")

        print("\n=== PILOTOS ===")

        for piloto in sorted(pilotos, key=pegar_numero):
            numero = piloto.get("driver_number", "?")
            nome = piloto.get("full_name", "Nome indisponível")
            equipe = piloto.get("team_name", "Equipe indisponível")

            print(f"#{numero} - {nome} - {equipe}")

    except Exception as erro:
        print(f"Erro ao consultar a OpenF1: {erro}")  # erro exception (caso de erro ao consultar a api)


if __name__ == "__main__":
    main()  # Executa a função main quando o script é executado diretamente