class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str

        其他优秀方案
        return ' '.join(map(lambda x: x[::-1], s.split()))
        """
        result = []
        for word in s.split(' '):
            result.append(word[::-1])

        return ' '.join(result)

if __name__ == "__main__":
    solution = Solution()
    result = solution.reverseWords("Let's take LeetCode contest")
    print(result)