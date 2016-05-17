#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "extmem.h"
#define true 1
#define MAX_SIZE 100
#define BLOCK_SIZE 64

typedef struct relation{
	int attributeA;
	int attributeB;
}relation;

relation R[112], S[224];

unsigned char *blk;
Buffer buf;
unsigned int baseAddr = 31415926, pointerAddr = baseAddr;
unsigned int *nextblk = &pointerAddr;

void genExperiment(){
	int i;
	for (i = 0; i < 112; i++){
		R[i].attributeA = (rand() % (40) + 1);
		R[i].attributeB = (rand() % (1000) + 1);
	}
	for (i = 0; i < 224; i++){
		S[i].attributeA = (rand() % (60 - 19) + 20);
		S[i].attributeB = (rand() % (1000) + 1);
	}
}

void guide(){
	int i;
	/* Initialize the buffer */
	if (!initBuffer(20, 8, &buf)){
		perror("Buffer Initialization Failed!\n");
		//return -1;
	}

	/* Get a new block in the buffer */
	blk = getNewBlockInBuffer(&buf);

	/* Fill data into the block */
	for (i = 0; i < 8; i++)
		*(blk + i) = 'a' + i;

	/* Write the block to the hard disk */
	if (writeBlockToDisk(blk, 31415926, &buf) != 0){
		perror("Writing Block Failed!\n");
		//return -1;
	}

	/* Read the block from the hard disk */
	if ((blk = readBlockFromDisk(31415926, &buf)) == NULL){
		perror("Reading Block Failed!\n");
		//return -1;
	}

	/* Process the data in the block */
	for (i = 0; i < 8; i++)
		printf("%c", *(blk + i));

	printf("\n");
	printf("# of IO's is %d\n", buf.numIO); /* Check the number of IO's */
}

bool init(){
	int i, j;
	if (!initBuffer(520, 64, &buf)){
		perror("Buffer Initialization Failed!\n");
		return -1;
	}
	relation *Wblk;
	genExperiment();
	//  TAT 
	for (i = 0; i < 16; i++){
		Wblk = (relation*)getNewBlockInBuffer(&buf);
		for (j = 0; j < 7; j++){
			//printf("(%d,%d)\n",R[i*7+j].attributeA,R[i*7+j].attributeB);
			*(Wblk + j) = *(R + i * 7 + j);
		}
		relation SpecialRelation = { 0, *nextblk };
		*(Wblk + 7) = SpecialRelation;
		if (writeBlockToDisk((unsigned char *)Wblk, pointerAddr, &buf) != 0){
			perror("Writing Block Failed!\n");
			return -1;
		}
		pointerAddr += BLOCK_SIZE;
	}

	for (i = 0; i < 32; i++){
		Wblk = (relation*)getNewBlockInBuffer(&buf);
		for (int j = 0; j < 7; j++){
			//printf("(%d,%d)\n",S[i*7+j].attributeA,S[i*7+j].attributeB);
			*(Wblk + j) = *(S + i * 7 + j);
		}
		relation SpecialRelation = { 0, *nextblk };
		*(Wblk + 7) = SpecialRelation;
		if (writeBlockToDisk((unsigned char *)Wblk, pointerAddr, &buf) != 0){
			perror("Writing Block Failed!\n");
			return -1;
		}
		pointerAddr += BLOCK_SIZE;
	}
}

bool Selection(){
	if (!initBuffer(520, 64, &buf)){
		perror("Buffer Initialization Failed!\n");
		return -1;
	}
	blk = getNewBlockInBuffer(&buf);
	relation *RBlk;
	int count = 0;
	int i, j;

	for (i = 0; i < 16; i++) {
		if ((RBlk = (relation *)readBlockFromDisk(baseAddr + i*BLOCK_SIZE, &buf)) == NULL) {
			perror("Reading Block Failed!\n");
			return -1;
		}
		for (j = 0; j < 7; j++) {
			//printf("(%d,%d)\n",RBlk[j].attributeA,RBlk[j].attributeB);
			if (RBlk[j].attributeA == 40) {
				printf("=====>(%d,%d)\n", RBlk[j].attributeA, RBlk[j].attributeB);
				*(unsigned int*)(blk + count * 8) = RBlk[j].attributeA; *(unsigned int*)(blk + count * 8 + 4) = RBlk[j].attributeB;
				count++;
				if (count == 7){
					*(blk + count * 8) = 0; *(blk + count * 8 + 4) = *nextblk;
					if (writeBlockToDisk(blk, pointerAddr, &buf) != 0){
						perror("Writing Block Failed!\n");
						return -1;
					}
					pointerAddr += BLOCK_SIZE;
					count = 0;
					freeBlockInBuffer(blk, &buf);
					blk = getNewBlockInBuffer(&buf);
				}
			}
		}
		freeBlockInBuffer((unsigned char *)RBlk, &buf);
	}
	for (i = 0; i < 32; i++) {
		if ((RBlk = (relation *)readBlockFromDisk(baseAddr + i*BLOCK_SIZE, &buf)) == NULL) {
			perror("Reading Block Failed!\n");
			return -1;
		}
		for (j = 0; j < 7; j++) {
			//printf("(%d,%d)\n",RBlk[j].attributeA,RBlk[j].attributeB);
			if (RBlk[j].attributeA == 60) {
				printf("=====>(%d,%d)\n", RBlk[j].attributeA, RBlk[j].attributeB);
				*(unsigned int*)(blk + count * 8) = RBlk[j].attributeA; *(unsigned int*)(blk + count * 8 + 4) = RBlk[j].attributeB;
				count++;
				if (count == 7){
					*(blk + count * 8) = 0; *(blk + count * 8 + 4) = *nextblk;
					if (writeBlockToDisk(blk, pointerAddr, &buf) != 0){
						perror("Writing Block Failed!\n");
						return -1;
					}
					pointerAddr += BLOCK_SIZE;
					count = 0;
					freeBlockInBuffer(blk, &buf);
					blk = getNewBlockInBuffer(&buf);
				}
			}
		}
		freeBlockInBuffer((unsigned char *)RBlk, &buf);
	}
	*(unsigned int *)(blk + 60) = *nextblk;
	if (writeBlockToDisk(blk, pointerAddr, &buf) != 0){
		perror("Writing Block Failed!\n");
		return -1;
	}
	pointerAddr += BLOCK_SIZE;
	freeBlockInBuffer(blk, &buf);
}

bool projection(){
	if (!initBuffer(520, 64, &buf)){
		perror("Buffer Initialization Failed!\n");
		return -1;
	}
	blk = getNewBlockInBuffer(&buf);

	relation *RBlk;
	int count = 0;
	int i, j;
	for (i = 0; i < 16; i += 2) {
		if ((RBlk = (relation *)readBlockFromDisk(baseAddr + i*BLOCK_SIZE, &buf)) == NULL) {
			perror("Reading Block Failed!\n");
			return -1;
		}
		for (j = 0; j < 8; j++) {
			//printf("(%d,%d)\n",RBlk[j].attributeA,RBlk[j].attributeB);
			*(unsigned int *)(blk + j * 4) = RBlk[j].attributeA;
		}
		freeBlockInBuffer((unsigned char *)RBlk, &buf);
		if ((RBlk = (relation *)readBlockFromDisk(baseAddr + (i + 1)*BLOCK_SIZE, &buf)) == NULL) {
			perror("Reading Block Failed!\n");
			return -1;
		}
		for (j = 0; j < 7; j++) {
			//printf("(%d,%d)\n",RBlk[j].attributeA,RBlk[j].attributeB);
			*(unsigned int *)(blk + (j + 8) * 4) = RBlk[j].attributeA;
		}
		*(unsigned int *)(blk + j * 4) = *nextblk;
		if (writeBlockToDisk(blk, pointerAddr, &buf) != 0){
			perror("Writing Block Failed!\n");
			return -1;
		}
		pointerAddr += BLOCK_SIZE;
		freeBlockInBuffer((unsigned char *)RBlk, &buf);
		freeBlockInBuffer(blk, &buf);
		blk = getNewBlockInBuffer(&buf);
	}
	freeBlockInBuffer(blk, &buf);
}

bool NLJ(){
	int i, j, k, l;
	if (!initBuffer(520, 64, &buf)){
		perror("Buffer Initialization Failed!\n");
		return -1;
	}
	blk = getNewBlockInBuffer(&buf);
	relation *RBlk1, *RBlk2;

	for (i = 0; i < 16; i++){
		if ((RBlk1 = (relation *)readBlockFromDisk(baseAddr + i*BLOCK_SIZE, &buf)) == NULL) {
			perror("Reading Block Failed!\n");
			return -1;
		}
		for (j = 0; j < 7; j++){
			unsigned int RA = RBlk1[j].attributeA;
			if (RA < 20){
				continue;
			}
			unsigned int address = RBlk1[7].attributeB;
			for (k = 0; k < 32; k++){
				if ((RBlk2 = (relation *)readBlockFromDisk(address) == NULL)) {
					perror("Reading Block Failed!\n");
					return -1;
				}
				for (l = 0; l < 7; l++){
					unsigned int SC = RBlk2[l].attributeA;
					if (SC > 40){
						continue;
					}
					if (RA == SC){
						/* TODO */
					}
				}
				freeBlockInBuffer((unsigned char *)RBlk2, &buf);
			}
		}
	}
}

int main(int argc, char **argv){
	srand((unsigned)time(NULL));
	int i, op;
	if (init()){
		printf("init error.\n");
	}

	while (true){
		printf("1. Selection\n");
		printf("2. projection\n");
		printf("3. NLJ\n");
		printf("4. Show Disk\n");
		scanf("%d", &op);
		if (op == 1){
			Selection() == true ? printf("Success.\n") : printf("Error.\n");
		}
		else if (op == 2){
			projection() == true ? printf("Success.\n") : printf("Error.\n");
		}
		else if (op == 3){
			NLJ() == true ? printf("Success.\n") : printf("Error.\n");
		}
		else if (op == 4){
			printf("Enter the disk address :\n");
			unsigned int address;
			scanf("%d", &address);
			relation *RBlk;

			if ((RBlk = (relation *)readBlockFromDisk(address, &buf)) == NULL){
				perror("Reading Block Failed!\n");
				return -1;
			}
			printf("\n");
			for (int i = 0; i < 8; i++){
				printf("(%d,%d)\n", RBlk[i].attributeA, RBlk[i].attributeB);
			}
			freeBlockInBuffer((unsigned char *)RBlk, &buf);
		}
		else{
			break;
		}
	}
}