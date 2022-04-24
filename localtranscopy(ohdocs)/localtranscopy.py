from genericpath import exists
from pkg_resources import EGG_DIST
import json
import os
import sys
import shutil


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
				line_paths.append(eval(repr(line_split[0]).replace('zh-cn','')))
			else:
				# print("%s 该路径是en路径或非docs仓路径，请注意" % line_split[0])
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

#将要查询的根目录和生成的文件夹名splitPath_Filename拼接，生成完成查询路径
def combineSourceDir(str_source_root):
	source_dir = []
	line_path_filenames = splitPath_Filename(lines)
	for each in line_path_filenames:
		if 'README+md' in each:
			str_source_dir = str_source_root
			if not os.path.exists(str_source_dir):
				print("%s 该路径不存在！请检查" % str_source_dir)
			else:
				source_dir.append(str_source_dir)
		else:
			str_source_dir = str_source_root + each
			if not os.path.exists(str_source_dir):
				print("%s 该路径不存在！请检查" % str_source_dir)
			else:
				source_dir.append(str_source_dir)
	return source_dir

#将目标根目录和gitee路径splitPath_Path拼接，生成目标完整路径
def combineTargetDir(str_target_root):
	target_dir = []
	line_paths = splitPath_Path(lines)
	for each in line_paths:
		if 'README.md' in each:
			str_target_dir = str_target_root
			if not os.path.exists(str_target_dir):
				print("%s 没有该路径！请检查是否正确" % str_target_dir)
			else:
				target_dir.append(str_target_dir)
		else:
			str_target_dir = str_target_root + each
			if not os.path.exists(str_target_dir):
				print("%s 没有该路径！请检查是否正确" % str_target_dir)
			else:
				target_dir.append(str_target_dir)
	return target_dir

def copyFile(source_dir,doc_names,target_dir):
	for a,b,c in zip(source_dir,doc_names,target_dir):
		for dirpath,dirnames,filenames in os.walk(a,topdown=True):
			if b in filenames:
				# print("%s 该文件已找到，在以下路径%s" % (b,a))
				if not os.path.exists(c):
					os.makedirs(c)
				try:
					shutil.copy(a+'\\'+b,c)
					# print("复制 %s 到 %s 成功" %(a+b,c))
				except IOError as e:
					print("Unable to copy file. %s" % e)
					exit(1)
				except:
					print("Unexpected error:",sys.exc_info())
				break
			else:
				print("没有找到该文件%s, 请确认是否已不存在" %b)
				


if __name__ == '__main__':

	while 1:
		print("请输入网络路径文件的路径，如：D:\\path_编号.txt")
		str = input()
		while True:
			if '.txt' in str:
				if os.path.exists(str):
					print('====================================================\npath文档加载成功！')
					fopen = open(str,'r',encoding='utf-8')
					lines = fopen.readlines()
					# print(lines)
					fopen.close()
					

					###分离gitee路径
					line_paths = splitPath_Path(lines)
					# print("这是所有网络的路径")
					# print(line_paths)

					###设置目标文件夹名
					line_paths_filenames =splitPath_Filename(lines)
					# print(line_paths_filenames)

					###分离gitee文件名
					doc_names = splitPath_Docname(lines)
					# print("这是所有文件名")
					# print(doc_names)

					print("请输入译文存放的根目录，如D:\\trans\\en\\")
					str_source_root = input()
					temp1 = str_source_root.endswith('\\')
					i = 0
					ih = 0
					source_dir = []
					if temp1 == False:
						print("请注意路径末尾以\\结尾！")
					###拼接查找文件路径 
					# source_dir = combineSourceDir(str_source_root)
					# line_path_filenames = splitPath_Filename(lines)
					else:
						for each in line_paths_filenames:
							if 'README+md' in each:
								str_source_dir = str_source_root
								if not os.path.exists(str_source_dir):
									i = i+1
								else:
									ih = ih +1
									source_dir.append(str_source_dir)
							else:
								str_source_dir = str_source_root + each
								if not os.path.exists(str_source_dir):
									i = i + 1
								else:
									ih = ih + 1
									source_dir.append(str_source_dir)
					if i != 0 & ih !=0:
						print("====================================================\n该路径%s输入错误\n====================================================\n"% str_source_root)					
					# print(source_dir)


					while True:
						s = 0
						if source_dir:
							print("请输入译文粘贴的根目录，如D:\docs\\en\\")
							str_target_root = input()
							temp = str_target_root.endswith('\\')
							t = 0
							th = 0
							target_dir = []
							if temp == False:
								print("请注意路径最后以\\结尾！")
							###拼接目标存放路径
							# target_dir = combineTargetDir(str_target_root)
							else:
								for each in line_paths:
									if 'README.md' in each:
										str_target_dir = str_target_root
										if not os.path.exists(str_target_dir):
											t = t +1
										else:
											th = th + 1
											target_dir.append(str_target_dir)
									else:
										str_target_dir = str_target_root + each
										if not os.path.exists(str_target_dir):
											t =t +1
										else:
											th = th + 1 
											target_dir.append(str_target_dir)
							if t !=0 & th!=0:
								print("====================================================\n该路径%s输入错误\n====================================================\n"% str_target_root)

							###复制文件
							while True:
								if target_dir:
									s = s+1
									copyFile(source_dir,doc_names,target_dir)
									break
									
								else:
									print("请重新输入译文粘贴的根目录，如D:\\doc\\en\\")
									str_target_root = input()
									for each in line_paths:
										if 'README.md' in each:
											str_target_dir = str_target_root
											if not os.path.exists(str_target_dir):
												t = t +1
											else:
												th = th + 1
												target_dir.append(str_target_dir)
										else:
											str_target_dir = str_target_root + each
											if not os.path.exists(str_target_dir):
												t =t +1
											else:
												th = th + 1 
												target_dir.append(str_target_dir)
							break
						else:
							print("该路径错误！请重新输入译文存放的根目录，如D:\\trans\\en")
							str_source_root = input()
							ii = 0 
							iih = 0
							for each in line_paths_filenames:
								if 'README+md' in each:
									str_source_dir = str_source_root
									if not os.path.exists(str_source_dir):
										ii=ii + 1
									else:
										iih = iih + 1
										source_dir.append(str_source_dir)
								else:
									str_source_dir = str_source_root + each
									if not os.path.exists(str_source_dir):
										ii = ii+1
									else:
										iih = iih + 1
										source_dir.append(str_source_dir)
							if ii != 0 & iih !=0:
								print("====================================================\n该路径%s输入错误\n====================================================\n"% str_source_root)
						# break
					if s!=0:
						input('文件复制成功！\n====================================================\n====================================================\n请按enter继续进行查找复制译文！')
						break
					else:
						input('文件复制失败！\n====================================================\n====================================================\n请按enter继续进行查找复制译文！')
					
				else:
					print("无该path文件，请重新输入")
					str = input()
					break
				break
			else:
				print ("请输入path正确路径")
				str = input()	
	

