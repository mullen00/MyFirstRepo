import tkinter as tk
#author: Pan

import random
import time,threading
import tkinter.messagebox as msg


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
		return 'pid:{},  status:{},  priority:{},  need_time:{}'.format(self.pid,self.status,self.priority,self.need_time)

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
		self.log = 'logging\n'


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
					res = ''
					if self.cur_p.used_time<1:
						res = '-------------------------\n'\
						      +str(self.cur_p)+'\n'\
							  +'is inserted into running table by force \n'
					else:
						res = '-------------------------\n' \
							  + str(self.cur_p)+'\n' \
							  +'has been running for ' + str(self.cur_p.used_time) + ' seconds\n'
					return res

	def running(self,ready_t,pause_t):
		while True and ((len(ready_t)>0 or len(pause_t)>0) or self.cur_p):
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

						log = self.display()
						self.log += log
						print(log)

					log = str(self.cur_p) + '---- over\n'
					print(log)
					self.log += log
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
						log = self.display()
						print(log)
						self.log += log
					log = 'process with pid=' + str(self.cur_p.pid) + '-' * 15 + 'over\n'
					print(log)
					self.log += log
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
		tmp = pcb(i, i, priority=j, need_time=2)
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


class GUI_PCB(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('PCB management by PSA')
		self.geometry('1200x800')

		self.ready_t = Ready_Table()
		self.running_t = Running_Table()
		self.pause_t = Pause_Table()
		self.status = tk.StringVar()

		self.status.set('None')
		tk.Label(self,text='Priority Scheming Algorithm Implementation'
				 ,font=25,height=3).pack(side=tk.TOP,fill=tk.X)
		tk.Label(self,text='Please select the number of process initially:',font=16,height=3).place(x=10,y=100)
		self.scale = tk.Scale(self, from_=0, to=20,
							  orient=tk.HORIZONTAL,
							  length=500, showvalue=1, tickinterval=1)
		self.scale.place(x=10,y=150)
		tk.Button(self,text='Submit',height=2,width=15,command=self.creat_running_t).place(x=10,y=220)
		tk.Button(self,text='Reset',height=2,width=15,command=self.reset).place(x=150,y=220)
		tk.Button(self,text='Normal-Running',height=2,width=15,command=self.show_running).place(x=290,y=220)
		tk.Button(self,text='PSA-Running',height=2,width=15,command=self.insert_process).place(x=430,y=220)

		tk.Label(self,text='the inserted Process :',font=20).place(x=10,y=300)
		self.running_tx = tk.Label(self,text='None',height=2,width=60,font=26,bg='white')
		self.running_tx.place(x=20,y=350)

		tk.Label(self,text='Processes in Ready Table:',font=20).place(x=10,y=400)
		self.tx = tk.Text(self,height=10,width=60,font=16)
		self.tx.place(x=20,y=450)

		tk.Label(self,text='System log:',font=20).place(x=650,y=150)
		self.log = tk.Text(self,height=25,width=60,font=16)
		self.log.place(x=650,y=200)

		tk.Label(self,text='Github:mullen00',font=24,bg='red').place(x=1000,y=100)





	def creat_running_t(self):
		if len(self.ready_t)==0:
			num = self.scale.get()
			l = list(range(5,num+5))
			k = list(range(5, num+5))
			random.shuffle(l)
			for i, j in zip(k, l):
				tmp = pcb(i, i, priority=j, need_time=random.randint(1,5))
				self.ready_t.add_pcb(tmp)
		self.show_process()

	def show_process(self):
		self.tx.delete(1.0,tk.END)
		for node in self.ready_t:
			self.tx.insert(tk.END,str(node)+'\n')
	def sort_by_pid(self):
		self.tx.delete(1.0,tk.END)
		tmp = {}
		for node in self.ready_t:
			tmp[node.pid]=node
		for i in sorted(list(tmp.keys())):
			node = tmp.get(i)
			self.tx.insert(tk.END,str(node)+'\n')
	def show_running(self):
		answer = msg.askquestion('confirmation', '请观察后台进程运行情况')
		if answer == 'yes':
			t1 = threading.Thread(target=self.running_t.running,args=(self.ready_t,self.pause_t))
			t1.start()
			t1.join()
			# self.running_t.running(self.ready_t,self.pause_t)
			self.log.insert(1.0,self.running_t.log)


	def insert_process(self):
		answer = msg.askquestion('confirmation', '请在后台输入相关信息')
		if answer == 'yes':

			p,t,need_time= self.get_new_p()
			new_p = pcb(1,1,p,need_time)
			print('System is starting....')
			self.running_tx.config(text=str(new_p))
			time.sleep(1)
			t1 = threading.Thread(target=self.running_t.running,args=(self.ready_t,self.pause_t))
			t2 = threading.Thread(target=self.running_t.new_p_by_PSA,args=(self.ready_t,self.pause_t,new_p))
			t1.start()
			time.sleep(t)

			t2.start()
			t1.join()
			t2.join()
			self.log.insert(1.0,self.running_t.log)

	def get_new_p(self):
		"pid, id, priority=1000, need_time=0"
		p = input('请输入new_process的优先级，数字1的优先级最高:\n')
		need_time = input('请输入new_process的运行时间(单位：秒):\n')
		t = input('请输入插入进程新时间点(例：在其他进程运行3秒之后插入，则输入 3):\n')
		while not p.isdigit():
			p = input('请重新输入new_process的优先级，数字1的优先级最高:\n')
		while not t.isdigit():
			t = input('请重新输入插入新进程时间点(例：在运行3秒之后插入，则输入 3):\n')
		while not need_time.isdigit():
			need_time = input('请重新输入new_process的运行时间(单位：秒):\n')


		return int(p),int(t),int(need_time)


	def reset(self):
		self.ready_t = Ready_Table()
		self.running_t = Running_Table()
		self.pause_t = Pause_Table()
		self.status.set('-------')

		self.running_tx.config(text=self.status)
		self.tx.delete(1.0,tk.END)
		self.log.delete(1.0,tk.END)



if __name__ == '__main__':
	app = GUI_PCB()
	app.mainloop()
