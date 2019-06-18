#include <iostream>
#include <fstream>
#include <vector>
#include <ctime>
#include <cstdlib>
#include <sstream>
#include <iomanip>
#include <cmath>
using namespace std;
class order
{
	public:
		order(float cost_, double distance_, short state_order_, int ID_user_, int ID_bike_, 
				int loca_start_, double long_start_, double lat_start_, int loca_finish_, double long_finish_, double lat_finish_, 
				string time_start_, string time_finish_, float time_total_):
			cost(cost_), distance(distance_), state_order(state_order_), ID_user(ID_user_), ID_bike(ID_bike_), 
			loca_start(loca_start_), long_start(long_start_), lat_start(lat_start_), 
			loca_finish(loca_finish_), long_finish(long_finish_), lat_finish(lat_finish_), 
			time_start(time_start_), time_finish(time_finish_), time_total(time_total_){}
		string time_start, time_finish;
		int ID_user, ID_bike, loca_start, loca_finish;
		float cost, time_total;
		double long_start, lat_start, long_finish, lat_finish;
		double distance;
		short state_order;
		void print(ofstream& fout)
		{
			fout << "(" << ID_user << ", " << ID_bike << ", " << state_order << ", \"" << time_start << "\", \"" << time_finish << "\", "
				<< fixed << loca_start << ", " << setprecision(6) << long_start << ", " << lat_start << ", " 
				<< loca_finish << ", " << setprecision(6) << long_finish << ", " << lat_finish << ", "
				<< setprecision(2) << cost << ", " << setprecision(6) << distance << ", " << setprecision(3) << time_total << ")";
			return;
		}
};
string month[12] = {"01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"};
string day[31] = {"01", "02", "03", "04", "05", "06", "07", "08", "09", "10", 
			"11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
			"21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"};
string hour[24] = {"00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", 
			"11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
			"21", "22", "23"};			
string minute[60] = {"00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", 
			"11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
			"21", "22", "23", "24", "25", "26", "27", "28", "29", "30", 
			"31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
			"41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
			"51", "52", "53", "54", "55", "56", "57", "58", "59"};
int main()
{
	ifstream fin;
	vector<order> vt;
	string ts, tf, tmp1, tmp2;
	int ls, lf, iduser, idbike;
	int row, col;
	short s;
	float cost, t1, t2, tt;
	double distance;
	double longs, longf, lats, latf;
	int a, b, c, d, e;
	ostringstream ss;
	srand(time(0));
	for (int i = 0 ; i < 10000 ; i ++)
	{
		//location_start
		a = rand();
		ls = (a%121) + 1;
		
		//longs, lats
		row = (ls-1)/11;
		col = (ls-1)%11;
		a = rand();
		b = rand();
		c = a % 20001;
		d = b % 20001;
		longs = 116.1 + 0.02 * col + c * 0.000001 - 0.01;
		lats = 39.9 + 0.02 * row + d * 0.000001 - 0.01;				
		
		//location_finish
		a = rand();
		lf = (a%121) + 1;
		
		//latf, longf
		row = (lf-1)/11;
		col = (lf-1)%11;
		a = rand();
		b = rand();
		c = a % 20001;
		d = b % 20001;
		longf = 116.1 + 0.02 * col + c * 0.000001 - 0.01;
		latf = 39.9 + 0.02 * row + d * 0.000001 - 0.01;	
		
		//distance
		distance = abs((longs - longf)*200) + abs((lats - latf)*200);
		
		//iduser
		a = rand();
		iduser = a%1000+1;

		//idbike
		a = rand();
		idbike = a%10000+1;

		//time_start, time_finish, time_total
		ts = "2017-";
		tf = "2017-";
		
		a = rand();
		b = a%12;
		ts += month[b] + "-";
		tf += month[b] + "-";
		
		a = rand();
		if (b == 1)
			c = a%28;
		else if (b == 3||b == 5||b == 8||b == 10)
				c = a%30;
			else
				c = a%31;
		ts += day[c] + " ";
		tf += day[c] + " ";
		
		a = rand();
		b = a%24;
		ts += hour[b] + ":";
		tf += hour[b] + ":";
		
		a = c = 0;
		while (a == c)
		{
			a = rand();
			c = rand();
			d = a%60;
			e = c%60;
			a = min(d, e);
			c = max(d, e); 
		}
		tt = (c-a)*60;
		ts += minute[a] + ":";
		tf += minute[c] + ":";
			
		a = rand();
		b = rand();
		c = (a << 15) + b;
		a = c % 60000;
		t1 = a/1000.0;
		ss.str("");
		ss << setfill('0') << setw(6) << fixed << setprecision(3) << t1;
		tmp1 = ss.str();
		ts += tmp1;
		
		a = rand();
		b = rand();
		c = (a << 15) + b;
		a = c % 60000;
		t2 = a/1000.0;
		ss.str("");
		ss << setfill('0') << setw(6) << fixed << setprecision(3) << t2;
		tmp2 = ss.str();
		tf += tmp2;
		
		tt += t2 - t1;
		//state_order
		s = 0;
		
		//cost
		cost = distance/100 + tt/36000;
		
		//vector
		vt.push_back(order(cost, distance, s, iduser, idbike, ls, longs, lats, lf, longf, latf, ts, tf, tt)); 
	}
	cout << vt.size() << endl;
	ofstream fout;
	fout.open("insert_order");

	for (int i = 0 ; i < vt.size() ; i ++)
	{
		if (i%10000 == 0)
		{
			fout << "INSERT INTO `order`" << endl;
			fout << "(`ID_user`, `ID_bike`, `state_order`, `time_start`, `time_finish`, `loca_start`, `long_start`, `lat_start`, `loca_finish`, `long_finish`, `lat_finish`, `cost`, `distance`, `time_total`)" << endl;
			fout << "VALUES" << endl;
		}
		vt[i].print(fout);
		if ((i+1)%10000==0||i == vt.size()-1) fout << ";" << endl;
		else fout << "," << endl;
	}
	fout.close();
	return 0;
}
