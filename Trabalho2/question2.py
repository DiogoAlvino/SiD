from threading import Thread, Lock
import time

class Race(Thread):
    def __init__(self, quantLoop, nomeCorrida, prioridade):
        Thread.__init__(self)
        self.quantLoop = quantLoop
        self.nomeCorrida = nomeCorrida
        self.prioridade = prioridade
        self.lock = Lock()

    def run(self):
        with self.lock:
            for x in range(1, self.quantLoop):
                print(f"Race {x} da {self.nomeCorrida} - imprimindo (Prioridade: {self.prioridade})")
                time.sleep(1)

race1 = Race(11, "Corrida 1", 1)
race2 = Race(12, "Corrida 2", 2)

race1.start()
race1.join()
race2.start()

# Respostas:
# a) A corrida 1 rodou por completo, e em seguida rodou a corrida 2.
# b) O comportamento do sistema mudou, as corridas rodaram de maneira alternada.
# c) Utilizando a prioridade, com auxilio do join, mesmo com o time.sleep foi possivel definir um processamento rodar com prioridade, para no seu fim iniciar a outra corrida.