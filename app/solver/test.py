import unittest
import paint_solver



class GenericSolverTest(unittest.TestCase):
    def convert_and_call(self, solver_klass, color, customers, demand):
        solver = solver_klass({"colors": color, "customers": customers, "demands": demand})
        return solver.solve()


class PaintshopTest(GenericSolverTest):
    def test_impossible(self):
        demand = [[1, 1, 0], [1, 1, 1]]
        self.assertEqual(self.convert_and_call(paint_solver.Solver, 1, 2, demand), "IMPOSSIBLE")

    def test_no_matte(self):
        demand = [[1, 1, 0], [1, 2, 0]]
        self.assertEqual(self.convert_and_call(paint_solver.Solver, 2, 2, demand), "0 0")

    def test_all_matte(self):
        demand = [[1, 1, 1], [2, 1, 0, 2, 1], [3, 1, 0, 2, 0, 3, 1]]
        self.assertEqual(self.convert_and_call(paint_solver.Solver, 3, 3, demand), "1 1 1")

    def test_color_not_requested(self):
        demand = [[1, 5, 1], [2, 1, 0, 2, 1]]
        self.assertEqual(self.convert_and_call(paint_solver.Solver, 5, 2, demand), "0 0 0 0 1")

if __name__ == "__main__":
     unittest.main()
