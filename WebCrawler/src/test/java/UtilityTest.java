import io.demo.ad.Utility;
import io.demo.crawler.AmazonCrawler;
import io.demo.crawler.CrawlerMain;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.List;

public class UtilityTest {

    Utility utility;
    CrawlerMain crawlerMain;


    @Test
    public void tokenizeData() {
        String testText = "This is a sample text for testing the Lucene utility. It includes some stopwords, punctuation marks like commas and periods, and various words to showcase the tokenization and stemming process.";
        List<String> tokens = Utility.cleanedTokenize(testText);
        System.out.println("Tokens: " + tokens);

        // String corrText = "Lucene is a powerful information retrieval library. It is widely used for full-text indexing and searching. The Lucene utility should tokenize and stem words effectively, removing stopwords and symbols.";
        // System.out.println(tokens.get(0).equals(corrText));
    }

    @Test
    public void testProxy() throws IOException {
        String proxyFilePath = "inputFiles/proxylist.csv";
        String logFilePath = "outputFiles/logFile.txt";
        AmazonCrawler amazonCrawler = new AmazonCrawler(proxyFilePath, logFilePath);
        amazonCrawler.testProxy();

    }
}
