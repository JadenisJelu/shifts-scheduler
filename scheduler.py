from typing import Union

def read_data(src):
    pass

def set_contrainsts(constraints):
    pass
'''
worker = {1: Ali, 2: Ahsan, 3: Ahmad}

availability = {worker:{day: tuple of start and end}}'''
class Operation():
    def __init__(self) -> None:
        self.operating_hours = {}
        #self.num_workers = 0
        self.availability = {}
        self.schedule = None
        self.min_hours = None
        self.workers = {}
        self.worker_names = set()

    def set_operating_hours(self, hours:Union[tuple, dict]) -> None:
        if isinstance(hours, tuple):
            for day in range(1, 8):
                self.operating_hours[day] = hours
        else:
            for day in range(1,8):
                if day in hours:
                    self.operating_hours[day] = hours[day]
                else:
                    self.operating_hours[day] = None

    # def set_num_workers(self, num:int) -> None:
    #     self.num_workers = num

    def set_availability(self, worker:int, dt:dict) -> None:
        self.availability[worker] = dt

    def set_min_hours(self, hours:Union[int, dict]) -> None:
        if isinstance(hours, int):
            self.min_hours=hours
        else:
            self.min_hours=hours

    def add_workers(self, name:str, contact:int) -> None:
        name = name.lower()
        if name in self.worker_names:
            raise Exception("Worker exists")
        else:
            if len(self.workers) != 0:
                id = max(self.workers) + 1
            else:
                id = 0
            self.workers[id] = (name, contact)
            self.worker_names.add(name)


    def _check_hours(self, worker: int, day:int) -> bool:
        '''check if employee fulfills hours'''
        if isinstance(self.min_hours, int):
            min_hours = self.min_hours
        
        worker = self.availability[worker]
        hours = 0
        for day in worker.keys():
            start, end = worker[day]
            hours += end - start

        if hours >= min_hours:
            return True
        else:
            return False

    def fit(self) -> None:
        pass

if __name__ == '__main__':
    storeA = Operation()
    storeA.set_operating_hours((8, 22))
    storeA.add_workers('Ahmad', '0123')
    storeA.add_workers('Ali', '0123')
    storeA.add_workers('Ahsan', '0123')