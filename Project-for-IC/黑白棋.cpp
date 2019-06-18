#include <iostream>
#include <cstring>
#include <cmath>
#include <iomanip>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <windows.h>
#include <limits> 
using namespace std;
void xuanze();
void chushi();
void qipan(bool);
void youxi();
int mychess, v, m; 
int white = 0, black = 0, blank = 0;
bool xin;
int a[10][10] = {0};
int c[10][10] = {0,0,0,0,0,0,0,0,0,0,
                 0,10,1,9,5,5,9,1,10,0,
				 0,1,1,3,7,7,3,1,1,0,
				 0,9,3,8,4,4,8,3,9,0,
				 0,5,7,4,0,0,4,7,5,0,
				 0,5,7,4,0,0,4,7,5,0,
				 0,9,3,8,4,4,8,3,9,0,
				 0,1,1,3,7,7,3,1,1,0,
				 0,10,1,9,5,5,9,1,10,0,
				 0,0,0,0,0,0,0,0,0,0};
struct dian
{
	int xx;
	int yy;
	int zz;
	int num;
	int score;
};
dian fenzhi[64];
dian t = {0,0,0,0,0}, temp;
bool f1(int h, int x, int y)
{
	int p = 1;
	for (p = 1;;p++)
		if (x - p == 0)
		    return false;
		else
		   if (a[x - p][y] == h)
		       break;
	if (p == 1)
	    return false;
	else
	    for (int i = 1;i < p;i++)
	        if (a[x - i][y] != -h)
	            return false;
	return true;
}
bool f2(int h, int x, int y)
{
	int p = 1;
	for (p = 1;;p++)
		if (x + p == 9)
		    return false;
		else
		   if (a[x + p][y] == h)
		       break;
	if (p == 1)
	    return false;
	else
	    for (int i = 1;i < p;i++)
	        if (a[x + i][y] != -h)
	            return false;
	return true;
}
bool f3(int h, int x, int y)
{
	int p = 1;
	for (p = 1;;p++)
		if (y - p == 0)
		    return false;
		else
		   if (a[x][y - p] == h)
		       break;
	if (p == 1)
	    return false;
	else
	    for (int i = 1;i < p;i++)
	        if (a[x][y - i] != -h)
	            return false;
	return true;
}
bool f4(int h, int x, int y)
{
	int p = 1;
	for (p = 1;;p++)
		if (y + p == 9)
		    return false;
		else
		   if (a[x][y + p] == h)
		       break;
	if (p == 1)
	    return false;
	else
	    for (int i = 1;i < p;i++)
	        if (a[x][y + i] != -h)
	            return false;
	return true;
}
bool f5(int h, int x, int y)
{
	int p = 1;
	for (p = 1;;p++)
		if (x - p == 0||y - p == 0)
		    return false;
		else
		   if (a[x - p][y - p] == h)
		       break;
	if (p == 1)
	    return false;
	else
	    for (int i = 1;i < p;i++)
	        if (a[x - i][y - i] != -h)
	            return false;
	return true;
}
bool f6(int h, int x, int y)
{
	int p = 1;
	for (p = 1;;p++)
		if (x + p == 9||y - p ==0)
		    return false;
		else
		   if (a[x + p][y - p] == h)
		       break;
	if (p == 1)
	    return false;
	else
	    for (int i = 1;i < p;i++)
	        if (a[x + i][y - i] != -h)
	            return false;
	return true;
}
bool f7(int h, int x, int y)
{
	int p = 1;
	for (p = 1;;p++)
		if (x + p == 9||y + p == 9)
		    return false;
		else
		   if (a[x + p][y + p] == h)
		       break;
	if (p == 1)
	    return false;
	else
	    for (int i = 1;i < p;i++)
	        if (a[x + i][y + i] != -h)
	            return false;
	return true;
}
bool f8(int h, int x, int y)
{
	int p = 1;
	for (p = 1;;p++)
		if (x - p == 0||y + p == 9)
		    return false;
		else
		   if (a[x - p][y + p] == h)
		       break;
	if (p == 1)
	    return false;
	else
	    for (int i = 1;i < p;i++)
	        if (a[x - i][y + i] != -h)
	            return false;
	return true;
}
bool check(int h, int x, int y)
{
	if (a[x][y])
	    return false;
	else
        return f1(h,x,y)+f2(h,x,y)+f3(h,x,y)+f4(h,x,y)+f5(h,x,y)+f6(h,x,y)+f7(h,x,y)+f8(h,x,y);
}
void dafen()
{
	for (int j = 0;j < m;j++)
	{
		int s = 0;
		if (f1(-mychess, fenzhi[j].xx, fenzhi[j].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[j].xx - p][fenzhi[j].yy] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            s++;
	    }
	    if (f2(-mychess, fenzhi[j].xx, fenzhi[j].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[j].xx + p][fenzhi[j].yy] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            s++;
	    }
	    if (f3(-mychess, fenzhi[j].xx, fenzhi[j].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[j].xx][fenzhi[j].yy - p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            s++;
        }
	    if (f4(-mychess, fenzhi[j].xx, fenzhi[j].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[j].xx][fenzhi[j].yy + p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            s++;
	    }
	    if (f5(-mychess, fenzhi[j].xx, fenzhi[j].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[j].xx - p][fenzhi[j].yy - p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            s++;
	    }
	    if (f6(-mychess, fenzhi[j].xx, fenzhi[j].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[j].xx + p][fenzhi[j].yy - p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            s++;
	    }
	    if (f7(-mychess, fenzhi[j].xx, fenzhi[j].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[j].xx + p][fenzhi[j].yy + p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            s++;
	    }
	    if (f8(-mychess, fenzhi[j].xx, fenzhi[j].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[j].xx - p][fenzhi[j].yy + p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	        	s++;
	    }
	    fenzhi[j].num = s;
	    fenzhi[j].score = fenzhi[j].zz * fenzhi[j].num;
	}
	return;
}
void paixu()
{
	for (int i = 0;i < m;i++)
	    for (int j = i + 1;j < m;j++)
	        if (fenzhi[i].score < fenzhi[j].score)
	        {
	        	temp = fenzhi[i];
	        	fenzhi[i] = fenzhi[j];
	        	fenzhi[j] = temp;
			}
			for (int i = 0;i < m;i++)
		cout <<fenzhi[i].score<<endl;
	return;
}
bool allcheck(int h)
{
	if (h == mychess)
	{
	    for (int i = 1;i < 9;i++)
	        for (int j = 1;j < 9;j++)
	        {
			    if (check(h, i, j))
	                return true;
	        }
	    return false;
	}
	else
	{
	    for (int i = 0;i < 64;i++)
	        fenzhi[i] = t;
	    m = 0;
        for (int i = 1;i < 9;i++)
	        for (int j = 1;j < 9;j++)
	        {
				if (check(h, i, j))
				{
					fenzhi[m].xx = i;
					fenzhi[m].yy = j;
					fenzhi[m].zz = c[i][j];
					m++;
				}
			}
		return m;
    }
}
void yourturn()
{
	if (allcheck(-mychess))
	{
		dafen();
		paixu();
		a[fenzhi[0].xx][fenzhi[0].yy] = -mychess;
		if (f1(-mychess, fenzhi[0].xx, fenzhi[0].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[0].xx - p][fenzhi[0].yy] == -mychess)
		            break;
			for (int i = 1;i < p;i++)
	            a[fenzhi[0].xx - i][fenzhi[0].yy] = -mychess;
	    }
		if (f2(-mychess, fenzhi[0].xx, fenzhi[0].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[0].xx + p][fenzhi[0].yy] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[fenzhi[0].xx + i][fenzhi[0].yy] = -mychess;   
	    }
	    if (f3(-mychess, fenzhi[0].xx, fenzhi[0].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[0].xx][fenzhi[0].yy - p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[fenzhi[0].xx][fenzhi[0].yy - i] = -mychess;
	    }
	    if (f4(-mychess, fenzhi[0].xx, fenzhi[0].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[0].xx][fenzhi[0].yy + p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[fenzhi[0].xx][fenzhi[0].yy + i] = -mychess;
	    }
	    if (f5(-mychess, fenzhi[0].xx, fenzhi[0].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[0].xx - p][fenzhi[0].yy - p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[fenzhi[0].xx - i][fenzhi[0].yy - i] = -mychess;
	    }
	    if (f6(-mychess, fenzhi[0].xx, fenzhi[0].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[0].xx + p][fenzhi[0].yy - p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[fenzhi[0].xx + i][fenzhi[0].yy - i] = -mychess;
	    }
	    if (f7(-mychess, fenzhi[0].xx, fenzhi[0].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[0].xx + p][fenzhi[0].yy + p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[fenzhi[0].xx + i][fenzhi[0].yy + i] = -mychess;
	    }
	    if (f8(-mychess, fenzhi[0].xx, fenzhi[0].yy))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[fenzhi[0].xx - p][fenzhi[0].yy + p] == -mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[fenzhi[0].xx - i][fenzhi[0].yy + i] = -mychess;
	    }
	}
	else
    {
    	cout << v << "号机器人无路可走，请继续落子" << endl;
		Sleep(500);
	}
}
bool myturn(int x, int y)
{
	if (check(mychess, x, y))
	{
		a[x][y] = mychess;
		if (f1(mychess, x, y))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[x - p][y] == mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[x - i][y] = mychess;
	    }
	    if (f2(mychess, x, y))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[x + p][y] == mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[x + i][y] = mychess;
	    }
	    if (f3(mychess, x, y))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[x][y - p] == mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[x][y - i] = mychess;
	    }
	    if (f4(mychess, x, y))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[x][y + p] == mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[x][y + i] = mychess;
	    }
	    if (f5(mychess, x, y))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[x - p][y - p] == mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[x - i][y - i] = mychess;
	    }
	    if (f6(mychess, x, y))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[x + p][y - p] == mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[x + i][y - i] = mychess;
	    }
	    if (f7(mychess, x, y))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[x + p][y + p] == mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[x + i][y + i] = mychess;
	    }
	    if (f8(mychess, x, y))
		{
			int p = 1;
	        for (p = 1;;p++)
	            if (a[x - p][y + p] == mychess)
		            break;
	        for (int i = 1;i < p;i++)
	            a[x - i][y + i] = mychess;
	    }
		return true;
	}
	else
	{
	    cout << "在这里落子不能吃掉任何对方子，请重新输入坐标" << endl; 
	    return false;
	}
}
void cundang()
{
	char name[40];
	cout << "请输入您希望存档的文件名" << endl <<"如不存在则会自动创建" << endl
	     << "仅按回车键则返回游戏" << endl ;
    int g = 0;
    do
    {
    	cin.ignore(std::numeric_limits<std::streamsize>::max(),'\n');
		cin.getline(name, sizeof(name));
    	if (name[0] == '\0')
    	{
    		qipan(true);
			youxi();
    		g = 1;
		}
		else
		{
			g = 1;
			ofstream fout(name);
			if (!fout)
			{
				cout << "存档失败！" << endl;
				cout << "请检查您所输入的路径是否正确" << endl;
				cout << "请检查您选择的文件是否正被其他程序调用" << endl;
				cout << "请在检查过后重试或按回车键返回游戏" << endl; 
				g = 0;
				continue; 
			}
	        fout << v << "  " << mychess << "  ";
	        fout << black << "  " << white << "  " << blank << endl;
	        for (int i = 0;i < 10;i++)
	            for (int j = 0;j < 10;j++)
		            fout << a[i][j] << endl;
			fout.close();
		}
	}
	while (g == 0);	
}
void tishi()
{
	cout << "是否保存当前棋局？" << endl << endl;
	cout << "如需要保存  请输入1" << endl;
	cout << "如不需保存  请输入0" << endl << endl;
	char o;
	int g = 0;
	do
	{
		cin >> o;
		switch (o)
		{
			case '0':xuanze();g = 1;return;break;
			case '1':cundang();g = 1;return;break;
			default:
				{
					cout << endl;
		            cout << "输入的不是0、1中的一个" << endl;
		            cout << "请重新输入" << endl << endl; 	
				}
		};
	}
	while (g == 0);
}
void tuichu()
{
	cout << "您确定要退出吗？" << endl;
	cout << "确定退出 请输入1" << endl;
	cout << "返回游戏 请输入0" << endl << endl;
	char o;
	int g = 0;
	do
	{
		cin >> o;
		switch (o)
		{
			case '0':qipan(true);youxi();g = 1;return;break;
			case '1':tishi();g = 1;return;break;
			default:
				{
					cout << endl;
		            cout << "输入的不是0、1中的一个" << endl;
		            cout << "请重新输入" << endl << endl; 	
				}
		};
	}
	while (g == 0);
 } 
void youxi()
{
	if (mychess == -1&&xin)
	{
	    Sleep(500);
		yourturn();
	    qipan(true);
	}
	xin = false;
	while (blank&&(allcheck(mychess)||allcheck(-mychess)))
	{
		char p, q;
		int x, y;
		int g = 0;
		do
		{
		    bool l = allcheck(mychess);
			if (l)
		    {
			    cin >> p;
			    switch (p)
		        {
			        case '0':cundang();g = 1;return;break;
			        case '9':tuichu();g = 1;return;break;
			        case '1':
			        case '2':
			        case '3':
			        case '4':
			        case '5':
			        case '6':
			        case '7':
			        case '8':cin >> q;
			                 g = 1;
				             switch (q)
				             {
				                 case '1':
				         	     case '2':
				         	     case '3':
				         	     case '4':
				         	     case '5':
				         	     case '6':
				         	     case '7':
				         	     case '8':x = p - '0';
				         	              y = q - '0';
									      g = myturn(x, y);
									      if (g == 1)
									      {
									 	      qipan(true);
									 	      Sleep(1000);
									 	      yourturn();
									 	      qipan(true);
									      }
										  break;
				         	     default:
				         		      {
				         			   cout << endl; 
						               cout << "您输入的不是正确的坐标" << endl;
						               cout << "请重新输入" << endl; 
						               g = 0; 
								       }
						     };break;
				    default:
					    {
						    cout << endl; 
					    	cout << "您输入的不是0、9或正确的坐标" << endl;
						    cout << "请重新输入" << endl; 
				        }
		        };
		    }
		    else
		    {
		    	cout << "您无路可走，" << v << "号机器人将继续落子" <<endl; 
				Sleep(1000);
				yourturn();
		    	qipan(true);
		    	g = 1;
			}
		}
		while (g == 0);
	};
}
void qizi(int b)
{
	if (b == 1)
	    cout << "●";
	if (b == -1)
	    cout << "○";
    if (b == 0)
	    cout << "  ";
	return;
}
void qipan(bool k) 
{
    system("cls");
	white = 0;
	black = 0;
	blank = 0;
	for (int i = 1;i < 9;i++)
	    for (int j = 1;j < 9;j++)
	    {
	    	if (a[i][j] == -1) white++;
	    	if (a[i][j] == 1) black++;
	    	if (a[i][j] == 0) blank++;
		}
    cout << "    1   2   3   4   5   6   7   8    " << endl;
	cout << "  ┏━┳━┳━┳━┳━┳━┳━┳━┓" << endl;
	for (int i = 1;i < 8;i++)
	{
	    cout << i << " ┃";
		qizi(a[i][1]);
		cout << "┃";
		qizi(a[i][2]);
		cout << "┃";
		qizi(a[i][3]);
		cout << "┃";
		qizi(a[i][4]);
		cout << "┃";
		qizi(a[i][5]);
		cout << "┃";
		qizi(a[i][6]);
		cout << "┃";
		qizi(a[i][7]);
		cout << "┃";
		qizi(a[i][8]);
		cout << "┃" << endl;										
        cout << "  ┣━╋━╋━╋━╋━╋━╋━╋━┫" << endl;
    }
	cout << "8 ┃";
	qizi(a[8][1]);
	cout << "┃";
	qizi(a[8][2]);
	cout << "┃";
	qizi(a[8][3]);
	cout << "┃";
	qizi(a[8][4]);
	cout << "┃";
	qizi(a[8][5]);
	cout << "┃";
	qizi(a[8][6]);
	cout << "┃";
	qizi(a[8][7]);
	cout << "┃";
	qizi(a[8][8]);
	cout << "┃" << endl;	 
    cout << "  ┗━┻━┻━┻━┻━┻━┻━┻━┛" << endl;	
	if (blank == 0||(!allcheck(mychess)&&!allcheck(-mychess)))
	{
		if (black == white)
		    cout << "本局是平局，黑子" << black << "枚，白子" << white << "枚" << endl << endl;
		else
		{
		    if (black > white&&mychess == 1)
			    cout << "本局黑方（你）胜，" << "黑子" << black << "枚，白子" << white << "枚" <<endl << endl;
			if (black > white&&mychess == -1)
			    cout << "本局黑方（" << v <<"号机器人）胜，" << "黑子" << black << "枚，白子" << white << "枚" <<endl << endl;
		    if (black < white&&mychess == -1)
			    cout << "本局白方（你）胜，" << "黑子" << black << "枚，白子" << white << "枚" <<endl << endl;
			if (black < white&&mychess == 1)
			    cout << "本局白方（" << v <<"号机器人）胜，" << "黑子" << black << "枚，白子" << white << "枚" <<endl << endl;
		}
	    cout << "再来一局    请输入1" << endl << endl;
	    cout << "返回主菜单  请输入2" << endl << endl;  
	    int g = 0;
	    do
	    {
		    char o;
		    cin >> o;
		    switch (o)
		    {
		    	case '1':chushi();g = 1;return;break;
		    	case '2':xuanze();g = 1;return;break;
			    default:
			    	{
		    	        cout << endl;
			            cout << "输入的不是1、2中的一个" << endl;
			            cout << "请重新输入" << endl << endl; 	
			    	}
	    	};
    	}
    	while (g == 0);
	}
	else
	{
		cout << "        黑子●： " << black << "  白子○： " << white << endl << endl;
		cout << "请输入您希望落子的位置 例如您想在第三行第五列落子 请输入“3  5”" << endl; 
		cout << "如要存档       请输入0" << endl << "如要返回主菜单 请输入9" << endl << endl; 
		if (k)
		    return;
		else
		    youxi();
    }
}
void chushi()
{
	system("cls");
	cout << "请选择您希望执先手(黑棋）还是后手（白棋）" << endl << endl;
	cout << "选择先手 请输入1" << endl << endl;
	cout << "选择后手 请输入2" << endl << endl;
	cout << "返回主菜单 请输入3" << endl << endl; 
	mychess = 0;
	xin = true;
	int g = 0;
	do
	{
	    char o;
	    cin >> o;
	    switch (o)
	    {
		    case '1':mychess = 1;g = 1;break;
		    case '2':mychess = -1;g = 1;break;
		    case '3':xuanze();return;break;
		    default:
			{
			    cout << endl;
			    cout << "输入的不是1、2、3中的一个" << endl;
			    cout << "请重新输入" << endl << endl; 	
			}
		};
	}
	while (g == 0);
	for (int i = 0;i < 10;i++)
	    for (int j = 0;j < 10;j++)
	        a[i][j] = 0;
	a[4][4] = -1;
	a[4][5] = 1;
	a[5][4] = 1;
	a[5][5] = -1;
	qipan(!xin);
}
void duqu()
{
	system("cls");
	xin = false;
	char name[50];
	cout << "请输入您希望读取的文件名称" << endl 
	     << "仅按回车键则返回主菜单" <<endl;
	int g = 0;     
	do
	{
    	cin.ignore(std::numeric_limits<std::streamsize>::max(),'\n');
		cin.getline(name,sizeof(name));
	    if (name[0] == '\0')
	    {
	        xuanze();
	        g = 1;
	    }
	    else
	    {
		    g = 1;
	        ifstream fin(name);
	        if (!fin)
	        {
		        cout << "存档打开失败！" << endl;
		        cout << "请检查您所输入的文件名及路径是否存在并正确" << endl << name << endl ;
		        cout << "请检查该文件是否正被其他程序调用" << endl;
		        cout << "请在检查过后重试或按回车返回主菜单" << endl << endl;
		        g = 0;
				continue; 
	        }
	        fin >> v >> mychess;
	        fin >> black >> white >> blank;
	        for (int i = 0;i < 10;i++)
	            for (int j = 0;j < 10;j++)
		            fin >> a[i][j];
		    fin.close();
	        qipan(false);
	    }
	}
	while (g == 0);
}
void guize()
{
    system("cls");
	cout << "这是一款经典的黑白棋游戏" << endl << endl; 
	cout << "游戏中棋盘共有8行8列，共64格" << endl << endl;
	cout << "开局时棋盘正中央的4格先置放黑白相隔的4枚棋子" << endl << endl;	
	cout << "先行双方轮流落子，只要落子和棋盘上任一枚己方的棋子在一条线上横直斜线皆可夹着对方棋子" << endl << endl; 
	cout << "就能将对方的这些棋子转变为己方棋子" << endl << endl;
	cout << "如果在任一位置落子都不能夹住对手的任一颗棋子" << endl << endl;
	cout << "就要让对手下子，当双方皆不能下子游戏就结束" << endl << endl;
	cout << "子多的一方胜" << endl << endl;
	cout << "好的，现在已经清楚游戏规则了，请输入任意数或字母返回" << endl << endl;
	char o;
	cin >> o; 
	xuanze();
}
void xuanze()
{
	system("cls");
	cout << "输入相应序号，开启游戏人生" << endl << endl;
	cout << "开始新游戏" << "   " << "请输入1" << endl << endl;
	cout << "读取存档" << "     " << "请输入2" << endl << endl;
	cout << "了解游戏规则" << " " << "请输入3"  << endl << endl;
	cout << "退出游戏" << "     " << "请输入4" << endl << endl;
	char o;
	int g = 0;
	do
	{
    cin >> o;
	switch (o)
	{
		case '1':chushi(); g = 1; break;
		case '2':duqu(); g = 1; break;
		case '3':guize(); g = 1; break;
		case '4':return;
		default:
		{
		    cout << endl;
			cout << "输入的不是1、2、3、4中的一个" << endl;
			cout << "请重新输入" << endl << endl; 
		}
	 } ;
    }
	 while (g == 0);
}
int main()
{
	cout << "欢迎来和我玩黑白棋 " << endl << endl;
	srand(time(0));
	v = rand();
	cout << "这里是" << v << "号机器人与您对弈" << endl << endl;
	cout << "输入相应序号，开启游戏人生" << endl << endl;
	cout << "开始新游戏" << "   " << "请输入1" << endl << endl;
	cout << "读取存档" << "     " << "请输入2" << endl << endl;
	cout << "了解游戏规则" << " " << "请输入3"  << endl << endl;
	cout << "退出游戏" << "     " << "请输入4" << endl << endl;
	char o;
	int g = 0;
	do
	{
        cin >> o;
	    switch (o)
	    {
	    	case '1':chushi(); g = 1; break;
	    	case '2':duqu(); g = 1; break;
	    	case '3':guize(); g = 1; break;
	    	case '4':return 0;
	    	default:
	    	{
	    	    cout << endl;
	    		cout << "输入的不是1、2、3、4中的一个" << endl;
	    		cout << "请重新输入" << endl << endl; 
	    	}
    	};
    }
	while (g == 0);
	return 0;
 } 
