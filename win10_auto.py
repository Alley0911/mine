'''用于下载全球热带气旋的卫星图片'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import time
import os
import shutil
import sys
from datetime import datetime
from datetime import timedelta
import socket


def auto_down(url,filename):
	global per
	try:
		urlretrieve(url,filename,jindu)
		if per < 100:
			print(100/0)
	except Exception as error:
		print(error)
		count = 1
		print(count)
		while count <= 5:
			try:
				urlretrieve(url, filename,jindu)
				if per < 100:
					print(100/0)
				break
			except Exception as error:
				print(error)
				count += 1
				print(count)
		if count > 5:
			print("下载失败")
			if os.path.exists(filename):
				os.remove(filename)
 
#urlretrieve()的回调函数，显示当前的下载进度
#a为已经下载的数据块
#b为数据块大小
#c为远程文件的大小
global myper
def jindu(a,b,c):
	global per
	if not a:
		print("连接打开")
	if c<0:
		print("要下载的文件大小为0")
	else:
		global myper
		per=100*a*b/c
 
		if per>100:
		   per=100
		myper=per
		print("当前下载进度为：" + '%.2f%%' % per)


socket.setdefaulttimeout(30)
sys.setrecursionlimit(1000000000)
while True:
	flag = 0  # 代表无台风生成
	end_dir = "Y:/"  # 目标文件夹
	cur_year = (datetime.now()).year
	cur_mon = (datetime.now()).month
	cur_hour = (datetime.now()).hour
	cur_day = (datetime.now()).day
	cur_min = (datetime.now()).minute
	last_1h_year = (datetime.now()-timedelta(days=1)).year
	last_1h_mon = (datetime.now()-timedelta(days=1)).month
	last_1h_hour = (datetime.now()-timedelta(days=1)).hour
	last_1h_day = (datetime.now()-timedelta(days=1)).day
	last_1h_min = (datetime.now()-timedelta(days=1)).minute
	if 8 <= cur_hour <= 12:
		time_dl = str(cur_year) + str(cur_mon).zfill(2) + str(cur_day).zfill(2) + "0000"
	elif 14 <= cur_hour <= 23:
		time_dl = str(cur_year) + str(cur_mon).zfill(2) + str(cur_day).zfill(2) + "0600"
	fout = open("E:/ssss/worm/"+time_dl+".log_win10",'a')
	sys.stdout = fout
	sys.stderr = fout
	print("-"*100)
	print(datetime.now())
	print("-"*100)
	try:
		html = urlopen("https://rammb-data.cira.colostate.edu/tc_realtime/",timeout=30).read().decode()
		soup = BeautifulSoup(html, features="lxml")
		basin_storms = soup.find_all('a',{'href':re.compile('storm.asp.storm_identifier=(ep|al)\d{6}')})
		if basin_storms:
			for i in basin_storms:
				print("*"*50)
				a = (i.get_text())
				print((a.split('\n')[0]))
				id = a.split(" ")[0][2:4]  # 获取编号如04、99，当编号大于40时认为是扰动无需下载
				name = (a.split('\n')[0]).split()[-1]
				print(name)
				if int(id) < 40:
					# print("There is tc")
					grade = a.split(" ")[2] + a.split(" ")[3]
					flag = 1 # 1标记有tc需要下载，并且已下载完成，当后续检测不到需下载的文件时，会变为-1
					id_all = a.split(" ")[0]  # 完整的编号 al072020
					print(id_all+"需要下载")
					basin = a.split(" ")[0][0:2]  # 获取海域名称al、ep
					add = "https://rammb-data.cira.colostate.edu/tc_realtime/products/storms/" + \
							"2020"+ str.lower(str(basin))+ str(id) + '/4kmirimg/' + \
								"2020"+ str.lower(str(basin))+ str(id) + '_4kmirimg_' + time_dl + ".gif"

					name_img = name + "_2020"+ str.lower(str(basin))+ str(id) + '_4kmirimg_' + time_dl + ".gif"
					file_adr = 'E:/ssss/worm/'+ name_img  # 文件下载的位置加文件名称
					if os.path.exists(file_adr):
						print(file_adr + "已经存在无需下载")
						pass
					else:
						try:
							auto_down(add, file_adr)
						except Exception as f:
							if cur_min >=45 or cur_hour ==9 or cur_hour == 15:
								for i in range(1,10):
									try:
										add = "https://rammb-data.cira.colostate.edu/tc_realtime/products/storms/" + \
												"2020"+ str.lower(str(basin))+ str(id) + '/4kmirimg/' + \
													"2020"+ str.lower(str(basin))+ str(id) + '_4kmirimg_' + time_dl + ".gif"

										name_img = name + "_2020"+ str.lower(str(basin))+ str(id) + '_4kmirimg_' + time_dl + ".gif"
										file_adr = 'E:/ssss/worm/'+ name_img  # 文件下载的位置加文件名称									
										add_s = list(add)
										add_s[-5] = str(i)
										add = ''.join(add_s)	
										file_adr_s = list(file_adr)
										file_adr_s[-5] = str(i)
										file_adr = ''.join(file_adr_s)
										name_img = file_adr.split('\\')[-1]											
										auto_down(add, file_adr)
										break
									except :
										try:
											n = 10 - i 
											if 8 <= cur_hour <= 12:
												time_dl_new = str(last_1h_year) + str(last_1h_mon).zfill(2) + str(last_1h_day).zfill(2) + "235" + str(n)
											elif 14 <= cur_hour <= 23:
												time_dl_new = str(cur_year) + str(cur_mon).zfill(2) + str(cur_day).zfill(2) + "055" + str(n)										
											add = "https://rammb-data.cira.colostate.edu/tc_realtime/products/storms/" + \
													"2020"+ str.lower(str(basin))+ str(id) + '/4kmirimg/' + \
														"2020"+ str.lower(str(basin))+ str(id) + '_4kmirimg_' + time_dl_new + ".gif"

											name_img = name + "_2020"+ str.lower(str(basin))+ str(id) + '_4kmirimg_' + time_dl_new + ".gif"
											file_adr = 'E:/ssss/worm/'+ name_img  # 文件下载的位置加文件名称
											if os.path.exists(file_adr):
												print(file_adr + "已经存在无需下载")
												break
											else:
												try:
													auto_down(add, file_adr)
													break
												except :
													pass
										except :								
											pass	

					name_tmp = file_adr.split('/')[-1]
					if os.path.exists(file_adr) and os.path.getsize(file_adr) > 102400:
						try:
							shutil.copy(file_adr, end_dir)
							time.sleep(5)
							if os.path.exists(end_dir + "/" + name_tmp):
								print(name_tmp + "已经复制到指定文件夹")
							else:
								print("文件存在但未复制到指定文件夹")
								flag = -1  # 未复制成功说明对需要下载的文件未能下载成功
						except:
							pass
					else:
						print("文件不存在或太小，需要重新下载")
						flag = -1
		print('@'*50)
		if flag == 0:
			print('无台风需要下载')
		elif flag == 1:
			print('本次爬虫，下载完成')
		elif flag == -1:
			print('本次爬虫，存在下载失败文件')

		if (cur_hour == 9 and cur_min >= 20) or (cur_hour == 15 and cur_min >= 20):
			print("结束")
			print("%"*100)
			fout.close()
			break
		else:
			fout.close() 
	except Exception as error:
		print(error)
		fout.close()
	time.sleep(100)