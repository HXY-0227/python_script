class Solution:
    def fib(self, N: int) -> int:
        if N <= 1:
            return N
        return self.fib(N - 1) + self.fib(N - 2)

if __name__ == "__main__":
    solution = Solution()
    print(solution.fib(3))