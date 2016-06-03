# __author__ = 'Xiang'
# coding:utf-8

import extmem
import relation
from random import randint
from math import ceil


def generate_data(r_, s_):
    """
    随机产生关系和关系B的数据
    :return:
    """
    # 产生r的元组，共112个
    for i_ in range(112):
        new_r = relation.RelationR(randint(1, 40), randint(1, 1000))
        # new_r = relation.RelationR(40, randint(1, 1000))
        r_.append(new_r)

    # 产生s的元组，共224个
    for i_ in range(224):
        new_s = relation.RelationS(randint(20, 60), randint(1, 1000))
        s_.append(new_s)


def buffer_busy():
    """
    检查缓冲区的块中有哪些是被占用的而没被释放的
    False表示块为空，True表示块中存放了数据
    :return:
    """
    for i in range(buffer_.numAllBlk):
        if buffer_.Data[i][0]:
            print i


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


def write_data(data_set, number_of_blk, tuple_number, blk_number_):
    """
    将关系写入到blk文件中
    :param data_set: 需要写的数据
    :param number_of_blk: 关系需要使用的缓冲区块数 number_of_blk * tuple_number = 关系的元组数
    :param tuple_number: 每个块中可以存放的元组个数
    :param blk_number_: 写入的磁盘文件号
    :return: blk_number加一
    """
    number_of_attr = len(data_set[0])  # 关系的属性数
    for i_ in range(number_of_blk - 1):
        buffer_index = buffer_.get_new_block_in_buffer()  # 申请到的缓冲区的索引
        data = []
        for j_ in range(tuple_number):
            for k_ in range(number_of_attr):
                data.extend([str(data_set[i_ * tuple_number + j_][k_]), str(' ')])
        data.append(str(blk_number_ + 1))
        buffer_.Data[buffer_index].append(data)
        if not buffer_.write_block_to_disk(blk_number_, buffer_index):
            print "写入磁盘文件号 %s 失败" % blk_number_
            exit()
        blk_number_ += 1

    # 最后一个缓冲区中的数据可能不够一个缓冲块，单独处理
    number_of_written = (number_of_blk - 1) * tuple_number  # 已经写入磁盘的数据个数
    buffer_index = buffer_.get_new_block_in_buffer()
    data = []
    for i_ in range(len(data_set) - number_of_written):
        for j_ in range(number_of_attr):
            data.extend([str(data_set[number_of_written + i_][j_]), str(' ')])
    data.append(str(0))
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
    relation_start_blk_number = blk_dict[relation_]
    present_blk_number = relation_start_blk_number  # 这两行代码是冗余的，但是为了程序易读，我觉得是有必要的
    write_data_ = []  # 保存满足条件的元组，会写入到文件块中
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

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 线性搜索
        for i_ in range(number_of_tuple):
            if int(read_data[i_ * 2 + attr_index]) == value_:
                write_data_.append([read_data[i_ * 2], read_data[i_ * 2 + 1]])
                print "关系", relation_, ":", read_data[i_ * 2], read_data[i_ * 2 + 1]

        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        if present_blk_number == '0':
            break

    if len(write_data_) == 0:
        print "没有对应的数据"
        return blk_number_

    blk_number_ = write_data(write_data_, int(ceil(len(write_data_) / 7.0)), 7, blk_number_)
    return blk_number_


def selection_binary_search(relation_, attr_, value_, blk_number_):
    """
    基于线性查找的关系选择算法
    :param relation_:查找的关系，是一个string
    :param value_:查找的值
    :param attr_:选择的属性
    :param blk_number_:文件块号
    :return:磁盘号
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
    relation_start_blk_number = blk_dict[relation_]
    present_blk_number = relation_start_blk_number  # 这两行代码是冗余的，但是为了程序易读，我觉得是有必要的
    write_data_ = []  # 保存满足条件的元组，会写入到文件块中
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

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 二分查找
        sort_data = []
        for i_ in range(number_of_tuple):
            sort_data.append([int(read_data[i_ * 2]), int(read_data[i_ * 2 + 1])])
        sort_data = sorted(sort_data, key=lambda t: t[attr_index])
        search_low = 0  # 搜索起始低位置
        search_high = number_of_tuple - 1  # 搜索起始高位置
        while search_low <= search_high:
            search_middle = (search_high - search_low) / 2 + search_low
            if sort_data[search_middle][attr_index] == value_:
                write_data_.append(sort_data[search_middle])
                print "关系", relation_, ":", sort_data[search_middle]

                # 查看是否具有重复项,先看前面的，再看后面的
                before_index = search_middle - 1  # 前面的
                while before_index >= 0 and sort_data[before_index][attr_index] == value_:
                    write_data_.append(sort_data[before_index])
                    print "关系", relation_, ":", sort_data[before_index]
                    before_index -= 1

                after_index = search_middle + 1  # 后面的
                while after_index < number_of_tuple and sort_data[after_index][attr_index] == value_:
                    write_data_.append(sort_data[after_index])
                    print "关系", relation_, ":", sort_data[after_index]
                    after_index += 1
                # 搜索下个磁盘块
                break
            elif sort_data[search_middle][attr_index] > value_:
                search_high = search_middle - 1
            else:
                search_low = search_middle + 1

        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        if present_blk_number == '0':
            break

    if len(write_data_) == 0:
        print "没有对应的数据"
        return blk_number_

    blk_number_ = write_data(write_data_, int(ceil(len(write_data_) / 7.0)), 7, blk_number_)
    return blk_number_


def sort_for_index(relation_, index_table_, attr_index_, blk_number_):
    """
    将随机生成关系的blk文件进行排序，然后再写入新的blk文件中
    :param relation_:关系
    :param index_table_:索引表
    :param attr_index_:表示第几个属性
    :param blk_number_:磁盘块号
    :return:索引表和磁盘块号
    """
    data = []
    # 首先找到第一个关系的起始文件块号
    present_blk_number = blk_dict[relation_]

    # 然后读取第一个关系的数据
    while True:
        index = buffer_.read_bloc_from_disk(present_blk_number)  # 为关系的数据申请一个缓冲
        if index == -1:
            print "缓冲区已满，不能为关系的数据申请一个缓冲区"
            break

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 读取所有的元组
        for i_ in range(number_of_tuple):
            data.append([int(read_data[i_ * 2]), int(read_data[i_ * 2 + 1])])
        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        # 读完退出
        if present_blk_number == '0':
            break

    # 先建立好索引，然后再写入磁盘块
    index_blk_number = blk_number_
    data = sorted(data, key=lambda t: t[attr_index_])
    index_table_, index_blk_number = create_index(data, attr_index_, index_table_, index_blk_number)

    if len(data) == 0:
        print "没有对应的数据"
        return blk_number_

    blk_number_ = write_data(data, int(ceil(len(data) / 7.0)), 7, blk_number_)

    if index_blk_number != blk_number_:
        print "索引建的有问题"
        exit()

    return index_table_, blk_number_


def create_index(data, attr_index, index_table_, blk_number_):
    """
    为data创建索引表项
    :param data: 数据
    :param attr_index: 表示第几个属性
    :param index_table_: 索引表
    :param blk_number_: 磁盘号
    :return: 索引表
    """
    index = 0
    while index < len(data):
        if index + 7 < len(data) and data[index][attr_index] < data[index + 7][attr_index]:
            index_table_.append([data[index][attr_index], blk_number_])
            blk_number_ += 1
            index += 7
        elif index + 7 < len(data) and data[index][attr_index] == data[index + 7][attr_index]:
            index_table_.append([data[index][attr_index], blk_number_])
            blk_number_ += 1
            index += 7
            count = 1
            while index + 7 * count < len(data) and data[index + 7 * count - 1][attr_index] \
                    == data[index + 7 * count][attr_index]:
                count += 1
            if index + 7 > len(data):
                blk_number_ += count
                break
            else:
                index += 7 * count
                blk_number_ += count
        else:
            index_table_.append([data[index][attr_index], blk_number_])
            blk_number_ += 1
            break
    return index_table_, blk_number_


def selection_index(relation_, attr_, value_, blk_number_):
    """
    基于线性查找的关系选择算法，需要使用sort_for_index和create_index
    :param relation_:查找的关系，是一个string
    :param value_:查找的值
    :param attr_:选择的属性
    :param blk_number_:文件块号
    :return:磁盘号
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

    index_table = []  # 索引表
    index_table, blk_number_ = sort_for_index(relation_, index_table, attr_index, blk_number_)
    index_table = sorted(index_table, key=lambda t: t[0])

    hit_blk_number = -1  # 找到
    for i in range(len(index_table)):
        if index_table[i][0] == value_:
            hit_blk_number = index_table[i][1]
            break
        elif index_table[i][0] < value_:
            hit_blk_number = index_table[i][1]
        else:
            break
    if hit_blk_number == -1:
        print "没找到指定记录"
        return blk_number_

    present_blk_number = hit_blk_number  # 这两行代码是冗余的，但是为了程序易读，我觉得是有必要的
    write_data_ = []  # 保存满足条件的元组，会写入到文件块中
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

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 搜索对应元组
        for i_ in range(number_of_tuple):
            if int(read_data[i_ * 2 + attr_index]) == value_:
                write_data_.append([int(read_data[i_ * 2]), int(read_data[i_ * 2 + 1])])
                print "关系", relation_, ":", read_data[i_ * 2], read_data[i_ * 2 + 1]
            elif int(read_data[i_ * 2 + attr_index]) > value_:
                next_blk_number = '0'
                break

        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)
        if present_blk_number == '0':
            break

    if len(write_data_) == 0:
        print "没有对应的数据"
        return blk_number_

    blk_number_ = write_data(write_data_, int(ceil(len(write_data_) / 7.0)), 7, blk_number_)
    return blk_number_


def project(relation_, attr_, blk_number_):
    """
    实现关系投影算法
    :param relation_:需要投影的关系
    :param attr_:投影的属性
    :param blk_number_:写入的磁盘文件号
    :return:下一次写入的磁盘文件号
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
    present_blk_number = blk_dict[relation_]
    write_data_ = []  # 保存满足条件的元组，会写入到文件块中
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

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 投影
        for i_ in range(number_of_tuple):
            write_data_.append([read_data[i_ * 2 + attr_index]])
            print "关系", relation_, ":", read_data[i_ * 2 + attr_index]

        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        if present_blk_number == '0':
            break

    if len(write_data_) == 0:
        print "没有对应的数据"
        return blk_number_

    blk_number_ = write_data(write_data_, int(ceil(len(write_data_) / 14.0)), 14, blk_number_)
    return blk_number_


def set_operate(relation_first, relation_second, operation, blk_number_):
    """
    实现集合操作：并, 交， 差
    :param relation_first: 关系
    :param relation_second: 关系
    :param operation: 操作
    :param blk_number_: 磁盘号
    :return:
    """
    if relation_first != 'R' and relation_first != 'S':
        print "关系名称错误"
        return blk_number_
    elif relation_second != 'R' and relation_second != 'S':
        print "关系名称错误"
        return blk_number_

    first_data = []
    # 首先找到第一个关系的起始文件块号
    present_blk_number = blk_dict[relation_first]
    # 然后读取第一个关系的数据
    while True:
        index = buffer_.read_bloc_from_disk(present_blk_number)  # 为关系的数据申请一个缓冲
        if index == -1:
            print "缓冲区已满，不能为关系的数据申请一个缓冲区"
            break

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 读取所有的元组
        for i_ in range(number_of_tuple):
            first_data.append([read_data[i_ * 2], read_data[i_ * 2 + 1]])
        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        # 读完退出
        if present_blk_number == '0':
            break

    second_data = []
    # 首先找到第二个关系的起始文件块号
    present_blk_number = blk_dict[relation_second]
    # 然后读取第二个关系的数据
    while True:
        index = buffer_.read_bloc_from_disk(present_blk_number)  # 为关系的数据申请一个缓冲
        if index == -1:
            print "缓冲区已满，不能为关系的数据申请一个缓冲区"
            break

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 读取所有的元组
        for i_ in range(number_of_tuple):
            second_data.append([read_data[i_ * 2], read_data[i_ * 2 + 1]])
        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        # 读完退出
        if present_blk_number == '0':
            break

    write_data_ = []
    if operation == 'union':  # 并
        union_data = []
        union_data.extend(first_data)
        union_data.extend(second_data)
        # 去重复
        for item in union_data:
            if union_data.count(item) > 1:
                print "关系", relation_first, '并', relation_second, ":", item[0], item[1]
                for i_ in range(union_data.count(item) - 1):
                    union_data.remove(item)
            else:
                print "关系", relation_first, '并', relation_second, ":", item[0], item[1]
        write_data_ = union_data
    elif operation == 'intersect':  # 交
        intersect_data = []
        for item in first_data:
            if item in second_data:
                intersect_data.append(item)
                print "关系", relation_first, '交', relation_second, ":", item[0], item[1]
        write_data_ = intersect_data
    elif operation == 'except':  # 差
        except_data = []
        for item in first_data:
            if item not in second_data:
                except_data.append(item)
                print "关系", relation_first, '差', relation_second, ":", item[0], item[1]
        write_data_ = except_data

    if len(write_data_) == 0:
        print "没有对应的数据"
        return blk_number_

    blk_number_ = write_data(write_data_, int(ceil(len(write_data_) / 7.0)), 7,  blk_number_)

    return blk_number_


def nest_loop_join(relation_first, relation_second, blk_numbers_of_first, blk_numbers_of_second, blk_number_):
    """
    实现Nest Loop Join
    :param relation_first:关系
    :param relation_second:关系
    :param blk_numbers_of_first:第一个关系的磁盘块数
    :param blk_numbers_of_second:第二个关系的磁盘块数
    :param blk_number_:磁盘块号
    :return:磁盘块号
    """
    # 选择块少的作为外层循环
    if blk_numbers_of_first > blk_numbers_of_second:
        out_relation = relation_second
        in_relation = relation_first
    else:
        out_relation = relation_first
        in_relation = relation_second

    # 首先找到外层关系的起始文件块号
    out_present_blk_number = blk_dict[out_relation]
    write_data_ = []  # 保存满足条件的元组，会写入到文件块中
    write_blk_index = buffer_.get_new_block_in_buffer()  # 为选择的数据申请一个缓冲区
    if write_blk_index == -1:
        print "缓冲区已满，不能为选择的数据申请一个缓冲区"
        return blk_number_

    # 读取选择的关系的所有的磁盘块,注意每次读取一个blk文件，搜索完之后需要释放，为选择到的数据申请的缓冲区也一样需要释放
    while True:
        out_index = buffer_.read_bloc_from_disk(out_present_blk_number)  # 为关系的数据申请一个缓冲
        if out_index == -1:
            print "缓冲区已满，不能为关系的数据申请一个缓冲区"
            break

        out_read_data = buffer_.Data[out_index][1]  # 从磁盘块中读取的数据
        out_number_of_tuple = (len(out_read_data) - 1) / 2
        out_next_blk_number = out_read_data[-1]  # 文件的后继磁盘块号

        # 首先找到关系的起始文件块号
        in_present_blk_number = blk_dict[in_relation]  # 这两行代码是冗余的，但是为了程序易读，我觉得是有必要的
        while True:
            in_index = buffer_.read_bloc_from_disk(in_present_blk_number)
            if in_index == -1:
                print "缓冲区已满，不能为关系的数据申请一个缓冲区"
                exit()
            in_read_data = buffer_.Data[in_index][1]
            in_number_of_tuple = (len(in_read_data) - 1) / 2
            in_next_blk_number = in_read_data[-1]

            for i_ in range(out_number_of_tuple):
                for j_ in range(in_number_of_tuple):
                    if out_read_data[i_ * 2] == in_read_data[j_ * 2]:
                        write_data_.append([int(out_read_data[i_ * 2]), int(out_read_data[i_ * 2 + 1]),
                                            int(in_read_data[j_ * 2 + 1])])
                        print '关系', out_relation, '的元组', [out_read_data[i_ * 2], out_read_data[i_ * 2 + 1]], \
                            '和关系', in_relation, '的元组', [in_read_data[j_ * 2], in_read_data[j_ * 2 + 1]], '连接'
            in_present_blk_number = in_next_blk_number
            buffer_.free_block_in_buffer(in_index)
            if in_present_blk_number == '0':
                break

        out_present_blk_number = out_next_blk_number
        buffer_.free_block_in_buffer(out_index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        if out_present_blk_number == '0':
            break

    if len(write_data_) == 0:
        print "没有对应的数据"
        return blk_number_

    blk_number_ = write_data(write_data_, int(ceil(len(write_data_) / 5.0)), 5, blk_number_)
    return blk_number_


def sort_merge_join(relation_first, relation_second, blk_number_):
    """
    实现Sort Merge Join
    :param relation_first:关系
    :param relation_second:关系
    :param blk_number_:磁盘块号
    :return:磁盘块号
    """
    if relation_first != 'R' and relation_first != 'S':
        print "关系名称错误"
        return blk_number_
    elif relation_second != 'R' and relation_second != 'S':
        print "关系名称错误"
        return blk_number_

    first_data = []
    # 首先找到第一个关系的起始文件块号
    present_blk_number = blk_dict[relation_first]
    # 然后读取第一个关系的数据
    while True:
        index = buffer_.read_bloc_from_disk(present_blk_number)  # 为关系的数据申请一个缓冲
        if index == -1:
            print "缓冲区已满，不能为关系的数据申请一个缓冲区"
            break

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 读取所有的元组
        for i_ in range(number_of_tuple):
            first_data.append([int(read_data[i_ * 2]), int(read_data[i_ * 2 + 1])])
        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        # 读完退出
        if present_blk_number == '0':
            break

    second_data = []
    # 首先找到第二个关系的起始文件块号
    present_blk_number = blk_dict[relation_second]
    # 然后读取第二个关系的数据
    while True:
        index = buffer_.read_bloc_from_disk(present_blk_number)  # 为关系的数据申请一个缓冲
        if index == -1:
            print "缓冲区已满，不能为关系的数据申请一个缓冲区"
            break

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 读取所有的元组
        for i_ in range(number_of_tuple):
            second_data.append([int(read_data[i_ * 2]), int(read_data[i_ * 2 + 1])])
        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        # 读完退出
        if present_blk_number == '0':
            break
    # sort
    first_data = sorted(first_data, key=lambda t: t[0])
    second_data = sorted(second_data, key=lambda t: t[0])

    # merge
    write_data_ = []
    i_ = 0
    j_ = 0
    while i_ < len(first_data) or j_ < len(second_data):
        if i_ < len(first_data) and j_ < len(second_data):
            if first_data[i_][0] == second_data[j_][0]:
                write_data_.append([first_data[i_][0], first_data[i_][1], second_data[j_][1]])
                print '关系', relation_first, '的元组', first_data[i_], \
                    '和关系', relation_second, '的元组', second_data[j_], '连接'
                temp_index = j_ + 1  # 让第二个关系先移动
                while temp_index < len(second_data) and first_data[i_][0] == second_data[temp_index][0]:
                    write_data_.append([first_data[i_][0], first_data[i_][1], second_data[temp_index][1]])
                    print '关系', relation_first, '的元组', first_data[i_], \
                        '和关系', relation_second, '的元组', second_data[temp_index], '连接'
                    temp_index += 1
                i_ += 1  # 只移动第二个关系不移动第一个关系
            elif first_data[i_][0] < second_data[j_][0]:
                i_ += 1
            elif first_data[i_][0] > second_data[j_][0]:
                j_ += 1
        else:
            break

    if len(write_data_) == 0:
        print "没有对应的数据"
        return blk_number_

    blk_number_ = write_data(write_data_, int(ceil(len(write_data_) / 5.0)), 5, blk_number_)
    return blk_number_


def hash_join(relation_first, relation_second, number_of_bucket, blk_number_):
    """
    实现Hash Join
    :param relation_first:关系
    :param relation_second:关系
    :param number_of_bucket:hash的桶的个数
    :param blk_number_:磁盘块号
    :return:磁盘块号
    """
    if relation_first != 'R' and relation_first != 'S':
        print "关系名称错误"
        return blk_number_
    elif relation_second != 'R' and relation_second != 'S':
        print "关系名称错误"
        return blk_number_

    # 构造桶
    bucket_of_r = []
    bucket_of_s = []
    for i_ in range(number_of_bucket):
        bucket_of_r.append([])
        bucket_of_s.append([])

    # 首先找到第一个关系的起始文件块号
    present_blk_number = blk_dict[relation_first]
    # 然后读取第一个关系的数据
    while True:
        index = buffer_.read_bloc_from_disk(present_blk_number)  # 为关系的数据申请一个缓冲
        if index == -1:
            print "缓冲区已满，不能为关系的数据申请一个缓冲区"
            break

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 读取所有的元组
        for i_ in range(number_of_tuple):
            bucket_index = (int(read_data[i_ * 2]) + 2) % number_of_bucket  # hash一下
            bucket_of_r[bucket_index].append([int(read_data[i_ * 2]), int(read_data[i_ * 2 + 1])])
        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        # 读完退出
        if present_blk_number == '0':
            break

    # 首先找到第二个关系的起始文件块号
    present_blk_number = blk_dict[relation_second]
    # 然后读取第二个关系的数据
    while True:
        index = buffer_.read_bloc_from_disk(present_blk_number)  # 为关系的数据申请一个缓冲
        if index == -1:
            print "缓冲区已满，不能为关系的数据申请一个缓冲区"
            break

        read_data = buffer_.Data[index][1]  # 从磁盘块中读取的数据
        number_of_tuple = (len(read_data) - 1) / 2
        next_blk_number = read_data[-1]  # 文件的后继磁盘块号

        # 读取所有的元组
        for i_ in range(number_of_tuple):
            bucket_index = (int(read_data[i_ * 2]) + 2) % number_of_bucket  # hash一下
            bucket_of_s[bucket_index].append([int(read_data[i_ * 2]), int(read_data[i_ * 2 + 1])])
        present_blk_number = next_blk_number
        buffer_.free_block_in_buffer(index)  # 这个缓冲区的数据已经搜索完毕，释放读取关系的数据的缓冲区
        # 读完退出
        if present_blk_number == '0':
            break
    # join
    write_data_ = []
    for i_ in range(number_of_bucket):
        for j_ in range(len(bucket_of_r[i_])):
            for k_ in range(len(bucket_of_s[i_])):
                if bucket_of_r[i_][j_][0] == bucket_of_s[i_][k_][0]:
                    write_data_.append([bucket_of_r[i_][j_][0], bucket_of_r[i_][j_][1], bucket_of_s[i_][k_][1]])
                    print '关系', relation_first, '的元组', bucket_of_r[i_][j_], '和关系', relation_second, '的元组', \
                        bucket_of_s[i_][k_], '连接'

    if len(write_data_) == 0:
        print "没有对应的数据"
        return blk_number_

    blk_number_ = write_data(write_data_, int(ceil(len(write_data_) / 5.0)), 5, blk_number_)
    return blk_number_


if __name__ == '__main__':
    blk_number = 0  # 磁盘文件号
    blk_numbers_of_R = 16  # 关系R的磁盘块数
    blk_numbers_of_S = 32  # 关系S的磁盘块数
    blk_dict = {}  # 用于记录关系和关系存放的第一个文件块的编号

    # 创建缓冲区
    # 元组为8个字节，所以我就设计块大小为8个元组，缓冲区大小为64个元组
    # 题目要求的520 = 512 + 8 ，8是每个缓冲区有一个标志位，我的缓冲区中不需要为它预留位置
    buffer_ = extmem.Buffer(64, 8)  # bufsize = 64, blksize = 8

    # 首先产生数据
    r = []
    s = []
    generate_data(r, s)

    # 将r写入到磁盘中
    # blk_dict['R'] = 0
    blk_dict['R'] = blk_number
    blk_number = write_relation(r, blk_numbers_of_R, blk_number)

    # 将s写入到磁盘中
    # blk_dict['S'] = 16
    # blk_dict['S'] = blk_number
    # blk_number = write_relation(s, blk_numbers_of_S, blk_number)

    # # 选择操作：线性搜索
    # blk_dict[blk_name] = blk_number
    # blk_number = selection_linear('R', 'A', 40, blk_number)

    # # 选择操作：二分搜索
    # blk_number = selection_binary_search('R', 'A', 40, blk_number)

    # # 选择操作：索引搜索
    # blk_number = selection_index('R', 'A', 40, blk_number)

    # # 投影操作
    # blk_name = '%s_project_%s' % (r, a)
    # blk_dict[blk_name] = blk_number
    # blk_number = project('R', 'A', blk_number)

    # # 集合操作
    # blk_number = set_operate('R', 'S', 'intersect', blk_number)

    # # nest-loop-join
    # blk_number = nest_loop_join('R', 'S', blk_numbers_of_R, blk_numbers_of_S, blk_number)

    # # sort_merge_join
    # blk_number = sort_merge_join('R', 'S', blk_number)

    # # hash_join
    # blk_number = hash_join('R', 'S', 5, blk_number)

