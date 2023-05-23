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
            armazenaPares = []
            for x in range(1, self.quantLoop):
                #print(x)
                if x % 2 != 0:
                    print(f"Race {x} da {self.nomeCorrida} - imprimindo (Prioridade: {self.prioridade})")
                    #time.sleep(1)
                else:
                    armazenaPares.append(x)
            for y in armazenaPares:
                print(f"Race {y} da {self.nomeCorrida} - imprimindo (Prioridade: {self.prioridade})")

class Racer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        contador = 0
        for i in range(1, 1001):
            contador += 1
            print(f"Racer {i} - imprimindo - {contador}")

race1 = Race(1001, "Corrida 1", 1)
racer1 = Racer()

#race1.start()
#race1.join()

#racer1.start()