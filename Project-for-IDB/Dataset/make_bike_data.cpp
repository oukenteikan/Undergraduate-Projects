#include <iostream>
#include <fstream>
#include <vector>
#include <ctime>
#include <iomanip>
#include <cstdlib>
using namespace std;
class bike 
{
	public:
		bike(string type_, float price_, string pwd_bike_, short state_bike_, short broken_, int location_, double x_, double y_)
			:type(type_), price(price_), pwd_bike(pwd_bike_), state_bike(state_bike_), broken(broken_), location(location_), x(x_), y(y_){}
		string type, pwd_bike;
		int location;
		short state_bike, broken;
		double x, y;
		float price;
		void print(ofstream& fout)
		{
			fout << "(\"" << type << "\", " << fixed << setprecision(1) << price << ", \"" << pwd_bike << "\", " << state_bike << ", " << broken << ", " 
				<< location << ", " << setprecision(6) << x << ", " << y << ")";
			return;
		}
};
string type[23] = {"Road", "Touring", "Randonneur", "Hybrid", "Cyclo-cross", 
					"Utility", "Freight", "Flat bar road", "Ice", "Mountain", 
					"Military", "Racing", "Time trial", "Triathlon", "Track", 
					"BMX", "Cruiser", "Cycle rickshaws", "Motorized", "Gyroscopic", 
					"Electric", "Rail", "Firefighter"};
int main()
{
	vector<bike> vt;
	string t, p;
	int l;
	int row,col;
	short s, br;
	int a, b, c, d;
	double x, y;
	float pr;
	srand(time(0));
	for (int i = 0 ; i < 10000 ; i ++)
	{
		//location
		a = rand();
		b = rand();
		c = (a << 15) + b;
		l = (c%121) + 1;
		
		//x, y
		row = (l-1)/11;
		col = (l-1)%11;

		a = rand();
		b = rand();
		c = a % 20001;
		d = b % 20001;
		x = 116.1 + 0.02 * col + c * 0.000001 - 0.01;
		y = 39.9 + 0.02 * row + d * 0.000001 - 0.01;		
		
		//state_bike
		s = 0;
		//broken
		a = rand();
		if (a % 1000 == 0) br = 1;
		else br = 0;
		//password
		p.clear();
		for (int j = 0 ; j < 6 ; j ++)
		{
			a = rand();
			c = a%10;
			p.push_back(char(c + '0'));
		}
		//t
		a = rand();
		b = a%23;
		t = type[b];
		//price
		pr = ((b%4)+1)/10.0;
		
		//vector
		vt.push_back(bike(t, pr, p, s, br, l, x, y)); 
	}
	cout << vt.size() << endl;
	ofstream fout;
	fout.open("insert_bike");
	fout << "INSERT INTO `bike`" << endl;
	fout << "(`type`, `price`, `pwd_bike`, `state_bike`, `broken`, `ID_location`, `long`, `lat`)" << endl;
	fout << "VALUES" << endl;	
	for (int i = 0 ; i < vt.size() ; i ++)
	{
		vt[i].print(fout);
		if (i == vt.size() - 1) fout << ";" << endl;
		else fout << "," << endl;
	}
	fout.close();
	return 0;
}
