#  coding: utf-8
#  author : Xiang
import MySQLdb


conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
cur = conn.cursor()
conn.select_db('company')
cur.execute('SET NAMES utf8;')
#  插入部门数据
f = open('d.txt', 'r')
lines = f.readlines()
for line in lines:
    line = line.split()
    cur.execute('insert into department(dname, dno, mgrssn, mgrstartdate) values (%s,%s,%s,%s)',
                line)
    conn.commit()

#  插入雇员数据
f = open('e.txt', 'r')
lines = f.readlines()
for line in lines:
    line = line.split()
    cur.execute('insert into employee values (%s,%s,%s,%s,%s,%s)',
                line)
    conn.commit()

#  插入项目数据
f = open('p.txt', 'r')
lines = f.readlines()
for line in lines:
    line = line.split()
    cur.execute('insert into project values (%s,%s,%s,%s)',
                line)
    conn.commit()

#  插入工作信息
f = open('w.txt', 'r')
lines = f.readlines()
for line in lines:
    line = line.split()
    cur.execute('insert into works_on values (%s,%s,%s)',
                line)
    conn.commit()

cur.close()
conn.close()
f.close()
