def read_data(src):
    pass

def set_contrainsts(constraints):
    pass

class operation():
    def __init__(self) -> None:
        self.operating_hours = {}
        self.num_workers = 0
        self.availability = {}
        self.schedule = None

    def set_operating_hours(self, dt:dict) -> None:
        self.operating_hours = dt

    def set_num_workers(self, num:int) -> None:
        self.num_workers = num

    def set_availability(self, worker:int, dt:dict) -> None:
        self.availability[worker] = dt

    def fit(self) -> None:
        pass