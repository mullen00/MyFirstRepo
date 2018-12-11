import re
import tkinter as tk
import tkinter.messagebox as msg
import os
import matplotlib.animation
from PIL import ImageTk,Image
import numpy as np
from itertools import count,cycle
import matplotlib.pyplot as plt
import scipy.signal as signal

class GUI_Freqz(tk.Tk):
	def __init__(self):
		super().__init__()

		self.tmp = []
		self.file_path = None

		self.title('系统幅频响应相位特性动态关联作图')
		self.geometry('1200x800')

		self.lb0  = tk.Label(self,text='系统幅频响应相位特性动态关联作图',font=30)
		self.lb0.pack(side=tk.TOP,fill=tk.X)

		self.lb1 = ImageLabel(self, height=500,anchor='nw')
		self.lb1.place(x=400,y=100)

		tk.Label(text='请输入系统的零点:',font=15).place(x=30,y=100)
		self.tx1 = tk.Text(self,width=40,height=2,borderwidth=3)
		self.tx1.place(x=30,y=150)
		tk.Label(text='请输入系统的极点:',font=15).place(x=30,y=200)
		self.tx2 = tk.Text(self, width=40, height=2, borderwidth=3)
		self.tx2.place(x=30, y=250)

		self.button0 = tk.Button(self, text='一键随机', width=30, height=2, command=lambda:self.get_num(self.tmp))
		self.button0.place(x=100, y=300)

		self.button1 = tk.Button(self,text='提交',width=30,height=2,command=self.random)
		self.button1.place(x=100,y=350)

		self.button2 = tk.Button(self,text='生成动态图',width=30,height=2,command=self.draw)
		self.button2.place(x=100,y=400)

		self.zeros = None
		self.polars = None




	def random(self):
		self.tx1.delete(1.0,tk.END)
		self.tx2.delete(1.0,tk.END)
		if len(self.tmp)==2:
			self.zeros = np.random.random_integers(0, 10, self.tmp[0]) if self.tmp[0]!=0 else 0
			self.polars = np.random.random_integers(-10, 1, self.tmp[1]) if self.tmp[1]!=0 else 0
			self.tx1.insert(tk.END, str(self.zeros))
			self.tx2.insert(tk.END, str(self.polars))
	def set_file_name(self):
		path = os.path.join(os.path.abspath('.'),'History')
		title = 'zeros={} polars={}.gif'.format(str(self.zeros),str((self.polars)))
		self.file_path = os.path.join(path,title)



	def get_num(self,tmp):
		sub = sub_window(tmp)
		sub.mainloop()



	def draw(self):
		s1 = self.tx1.get(1.0, tk.END)
		s2 = self.tx2.get(1.0, tk.END)
		self.zeros = np.array([int(i) for i in re.findall('\d+', s1)])
		self.polars = np.array([int(i) for i in re.findall('\d+', s2)])
		print(self.zeros)
		self.set_file_name()
		# try:
		response_draw(self.polars,self.zeros,40,self.file_path)
		self.lb1.load(self.file_path)
		# except:
		# 	print('retry')


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

class sub_window(tk.Toplevel):
	def __init__(self,tmp):
		super().__init__()

		self.num_zeros = None
		self.num_polars = None
		self.tmp = tmp
		self.geometry('400x400')
		tk.Label(self, text='请选择零点个数', font=16, height=3).place(x=10, y=10)
		self.scale_zeros = tk.Scale(self, from_=0, to=10,
							   orient=tk.HORIZONTAL,
							   length=300, showvalue=1, tickinterval=1)
		self.scale_zeros.place(x=10, y=50)

		tk.Label(self, text='请选择极点个数', font=16, height=3).place(x=10, y=130)
		self.scale_polars = tk.Scale(self, from_=0, to=10,
								orient=tk.HORIZONTAL,
								length=300, showvalue=1, tickinterval=1)
		self.scale_polars.place(x=10, y=200)
		tk.Button(self, text='提交', width=20, height=2, command=self.ask).place(x=100, y=280)


	def ask(self):
		answer = msg.askquestion('confirmation', '好的，主人！')
		if answer == 'yes':
			self.tmp.clear()
			self.tmp.append(self.scale_zeros.get())
			self.tmp.append(self.scale_polars.get())
			# print(self.tmp)
			self.destroy()

def response_draw(zeros_x,zeros_y,frame_num,file_name):
	fig = plt.figure()
	fig.figsize=(5,5)
	fig.suptitle('Frequency Response of a random system',fontsize=20)
	co_x = np.poly1d(zeros_x,True).c
	co_y = np.poly1d(zeros_y,True).c

	w,h  = signal.freqz(co_y,co_x,worN=frame_num*10,whole=True)
	print(w.shape,w.max())
	mag = 20*np.log10(abs(h))

	ax1 = plt.subplot2grid((23,10),(1,1),rowspan=9,colspan=9)
	ax1.set_ylabel('Amplitude [dB]',color='b')
	ax1.set_xlim(0,2*np.pi)

	try:
		ax1.set_ylim(mag.min(),mag.max())
	except:
		ax1.set_autoscaley_on(True)

	ax2 = plt.subplot2grid((23,10),(14,1),rowspan=9,colspan=9)
	angle = np.unwrap(np.angle(h,deg=True))
	# angle = np.angle(h, deg=True)
	try:
		ax2.set_xlim(0,2*np.pi)
	except:
		ax2.set_ylim(angle.min(),angle.max())
	# ax2.set_autoscaley_on(True)
	ax2.set_ylabel('Angle (Degree)')
	def draw_frame(i):
		ax2.plot(w[:i], angle[:i],'r-')
		ax1.plot(w[:i], mag[:i],'k-')
		ax1.set_xlabel('Frequency = %f'%w[i])
		ax1.set_title('Response Magnitude = %f dB'%mag[i])
		ax2.set_title('Response Angle = %f '%angle[i])
	def update(i):
		draw_frame(10*i)

	ani = matplotlib.animation.FuncAnimation(fig, update, frames=frame_num, interval=800)
	ani.save(file_name, writer='imagemagick')
	plt.show()

if __name__ == '__main__':
	app = GUI_Freqz()
	app.mainloop()