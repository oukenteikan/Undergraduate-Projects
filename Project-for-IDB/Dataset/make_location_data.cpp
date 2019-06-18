#include <iostream>
#include <iomanip>
#include <vector>
#include <string> 
#include <fstream>
#include <cstdlib>
#include <ctime>
using namespace std;
class location
{
	public:
		location(string row_, string col_):row(row_), col(col_){}
		string row, col;
		void print(ofstream& fout)
		{
			fout << "(\"Haidian District\", \"" << row << "\", \"" << col << "\")";
			return;
		}
};
int main()
{
	string street[22] = {"Wanshoulu", "Shangdi" ,"Zhongguancun"
						, "Balizhuang", "Beixiaguan", "Beitaipingzhuang"
						, "Xueyuanlu", "Shuguang", "Yongdinglu"
						, "Haidian", "Qinghuayuan", "Yanyuan"
						, "Qinghe", "Ganjiakou", "Tiancunlu"
						, "Zizhuyuan", "Yangfangdian", "Huayuanlu"
						, "Xisanqi", "Qinglongqiao", "Xiangshan"
						, "Malianwa"};
	for (int i = 0 ; i < 22 ; i ++)
		street[i] += " Street";
	vector<location> vec;
	for (int i = 0 ; i < 11 ; i ++)
		for (int j = 0 ; j < 11 ; j ++)
			vec.push_back(location(street[i], street[j+11]));	 
	cout << vec.size() << endl;
	ofstream fout;
	fout.open("insert_location");
	fout << "INSERT INTO `location`" << endl;
	fout << "(`district`, `street-r`, `street-c`)" << endl;
	fout << "VALUES" << endl;
	for (int i = 0 ; i < vec.size() ; i ++)
	{
		vec[i].print(fout);
		if (i == vec.size()-1) fout << ";" << endl;
		else fout << "," << endl;
	}
	fout.close();
	return 0;
}
