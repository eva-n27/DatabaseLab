#  coding: utf-8
#  author : Xiang
import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='24678', port=3306)
cur = conn.cursor()
conn.select_db('company')
cur.execute('SET NAMES utf8;')

