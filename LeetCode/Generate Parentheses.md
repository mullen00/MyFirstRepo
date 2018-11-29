# Generate Parenthese
## [LeetCode 22](https://leetcode.com/problems/generate-parentheses/description/)
>Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

>>For example, given n = 3, a solution set is:
 [
  "((()))",
  "(()())",
  "(())()",
  "()(())",
  "()()()"
 ]

--------------
I refer to some geniuses ,they some used recursion by add another function,some just expand the function to a recursion form. I appreciate them, and after digesting one artful algorithm, I rewrote it as follows:
```python
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
```
