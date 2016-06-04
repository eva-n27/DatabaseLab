# __author__ = 'Xiang'
# coding:utf-8

from SyntaxTree import Tree

employee = ["ESSN", "ADDRESS", "SALARY", "SUPERSSN", "ENAME", "DNO"]
department = ["DNO", "DNAME", "DNEMBER", "MGRSSN", "MGRSTARTDATE"]
project = ["PNAME", "PNO", "PLOCATION", "DNO"],
works_on = ["HOURS", "ESSN", "PNO"]


def parse(sql_statement):
    """
    分析sql语句，转化为查询执行树
    :param sql_statement:sql语句
    :return:转化后的查询执行树
    """
    sql = sql_statement.split()
    execute_tree = Tree()

    i_ = 0
    while True:
        if i_ >= len(sql):
            break
        elif sql[i_] == 'SELECT' or sql[i_] == 'PROJECTION':
            # 两种操作符
            execute_tree.set_operator(sql[i_])
            i_ += 2  # 从[开始到]里面的全部记录下来
            condition = ''
            while sql[i_] != ']':
                condition += sql[i_]
                condition += ' '
                i_ += 1
            i_ += 1
            execute_tree.set_condition(condition)
        elif sql[i_] == 'JOIN':
            # 连接操作需要创建子树，所以分开写
            execute_tree.set_operator(sql[i_])
            execute_tree.l_child = Tree()
            execute_tree.l_child.set_attribute(sql[i_ - 1])
            execute_tree.r_child = Tree()
            execute_tree.r_child.set_attribute(sql[i_ + 1])
            i_ += 1
        elif sql[i_] == '(':
            # 每次遇到这个说明需要创建一棵子树，由于题目中的查询都是只有一个分支，所以可以直接进入下一个子树中
            i_ += 1
            statement = ''
            while i_ < len(sql) and sql[i_] != ')':
                statement += sql[i_]
                statement += ' '
                i_ += 1
            i_ += 1
            execute_tree.l_child = parse(statement)
        else:
            i_ += 1

    return execute_tree


def search(sql_):
    """
    查找属性对应的关系
    :param sql_:
    :return:
    """
    sql_ = sql_.split()
    if sql_[0] in employee:
        return "EMPLOYEE"
    elif sql_[0] in department:
        return "DEPARTMENT"
    elif sql_[0] in project:
        return "PROJECT"
    elif sql_[0] in works_on:
        return "WORKS_ON"
    return None


def optimize(syntax_tree, sql_):
    """
    优化
    :param syntax_tree:
    :return:
    """
    if syntax_tree.operator == 'SELECT':
        condition = syntax_tree.condition
        sql_ = condition.split('&')
        relation = []
        for i_ in range(len(sql_)):
            if search(sql_[i_]) is not None:
                relation.append(search(sql_[i_]))
        syntax_tree = optimize(syntax_tree.l_child, sql_)
    elif syntax_tree.operator == 'PROJECTION':
        syntax_tree.l_child = optimize(syntax_tree.l_child, sql_)
    elif syntax_tree.operator == 'JOIN':
        first_tree = Tree()
        first_tree.operator = 'SELECT'
        first_tree.condition = sql_[0]
        first_tree.l_child = syntax_tree.l_child
        syntax_tree.l_child = first_tree
        if len(sql_) == 1:
            return syntax_tree
        second_tree = Tree()
        second_tree.operator = 'SELECT'
        second_tree.condition = sql_[1]
        second_tree.r_child = syntax_tree.r_child
        syntax_tree.r_child = second_tree
    return syntax_tree


def print_tree(syntax_tree):
    """
    打印出树
    :param syntax_tree:
    :return:
    """
    if syntax_tree.operator != '':
        print syntax_tree.operator, syntax_tree.condition
    else:
        print syntax_tree.attribute
    if syntax_tree.l_child is not None:
        print_tree(syntax_tree.l_child)
    if syntax_tree.r_child is not None:
        print_tree(syntax_tree.r_child)

if __name__ == '__main__':
    test_sql = "PROJECTION [ BDATE ] ( SELECT [ ENAME = ’John’ & DNAME = ’ Research’ ] ( EMPLOYEE JOIN DEPARTMENT ) )"
    etree = parse(test_sql)
    print_tree(etree)
    otree = optimize(etree, '')
    print_tree(otree)
