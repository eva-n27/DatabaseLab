#  coding: utf-8
#  author : Xiang
import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
cur = conn.cursor()
conn.select_db('company')
cur.execute('SET NAMES utf8;')

#  1.参加了项目名为“SQL Project”的员工名字
cur.execute('select ename from employee NATURAL JOIN works_on NATURAL JOIN project where pname="SQLProject"')
ename = cur.fetchall()
for item in ename:
    print item[0]

#  2.在“Research Department”工作且工资低于3000元的员工名字和地址
cur.execute('select ename,address from employee NATURAL JOIN department where dname="研发部" and salary <3000 ')
infor = cur.fetchall()
for item in infor:
    print item[0], item[1]

#  3.没有参加项目编号为P1的项目的员工姓名
cur.execute("select distinct ename from employee where essn not in(select DISTINCT essn from employee NATURAL JOIN "
            "works_on where pno = 'P1')")
ename = cur.fetchall()
for item in ename:
    print item[0]

#  4.由张红领导的工作人员的姓名和所在部门的名字
cur.execute('select ename, dname from employee natural join department where superssn = (select essn from '
            'employee where ename = "张红")')
infor = cur.fetchall()
for item in infor:
    print item[0], item[1]

#  5.至少参加了项目编号为P1和P2的项目的员工号
cur.execute('select essn from employee NATURAL JOIN works_on where pno="P1" and essn in '
            '(select essn from employee NATURAL JOIN works_on where pno="P2")')
ename = cur.fetchall()
for item in ename:
    print item[0]
cur.close()

#  6.参加了全部项目的员工号码和姓名
cur.execute('select essn, ename from employee natural join works_on group by essn having count(*) = '
            '(select count(*) from project) ')
infor = cur.fetchall()
for item in infor:
    print item[0], item[1]

#  7.员工平均工资低于3000元的部门名称
cur.execute('select dname from employee NATURAL JOIN department group by dno having avg(salary) < 3000')
dname = cur.fetchall()
for item in dname:
    print item[0]

#  8.至少参与了3个项目且工作总时间不超过8小时的员工名字
cur.execute('select ename from employee NATURAL JOIN works_on group by essn having sum(hours) <= 8 and count(*) > 2')
dname = cur.fetchall()
for item in dname:
    print item[0]

#  9.每个部门的员工小时平均工资
cur.execute('select sum(salary) / sum(hours) as avg_salary_per_hour from employee NATURAL JOIN works_on NATURAL JOIN '
            'department group by dno')
avg_salary_per_hour = cur.fetchall()
for item in avg_salary_per_hour:
    print item[0]

conn.close()
