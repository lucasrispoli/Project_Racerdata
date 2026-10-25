from service.corrida_service import CorridaService


def main():
    service = CorridaService()

    # Escolha o Grande Prêmio
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

        nome_gp = (
            gp.get("meeting_name", "Nome indisponível")
            if gp else "Nome indisponível"
        )

        print("\n=== DADOS DA CORRIDA ===")
        print(f"Grande Prêmio: {nome_gp}")
        print(f"Ano: {ano}")
        print(f"Sessão: {corrida.get('session_name')}")
        print(f"Session key: {corrida.get('session_key')}")

        print(f"\nTotal de pilotos: {len(pilotos)}")
        print(f"Registros de voltas: {len(voltas)}")

        print("\n=== PILOTOS ===")

        for piloto in sorted(
            pilotos,
            key=lambda p: p.get("driver_number") or 0
        ):
            numero = piloto.get("driver_number", "?")
            nome = piloto.get("full_name", "Nome indisponível")
            equipe = piloto.get("team_name", "Equipe indisponível")

            print(f"#{numero} - {nome} - {equipe}")

    except Exception as erro:
        print(f"Erro ao consultar a OpenF1: {erro}")


if __name__ == "__main__":
    main()
