class Solution:
    """
    递归算法实现
    """
    def fib1(self, N: int) -> int:
        if N <= 1:
            return N
        return self.fib1(N - 1) + self.fib1(N - 2)
    
    """
    通过数组的方式去实现
    """
    def fib(self, N: int) -> int:
        if N <= 1:
            return N
        return self.memoize(N)
        
    
    def memoize(self, N: int) -> {}:
        cache = {0:0, 1:1}
        for i in range(2, N + 1):
            cache[i] = cache[i - 1] + cache[i - 2]
        return cache[N]

if __name__ == "__main__":
    solution = Solution()
    print(solution.fib(3))