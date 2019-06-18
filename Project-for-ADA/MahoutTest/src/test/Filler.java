package test;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;

public class Filler {
	double data[][], ref[], af[][];
	double ave[];
	String before, after;
	int user;
	int item;
	public Filler(String b, String a)
	{
		before = b;
		after = a;
	}
	public void operate(){
		class Entry{
			int userid, itemid;
			double score;
			Entry(int u, int i, double s){
				userid = u;
				itemid = i;
				score = s;
			}
		}
		File file;
		List<Entry> list=new ArrayList<Entry>();
		String[] line;
		int t1, t2;
		int maxUser = Integer.MIN_VALUE, minUser = Integer.MAX_VALUE;
		int maxItem = Integer.MIN_VALUE, minItem = Integer.MAX_VALUE;
		String s;
		if(new File(after).exists() == true)
			return;
		try {
			file = new File(before);
			BufferedReader reader = new BufferedReader(new FileReader(file));
			while((s = reader.readLine()) != null){
				line = s.split(",");
				t1 = Integer.parseInt(line[0]);
				t2 = Integer.parseInt(line[1]);
				maxUser = Math.max(maxUser, t1);
				minUser = Math.min(minUser, t1);
				maxItem = Math.max(maxItem, t2);
				minItem = Math.min(minItem, t2);
				list.add(new Entry(t1, t2,Double.parseDouble(line[2])));
			}
			reader.close();
			user = maxUser - minUser + 1;
			item = maxItem - minItem + 1;
			System.out.println(user+" "+item);
			data = new double[user+1][item+1];
			for(Entry i : list)
				data[i.userid-minUser+1][i.itemid-minItem+1]=i.score;
			
			fill();
			
			file = new File(after);
			if(file.exists() == false)
				file.createNewFile();
			BufferedWriter writer = new BufferedWriter(new FileWriter(file));
			for(int i = 1; i <= user; ++i)
				for(int j = 1; j<=item; ++j){
					s = String.format("%.6f", af[i][j]);
					if(s.equals("0.000000"))
						continue;
					writer.write((i+minUser-1)+",");
					writer.write((j+minItem-1)+",");
					writer.write(s);
					writer.newLine();
				}
			writer.close();
		} catch (Exception e) {
			e.printStackTrace();
			return;
		}
	}
	void fill()
	{
		ini();
		af = new double[user+1][item+1];
		long time1s = System.currentTimeMillis(); 
		ref = new double[item+1];
		for(int j=1; j<=item; ++j)
		{
			
			for(int i=1; i<=item; ++i)
			{
				double sumXY = 0;
				double sumX2 = 0;
				double sumY2 = 0;
				if(i == j){
					ref[i] = 0;
					continue;
				}
					
				for(int k=1; k<=user; ++k)
				{
					// 修改从这里开始
					double t1 = data[k][i];
					double t2 = data[k][j];
					sumXY += t1*t2;
					sumX2 += t1*t1;
					sumY2 += t2*t2;
					// 修改从这里结束
				}
				if(sumX2 == 0 || sumY2 == 0)
					ref[i] = 0;
				else
				{
					double result = sumXY/Math.sqrt(sumX2*sumY2);
					ref[i] = result;
				}
				
			}		
			for(int i=1; i<=user; ++i)
			{
				if(data[i][j] == 0)
				{
					double s1 = 0;
					double s2 = 0;
					for(int k=1 ; k<= item; ++k)
					{
						if(data[i][k] != 0)
						{
							s1 += data[i][k] * ref[k];
							s2 += ref[k];
						}
					}
					if(s2 != 0)
						af[i][j] = s1/s2;
					else
					{
						af[i][j] = ave[j];
					}
				}
				else
					af[i][j] = data[i][j];
			}
		}
		long time1e = System.currentTimeMillis();
		System.out.println("耗时："+(time1e-time1s));
	}
	public void ini()
	{
		ave = new double[item+1];
		for(int j=1; j<=item; j++)
		{
			int sum = 0;
			int cnt = 0;
			for(int i=1; i<= user; ++i)
			{
				if(data[i][j] != 0)
				{
					sum += data[i][j];
					cnt++;
				}
				
			}
			if(cnt != 0)
				ave[j] = sum/cnt;
			else
				ave[j] = 0;
		}
	}
}
