class A:
    def test(self):
        print("A")

class B(A):
    def print(self):
        self.test()

    # def test(self):
    #     print("B")

B().print()