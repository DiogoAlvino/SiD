from threading import Thread

class Racer(Thread):
    def __init__(self, i):
        Thread.__init__(self)
        self.i = i

    def run(self):
        while True:
            print(f"Racer {self.i} - imprimindo")

racer1 = Racer(1)
racer2 = Racer(2)
racer3 = Racer(3)

racer1.start()
racer2.start()
racer3.start()
