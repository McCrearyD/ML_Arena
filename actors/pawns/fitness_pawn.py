from actors.pawns.pawn import *
import time


class FitnessPawn(Pawn):
    total_hits: int = 1
    total_attacks: int = 1
    total_hits_taken: int = 1
    start_time: int
    death_time: int = None

    def calculate_fitness(self):
        hit_rate = self.total_hits / self.total_attacks ** 2
        time_alive = 0

        if self.death_time == None:
            time_alive = time.time() - self.start_time
        else:
            time_alive = self.death_time - self.start_time

        return hit_rate * time_alive

    def log_hit(self):
        self.total_hits += 1

    def long_attack(self):
        if super().long_attack():
            self.total_attacks += 1

    def short_attack(self):
        if super().short_attack():
            self.total_attacks += 1

    def take_damage(self, amount):
        self.total_hits_taken += 1
        return super().take_damage(amount)

    def kill(self):
        self.death_time = time.time()
        super().kill()

    def reset(self):
        self.start_time = time.time()
        self.death_time = None
        self.total_hits = 0
        self.total_hits_taken = 0
        super().reset()
