#include <iostream>
#include <fstream>
#include <vector>
#include <ctime>
#include <iomanip>
#include <cstdlib>
using namespace std;
class user
{
	public:
		user(string account_number_, string pwd_user_, string name_, string gender_, string job_, 
		float balance_, short state_user_):
		account_number(account_number_), name(name_), pwd_user(pwd_user_), gender(gender_), job(job_), 
		balance(balance_), state_user(state_user_){}
		string account_number, name, pwd_user, gender, job;
		float balance;
		short state_user;
		void print(ofstream& fout)
		{
			fout << "(\"" << account_number << "\", \"" << pwd_user << "\", \"" << name << "\", \"" << gender << "\", \"" << job << "\", " 
				<< fixed << setprecision(2) << balance << ", " << state_user << ")";
			return;
		}
};
int main()
{
	vector<user> vt;
	string acn, n, p, g, job;
	float balance;
	int a, b, c, d;
	srand(time(0));
	for (int i = 0 ; i < 1000 ; i ++)
	{
		//balance
		a = rand();
		balance = a/100.0;
		//gender
		a = rand();
		b = a%2;
		if (b == 0) g = "male";
		else g = "female";
		
		//account_number
		a = rand();
		b = a%11 + 6;
		acn.clear();
		for (int j = 0 ; j < b ; j ++)
		{
			a = rand();
			c = a%27;
			if (c == 26) 
				acn.push_back('_');
			else
				acn.push_back(char(c + 'a'));
		}		
		//name
		a = rand();
		b = a%11 + 6;
		n.clear();
		for (int j = 0 ; j < b ; j ++)
		{
			a = rand();
			c = a%27;
			if (c == 26) 
				n.push_back('_');
			else
				n.push_back(char(c + 'a'));
		}
		//password
		a = rand();
		b = a%11 + 6;
		p.clear();
		for (int j = 0 ; j < b ; j ++)
		{
			a = rand();
			c = a%36;
			if (c > 9) 
				p.push_back(char(c - 10 + 'a'));
			else
				p.push_back(char(c + '0'));
		}
		//job
		a = rand();
		b = a%32 + 1;
		job.clear();
		for (int j = 0 ; j < b ; j ++)
		{
			a = rand();
			c = a % 26;
			job.push_back(char(c + 'a'));
		}
		//vector
		vt.push_back(user(acn, p, n, g, job, balance, 0)); 
	}
	cout << vt.size() << endl;
	ofstream fout;
	fout.open("insert_user");
	fout << "INSERT INTO `user`" << endl;
	fout << "(`account_number`, `pwd_user`, `alias`, `gender`, `job`, `balance`, `state_user`)" << endl;
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
