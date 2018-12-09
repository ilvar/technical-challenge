import logging


class Solver(object):
    colors = None
    customers = None
    demands = None
    mattes = None
    glossy = None
    
    _iterations = 0
    
    def __init__(self, problem):
        self.colors = problem.get("colors")
        self.customers = problem.get("customers")
        self.demands = problem.get("demands")
    
        self.mattes = {}
        self.glossy = []
        for c in range(self.customers):
            length = self.demands[c][0]
            demand = self.demands[c][1:]
            self.glossy.append(set())
            for i in range(length):
                (color, matte) = (demand[2 * i], demand[2 * i + 1])
                if matte == 1:
                    self.mattes[c] = color - 1
                else:
                    self.glossy[c].add(color - 1)
                    
    def solve(self):
        solved, solution = self.start()

        logging.debug("Finished in %s iterations" % self._iterations)

        if solved:
            return " ".join(map(str, solution))
        else:
            return "IMPOSSIBLE"
    
    def check(self, solution):
        for customer in range(self.customers):
            good = False
            for i in range(len(solution)):
                if solution[i] == 0 and i in self.glossy[customer]:
                    good = True
                if solution[i] == 1 and self.mattes.get(customer) == i:
                    good = True
            if not good:
                return False
        return True
        
    def start(self):
        solution = [0] * self.colors

        return self.reduce(solution, None)
    
    def reduce(self, solution_on_stack, change, best_sum=None):
        solution = list(solution_on_stack[:])
        if change is not None:
            solution[change] = 1
            
        if self.check(solution):
            return True, solution
        
        solution_sum = sum(solution)
        solution_len = len(solution)
        if solution_sum == solution_len:
            return False, None

        if best_sum is not None and solution_sum > best_sum:
            return False, None
        
        result = None
        solved = False
        for i in range(solution_len):
            if solution[i] == 0:
                solved_i, result_i = self.reduce(solution, i, best_sum)
                if solved_i:
                    current_sum = sum(result_i)
                    self._iterations += 1
                    if best_sum is None or current_sum < best_sum:
                        solved = True
                        result = result_i
                        best_sum = current_sum
        return solved, result
