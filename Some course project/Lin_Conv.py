import tkinter as tk
import tkinter.messagebox as msg
from PIL import ImageTk,Image
import numpy as np
from itertools import count,cycle
import matplotlib.animation
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
import re



class GUI_Lin_Conv(tk.Tk):
	def __init__(self):
		super().__init__()

		self.title('linear convolution animation')
		self.geometry('1200x800')

		self.lb0  = tk.Label(self,text='Animation of Linear Convolution',font=30)
		self.lb0.pack(side=tk.TOP,fill=tk.X)

		self.lb1 = ImageLabel(self, height=500,anchor='nw')
		self.lb1.place(x=400,y=100)

		tk.Label(text='Input sequence 1:',font=15).place(x=30,y=100)
		self.tx1 = tk.Text(self,width=40,height=2,borderwidth=3)
		self.tx1.place(x=30,y=150)
		tk.Label(text='Input sequence 2:',font=15).place(x=30,y=200)
		self.tx2 = tk.Text(self, width=40, height=2, borderwidth=3)
		self.tx2.place(x=30, y=250)

		self.button0 = tk.Button(self, text='一键随机生成序列', width=30, height=2, command=self.random)
		self.button0.place(x=100, y=300)

		self.button1 = tk.Button(self,text='提交',width=30,height=2,command=self.ask)
		self.button1.place(x=100,y=350)

		self.button2 = tk.Button(self,text='生成动态图',width=30,height=2,command=self.draw)
		self.button2.place(x=100,y=400)

		self.conv = ''
		self.seq1 = np.zeros(10)
		self.seq2 = np.zeros(10)
		self.tx3 = tk.Text(self,font=20, height=10, width=30,borderwidth=3)
		self.tx3.place(x=20, y=500)



	def random(self):
		self.tx1.delete(1.0,tk.END)
		self.tx2.delete(1.0,tk.END)

		def seq():
			txt = str(np.random.random_integers(0,10,10))
			txt = txt[1:-1].split(' ')
			seq = ''
			for i in txt:
				if not seq:
					seq=str(i)
				elif i:
					seq += ','+str(i)
			return seq

		self.tx1.insert(tk.END,seq())
		self.tx2.insert(tk.END,seq())

	def ask(self):
		answer=msg.askquestion('confirmation','convolution immediately?')
		if answer=='yes':
			self.get_seq()
		else:
			self.quit()

	def get_seq(self):
		var1 = self.tx1.get(1.0,tk.END).strip().split(',')
		var2 = self.tx2.get(1.0,tk.END).strip().split(',')
		print(var2,var1)
		self.tx3.delete(1.0,tk.END)

		self.seq1=np.array([int(i) for i in var1],dtype='int')
		self.seq2=np.array([int(i) for i in var2],dtype='int')

		self.conv=str(np.convolve(self.seq1,self.seq2,'full'))
		re.sub(' {1-10}',',',self.conv)
		txt = 'convolution sum is :\n'+re.sub(' {1,20}',',',self.conv[2:-1]).replace('\n','')

		print(re.sub(' {1,20}',',',self.conv).replace('\n',''))
		self.tx3.insert(tk.END,txt)

	def draw(self):
		lin_conv(self.seq1,self.seq2)
		self.lb1.load("random.gif")


class ImageLabel(tk.Label):
	def load(self, im):
		if isinstance(im, str):
			im = Image.open(im)
		frames = []

		try:
			for i in count(1):
				frames.append(ImageTk.PhotoImage(im.copy()))
				im.seek(i)
		except EOFError:
			pass
		self.frames = cycle(frames)

		try:
			self.delay = im.info['duration']
		except:
			self.delay = 100

		if len(frames) == 1:
			self.config(image=next(self.frames))
		else:
			self.next_frame()

	def unload(self):
		self.config(image=None)
		self.frames = None

	def next_frame(self):
		if self.frames:
			self.config(image=next(self.frames))
			self.after(self.delay, self.next_frame)
def lin_conv(L1,L2):
	fig = plt.figure(1)
	# L1 = np.random.random_integers(0, 10, 10)
	# L2 = np.random.random_integers(0, 10, 8)
	L3 = np.convolve(L1,L2,'full')
	max_l1 = max(L1)
	max_l2 = max(L2)
	max_l3 = max(L3)
	min_l1 = min(L1) if min(L1)<0 else 0
	min_l2 = min(L2) if min(L2)<0 else 0
	min_l3 = min(L3) if min(L3)<0 else 0
	M_len=max(len(L1),len(L2))
	temp = L2[::-1]
	gs = grid.GridSpec(2,3,figure=fig)
	ax1 = fig.add_subplot(gs[0,:2])
	ax2 = fig.add_subplot(gs[0,2])
	ax = fig.add_subplot(gs[1,:])

	def draw_first_step(i):

		if i < len(L1) and i > 0:
			ax1.cla()
			ax1.set_title("drawing sequence 1")
			ax1.set_ylim(min_l1,max_l1)
			ax1.set_xlim(0,M_len+2)
			ax1.stem(L1[:i], linefmt='r-.', markerfmt='ro', basefmt='k-')
		if i < len(L2) and i > 0:
			ax2.cla()
			ax2.set_title('drawing sequence 2')
			ax2.set_xlim(0,len(L2)+2)
			ax2.set_ylim(min_l2,max_l2+2)
			ax2.stem(L2[:i], linefmt='r-.', markerfmt='ro',basefmt='k-')

	def draw_second_step(i):
		ax2.set_title('seq_2 completed')
		ax1.cla()
		ax1.set_title("moving anti-seq_2 towards seq_1")
		ax1.set_xlim(-M_len,2*M_len+2)
		ax1.set_ylim(min_l1,max(max_l1,max_l2)+2)
		x_range = np.arange(i-len(L2),i)
		ax1.stem(x_range,temp,linefmt='k-', markerfmt='ko')
		ax1.stem(np.arange(0,len(L1)),L1,linefmt='r-.', markerfmt='ro')

		ax.set_ylim(min_l3, max_l3)
		ax.set_xlim(0,len(L1)+len(L2)+3)
		ax.set_xlabel('the convolution sum under computing')
		if i>0 and i<len(L3):
			ax.stem(L3[:i],linefmt='r-', markerfmt='ro')

	def init():
		ax1.set_ylim(0,max_l1)
		ax2.set_ylim(0,max_l2)
		ax.cla()

	def anima(i):
		if i < M_len:
			draw_first_step(i)
		elif i<M_len*3:
			draw_second_step(i-M_len)

	anim  = matplotlib.animation.FuncAnimation(
		fig,anima,init_func=init,frames=3*M_len,interval=1000)
	anim.save('random.gif',writer='imagemagick')


if __name__ == '__main__':
	app = GUI_Lin_Conv()
	app.mainloop()
