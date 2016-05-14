#  coding: utf-8
#  author : Xiang
import MySQLdb
import sys


class Query:
    def __init__(self, argv):
        #  if user doesn't enter any parameters
        if len(argv) < 5:
            print "You should enter enough parameters!"
            sys.exit(1)

        #  check all the parameters
        self.argv_list = argv[1:]
        if self.argv_list[0] != 'company_query':
            print "The first parameter is wrong."
            sys.exit(1)

        if self.argv_list[1] != '-q':
            print "The second parameter is wrong."
            sys.exit(1)

        if self.argv_list[2] > '9' or self.argv_list[2] < '1':
            print "The third parameter is wrong."
            sys.exit(1)

        if self.argv_list[3] != '-p':
            print "The forth parameter is wrong."
            sys.exit(1)

        #  connect to the database
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
        self.cur = self.conn.cursor()
        self.conn.select_db('company')
        self.cur.execute('SET NAMES utf8;')

        #  choose the query number
        if self.argv_list[2] == '1':
            self.query1()
        elif self.argv_list[2] == '2':
            self.query2()
        elif self.argv_list[2] == '3':
            self.query3()
        elif self.argv_list[2] == '4':
            self.query4()
        elif self.argv_list[2] == '5':
            self.query5()
        elif self.argv_list[2] == '6':
            self.query6()
        elif self.argv_list[2] == '7':
            self.query7()
        elif self.argv_list[2] == '8':
            self.query8()
        else:
            self.query9()

        self.conn.close()
        sys.exit(0)

    def query1(self):
        """
        参加了项目编号为%PNO%的项目的员工号
        :return:无
        """
        self.cur.execute('select essn from works_on where pno = %s', self.argv_list[4])
        data = self.cur.fetchall()
        for item in data:
            print item[0]

    def query2(self):
        """
        参加了项目名为%PNAME%的员工名字
        :return:
        """
        self.cur.execute('select ename from employee NATURAL JOIN works_on NATURAL JOIN project where pname = %s',
                         self.argv_list[4])
        data = self.cur.fetchall()
        for item in data:
            print item[0].decode('utf-8').encode('gbk')  # 输出到命令行的中文需要编码为gbk

    def query3(self):
        """
        在%DNAME%工作的所有工作人员的名字和地址
        :return:
        """
        self.cur.execute('select ename, address from employee NATURAL JOIN department where dname = %s',
                         self.argv_list[4].decode('gbk').encode('utf-8'))
        data = self.cur.fetchall()
        for item in data:
            print item[0].decode('utf-8').encode('gbk'), item[1].decode('utf-8').encode('gbk')

    def query4(self):
        """
        在%DNAME%工作且工资低于%SALARY%元的员工名字和地址
        :return:
        """
        # the wrong way 1#
        # self.cur.execute("select ename, address from employee NATURAL JOIN department where dname = '%s' "
        #                  "and salary < '%s' ", (self.argv_list[4].decode('gbk').encode('utf-8'), self.argv_list[5]))

        # the wrong way 2#
        # self.cur.execute("select ename, address from employee NATURAL JOIN department where dname = %s "
        #                  "and salary < %s ", self.argv_list[4].decode('gbk').encode('utf-8'), self.argv_list[5])

        # the right way 1#
        # sql = "select ename, address from employee NATURAL JOIN department where dname = '%s' " \
        #       "and salary < '%s' " % (self.argv_list[4].decode('gbk').encode('utf-8'), self.argv_list[5])
        # self.cur.execute(sql)

        # the right way 2#
        self.cur.execute("select ename, address from employee NATURAL JOIN department where dname = %s "
                         "and salary < %s ", (self.argv_list[4].decode('gbk').encode('utf-8'), self.argv_list[5]))
        data = self.cur.fetchall()
        for item in data:
            print item[0].decode('utf-8').encode('gbk'), item[1].decode('utf-8').encode('gbk')

    def query5(self):
        """
        没有参加项目编号为%PNO%的项目的员工姓名
        :return:
        """
        self.cur.execute('select DISTINCT ename from employee NATURAL JOIN works_on where essn NOT IN (select DISTINCT '
                         ' essn from works_on where pno = %s)', self.argv_list[4])
        data = self.cur.fetchall()
        for item in data:
            print item[0].decode('utf-8').encode('gbk')

    def query6(self):
        """
        由%ENAME%领导的工作人员的姓名和所在部门的名字
        :return:
        """
        self.cur.execute('select ename, dname from employee NATURAL JOIN department where superssn = (SELECT essn '
                         ' from employee where ename = %s)', self.argv_list[4].decode('gbk').encode('utf-8'))
        data = self.cur.fetchall()
        for item in data:
            print item[0].decode('utf-8').encode('gbk'), item[1].decode('utf-8').encode('gbk')

    def query7(self):
        """
        至少参加了项目编号为%PNO1%和%PNO2%的项目的员工号
        :return:
        """
        sql = "select essn from employee NATURAL JOIN works_on where pno= '%s' and essn in (select essn from " \
              "employee NATURAL JOIN works_on where pno= '%s')" % (self.argv_list[4], self.argv_list[5])
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for item in data:
            print item[0]

    def query8(self):
        """
        员工平均工资低于%SALARY%元的部门名称
        :return:
        """
        self.cur.execute('select dname from employee NATURAL JOIN department group by dno having avg(salary) < %s',
                         self.argv_list[4])
        data = self.cur.fetchall()
        for item in data:
            print item[0].decode('utf-8').encode('gbk')

    def query9(self):
        """
        至少参与了%N%个项目且工作总时间不超过%HOURS%小时的员工名字
        :return:
        """
        self.cur.execute('select ename from employee NATURAL JOIN works_on group by essn having '
                         ' count(*) >= %s and sum(hours) <= %s', (self.argv_list[4], self.argv_list[5]))
        data = self.cur.fetchall()
        for item in data:
            print item[0].decode('utf-8').encode('gbk')


if __name__ == '__main__':
    query = Query(sys.argv)
