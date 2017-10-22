#include <cstdio>
#include <cstring>
#include <cmath>
#include <cstdlib>
#include <string>
#include <vector>
#include <queue>
#include <bitset>
#include <stack>
#include <algorithm>
#include <utility>
using namespace std;
const int inf = 100*100*100*100;
const int minf = -100*100*100*100;
typedef pair<int,int> ii;
typedef pair<ii,int> iii;
typedef vector<int> vi;
typedef vector<ii> vii;
typedef vector<vi> vvi;
typedef vector<vii> vvii;
typedef long long ll;
typedef unsigned long long llu;

int fact(int n) {
	if (n == 1) return 1;
	return n*fact(n-1);
}

int main () {
	int N;
	int fats[9];
	for (int i = 1; i <= 8; i++) fats[i] = fact(i);
	while (scanf ("%d",&N) != EOF) {
		int total = 0;
		int ind = 8;
		while (N) {
			while (fats[ind] > N) ind--;
			N-=fats[ind];
			total++;
		}

		printf ("%d\n",total);
	}
	return 0;
}