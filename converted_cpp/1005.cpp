#include &lt;bits/stdc++.h&gt;
using namespace std;
int main ()
{
    int t;
    scanf("%d",&t);
    int cas=1;
    while (t--){
        int n,i,k;
        unsigned long long int ans=1;
        scanf("%d %d",&n,&k);
        printf("Case %d: ",cas++);
        for (i=1;i&lt;=k;i++){
            ans=ans*n*n;
            ans=ans/i;
            n--;
        }
        cout&lt;&lt;ans&lt;&lt;endl;
    }
    return 0;
}

