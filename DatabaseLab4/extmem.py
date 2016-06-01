# __author__ = 'Xiang'
# coding:utf-8

import os


def drop_block_on_disk(addr):
    """
    从磁盘上删除地址为addr的磁盘块内的数据。
    :return:若删除成功，则返回True；否则，返回False。
    """
    filename = "%s.blk" % addr
    if os.path.exists(filename):
        os.remove(filename)
        print "删除成功"
        return True
    print "删除失败"
    return False


class Buffer:
    """
    Buffer的结构体
    """
    def __init__(self, buf_size, blk_size):
        """
        初始化
        """
        self.numIO = 0
        self.bufSize = buf_size
        self.blkSize = blk_size
        self.numAllBlk = buf_size / (blk_size + 1)
        self.numFreeBlk = self.numAllBlk
        self.Data = []
        for i in range(self.numAllBlk):
            self.Data.append([False])  # False表示块为空，True表示块中存放了数据

    def __del__(self):
        """
        析构函数
        :return:无
        """
        print "缓冲区已释放"

    def get_new_block_in_buffer(self):
        """
        在缓冲区buf中申请一个新的块。
        :return:若申请成功，则返回该块的起始地址（索引）；否则，返回NULL（-1）。
        """
        if self.numFreeBlk == 0:
            print "Buffer is full!"
            return -1

        for i in range(self.numAllBlk):
            if not self.Data[i][0]:
                self.Data[i][0] = True
                self.numFreeBlk -= 1
                return i  # 找到第一个非空的块

    def free_block_in_buffer(self, index):
        """
        解除块blk对缓冲区内存的占用，即将blk占据的内存区域标记为可用
        :return:无
        """
        self.Data[index] = [False]
        self.numFreeBlk += 1

    def read_bloc_from_disk(self, addr):
        """
        将磁盘上地址为addr的磁盘块读入缓冲区buf。
        :return:若读取成功，则返回缓冲区内该块的索引，缓冲区buf的I/O次数加1。否则，返回-1。
        """
        if self.numFreeBlk == 0:
            print "缓存区已满"
            return -1

        index = 0
        for i in range(self.numAllBlk):
            if not self.Data[i][0]:
                index = i  # 找到第一个非空的块

        filename = "%s.blk" % addr
        f = open(filename)
        if not f:
            print "打开文件失败"
            return -1

        # 成功读入后再修改
        self.Data[index] = [True]
        self.numFreeBlk -= 1
        self.numIO += 1

        data = []
        lines = f.readlines()
        for line in lines:
            data.extend(line)

        self.Data[index].append(data)
        f.close()
        return index

    def write_block_to_disk(self, addr, index):
        """
        将缓冲区buf内的块blk写入磁盘上地址为addr的磁盘块。
        :return:若写入成功，则返回True,同时,缓冲区buf的I/O次数加1；否则，返回False。
        """
        filename = "%s.blk" % addr
        f = open(filename, 'w')

        if not f:
            print "打开文件失败"
            return False

        f.writelines(self.Data[index][1])
        f.close()
        self.Data[index] = [False]  # 写入后该块释放
        self.numFreeBlk += 1
        self.numIO += 1
        return True


if __name__ == '__main__':
    a = ['1\n', '2', '3', '4']
    b = open('1.txt', 'w')
    b.writelines(a)

