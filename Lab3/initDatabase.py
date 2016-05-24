#  coding: utf-8
#  author : Xiang
import MySQLdb


class SchoolDBSystem:
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
        self.cur = self.conn.cursor()
        self.conn.select_db('school_db_system')

    def __del__(self):
        """
        析构函数
        :return:
        """
        self.cur.close()
        self.conn.close()

    def create_database(self):
        """
        创建一个新的数据库
        :return:
        """
        self.cur.execute('create database if not exists school_db_system;')

    def create_tables(self):
        """
        创建一个新的数据库中的表项
        :return:
        """
        # 学院表
        self.cur.execute('create table institute'
                         '(i_name VARCHAR (100) NOT NULL PRIMARY KEY ,'  # 院系名称
                         'location VARCHAR (100) NOT NULL);'  # 院系地点;'
                         )

        # 专业表
        self.cur.execute('create table discipline'
                         '(d_name VARCHAR (100) NOT NULL PRIMARY KEY ,'  # 专业名称
                         'i_name  VARCHAR (100) NOT NULL,'
                         'FOREIGN KEY (i_name) REFERENCES institute(i_name));'  # 院系地点;'
                         )
        # 学生表
        self.cur.execute('create table student'
                         '(student_no VARCHAR(20)  PRIMARY KEY NOT NULL , '
                         'student_name VARCHAR (20) NOT NULL,'
                         'id VARCHAR(20) NOT NULL , '
                         'd_name VARCHAR(100) NOT  NULL ,'
                         'telephone varchar(20),'
                         'email varchar(100),'
                         'FOREIGN KEY (d_name) REFERENCES discipline(d_name));'
                         )

        # 教师表
        self.cur.execute('create table teacher'
                         '(t_no VARCHAR(20)  PRIMARY KEY NOT NULL , '
                         'id VARCHAR(20) NOT NULL , '
                         'teacher_name VARCHAR(100) NOT  NULL ,'
                         'i_name VARCHAR(100) NOT  NULL ,'
                         'telephone varchar(20),'
                         'email varchar(100),'
                         'location VARCHAR (100) NOT NULL,'
                         'FOREIGN KEY (i_name) REFERENCES institute(i_name));'
                         )

        # 教务处工作人员表
        self.cur.execute('create table stuff'
                         '(stuff_no VARCHAR(20)  PRIMARY KEY NOT NULL , '
                         'id VARCHAR(20) NOT NULL ,'
                         'stuff_name VARCHAR(100) NOT  NULL ,'
                         'telephone varchar(20),'
                         'email varchar(100));'
                         )

        # 账号密码表
        self.cur.execute('create table login'
                         '(username VARCHAR(20) PRIMARY KEY NOT NULL,'
                         'class VARCHAR(20) NOT NULL,'  # 类别：学生student、教师teacher、职工stuff
                         'password VARCHAR(20) NOT NULL );'
                         )

        # 课程表
        self.cur.execute('create table course'
                         '(c_no VARCHAR(20)  PRIMARY KEY NOT NULL ,'
                         't_no VARCHAR(20)  NOT NULL,'
                         'c_name VARCHAR (100) NOT NULL,'
                         'FOREIGN KEY (t_no) REFERENCES teacher(t_no));'
                         )

        # 选课表
        self.cur.execute('create table selection'
                         '(c_no VARCHAR(20)  NOT NULL ,'
                         'student_no VARCHAR(20) NOT NULL,'
                         'PRIMARY KEY(c_no, student_no),'
                         'FOREIGN KEY (c_no) REFERENCES course(c_no),'
                         'FOREIGN KEY (student_no) REFERENCES student(student_no));')

        # 教学主管表
        self.cur.execute('create table manager'
                         '(m_no VARCHAR(20)  NOT NULL,'
                         'id VARCHAR(20) NOT NULL , '
                         'm_name VARCHAR(100) NOT  NULL ,'
                         'i_name VARCHAR(100) NOT  NULL ,'
                         'telephone varchar(20),'
                         'email varchar(100),'
                         'location VARCHAR (100) NOT NULL,'
                         'FOREIGN KEY (i_name) REFERENCES institute(i_name));'
                         )

    def delete_tables(self):
        """
        删除数据库和对应的表项
        :return:
        """
        self.conn.select_db('school_db_system')
        self.cur.execute('SET foreign_key_checks=0')
        # self.cur.execute('drop table institute;')
        # self.cur.execute('drop table student;')
        # self.cur.execute('drop table teacher;')
        # self.cur.execute('drop table discipline;')
        # self.cur.execute('drop table stuff;')
        # self.cur.execute('drop table login;')
        # self.cur.execute('drop table course;')
        # self.cur.execute('drop table selection;')
        self.cur.execute('drop table manager;')
        self.cur.execute('SET foreign_key_checks=1')

    def delete_database(self):
        """
        删除数据库
        :return:
        """
        self.cur.execute('drop database school_db_system;')

    def create_view(self):
        """
        创建视图
        :return:
        """
        # self.cur.execute('create view manager_view_student as select student_no, student_name from student')
        self.cur.execute('create view stuff_view_student as select student_no, student_name from student')

    def create_index(self):
        """
        创建索引
        :return:
        """
        # self.cur.execute('create index student_number on student(student_no)')
        # self.cur.execute('create index student_info on student(student_no, student_name)')
        # self.cur.execute('create index username_index on login(username)')
        self.cur.execute('create index s_name on student(student_name)')

    def create_trigger(self):
        """
        创建触发器
        :return:
        """
        self.cur.execute('create trigger delete_student before delete on course for each row '
                         'delete from selection where c_no = old.c_no ')

    def test(self):
        """
        测试sql语句
        :return:
        """
        self.cur.execute('select * from manager_view_student ')
        data = self.cur.fetchall()
        print data[0][1]


if __name__ == "__main__":
    s = SchoolDBSystem()
    # s.delete_database()
    # s.delete_tables()
    # s.create_database()
    # s.create_tables()
    # s.create_view()
    # s.test()
    # s.create_index()
    s.create_trigger()
