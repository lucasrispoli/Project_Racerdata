import requests


class OpenF1Repository:
    BASE_URL = "https://api.openf1.org/v1"

    def _buscar_dados(self, endpoint, parametros=None):
        """Executa uma consulta à API e retorna os dados."""
        url = f"{self.BASE_URL}/{endpoint}"

        resposta = requests.get(
            url,
            params=parametros or {},
            timeout=15
        )
        resposta.raise_for_status()

        return resposta.json()

    def buscar_sessoes(self, parametros=None):
        return self._buscar_dados("sessions", parametros)

    def buscar_reunioes(self, parametros=None):
        return self._buscar_dados("meetings", parametros)

    def buscar_pilotos(self, parametros=None):
        return self._buscar_dados("drivers", parametros)

    def buscar_voltas(self, parametros=None):
        return self._buscar_dados("laps", parametros)
