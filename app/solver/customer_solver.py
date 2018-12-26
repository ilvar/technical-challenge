import logging


class Solver(object):
    colors = None
    customers = None
    demands = None
    mattes = None

    _iterations = 0
    
    def __init__(self, problem):
        self.colors = int(problem.get("colors"))
        self.customers = int(problem.get("customers"))
        self.demands = problem.get("demands")

    def get_customer_data(self, c):
        length = self.demands[c][0]
        demand = self.demands[c][1:]
    
        customer_glosses = []
        customer_matte = None
    
        for i in range(length):
            (color, matte) = (demand[2 * i], demand[2 * i + 1])
        
            if matte == 1:
                customer_matte = color
            else:
                customer_glosses.append(color)
        return customer_glosses, customer_matte

    def solve(self):
        # TODO: Watch out for race conditions! Maybe, make it local and propagate?
        self.mattes = set([])

        any_changes = self.iterate()
        while any_changes and self.mattes is not None:
            any_changes = self.iterate()

        logging.info("Finished in %s iterations" % self._iterations)
    
        if self.mattes is not None:
            colors = ["0"] * self.colors
            for m in self.mattes:
                colors[m - 1] = "1"
            return " ".join(colors)
        else:
            return "IMPOSSIBLE"

    def iterate(self):
        any_changes = False
        for c in range(self.customers):
            customer_glosses, customer_matte = self.get_customer_data(c)
            
            if not self.check(customer_glosses, customer_matte):
                if customer_matte is not None and customer_matte not in self.mattes:
                    self.mattes.add(customer_matte)
                    any_changes = True
                    if not self.check(customer_glosses, customer_matte):
                        self.mattes = None
                        break
                else:
                    self.mattes = None
                    break
        return any_changes
    
    def check(self, customer_glosses, customer_matte):
        """
        Check if customer can be pleased with current setup

        :param customer_glosses: glossy demands
        :param customer_matte: matte demand (or None)
        :return: bool
        """
        if self.mattes is None and len(customer_glosses) > 0:
            return True
        
        matte_fail = customer_matte is None or self.mattes is None or customer_matte not in self.mattes
        gloss_fail = len(customer_glosses) == 0 or all([g in self.mattes for g in customer_glosses])

        self._iterations += len(customer_glosses)
        return not(matte_fail and gloss_fail)
