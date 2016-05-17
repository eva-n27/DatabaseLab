/*
* extmem.c
* Zhaonian Zou
* Harbin Institute of Technology
* Jun 22, 2011
*/

#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include "extmem.h"

//初始化缓冲区，其输入参数bufSize为缓冲区大小（单位：字节），
//blkSize为块的大小（单位：字节），buf为指向待初始化的缓冲区的指针。
//若缓冲区初始化成功，则该函数返回指向该缓冲区的地址；否则，返回NULL。
Buffer *initBuffer(size_t bufSize, size_t blkSize, Buffer *buf)
{
	int i;

	buf->numIO = 0;
	buf->bufSize = bufSize;
	buf->blkSize = blkSize;
	buf->numAllBlk = bufSize / (blkSize + 1);
	buf->numFreeBlk = buf->numAllBlk;
	buf->data = (unsigned char*)malloc(bufSize * sizeof(unsigned char));

	if (!buf->data)
	{
		perror("Buffer Initialization Failed!\n");
		return NULL;
	}

	memset(buf->data, 0, bufSize * sizeof(unsigned char));
	return buf;
}

//释放缓冲区buf占用的内存空间。
void freeBuffer(Buffer *buf)
{
	free(buf->data);
}

//在缓冲区buf中申请一个新的块。若申请成功，则返回该块的起始地址；否则，返回NULL。
unsigned char *getNewBlockInBuffer(Buffer *buf)
{
	unsigned char *blkPtr;

	if (buf->numFreeBlk == 0)
	{
		perror("Buffer is full!\n");
		return NULL;
	}

	blkPtr = buf->data;

	//buf->blkSize + 1是因为每个块都有一个标志位，BLOCK_AVAILABLE块可用，BLOCK_UNAVAILABLE不可用
	while (blkPtr < buf->data + (buf->blkSize + 1) * buf->numAllBlk)
	{
		if (*blkPtr == BLOCK_AVAILABLE)//BLOCK_AVAILABLE = 0
			break;
		else
			blkPtr += buf->blkSize + 1;
	}

	*blkPtr = BLOCK_UNAVAILABLE;//BLOCK_UNAVAILABLE = 1，表示这块block已经被使用了
	buf->numFreeBlk--;
	return blkPtr + 1;//返回的是缓冲区的起始位，跳过标志位
}

//解除块blk对缓冲区内存的占用，即将blk占据的内存区域标记为可用。
void freeBlockInBuffer(unsigned char *blk, Buffer *buf)
{
	*(blk - 1) = BLOCK_AVAILABLE;
	buf->numFreeBlk++;
}

//从磁盘上删除地址为addr的磁盘块内的数据。若删除成功，则返回0；否则，返回-1。
int dropBlockOnDisk(unsigned int addr)
{
	char filename[40];

	sprintf(filename, "%d.blk", addr);
	//remove()函数用于删除指定的文件，其原型如下：
    //int remove(char * filename);
	//成功则返回0，失败则返回-1，错误原因存于errno。
	if (remove(filename) == -1)
	{
		perror("Dropping Block Fails!\n");
		return -1;
	}

	return 0;
}

//将磁盘上地址为addr的磁盘块读入缓冲区buf。
//若读取成功，则返回缓冲区内该块的地址，缓冲区buf的I/O次数加1。；
//否则，返回NULL。
unsigned char *readBlockFromDisk(unsigned int addr, Buffer *buf)
{
	char filename[40];
	unsigned char *blkPtr, *bytePtr;
	char ch;

	if (buf->numFreeBlk == 0)
	{
		perror("Buffer Overflows!\n");
		return NULL;
	}

	blkPtr = buf->data;

	while (blkPtr < buf->data + (buf->blkSize + 1) * buf->numAllBlk)
	{
		if (*blkPtr == BLOCK_AVAILABLE)
			break;
		else
			blkPtr += buf->blkSize + 1;
	}

	sprintf(filename, "%d.blk", addr);
	FILE *fp = fopen(filename, "r");

	if (!fp)
	{
		perror("Reading Block Failed!\n");
		return NULL;
	}

	//读成功后再确认申请这个块
	*blkPtr = BLOCK_UNAVAILABLE;
	blkPtr++;//移动到缓存的数据区
	bytePtr = blkPtr;

	while (bytePtr < blkPtr + buf->blkSize)
	{
		ch = fgetc(fp);
		*bytePtr = ch;
		bytePtr++;
	}

	fclose(fp);
	buf->numFreeBlk--;
	buf->numIO++;
	return blkPtr;//返回缓存的数据区
}

//将缓冲区buf内的块blk写入磁盘上地址为addr的磁盘块。
//若写入成功，则返回0；
//否则，返回-1。同时，缓冲区buf的I/O次数加1。
int writeBlockToDisk(unsigned char *blkPtr, unsigned int addr, Buffer *buf)
{
	char filename[40];
	unsigned char *bytePtr;

	sprintf(filename, "%d.blk", addr);
	FILE *fp = fopen(filename, "w");

	if (!fp)
	{
		perror("Writing Block Failed!\n");
		return -1;
	}

	for (bytePtr = blkPtr; bytePtr < blkPtr + buf->blkSize; bytePtr++)
		fputc((int)(*bytePtr), fp);

	fclose(fp);
	*(blkPtr - 1) = BLOCK_AVAILABLE;
	buf->numFreeBlk++;
	buf->numIO++;
	return 0;
}
