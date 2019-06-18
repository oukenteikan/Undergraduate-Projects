#include "typedef.h"
/*class Sample {             //语句类 
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
};*/
Sample::Sample() {                                                          //构造函数 
	word = label = NULL;
}
Sample::~Sample() {                                                         //析构函数 
	if (word) delete [] word;
	if (label) delete [] label;
}
void Sample::Input_Sample(ifstream &fin) {                                  //输入处理过的训练数据 
	fin >> id >> wordnum;
	word = new string[wordnum];
	for (int i = 0 ; i < wordnum ; i ++)
		fin >> word[i];
	fin >> labelnum;
	char o = fin.get();
	label = new string[labelnum];
	for (int i = 0 ; i < labelnum ; i ++)
		getline(fin, label[i]);
	return;
}
void Sample::Import_Sample(ifstream &fin, int n) {                          //输入训练数据
	getline(fin, sentence);
	id = n;
	if (id % (Train_Num / divided) == 0) cout << "It's sample sentence " << id << " now." << endl;
	wordnum = labelnum = 0;
	word = new string[word_max_num];
	label = new string[label_max_num];
	return;
}
void Sample::Export_Sample(ofstream &fout) {                                //输出处理过的训练数据 
	fout << id << endl;
	fout << wordnum << endl;
	for (int i = 0 ; i < wordnum ; i ++)
		fout << word[i] << " ";
	fout << endl;
	fout << labelnum << endl;			
	for (int i = 0 ; i < labelnum ; i ++)
		fout << label[i] << endl;
	return;
}
void Sample::mystrlwr(string &str) {                                        //string串大写转为小写 
	for (int i = 0 ; i < str.length() ; i ++)
		if (str[i] >= 'A' && str[i] <= 'Z')
			str[i] += 'a' - 'A';
	return;
}
void Sample::Set_word() {                                                   //提取单词 
	for (int i = 0 ; i < sentence.length() ; i ++) {
		if (!isalpha(sentence[i])) {
			if (!word[wordnum].empty())
					wordnum ++;
		}
		else word[wordnum].append(1, sentence[i]);
	}
	if (!word[wordnum].empty()) wordnum ++;
	for (int i = 0 ; i < wordnum ; i ++) {
		mystrlwr(word[i]);
	}
	return;
}
void Sample::Clear_tail() {                                                 //清除尾部"#$#"及之后内容 
	int length = sentence.length();
	int p = length;
	while (true)
		if (sentence[-- p] == '#') {
			sentence.erase(p - 2, length - p + 2);
				break;
		}
	return;
}
void Sample::Clear_head() {                                                 //清除头部"#$#"及之前内容，
	int p = 0;
	while (true)
		if (sentence[p ++] == '#') {
				sentence.erase(0, p + 2);
				break;
		}
	return;	
}
void Sample::Set_label() {                                                  //提取训练数据标签 
	int begin = sentence.length() - 1;
	while (sentence[begin] != '#') begin --;
	while (begin != sentence.length() - 1) {
		begin ++;
		if (sentence[begin] == ',') labelnum ++;
		else label[labelnum].append(1, sentence[begin]);
	}
	for (int i = 0 ; i < labelnum ; i ++) mystrlwr(label[i]); 
	return;
}
void Sample::Push(vector<Word> *All_words) {                                //统计全部单词 
	for (int i = 0 ; i < wordnum ; i ++) {
		vector<Word>::iterator p = find(All_words[word[i][0] - 'a'].begin(), All_words[word[i][0] - 'a'].end(), word[i]);
		if (p == All_words[word[i][0] - 'a'].end())
			All_words[word[i][0] - 'a'].push_back(Word(word[i]));
		p = find(All_words[word[i][0] - 'a'].begin(), All_words[word[i][0] - 'a'].end(), word[i]);
		p->times[id] ++;
		p->sum ++;
	}
	return;
}
void Sample::Deal_with_Sample(vector<Word> *All_words) {                    //处理训练数据总函数 
	Set_label();
	Clear_tail();
	Clear_head();
	Set_word();
	Push(All_words);
	return;
}
void Sample::Deal_with_Test(string current, int n) {                        //处理测试数据总函数 
	sentence = current;
	id = n;
	if (id % (Train_Num / divided / divided) == 0) cout << "It's test sentence " << id << " now." << endl;			
	wordnum = labelnum = 0;
	word = new string[word_max_num];
	label = new string[result_labelnum];
	Clear_head();
	Set_word();
	return;
}
void Sample::Output_Result(ofstream &fout) {                                //输出结果的总函数 
	fout << id << "#$#";
	for (int i = 0 ; i < result_labelnum ; i ++)
		fout << label[i] << ",";
	fout << endl;
	return;
}
