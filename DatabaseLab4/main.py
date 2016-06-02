# __author__ = 'Xiang'
# coding:utf-8

import extmem
import relation
import random


def generate_data(r_, s_):
    """
    随机产生关系和关系B的数据
    :return:
    """
    # 产生r的元组，共112个
    for i_ in range(112):
        new_r = relation.RelationR(40, random.randint(1, 1000))
        r_.append(new_r)

    # 产生s的元组，共224个
    for i_ in range(224):
        new_s = relation.RelationS(random.randint(20, 60), random.randint(1, 1000))
        s_.append(new_s)


def write_relation(relation_, number_of_blk, blk_number_):
    """
    将关系写入到blk文件中
    :param relation_: 关系
    :param number_of_blk: 关系需要使用的缓冲区块数 number_of_blk * 7 = 关系的元组数
    :param blk_number_: 写入的磁盘文件号
    :return: blk_number加一
    """
    for i_ in range(number_of_blk):
        buffer_index = buffer_.get_new_block_in_buffer()  # 申请到的缓冲区的索引
        data = []
        for j_ in range(7):
            # 在这里需要说明的是，我用空格来分隔每个元组的每个属性值，是因为我没找到python控制变量的字节的方法，如果连续写入到blk文件，
            # 就无法区分每个值
            data.extend([str(relation_[i_ * 7 + j_].first_attr), str(' '),  str(relation_[i_ * 7 + j_].second_attr),
                         str(' ')])
        data.append(str(blk_number_ + 1))
        if i_ == number_of_blk - 1:
            data[-1] = str(0)
        buffer_.Data[buffer_index].append(data)
        if not buffer_.write_block_to_disk(blk_number_, buffer_index):
            print "写入磁盘文件号 %s 失败" % blk_number_
            exit()
        blk_number_ += 1
    return blk_number_


def selection_linear(relation_, attr_, value_, blk_number_):
    """
    基于线性查找的关系选择算法
    :param relation_:查找的关系，是一个string
    :param value_:查找的值
    :param attr_:选择的属性
    :param blk_number_:文件块号
    :return:暂时没有返回值
    """
    if relation_ != 'R' and relation_ != 'S':
        print "关系名称错误"
        return blk_number_

    # 看选择的属性是第一个属性还是第二个属性
    if attr_ == 'A' or attr_ == 'C':
        attr_index = 0
    elif attr_ == 'B' or attr_ == 'D':
        attr_index = 1
    else:
        print "属性输入错误"
        return blk_number_

    # 首先找到关系的起始文件块号
    relation_start_blk_number = relation_blk[relation_]
    present_blk_number = relation_start_blk_number  # 这两行代码是冗余的，但是为了程序易读，我觉得是有必要的
    write_data = []  # 保存满足条件的元组，会写入到文件块中
    count = 0  # 记录已经找到的满足条件的元组个数，当元组个数达到7个时，需要写入到内存中
    write_blk_index = buffer_.get_new_block_in_buffer()  # 为选择的数据申请一个缓冲区
    if write_blk_index == -1:
        print "缓冲区已满，不能为选择的数据申请一个缓冲区"
        return blk_number_

    # 读取选择的关系的所有的磁盘块,注意每次读取一个blk文件，搜索完之后需要释放，为选择到的数据申请的缓冲区也一样需要释放
    while True:
        index = buffer_.read_bloc_from_disk(present_blk_number)  # 为关系的数据申请一个缓冲
        if index == -1:
            print "缓冲区已满，不能为关系的数据申请一个缓冲区"
            break

        read_data = buffer_.Data[index][1]  # 从C盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 线性搜索
        for i_ in range(number_of_tuple):
            if read_data[i_ * 2 + attr_index] == value_:
                write_data.extend([str(read_data[i_ * 2]), str(' '), str(read_data[i_ * 2 + 1]), str(' ')])
                print "关系", relation_, ":", read_data[i_ * 2], read_data[i_ * 2 + 1]
                count += 1
            if count == 7:
                write_data.append(str(blk_number_ + 1))
                # 如果文件已经读到最后一块的最后一个分组了
                if next_blk_number == '0' and i_ == number_of_tuple - 1:
                    write_data[-1] = str(0)
                buffer_.Data[write_blk_index].append(write_data)
                if not buffer_.write_block_to_disk(blk_number_, write_blk_index):
                    print "写入磁盘文件号 %s 失败" % blk_number_
                    exit()
                buffer_.free_block_in_buffer(write_blk_index)
                blk_number_ += 1
                write_data = []
                count = 0
                # 新申请缓冲区
                write_blk_index = buffer_.get_new_block_in_buffer()

        # 如果最后一个磁盘块的最后一个元组都被搜索了，且没有待写的数据，则返回
        if next_blk_number == '0' and count == 0:
            buffer_.free_block_in_buffer(write_blk_index)
            buffer_.free_block_in_buffer(index)
            break

        # 缓冲区还有数据没有写出去
        if next_blk_number == '0' and count != 0:
            write_data.append(str(0))
            buffer_.Data[write_blk_index].append(write_data)
            if not buffer_.write_block_to_disk(blk_number_, write_blk_index):
                print "写入磁盘文件号 %s 失败" % blk_number_
                exit()
            blk_number_ += 1
            buffer_.free_block_in_buffer(write_blk_index)
            buffer_.free_block_in_buffer(index)
            break
        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
    return blk_number_

if __name__ == '__main__':
    # 磁盘文件号
    blk_number = 0

    # 首先产生数据
    r = []
    s = []
    generate_data(r, s)

    # 用于记录关系和关系存放的第一个文件块的编号
    relation_blk = {}

    # 创建缓冲区
    # 元组为8个字节，所以我就设计块大小为8个元组，缓冲区大小为65个元组
    buffer_ = extmem.Buffer(65, 8)  # bufsize = 65, blksize = 8

    # 将r写入到磁盘中
    relation_blk['R'] = blk_number
    blk_number = write_relation(r, 3, blk_number)

    # # 将s写入到磁盘中
    # relation_blk['S'] = blk_number
    # blk_number = write_relation(s, 32, blk_number)

    r = 'R'
    a = 'A'
    v = '40'
    blk_number_ = selection_linear(r, a, v, blk_number)
