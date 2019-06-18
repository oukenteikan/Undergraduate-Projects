package test;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.eval.IRStatistics;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.eval.RecommenderIRStatsEvaluator;
import org.apache.mahout.cf.taste.impl.common.LongPrimitiveIterator;
import org.apache.mahout.cf.taste.impl.eval.AverageAbsoluteDifferenceRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.eval.GenericRecommenderIRStatsEvaluator;
import org.apache.mahout.cf.taste.impl.model.file.*;  
import org.apache.mahout.cf.taste.impl.neighborhood.*;  
import org.apache.mahout.cf.taste.impl.recommender.*;  
import org.apache.mahout.cf.taste.impl.similarity.*;  
import org.apache.mahout.cf.taste.model.*;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.*;  
import org.apache.mahout.cf.taste.similarity.*;  

import java.io.*;  
import java.util.*;  



public class MahoutTest {
	final static int NEIGHBORHOOD_NUM = 2;
    final static int RECOMMENDER_NUM = 3;

    public static void main(String[] args) throws IOException, TasteException {
    	//预处理，打开,dataSize可为1000、5000、10000
    	int dataSize = 1000;
        String file = "data\\write"+dataSize+".csv";
        String file2 = "data\\after"+dataSize+".csv";
        Filler f = new Filler(file,file2);
        f.operate();
        DataModel model = new FileDataModel(new File(file));
        DataModel model2 = new FileDataModel(new File(file2));
        
        //建立推荐系统
        RecommenderEvaluator evaluator = new AverageAbsoluteDifferenceRecommenderEvaluator();
        RecommenderIRStatsEvaluator statsEvaluator = new GenericRecommenderIRStatsEvaluator();
        
        //改进前
        System.out.println("改进前：");
        RecommenderBuilder recommenderBuilder = new RecommenderBuilder(){
        	@Override
        	public Recommender buildRecommender(DataModel model) throws TasteException {
        		UserSimilarity similarity = new PearsonCorrelationSimilarity(model);
        	    UserNeighborhood neighborhood = new NearestNUserNeighborhood(NEIGHBORHOOD_NUM,similarity,model);
        	    return new GenericUserBasedRecommender(model, neighborhood,similarity);
        	}
        };
        
        double score = evaluator.evaluate(recommenderBuilder, null, model, 0.7, 1.0);
        IRStatistics stats = statsEvaluator.evaluate(recommenderBuilder,null, model, null, RECOMMENDER_NUM,
        		GenericRecommenderIRStatsEvaluator.CHOOSE_THRESHOLD,1.0);
        System.out.println("评分："+score);
        System.out.println("准确率："+stats.getPrecision());
        System.out.println("召回率："+stats.getRecall());
        System.out.println("F1值："+stats.getF1Measure());
        
        //改进后
        System.out.println("改进后：");
        recommenderBuilder = new RecommenderBuilder(){
        	@Override
        	public Recommender buildRecommender(DataModel model) throws TasteException {
        		UserSimilarity similarity = new PearsonCorrelationSimilarity(model2);
        	    UserNeighborhood neighborhood = new NearestNUserNeighborhood(NEIGHBORHOOD_NUM,similarity,model);
        	    return new GenericUserBasedRecommender(model, neighborhood,similarity);
        	}
        };
        
        score = evaluator.evaluate(recommenderBuilder, null, model, 0.7, 1.0);
        stats = statsEvaluator.evaluate(recommenderBuilder,null, model, null, RECOMMENDER_NUM,
        		GenericRecommenderIRStatsEvaluator.CHOOSE_THRESHOLD,1.0);
        System.out.println("评分："+score);
        System.out.println("准确率："+stats.getPrecision());
        System.out.println("召回率："+stats.getRecall());
        System.out.println("F1值："+stats.getF1Measure());
    }
}
