#-*- coding: utf-8 -*-
import matplotlib.font_manager
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
font = matplotlib.font_manager.FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)


def lin_conv():
	l1 = np.random.random_integers(0,10,10)
	l2 = np.random.random_integers(0,10,8)
	l3 = np.convolve(l1,l2,'full')

	max_len = max(len(l2),len(l1))
	min_len = min(len(l1),len(l2))
	total = max_len+min_len

	max_l1 = max(l1)
	max_l2 = max(l2)
	max_l3 = max(l3)
	fig_1,ax= plt.subplots(3,1)

	x1_num = min_len+total-1
	x2_num = 2*min_len - 1
	x3_num = total- 1

	x1_range = (-min_len+1,total)
	x2_range = (-min_len+1,min_len)
	x3_range = (0,total-1)

	y1 = np.zeros(x1_num)
	y2 = np.zeros(x2_num)
	y3 = np.zeros(x3_num)


	def reset_axes(i):
		ax[0].set_xlim(-total,total)
		ax[1].set_xlim(-total,total)
		ax[2].set_xlim(0,total)
		


		if int(i/max_len)<3:
			ax[0].set_ylim(0,int(max_l1*2))
			ax[0].set_ylabel('序列大小',fontproperties=font)
			ax[1].set_ylabel('序列大小',fontproperties=font)
			ax[2].set_ylabel('序列大小',fontproperties=font)
			if int(i / max_len) == 0:
				ax[0].set_title('正在绘制序列1',fontproperties=font)
				ax[1].set_title('正在绘制序列2',fontproperties=font)
			if int(i / max_len) == 1:
				ax[0].set_title('序列1已绘制完成',fontproperties=font)
				ax[1].set_title('正在绘制序列2的Y轴对称序列',fontproperties=font)
			if int(i / max_len) == 2:
				ax[0].set_title('正在将序列2的反对称序列搬移至序列同轴',fontproperties=font)
				ax[1].set_title('序列2以绘制完成',fontproperties=font)


		if int(i / max_len) >= 3:
			ax[0].set_ylim(0, int(max_l1*10))
			ax[0].set_ylabel('x1[m]*x2[n-m]')
			ax[1].set_ylabel('序列大小',fontproperties=font)
			ax[2].set_ylabel('h[n]')

			if int(i / max_len) == 3:
				ax[0].set_title('序列2的反对称序列正在向序列1移动',fontproperties=font)
				ax[1].set_title('序列2的对称序列绘制完成',fontproperties=font)
				ax[2].set_title('对应卷积计算中',fontproperties=font)
			if int(i / max_len) == 4:
				ax[0].set_title('序列2的反对称序列正在序列1的内部移动',fontproperties=font)
				ax[1].set_title('序列2的对称序列绘制完成',fontproperties=font)
				ax[2].set_title('对应卷积计算中',fontproperties=font)
			if int(i / max_len) == 5:
				ax[0].set_title('序列2的反对称序列正在逐渐远离序列1',fontproperties=font)
				ax[1].set_title('序列2的对称序列绘制完成',fontproperties=font)
				ax[2].set_title('对应卷积计算中',fontproperties=font)


		ax[1].set_ylim(0,int(max_l2*2))
		ax[2].set_ylim(0,max_l3+40)
		ax[0].stem(np.arange(x1_range[0], x1_range[1]), y1, 'r-')
		ax[1].stem(np.arange(x2_range[0], x2_range[1]), y2, 'r-')
		ax[2].stem(np.arange(x3_range[0], x3_range[1]), y3, 'r-')

	def init():
		reset_axes(1)


	def animate_1(i, y1, y2,y3):
		delta = i%max_len
		if i < max_len:
			y1[delta+min_len-1] = l1[delta]
			if delta<min_len:
				y2[delta+min_len-1] = l2[delta]
		elif i< 2*max_len:
			if delta<=min_len-1:
				if delta<min_len-1:
					y2[min_len+delta] = 0
				y2[min_len-1-delta] = l2[delta]
				ax[1].cla()
		elif i<3*max_len:
			if delta == 0:
				y1[min_len - 1] = l2[0]+l1[0]
			elif delta<=min_len-1:
				y1[min_len-1-delta] = l2[delta]

		elif i<4*max_len:
			if delta<min_len:
				if delta == 0:
					pass
				else:
					y1[min_len-1:min_len+delta] = l1[:delta+1]*l2[:delta+1]
					if delta < min_len - 1:
						y1[delta:min_len-1] = y1[0:min_len-1-delta]
						y1[delta-1] = 0
				y3[delta] = sum(y1[min_len-1:min_len+delta])
		elif i<5*max_len:
			if delta<=max_len-min_len:
				y1[min_len-1+delta:2*min_len-2+delta+1] = l1[delta:min_len+delta] * l2[:]
				y3[delta+min_len] = sum(y1[min_len-1+delta:2*min_len-2+delta+1])

		elif i<6*max_len:
			if delta < min_len-1:
				y1[max_len+1+delta:total-1] = l2[delta:min_len-2]*l1[delta+2:min_len]
				if max_len+delta+1<total-1:
					y3[max_len+delta+1] = sum(y1[max_len+1+delta:total-1])

		ax[0].cla()
		reset_axes(i)








	ani = animation.FuncAnimation(fig_1,animate_1,60,init,fargs=(y1,y2,y3), interval=800)
	writer = FFMpegWriter(fps=1, metadata=dict(artist='Me'), bitrate=1800)
	ani.save("movie.mp4", writer=writer)

	# fig_2,ax_2= plt.subplots(1,1)
	# con_len = len(l1)+len(l2)
	# ax_2.set_xlim(-1,con_len)
	# ax_2.set_ylim(0,300)
	# ax_2.stem(np.arange(len(l3)),np.zeros_like(l3))





	init()
	plt.show()

	# plt.setp(axes[0].get_xticklabels(),fontsize=6)
	# axes[1].stem(l2)
	# axes[2].stem(l3)
	# plt.show()
lin_conv()

