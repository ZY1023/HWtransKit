from genericpath import exists
import requests
import json
import os
import sys
import shutil

#搜索并保存网络路径
def webpagesearch(url):
	header = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39',
	}

	resp = requests.get(url=url, headers=header, timeout=3)

	#print(resp.status_code)

	res = resp.content.decode()
	json_data = resp.json()
	lines = []

	for i in json_data['diffs']:
		line = i['statistic']['path']
		lines.append(line)

	url_split1 = url.rsplit('/',1)
	url_split2 = url_split1[0].rsplit('/',1)
	programNum = url_split2[1]
	path_gen = 'D:\path_' + programNum + '.txt'
	with open(path_gen,'w',encoding = 'utf-8') as f:
		for i in lines:
			f.write(i+'\n')
	print("读取的路径已保存到D:\path_%s.txt，共计%s个文件路径" % (programNum,len(lines)))
	#print(lines)

	#测试分割url地址
	# url_split1 = url.rsplit('/',1)
	# url_split2 = url_split1[0].rsplit('/',1)
	# programNum = url_split2[1]
	# path_gen = 'D:\path_' + programNum + '.txt'

	# with open(path_gen,'w',encoding = 'utf-8') as f:
	# 	for i in lines:
	# 		f.write(i+'\n')
	# print("读取的路径已保存到D:\path_%s.txt" % programNum)
	return lines


#将gitee路径转换成Windows可识别路径
def splitPath_Path(lines):
	line_paths = []
	for line in lines:
		if 'README.md' in line:
			line_paths.append(line)
		else:
			line_split = line.rsplit('/',1)
			#print(line_split)
			line_split[0] = eval(repr(line_split[0]).replace('/','\\\\'))
			if "zh-cn" in line_split[0]:
				line_paths.append(line_split[0])
			else:
				print("%s\%s 该路径包含en路径或其他非docs仓路径，不进行复制！" % (line_split[0],line_split[1]))
		
				line_paths = []
	
	return line_paths

#将gitee路径的反斜杠变为“+”，方便后续创建文件夹，直接以splitpath_filename命名
def splitPath_Filename(lines):
	line_paths_filename = []
	for line in lines:
		if 'README.md' in line:
			line = eval(repr(line).replace(r'.','+'))
			line_paths_filename.append(line)
		else:
			line_split = line.rsplit('/',1)
			#print(line_split)
			line_split[0] = eval(repr(line_split[0]).replace('/','\\\\'))
			if "zh-cn" in line_split[0]:
				line_paths_filename.append(eval(repr(line_split[0]).replace(r'\\','+')))
				
	return line_paths_filename

#将gitee路径分离，保存文件名
def splitPath_Docname(lines):
	doc_names = []
	for line in lines:
		if 'README.md' in line:
			doc_names.append(line.strip())
		else:
			line_split = line.rsplit('/',1)
			#print(line_split)
			line_split[0] = eval(repr(line_split[0]).replace('/','\\\\'))
			if "zh-cn" in line_split[0]:
				doc_names.append(line_split[1].strip())
	return doc_names

#将要查询的根目录和gitee路径splitpath_path拼接，生成完成查询路径
def combineSourceDir(str_source_root):
	source_dir = []
	line_paths = splitPath_Path(lines)
	for each in line_paths:
		if 'README.md' in each:
			str_source_dir = str_source_root
			source_dir.append(str_source_dir)
		else:
			str_source_dir = str_source_root + each
			if not os.path.exists(str_source_dir):
				print("%s 该路径不存在！请检查" % str_source_dir)
			else:
				source_dir.append(str_source_dir)
	return source_dir

#将目标根目录和gitee文件名splitpath_filename拼接，生成目标完整路径
def combineTargetDir(str_target_root):
	target_dir = []
	line_paths_filename = splitPath_Filename(lines)
	for each in line_paths_filename:
		if 'README+md' in each:
			str_target_dir = str_target_root
			target_dir.append(str_target_dir)
		else:
			str_target_dir = str_target_root + each
			target_dir.append(str_target_dir)
	return target_dir

def copyFile(source_dir,doc_names,target_dir):
	i = 0
	for a,b,c in zip(source_dir,doc_names,target_dir):
		for dirpath,dirnames,filenames in os.walk(a,topdown=True):
			if b in filenames:
				print("%s 该文件已找到，在以下路径%s" % (b,a))
				if not os.path.exists(c):
					os.makedirs(c)
				try:
					shutil.copy(a+'\\'+b,c)
					print("复制 %s 到 %s 成功" %(a+b,c))
					i= i + 1
				except IOError as e:
					print("Unable to copy file. %s" % e)
					exit(1)
				except:
					print("Unexpected error:",sys.exc_info())
				break
			else:
				print("没有找到该路径下的%s该文件%s, 请确认是否已不存在或分支错误！！" %(a,b))

	print ("共计找到并成功复制%s个文件" % i)


if __name__ == '__main__':

#   print("请输入网络路径文件的路径，如：D:\\en\\path.txt")
#   str = input()
#   fopen = open(str,'r')
#   lines = fopen.readlines()
#   fopen.close()
	while 1:
		print("请输入网址，如：https:/gitte.com/file.json")
		url = input()  
		while True:
			if 'files.json' in url:
				lines = webpagesearch(url)
				###分离gitee路径
				line_paths = splitPath_Path(lines)
				# if line_paths:
				# 	print("这是所有网络的路径")
				# 	print(line_paths)

				###设置目标文件夹名
				line_paths_filenames =splitPath_Filename(lines)
				#print(line_paths_filenames)

				###分离gitee文件名
				doc_names = splitPath_Docname(lines)
				# if doc_names:  
				# 	print("这是所有文件名")
				# 	print(doc_names)

				while True:
					
					if line_paths:
						print("请输入查询原文存放的根目录，如D:\docs\\")
						str_source_root = input()
						temp1 = str_source_root.endswith('\\')
						source_dir = []
						if temp1 == False:
							print('请注意路径末尾需要加\\！')
						# source_dir = combineSourceDir(str_source_root)
                     #############拼接原文查找路径
						# line_paths = splitPath_Path(lines)
						else:
							for each in line_paths:
								if 'README.md' in each:
									str_source_dir = str_source_root
									source_dir.append(str_source_dir)
								else:
									str_source_dir = str_source_root + each
									if not os.path.exists(str_source_dir):
										print("%s\\%s 该路径不存在！请检查" % (str_source_dir))
									else:
										source_dir.append(str_source_dir)		
						while True:
							if source_dir:
					###拼接查找文件路径
							# while True:
							# 	if not os.path.exists(source_dir):
							# 		print("该路径不存在！请检查！")
							# 		str_source_root = input()
							# 		source_dir = combineSourceDir(str_source_root)
								_continue = True
								while _continue:
									print("请输入翻译文档管理的根目录，如D:\\translation\\,如果没有该目录，将会自动创建")
									str_target_root = input()
									temp = str_target_root.endswith('\\')
									i=0
									###拼接目标存放路径
									if temp == False:
										print("请注意路径末尾需要加\\")
									else:
										target_dir = combineTargetDir(str_target_root)
										for a,b,c in zip(source_dir,doc_names,target_dir):
											for dirpath,dirnames,filenames in os.walk(a,topdown=True):
												if b in filenames:
													# print("%s 该文件已找到，在以下路径%s" % (b,a))
													if not os.path.exists(c):
														os.makedirs(c)
													try:
														shutil.copy(a+'\\'+b,c)
														# print("复制 %s 到 %s 成功" %(a+b,c))
														i= i + 1
													except IOError as e:
														print("Unable to copy file. %s" % e)
														exit(1)
													except:
														print("Unexpected error:",sys.exc_info())
													_continue = False
													break
												else:
													print("没有找到该路径下的%s该文件%s, 请确认是否已不存在或分支错误！！" %(a,b))
													print("请输入yes进行分支切换，或输入任意直接忽略！")
													comfirm = input()	
													if "yes" in comfirm:
														print("====================================================\n在切换分支后请重新进行以下操作！按方向键上即可！\n====================================================")
														break
													else:
														_continue = False
														break
								if i!=0:	
									print ("共计找到并成功复制%s个文件" % i)
								input('====================================================\n====================================================\n请按enter继续进行查找！')
								break		
							else:
								print("请重新输入查询原文存放的根目录，如D:\docs\\")
								str_source_root = input()
								source_dir = combineSourceDir(str_source_root)	
							# break
						break
					else:
							print("请再次检查所有路径是否正确！！")
							break
				break
			else:
				print("请注意网页最后是files.json，请重新输入！")
				url = input()

