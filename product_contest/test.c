#include <stdio.h>

void main() 
{
	int i, j, count = 1;
	long sum = 0;

	printf("1~1000 사이의 수 중에서 소수를 구하는 프로그램 \n");

	printf("%d\t", 1);

	for (i = 1; i <= 1000; i++) {
		for (j = 2; j < i; j++) {
			if ((i % j) == 0)
				break;
		}

		if (i == j) {
			printf("%d\t", i);
			count++;

			// if ((count % 8) == 0)
				// printf("\n");
		}
	}
	printf("\n1부터 1000 사이의 소수는 %d개이다. \n", count);
}