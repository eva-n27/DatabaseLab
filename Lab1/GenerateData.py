#  coding: utf-8
#  author : Xiang
import time
import random

#  生成部门数据
department = ['研发部', '财务部', '人事部', '测试部', '管理部']
mgrssn = 100861
f = open('d.txt', 'w')
for i in range(5):
    lst = [department[i], ' ', 'D' + str(i + 1), ' ',
           str(mgrssn + i), ' ',
           str(time.strftime('%Y-%m-%d', time.localtime(time.time()))), '\n']
    f.writelines(lst)
f.close()

#  生成雇员数据
f = open('e.txt', 'w')
first_name = ['张', '王', '周', '李', '唐']
last_name = ['红', '黄', '蓝', '绿', '青', '靛', '紫', '黑', '白' ,'灰']
city = ['哈尔滨', '绥化', '鸡西', '牡丹江', '大庆']
street = ['长江路', '黄河路', '海河路', '清河路', '浑河路', '渤海路', '黄海路', '南海路', '东海路' ,'西海路']
essn = 1000
salary = 2970
for i in range(5):
    for j in range(10):
        lst = [first_name[i] + last_name[j], ' ',
               str(essn + i * 10 + j), ' ',
               city[i] + street[j], ' ',
               str(salary + i * 10 + j), ' ',
               str(essn + i * 20 ), ' ',
               'D' + str(i + 1), '\n']
        f.writelines(lst)

#  生成项目数据
f = open('p.txt', 'w')
pname = ['SQLProject', 'PythonProject', 'C++Project', 'CProject', 'JavaProject',
         'Hadoop Project', 'JavaScript Project', 'Swift Project', 'Pascal Project', 'Lua Project']
location = ['哈尔滨', '绥化', '鸡西', '牡丹江', '大庆', '吉林', '长春', '沈阳', '大连', '锦州']
for i in range(10):
    lst = [pname[i], ' ', 'P' + str(i + 1), ' ', location[i], ' ', 'D' + str(i + 1), '\n']
    f.writelines(lst)
f.close()

#  生成works_on的数据
f = open('e.txt', 'r')
lines = f.readlines()
essn = []
for line in lines:
    essn.append(line.split()[1])
f.close()

f = open('p.txt', 'r')
lines = f.readlines()
pno = []
for line in lines:
    pno.append(line.split()[1])
f.close()

lst_final = []
f = open('w.txt', 'w')
for i in range(5):
    for j in range(10):
        lst = [essn[i * 10 + j], ' ', pno[j]]
        lst_final.append(lst)

for i in range(5):
    for j in range(0, 10, 2):
        lst = [essn[i * 10 + j], ' ', pno[j]]
        lst_final.append(lst)

for i in range(5):
    for j in range(0, 10, 3):
        lst = [essn[i * 10 + j], ' ', pno[j]]
        lst_final.append(lst)

for i in range(0, 5, 2):
    for j in range(10):
        lst = [essn[i * 10 + j], ' ', pno[j]]
        lst_final.append(lst)

for i in range(5):
    for j in range(10):
        lst = [essn[i * 3 + j + 5], ' ', pno[j]]
        lst_final.append(lst)

lst_final = sorted(lst_final, key=lambda t: t[0])
for item in lst_final:
    while lst_final.count(item) > 1:
        lst_final.remove(item)

for i in range(len(lst_final)):
    lst_final[i].extend([' ', str(random.randint(1, 10)), '\n'])
    f.writelines(lst_final[i])

f.close()
