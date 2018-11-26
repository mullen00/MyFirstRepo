# **4 Sum**
## [Leetcode 第18题](https://leetcode.com/problems/4sum/description/)
### *具体描述*
--------
>>Given an array nums of n integers and an integer target, are there elements a, b, c, and d in nums such that a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target.

--------------
### *解题思路*
+ 为节省时间开销，需要额外的空间存储前面的结果
   + 优先考虑哈希表存储，python对应的结构选择字典
+ LeetCode第一题: [**2 Sum**](https://leetcode.com/problems/two-sum/description/)，可将此题转换至同一类型
   +启发：可一次存储任意两个数的和作为字典的key，两个数的index作为value
   +为便于后面去重，可将两个数的index保存在一个集合中
+ 开始撸代码
(```)
	class Solution:
	    def fourSum(self, nums, target):
	        """
	        :type nums: List[int]
	        :type target: int
	        :rtype: List[List[int]]
	        """
	        if len(nums)<4:
	            return []
	        res = dict()
	        d = dict()
	        size = len(nums)
	        for i in range(size):
	            for j in range(i+1):
	                s = nums[i]+nums[j]
	                if d.get(s) is None:
	                    d[s] = []
	                d[s].append({i,j})
	        s = d.keys()
	        for i in s:
	            j = target - i
	            tmp1 = d.get(i)
	            tmp2 = d.get(j)
	            if tmp2:
	                for k in tmp1:
	                    for h in tmp2:
	                        tmp3 = k^h
	                        if len(tmp3)==4:
	                            tmp4=[]
	                            for i in tmp3:
	                                tmp4.append(nums[i])
	                            tmp4 = sorted(tmp4)
	                            res[tuple(tmp4)]=1
	        return list(res.keys())              
(```)
-----------
```flow
st=>start: 第一次使用Markdown
op=>operation: Markdown 真好用
cond=>condition: 真的吗？
e=>end:没错
st->op->cond
cond(yes)->e
cond(no)->op
&```
