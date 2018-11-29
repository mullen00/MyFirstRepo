import tkinter as tk
from PCB_PSA import *
import threading

class GUI_PCB(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('PCB management by PSA')
		self.geometry('800x1200')

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
		tk.Button(self,text='Start',height=2,width=15,command=self.show_running).place(x=290,y=220)
		tk.Button(self,text='Insert',height=2,width=15,command=self.insert_process).place(x=430,y=220)

		tk.Label(self,text='the inserted Process :',font=20).place(x=10,y=300)
		self.running_tx = tk.Label(self,text='None',height=2,width=60,font=26,bg='white')
		self.running_tx.place(x=20,y=350)

		tk.Label(self,text='Processes in Ready Table:',font=20).place(x=10,y=400)
		self.tx = tk.Text(self,height=10,width=60,font=16)
		self.tx.place(x=20,y=450)

		tk.Label(self,text='System log:',font=20).place(x=650,y=150)
		self.log = tk.Text(self,height=25,width=60,font=16)
		self.log.place(x=650,y=200)




	def creat_running_t(self):
		if len(self.ready_t)==0:
			num = self.scale.get()
			l = list(range(5,num+5))
			k = list(range(5, num+5))
			random.shuffle(l)
			for i, j in zip(k, l):
				tmp = pcb(i, i, priority=j, need_time=2)
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
		self.running_t.running(self.ready_t,self.pause_t)
		self.log.insert(1.0,self.running_t.log)
	def insert_process(self):
		new_p = pcb(1,1,3,4)
		self.running_tx.config(text=str(new_p))
		t1 = threading.Thread(target=self.running_t.running,args=(self.ready_t,self.pause_t))
		t2 = threading.Thread(target=self.running_t.new_p_by_PSA,args=(self.ready_t,self.pause_t,new_p))
		t1.start()
		t2.start()
		t1.join()
		t2.join()
		self.log.insert(1.0,self.running_t.log)
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
