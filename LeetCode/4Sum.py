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
