class Solution:
    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        if n == 0:
            return []
        if n == 1:
            return ['()']
        prev = self.generateParenthesis(n-1)
        res = set()
        for s in prev:
            for i in range(len(s)):
                res.add(s[:i]+'()'+s[i:])
        return list(res)
                    