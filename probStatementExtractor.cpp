#include <bits/stdc++.h>
using namespace std;

int main()
{
    freopen("temphtml.html","r",stdin);
    freopen("probstatement.txt","w",stdout);
    string s;
    int f=0;
    while(getline(cin,s))
    {
        istringstream is(s);
        string cur;
        while(is>>cur)
        {
            if (cur == "class=Section1>")
                f=1;
        }
        if (f==1){
            while(getline(cin,s))
            {
                istringstream is(s);
                string cur;
                while(is>>cur)
                {
                    if (cur == "<h1>Input</h1>")
                        return 0;
                    cout<<cur<<" ";
                }
                cout<<endl;
            }
        }
    }
    return 0;
}
