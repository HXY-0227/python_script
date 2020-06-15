class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        arr = s.rstrip().split(' ')
        if len(arr) > 0:
            return len(arr[-1])
        else:
            return 0

if __name__ == "__main__":
    solution = Solution()
    result = solution.lengthOfLastWord('a ')
    print(result)