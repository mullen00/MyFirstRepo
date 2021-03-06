#author: Pan
# the first version
import random
import time,threading

lock = threading.Lock()

class pcb(object):
	def __init__(self, pid, id, priority=1000, need_time=0,used_time=0, status='ready', ppid=0, next=None):
		self.pid = pid
		self.id = id
		self.priority = priority
		self.status = status
		self.ppid = ppid
		self.need_time = need_time
		self.used_time = used_time
		self.next = next
	def __str__(self):
		return 'pid:{},status:{},priority:{}'.format(self.pid,self.status,self.priority)

class table(object):
	def __init__(self,Max_size=None):
		self.root = pcb(0,0,0)
		self.Max_size = Max_size
		self.length = 0
	def __len__(self):
		return self.length
	def iter_pcb(self):
		cur = self.root.next
		while cur:
			yield cur
			cur = cur.next

	def __iter__(self):
		return self.iter_pcb()


	def add_pcb(self,node):
		if self.Max_size and self.length>=self.Max_size:
			return 0
		cur = self.root
		while cur and cur.next:
			cur=cur.next
		cur.next = node
		self.length += 1

	def delete_pcb(self,node):
		cur = self.root.next
		prev = self.root
		while cur and cur.pid!=node.pid:
			prev = cur
			cur = cur.next
		if cur is None:
			return 0
		prev.next = cur.next
		self.length -= 1
		del node
		return 1

	def insert_pcb(self,pid,node):
		if self.Max_size and self.length>=self.Max_size:
			return 0

		prev = self.root
		if len(self)==0:
			self.root.next=node
			self.length += 1
			return 1
		if pid == 0:
			node.next = self.root.next
			self.root.next = node
			self.length += 1
		for item in self:
			if item.pid == pid:
				prev = item
				break
		if prev != self.root:
			node.next = prev.next
			prev.next = node
			self.length += 1
			return 1
		else:return 0

	def get_node_by_pid(self,pid):
		cur = self.root.next
		while cur and cur.pid!=pid:
			cur = cur.next
		return cur if cur else None
	def get_first(self):
		node = self.root.next
		if node:
			self.root.next = node.next
			self.length -= 1
		return node


	def display(self):
		for node in self:
			print(node)

class Ready_Table(table):
	def add_pcb(self,node):
		if node.status == 'ready':
			cur = self.root
			prev = self.root
			while cur and node.priority>=cur.priority:
				prev = cur
				cur = cur.next
			node.next = prev.next
			prev.next = node
			self.length += 1


class Running_Table(table):
	def __init__(self,Max_size=1):
		super().__init__(Max_size)
		self.cur_p = self.root.next

	def clear(self):
		node = self.root.next
		if node:
			del node
			self.length -= 1
		self.root.next = None
		self.cur_p = None
	def add_pcb(self,node):
		self.clear()
		self.cur_p = node
		self.root.next = node

	def display(self):
			with lock:
				if self.cur_p:
					if self.cur_p.used_time<1:
						print('-------------------------')
						print(self.cur_p)
						print('is inserted into running table by force ')
					else:
						print('-------------------------')
						print(self.cur_p)
						print('has been running for ' + str(self.cur_p.used_time) + ' seconds')

	def running(self,ready_t,pause_t):
		while True and (len(ready_t)>0 or len(pause_t)>0):
			while len(pause_t)>0 and self.cur_p is None:
				node = pause_t.get_first()
				if node :
					self.add_pcb(node)
					start = time.time()
					self.cur_p.used_time = int(time.time()-start)
					while self.cur_p.used_time<node.need_time:
						time.sleep(1)
						if self.cur_p is not node:
							node = self.cur_p
							start = time.time()
						self.cur_p.used_time = int(time.time()-start)
						self.display()
					print(self.cur_p,end='---is over\n')
					self.clear()

			while len(ready_t)>0 and self.cur_p is None:
				if len(pause_t)>0:
					break
				node = ready_t.get_first()
				if node :
					self.add_pcb(node)
					start = time.time()
					self.cur_p.used_time = int(time.time()-start)
					while self.cur_p.used_time <self.cur_p.need_time:
						time.sleep(1)
						if self.cur_p is not node:
							node =  self.cur_p
							start = time.time()
						self.cur_p.used_time = int(time.time() - start)
						self.display()
					print(self.cur_p,end='---is over\n')
					self.clear()

	def new_p_by_PSA(self,ready_t, pause_t, new_p):
		if self.cur_p:
			if new_p.priority<self.cur_p.priority:
				self.cur_p.need_time -= self.cur_p.used_time
				pause_t.add_pcb(self.cur_p)
				self.clear()
				self.add_pcb(new_p)
			else:
				ready_t.add_pcb(new_p)
		else:
			self.add_pcb(new_p)

class Block_Table(table):
	def add_pcb(self,node):
		if node.status == 'blocked':
			self.insert_pcb(0,node)

class Pause_Table(table):
	pass

def test():
	l = list(range(3,5))
	k = list(range(3,5))

	random.shuffle(l)
	ready_t = Ready_Table()
	pause_t = Pause_Table()
	for i,j in zip(k,l):
		tmp = pcb(i, i, priority=j, need_time=4)
		ready_t.add_pcb(tmp)
	ready_t.display()
	running_t = Running_Table()
	new_p = pcb(2,2,1,3)
	t1 = threading.Thread(target=running_t.running,args=(ready_t,pause_t),name='running')
	t2 = threading.Thread(target=running_t.new_p_by_PSA,name='PSA',args=(ready_t,pause_t,new_p))
	t1.start()
	time.sleep(1)
	t2.start()
	t1.join()
	t2.join()


if __name__ == '__main__':
	test()