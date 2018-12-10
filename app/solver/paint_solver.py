import logging

import sys


class Solver(object):
    colors = None
    customers = None
    demands = None
    demand_bits = None
    all_glossy_bits = None
    all_matte_bits = None

    _iterations = 0
    
    def __init__(self, problem):
        self.colors = int(problem.get("colors"))
        self.customers = int(problem.get("customers"))
        self.demands = problem.get("demands")

        self.all_glossy_bits = int(''.join(['0'] * self.colors), 2)
        self.all_matte_bits = int(''.join(['1'] * self.colors), 2)

        self.demand_bits = []
        for c in range(self.customers):
            length = self.demands[c][0]
            demand = self.demands[c][1:]

            customer_gloss = 0
            customer_matte = 0

            for i in range(length):
                (color, matte) = (demand[2 * i], demand[2 * i + 1])
                if matte == 1:
                    customer_matte |= 1 << (self.colors - color)
                else:
                    customer_gloss |= 1 << (self.colors - color)

            customer_request = (customer_gloss, customer_matte)
            self.demand_bits.append(customer_request)
                    
    def solve(self):
        """
        Start solving

        :return: solution string or "IMPOSSIBLE"
        """
        sys.setrecursionlimit(2500)

        solved, solution, best_sum = self.reduce(0, None)

        logging.error("Finished in %s iterations" % self._iterations)

        if solved:
            solution_str = list("{0:b}".format(solution))
            padded_solution = ['0'] * (self.colors - len(solution_str)) + solution_str
            return " ".join(padded_solution[-self.colors:])
        else:
            return "IMPOSSIBLE"
    
    def check(self, solution):
        """
        Check if solution meets all customers' demands

        :param solution:
        :return: bool
        """
        sol_glossy_bits = solution ^ self.all_matte_bits
        sol_matte_bits = solution
        for customer in range(self.customers):
            customer_gloss, customer_matte = self.demand_bits[customer]
            match_gloss = customer_gloss & sol_glossy_bits
            match_matte = customer_matte & sol_matte_bits
            match_any = match_gloss != 0 or match_matte != 0
            if not match_any:
                return False
        return True
        
    def reduce(self, solution_on_stack, change, curr_sum=0, best_sum=None):
        """
        Recursively check possible solutions tree

        :param solution_on_stack: base solution
        :param change: bit to change
        :param curr_sum: current mattes count
        :param best_sum: best mattes count so far
        :return:
        """
        solution = solution_on_stack
        if change is not None:
            solution |= 1 << (self.colors - change - 1)
            curr_sum += 1
            
        if self.check(solution):
            return True, solution, curr_sum
        
        if curr_sum == self.colors:
            return False, None, None

        if best_sum is not None and curr_sum > best_sum:
            return False, None, None
        
        result = None
        solved = False
        for i in range(self.colors):
            if (solution >> (self.colors - i - 1)) % 2 == 0:
                self._iterations += 1
                solved_i, result_i, sum_i = self.reduce(solution, i, curr_sum, best_sum)
                if solved_i:
                    if best_sum is None or sum_i < best_sum:
                        solved = True
                        result = result_i
                        best_sum = sum_i
        return solved, result, best_sum
