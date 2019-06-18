#include "typedef.h"
/*class Database {           //库类
	private:
		int Count_num;                                                     //编号 
		Sample *sample;                                                    //库 
		Sample current;                                                    //当前测试数据 
		vector<Word> All_words[letter_num];                                //单词表，按首字母分桶，方便查找 
		vector<Word> Vocabulary;                                           //总单词表，方便按词频排序 
		map <string, vector<double> > Map;								   //用于存储标签对应的特征向量 
		priority_queue<pair<double, string> > Q;                           // 优先队列Q用于存储与当前句子特征向量夹角最小的前三个标签，
		                                                      //每个pair元素的first是夹角的余弦值（保留余弦值最大的），second是标签名。
	public:
		Database();                                                        //构造函数 
		~Database();                                                       //析构函数 
		void Import_Database(ifstream &fin);                               //输入单词表和语句表 
		int Find_Word_Index(const string&);                                //找到已知单词的下标
		void Import_Samples(ifstream &fin);                                //输入训练数据 
		void Export_Samples(ofstream &fout);                               //输出语句表 
		void Deal_with_Samples();                                          //处理训练数据 
		void Export_Words(ofstream &fout);                                 //输出单词表 
		void Calc_Label_Feature();										   //处理标签特征向量
		void Extract_Labels(string current_, ofstream &fout);              //处理测试数据 
};*/
Database::Database() {sample = NULL;Count_num = 1;}                          //构造函数 
Database::~Database() {if (sample) delete [] sample;}                        //析构函数 
void Database::Import_Database(ifstream &fin) {                              //输入单词表和语句表 
	sample = new Sample[Train_Num];
	fin.open("sentence list.data");
	for (int i = 0 ; i < Train_Num ; i ++) {
		sample[i].Input_Sample(fin);
	}
	fin.close();
	fin.open("word list.data");
	for (int i = 0 ; i < letter_num ; i ++) {
		int t;
		fin >> t;
		for (int j = 0 ; j < t ; j ++)
			Vocabulary.push_back(Word(fin));
	}
	fin.close();
	return;
}
void Database::Import_Samples(ifstream &fin) {                               //输入训练数据 
	sample = new Sample[Train_Num / divided];
	for (int i = 0 ; i < Train_Num / divided ; i ++)
		sample[i].Import_Sample(fin, Count_num ++);
	return;
}
void Database::Export_Samples(ofstream &fout) {                              //输出语句表 
	for (int i = 0 ; i < Train_Num / divided ; i ++)
		sample[i].Export_Sample(fout);
	delete [] sample;
	sample = NULL;
	return;
}
void Database::Deal_with_Samples() {                                         //处理训练数据 
	for (int i = 0 ; i < Train_Num / divided ; i ++)
		sample[i].Deal_with_Sample(All_words);
	return;
}
void Database::Export_Words(ofstream &fout) {                                //输出单词表 
	for (int i = 0 ; i < letter_num ; i ++) {
		sort(All_words[i].begin(), All_words[i].end());
		fout << All_words[i].size() << endl;
		for (vector<Word>::iterator p = All_words[i].begin() ; p < All_words[i].end() ; p ++)
			p->Export_Word(fout); 
	}
	return;
}
double Module(const vector<double>& V) 
// 求出向量的模长
{
	size_t sz = V.size();
	double Sum = 0;
	for (int i = 0; i < sz; i++)
		Sum += V[i] * V[i];
	return sqrt(Sum);
}
double CosAngle(const vector<double>& V1, const vector<double>& V2)
// 求出向量的夹角 
{
	size_t sz = V1.size();
	double Sum = 0;
	for (int i = 0; i < sz; i++)
		Sum += V1[i] * V2[i];
	return Sum;
}
int Database::Find_Word_Index(const string& w)
// 利用二分法找到已知单词的下标
{
	int l = 0, r = Vocabulary.size(), mid;
	while (r - l >= 2)
	{
		mid = (r + l)>> 1;
		if (Vocabulary[mid].Get_word() < w)
			l = mid;
		else
			r = mid;
	}
	if (Vocabulary[l].Get_word() == w) 
		return l;
	else if (Vocabulary[r].Get_word() == w)
		return r;
	else return -1;
}
void Database::Calc_Label_Feature()
// 计算标签的特征向量，结果反映在成员Map中。 
{
	int i, j, jj, sz = Vocabulary.size();
	map <string, vector <double> >::iterator it;
	for (i = 0; i < Train_Num; i++)
	{
		Sample& Sam = sample[i];
		for (j = 0; j < Sam.labelnum; j++)
		{
			if ((it = Map.find(Sam.label[j]))== Map.end())
				Map[Sam.label[j]] = vector<double>(sz);
			for (jj = 0; jj < Sam.wordnum; jj++) {
				int tar = Find_Word_Index(Sam.word[jj]);
				Map[Sam.label[j]][tar] -= log((double)Vocabulary[tar].show / (double)Train_Num);
				//利用对数的TF-IDF 
			}
		}
	}
	for(it = Map.begin(); it != Map.end(); it++)
	{
		double len = Module(it->second);
		for (int i = 0; i < sz; i++)
			it->second[i] /= len;
	}
}
void Database::Extract_Labels(string current_, ofstream &fout) {             //处理测试数据 
	current.Deal_with_Test(current_, Count_num ++);

	vector <double> SampVec(Vocabulary.size()); //用于存储当前处理的句子的特征向量 
	map<string, vector<double> >::iterator it;
	int i, j, sz = Vocabulary.size();
	for (i = 0; i < current.wordnum; i++)
	{
		int at = Find_Word_Index(current.word[i]); // 寻找当前处理单词的下标 
		if (at < 0) continue; // 遇见未知单词，不予处理 
		Word& W = Vocabulary[at];
		SampVec[at] -= log((double)W.show / (double)Train_Num); // 对于每个已知词增加权度 
	}
	double lenth = Module(SampVec);
	for (int i = 0; i < sz; i++)
		SampVec[i] /= lenth;
	for (it = Map.begin(); it != Map.end(); it++)
	{
		double angle = CosAngle(it->second, SampVec);
		Q.push(make_pair(angle, it->first));
	}
	for (int ii = 0; ii < result_labelnum; ii++)
	{
		current.label[ii] = Q.top().second;
		Q.pop();
		// 把夹角余弦值最大的三个标签保存在current中 
	}
	while (!Q.empty()) Q.pop();
	current.Output_Result(fout);
	return;
}
