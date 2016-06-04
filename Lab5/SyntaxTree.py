# __author__ = 'Xiang'
# coding:utf-8


class Tree:
    def __init__(self):
        self.l_child = None  # 左儿子
        self.r_child = None  # 右儿子
        self.operator = ''  # 操作符
        self.condition = ''  # 条件
        self.attribute = ''  # 属性

    def set_left_child(self, l_child):
        """
        设置左子树
        :param l_child: 左子树
        :return:
        """
        self.l_child = l_child

    def set_right_child(self, r_child):
        """
        设置右子树
        :param r_child: 右子树
        :return:
        """
        self.r_child = r_child

    def set_operator(self, operator):
        """
        设置操作符
        :param operator: 操作符
        :return:
        """
        self.operator = operator

    def set_condition(self, condition):
        """
        设置条件
        :param condition:条件
        :return:
        """
        self.condition = condition

    def set_attribute(self, attribute):
        """
        设置属性
        :param attribute:属性名
        :return:
        """
        self.attribute = attribute
