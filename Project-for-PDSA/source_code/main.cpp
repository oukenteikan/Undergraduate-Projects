#include "typedef.h"
int main() {               //主函数 
	Database database;                            //建立一个对象 
	ifstream fin("train.data");                   //打开训练数据文件
	if (!fin) {
		cerr << "Fail to open \"train.data\", please make sure that it is under the same directory with this programme then try again!" << endl; 
		return 0;		
	} 
	ofstream fout("sentence list.data");          //创建语句表 
	cout << "Making sentence list ......" << endl;
	for (int i = 0 ; i < divided ; i ++) {        //执行divided次 
		database.Import_Samples(fin);             //输入训练数据 
		database.Deal_with_Samples();             //处理训练数据
		database.Export_Samples(fout);            //输出语句表 
	}
	cout << "Sentence list is finished." << endl;
	fin.close();                                  //关闭训练数据 
	fout.close();                                 //关闭语句表 
	fout.open("word list.data");                  //创建单词表 
	cout << "Making word list ......" << endl;
	database.Export_Words(fout);                  //输出单词表 
	cout << "Word list is finished." << endl;
	fout.close();                                 //关闭单词表
	string current;                               //临时存储测试数据
	database.Import_Database(fin);                //导入语句表和单词表
	database.Calc_Label_Feature();				  //计算标签特征值
	
	fin.open("test.data");                        //打开测试数据 
	if (!fin) {
		cerr << "Fail to open \"test.data\", please make sure that it is under the same directory with this programme then try again!" << endl; 
		return 0;
	}
	fout.open("result.data");                     //创建结果文件
	cout << "Extracting the labels ......" << endl;
	while (getline(fin, current)) {                //输入测试数据 
		database.Extract_Labels(current, fout);  //提取并输出标签
	}
	cout << "All the work is finished." << endl << "You can check the result now." << endl;;
	fin.close();                                  //关闭测试数据 
	fout.close();                                 //关闭结果文件 
	return 0; 
}
