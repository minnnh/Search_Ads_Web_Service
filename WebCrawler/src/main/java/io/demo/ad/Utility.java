package io.demo.ad;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.StopFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.en.KStemFilter;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Utility {
    private static List<Character> symbolStopWords = Arrays.asList('.', ',', '"', '\'', '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '&', '/', '.', '.', '.', '-', '+', '*', '|', ')', ',');

    private static CharArraySet symbolStopSet = new CharArraySet(symbolStopWords, true);

    private static String stopWords = "a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your";
    private static CharArraySet getStopwords(String stopwords) {
        List<String> stopwordsList = Arrays.asList(stopwords.split(","));
        return new CharArraySet(stopwordsList, true);
    }

    public static String strJoin(List<String> aArr, String sSep) {
        StringBuilder sbStr = new StringBuilder();
        for (int i = 0, il = aArr.size(); i < il; i++) {
            if (i > 0)
                sbStr.append(sSep);
            sbStr.append(aArr.get(i));
        }
        return sbStr.toString();
    }

    // remove stop word, tokenize, stem
    public static List<String> cleanedTokenize(String input) {
        List<String> tokens = new ArrayList<>();
        StringReader reader = new StringReader(input.toLowerCase());

        Analyzer analyzer = new EnglishAnalyzer(getStopwords(stopWords));
        TokenStream tokenStream = analyzer.tokenStream("field", reader);
        tokenStream = new KStemFilter(tokenStream);
        tokenStream = new StopFilter(tokenStream, symbolStopSet);

        StringBuilder sb = new StringBuilder();
        CharTermAttribute charTermAttribute = tokenStream.addAttribute(CharTermAttribute.class);
        try {
            tokenStream.reset();
            while (tokenStream.incrementToken()) {
                String term = charTermAttribute.toString();
                tokens.add(term);
                sb.append(term).append(" ");
            }
            tokenStream.end();
            tokenStream.close();
            analyzer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("cleaned Tokens =" + sb.toString());
        return tokens;
    }

    public static double sigmoid(double x) {
        return 1 / (1 + Math.exp(-x));
    }
}
