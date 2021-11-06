from typing import Union
import numpy as np
import random

def read_data(src):
    pass

def set_contrainsts(constraints):
    pass
'''
worker = {1: Ali, 2: Ahsan, 3: Ahmad}

availability = {worker:{day: tuple of start and end}}'''

class Schedule():
    pass

class Operation():
    def __init__(self) -> None:
        self.operating_hours = {}
        self.shift_hours = None
        #self.num_workers = 0
        self.availability = {}
        #self.granularity = 'hour'
        self.schedule = None # modify schedule in place
        self.min_hours = None
        self.workers = {}
        self.worker_names = set()
        self.blocks = None

        self._instatiate_schedule()

    def __repr__(self) -> str:
        return f"This operation operates on {self.operating_hours} with {self.worker_names}."

    def _instatiate_schedule(self, granularity:str ='hour') -> None:
        '''likely depreceated'''
        if granularity == 'hour':
            if not self.schedule:
                ls = [0] * 24
                sches = []
                for i in range(1, 8):
                    #hr = self.operating_hours[i]
                    #ls = [0] * (hr[1] - hr[0])
                    sches.append(ls)
                self.schedule = sches

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
    def set_shift_hours(self, hours:Union[dict, int]) -> None:
        self.shift_hours = hours 

    def set_availability(self, worker:int, dt:dict) -> None:
        self.availability[worker] = dt

    def set_min_hours(self, hours:Union[int, dict]) -> None:
        if isinstance(hours, int):
            self.min_hours=hours
        else:
            self.min_hours=hours
    
    def worker_available(self, hours:tuple, worker:int, day:int) -> bool:
        avail_hrs = self.availability[worker]
        start, end = hours
        if isinstance(avail_hrs, int):
            if 0 <= start and avail_hrs >= end:
                return True
        elif isinstance(avail_hrs, tuple):
            if avail_hrs[0] <= start and avail_hrs[1] >= end:
                return True
        elif isinstance(avail_hrs, dict):
            if avail_hrs[day][0] <= start and avail_hrs[day][1] >= end:
                return True
        return False
    
    def create_blocks(self) -> dict:
        '''create blocks for scheduling'''
        blocks_dt = {}
        i = 0
        for day in range(7):
            start, end = self.operating_hours[day+1]
            curr = start
            # create daily block
            while curr != end:
                step = min(curr + self.shift_hours, end)
                avail_workers = set([worker for worker in self.workers if self.worker_available((curr, step), worker, day)])
                blocks_dt[i] = [(day, (curr, step)), avail_workers]
                i += 1
                curr = step
        del i
        return blocks_dt

    @staticmethod
    def select_random(worker_shifts:dict) -> bool:
        worker = random.choice(list(worker_shifts.keys()))
        worker_shifts[worker] -= 1
        if worker_shifts[worker] == 0:
            del worker_shifts[worker]
        return worker, worker_shifts

    def scheduler(self) -> None:
        # create blocks
        blocks_dt = self.create_blocks()

        # create max shifts
        shifts = len(blocks_dt.keys())
        workers = len(self.workers.keys())
        worker_shifts = {worker: 0 for worker in self.workers}
        for shift in range(shifts):
            worker_shifts[shift%workers] += 1

        # scheduler
        np.random.seed(23)
        for i in range(shifts):
            # place 1 worker
            worker, worker_shifts = self.select_random(worker_shifts)
            blocks_dt[i][1] = worker
        
        blocks_dt = self._beauty_parser(blocks_dt)
        self.schedule = blocks_dt

    @staticmethod
    def _beauty_parser(dt:dict) -> dict:
        tmp = {}
        for i, ((key, hours), worker) in dt.items():
            if key in tmp:
                tmp[key][hours] = worker
            else:
                tmp[key] = {hours: worker}
        return tmp

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

    # dynamic backtracking approach for cleaner code
    """ def fit(self) -> None:
        pass

    def is_valid_state(self, schedule) -> bool:
        '''given schedule, check if valid'''
        # check if it is a valid solution
        # validate all workers present
        # validate all workers achieve min time
        # validate all schedule time slot filled
        workers = set()
        for day in schedule:
            workers = workers | set(day)

        if len(workers) != len(self.worker_names):
            return False
        return True

    def get_candidates(self, state):
        return []

    def search(self, state, solutions):
        if self.is_valid_state(state):
            solutions.append(state.copy())
            # return

        for candidate in self.get_candidates(state):
            state.add(candidate)
            self.search(state, solutions)
            state.remove(candidate)

    def solve(self):
        solutions = []
        state = set()
        self.search(state, solutions)
        return solutions """

if __name__ == '__main__':
    storeA = Operation()
    storeA.set_operating_hours((8, 22))
    storeA.add_workers('Ahmad', '0123')
    storeA.add_workers('Ali', '0123')
    storeA.add_workers('Ahsan', '0123')
    storeA.set_availability(0, 24)
    storeA.set_availability(1, 24)
    storeA.set_availability(2, 24) # take list as input too
    storeA.set_operating_hours((8, 24))
    storeA.set_shift_hours(8)
    storeA.scheduler()
    import pprint 
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(storeA.schedule)