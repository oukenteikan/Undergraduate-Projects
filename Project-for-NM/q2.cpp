#include<cstdio>
#include<cmath>

#define pi 3.1415926535897932

double f(double);

int main()
{
    float p0=0.9,h=0.1,k=0.1;
    int a=1,t=1,l=1,m=10,n=10,lambda=1;
    double w[11][11];


    for(int j=1;j<=n;j++)
    {
        w[0][j]=p0;
    }

    w[0][0]=f(0);
    w[m][0]=f(l);

    for(int i=1;i<m;i++)
    {
        w[i][0]=f(i*h);
        w[i][1]=lambda*(f((i+1)*h)+f((i-1)*h))/2.0;
    }
    w[m][0]=(4*w[m-1][0]-w[m-2][0])/3.0;
    w[m][1]=(4*w[m-1][1]-w[m-2][1])/3.0;   //导数近似公示来近似w[m][i]

    for(int j=1;j<n;j++)
    {
        for(int i=1;i<m;i++)
        {
            w[i][j+1]=lambda*(w[i+1][j]+w[i-1][j])-w[i][j-1];
        }
        w[m][j+1]=(4*w[m-1][j+1]-w[m-2][j+1])/3.0;
    }
    printf("p(0.5.0.5)=%lf p(0.5,1)=%.10lf\n",w[5][5],w[5][10]);

    return 0;
}

double f(double x)
{
    return 0.9*cos(2*pi*x);
}
