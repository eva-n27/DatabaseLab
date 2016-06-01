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
        new_r = relation.relation_r(random.randint(1, 40), random.randint(1, 1000))
        r_.append(new_r)

    # 产生s的元组，共224个
    for i_ in range(224):
        new_s = relation.relation_s(random.randint(20, 60), random.randint(1, 1000))
        s_.append(new_s)


if __name__ == '__main__':
    # 磁盘文件号
    blk_number = 0

    # 首先产生数据
    r = []
    s = []
    generate_data(r, s)

    # 创建缓冲区
    # 元组为8个字节，所以我就设计块大小为8个元组，缓冲区大小为65个元组
    buffer_ = extmem.Buffer(65, 8)  # bufsize = 65, blksize = 8

    # 将r写入到磁盘中
    for i in range(16):
        buffer_index = buffer_.get_new_block_in_buffer()  # 申请到的缓冲区的索引
        data = []
        for j in range(7):
            data.extend([str(r[i].attr_a), str(' '),  str(r[i].attr_b), str(' ')])
        data.append(str(blk_number + 1))
        if i == 15:
            data[-1] = str(0)
        buffer_.Data[buffer_index].append(data)
        if not buffer_.write_block_to_disk(blk_number, buffer_index):
            print "写入磁盘文件号 %s 失败" % blk_number
            exit()
        blk_number += 1

    # 将s写入到磁盘中
    for i in range(32):
        buffer_index = buffer_.get_new_block_in_buffer()  # 申请到的缓冲区的索引
        data = []
        for j in range(7):
            data.extend([str(s[i].attr_c), str(' '),  str(s[i].attr_d), str(' ')])
        data.append(str(blk_number + 1))
        if i == 31:
            data[-1] = str(0)
        buffer_.Data[buffer_index] = data
        if not buffer_.write_block_to_disk(blk_number, buffer_index):
            print "写入磁盘文件号 %s 失败" % blk_number
            exit()
        blk_number += 1


