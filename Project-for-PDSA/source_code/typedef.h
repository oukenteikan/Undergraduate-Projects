#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <cstring>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <map> 
#include <queue>
#include <stack>
#include <ctime>
#define Train_Num 4000     //建库数据量 
#define divided 10          //分divided次输入 
#define label_max_num 10   //标签最多 
#define word_max_num 200   //单词最多 
#define letter_num 26      //字母数量 
#define result_labelnum 3  //结果标签数目 
using namespace std;
class Word {               //单词类 
	private:
		string word;                                          //单词 
		short times[Train_Num + 1];                           //在所有测试数据中分别出现多少次 
		int show, sum;                                        //含有该单词的句子数和单词出现的总次数 
		void Calculate_show();                                //计算含有该单词的句子数 
	public:
		Word(ifstream &fin);                                                               //从单词表输入的构造寒素 
		Word(string word_);                                                                //从训练数据提取的构造函数                                                                       //构造 
		void Export_Word(ofstream &fout);                                                  //输出单词全部信息                                                                         //输出 
		bool operator==(const Word &w) const;                                              //定义等于 
		bool operator<(const Word &w) const;                                               //定义小于 
		int Get_sum() const;                                                               //获取出现总次数 
		string Get_word() const;                                                           //获取单词 
	friend class Sample;
	friend class Database;
};
class Sample {             //语句类 
	private:
		string sentence;                                                    //句子 
		string *word, *label;                                               //单词和标签 
		int id, wordnum, labelnum;                                          //句子编号、单词数量、标签数量 
	public:
		Sample();                                                           //构造函数 
		~Sample();                                                          //析构函数 
		void Input_Sample(ifstream &fin);                                   //输入处理过的训练数据 
		void Import_Sample(ifstream &fin, int n);                           //输入训练数据
		void Export_Sample(ofstream &fout);                                 //输出处理过的训练数据 
		void mystrlwr(string &str);                                         //string串大写转为小写 
		void Set_word();                                                    //提取单词 
		void Clear_tail();                                                  //清除尾部"#$#"及之后内容 
		void Clear_head();                                                  //清除头部"#$#"及之前内容，
		void Set_label();                                                   //提取训练数据标签 
		int Get_Label_Count();												//返回标签的数量
		string* Get_Label_Array();											//返回存储标签位置的数组
		void Push(vector<Word> *All_words);                                 //统计全部单词 
		void Deal_with_Sample(vector<Word> *All_words);                     //处理训练数据总函数 
		void Deal_with_Test(string current, int n);                         //处理测试数据总函数
		void Output_Result(ofstream &fout);                                 //输出结果的总函数 
	friend class Database;
};
class Database {           //库类
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
};
