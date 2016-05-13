#  coding: utf-8
#  author : Xiang
import MySQLdb


class SchoolDBSystem:
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
        self.cur = self.conn.cursor()

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
        self.conn.select_db('school_db_system')

        # 学院表
        self.cur.execute('create table institute'
                         '(i_name VARCHAR (100) NOT NULL PRIMARY KEY ,'  # 院系名称
                         'location VARCHAR (100) NOT NULL,'  # 院系地点
                         'telephone VARCHAR (20));'
                         )

        # 学生表
        self.cur.execute('create table student'
                         '(student_no INT PRIMARY KEY NOT NULL , '
                         'id INT NOT NULL , '
                         'admission_time VARCHAR(20) NOT NULL ,'  # 入学时间
                         'i_name VARCHAR(100) NOT  NULL ,'
                         'grade INT NOT NULL,'
                         'telephone varchar(20),'
                         'email varchar(100),'
                         'FOREIGN KEY (i_name) REFERENCES institute(i_name));'
                         )

        # 教师表
        self.cur.execute('create table teacher'
                         '(t_no INT PRIMARY KEY NOT NULL , '
                         'id INT NOT NULL , '
                         'entry_time VARCHAR(20) NOT NULL ,'  # 开始任教时间
                         'i_name VARCHAR(100) NOT  NULL ,'
                         'telephone varchar(20),'
                         'email varchar(100),'
                         'location VARCHAR (100) NOT NULL,'
                         'FOREIGN KEY (i_name) REFERENCES institute(i_name));'
                         )

        # 部门表
        self.cur.execute('create table department'
                         '(d_name VARCHAR (100) NOT NULL PRIMARY KEY ,'  # 部门名称
                         'location VARCHAR (100) NOT NULL,'  # 院系地点
                         'telephone VARCHAR (20));'
                         )

        # 职工表
        self.cur.execute('create table stuff'
                         '(stuff_no INT PRIMARY KEY NOT NULL , '
                         'id INT NOT NULL , '
                         'work_time VARCHAR(20) NOT NULL ,'  # 开始工作时间
                         'd_name VARCHAR(100) NOT  NULL ,'
                         'telephone varchar(20),'
                         'email varchar(100),'
                         'location VARCHAR (100) NOT NULL,'
                         'FOREIGN KEY (d_name) REFERENCES department(d_name));'
                         )

        # 账号密码表
        self.cur.execute('create table login'
                         '(p_no INT PRIMARY KEY NOT NULL,'
                         'password VARCHAR(20) NOT NULL );'
                         )

        # 课程表
        self.cur.execute('create table course'
                         '(c_no INT PRIMARY KEY NOT NULL ,'
                         't_no INT NOT NULL,'
                         'date VARCHAR(20),'
                         'c_name VARCHAR (100) NOT NULL,'
                         'FOREIGN KEY (t_no) REFERENCES teacher(t_no));'
                         )

        # 成绩表
        self.cur.execute('create table grades'
                         '(student_no INT NOT NULL,'
                         'c_no INT NOT NULL,'
                         'grade INT,'
                         'FOREIGN KEY (student_no) REFERENCES student(student_no),'
                         'FOREIGN KEY (c_no) REFERENCES course(c_no),'
                         'PRIMARY KEY (student_no, c_no));'
                         )

    def delete_tables(self):
        """
        删除数据库和对应的表项
        :return:
        """
        self.cur.execute('SET foreign_key_checks=0')
        self.cur.execute('truncate table institute')
        self.cur.execute('truncate table student')
        self.cur.execute('truncate table teacher')
        self.cur.execute('truncate table department')
        self.cur.execute('truncate table stuff')
        self.cur.execute('truncate table login')
        self.cur.execute('truncate table course')
        self.cur.execute('truncate table grades')
        self.cur.execute('SET foreign_key_checks=1')


if __name__ == "__main__":
    s = SchoolDBSystem()
    s.create_database()
    s.create_tables()
