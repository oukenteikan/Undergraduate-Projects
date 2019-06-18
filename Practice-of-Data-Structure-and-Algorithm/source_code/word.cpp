#include "typedef.h"
/*class Word {               //单词类 
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
};*/
void Word::Calculate_show() {                                                            //计算含有该单词的句子数 
	for (int i = 1 ; i <= Train_Num ; i ++)
		if (times[i]) show ++;
}
Word::Word(ifstream &fin) {                                                              //从单词表输入的构造寒素 
	fin >> word >> show >> sum;
	memset(times, 0, sizeof(times)); 
	int t;
	for (int i = 0 ; i < show ; i ++) {
		fin >> t;
		fin >> times[t];
	}
	return;
}
Word::Word(string word_):word(word_) {                                                   //从训练数据提取的构造函数 
	memset(times, 0, sizeof(times));
	show = sum = 0;
	return;
}                                                                                        //构造 
void Word::Export_Word(ofstream &fout) {                                                 //输出单词全部信息 
	Calculate_show();
	fout << word << " " << show << " " << sum;
	for (int i = 1 ; i <= Train_Num ; i ++)
		if (times[i])
			fout << " " << i << " " << times[i];
	fout << endl;
	return;
}                                                                                        //输出 
bool Word::operator==(const Word &w) const {return word == w.word;}                      //定义等于 
bool Word::operator<(const Word &w) const {return word < w.word;}                        //定义小于 
int Word::Get_sum() const {return sum;}                                                  //获取出现总次数 
string Word::Get_word() const {return word;}   
