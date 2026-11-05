from repositories.piloto_repository import PilotoRepository
from repositories.carro_repository import CarroRepository
from repositories.telemetria_repository import TelemetriaRepository

# Cada repository é criado UMA vez aqui e todos os services usam estes mesmos.
# Assim, o piloto cadastrado no PilotoController é o mesmo que o
# TelemetriaService enxerga (os dados ficam em memória).
piloto_repository = PilotoRepository()
carro_repository = CarroRepository()
telemetria_repository = TelemetriaRepository()