package bias;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map.Entry;

import translate.WebTranslator;
import xml.Parser;

public class BaselineDetector {

	private ArrayList<HashMap<String, Integer>> words = new ArrayList<HashMap<String, Integer>>();
	private ArrayList<String> allWords = new ArrayList<String>();
	private  final String fileFolder = "C:/Users/jmcaninl/Documents/Workspace/Biases/data/xml/";
	private String[] filenames = {"enwiki-", "eswiki-", "ruwiki-"};
	private final int ENWIKI = 0, ESWIKI = 1, RUWIKI = 2;

	public static void main(String[] args) throws IOException {
		
		BaselineDetector bd = new BaselineDetector();
		
		bd.analyzeTriple(args[0]);
	}
	
	public BaselineDetector() {
		
		for(int i = 0; i < 3; i++) {
			words.add(new HashMap<String, Integer>());
			filenames[i] = this.fileFolder + filenames[i];
		}
	}
	
	public void analyzeTriple(String enArticleName) throws IOException {
		
		String[] plainText = new String[3];
		int[] wordCount = {0, 0, 0};
		
		Parser parser = new Parser();
		WebTranslator wt = new WebTranslator();
		
		for(int lang = 0; lang < 3; lang++) {
			
			plainText[lang] = parser.parseSingleExportFromFile(filenames[lang] + enArticleName + ".xml");

			if(lang == ESWIKI) plainText[lang] = wt.translate("es", "en", plainText[lang]);
			else if(lang == RUWIKI) plainText[lang] = wt.translate("ru", "en", plainText[lang]);
			
			boolean wordFound = false;
			int startIndex = 0;
			for(int c = 0; c < plainText[lang].length(); c++) {
				
				if(plainText[lang].charAt(c) == ' ') {
					if(wordFound) {
					  wordCount[lang]++;
					  String word = plainText[lang].substring(startIndex, c);
					  if(words.get(lang).containsKey(word)) {
						  words.get(lang).put(word, words.get(lang).get(word)+1);
					  }
					  else {
						  words.get(lang).put(word, 1);
						  if(!allWords.contains(word)) {
							  allWords.add(word);
						  }
					  }
					  wordFound = false;
					  startIndex = c+1;
					}
				} else {
					wordFound = true;
				}
			}
		}
		
		double[] magnitude = new double[3];
		for(int lang = 0; lang < 3; lang++) {
			for(Entry<String, Integer> word : words.get(lang).entrySet()) {
				magnitude[lang] += Math.pow(word.getValue(), 2);
			}
			magnitude[lang] = Math.sqrt(magnitude[lang]); 
		}
		
		int en_ru_dot = 0;
		for(String word : allWords) {
			int enValue = words.get(ENWIKI).get(word) == null ? 0 : words.get(ENWIKI).get(word);
			int ruValue = words.get(RUWIKI).get(word) == null ? 0 : words.get(RUWIKI).get(word);
			en_ru_dot += enValue * ruValue;
		}
		double en_ru_cosine = (double)en_ru_dot / (double)(magnitude[ENWIKI] * magnitude[RUWIKI]);

		int en_es_dot = 0;
		for(String word : allWords) {
			int enValue = words.get(ENWIKI).get(word) == null ? 0 : words.get(ENWIKI).get(word);
			int esValue = words.get(ESWIKI).get(word) == null ? 0 : words.get(ESWIKI).get(word);
			en_es_dot += enValue * esValue;
		}
		double en_es_cosine = (double)en_es_dot / (double)(magnitude[ENWIKI] * magnitude[ESWIKI]);
		
		int es_ru_dot = 0;
		for(String word : allWords) {
			int esValue = words.get(ESWIKI).get(word) == null ? 0 : words.get(ESWIKI).get(word);
			int ruValue = words.get(RUWIKI).get(word) == null ? 0 : words.get(RUWIKI).get(word);
			es_ru_dot += esValue * ruValue;
		}
		double es_ru_cosine = (double)es_ru_dot / (double)(magnitude[ESWIKI] * magnitude[RUWIKI]);
		
		System.out.println("EN_RU COSINE: " + en_ru_cosine);
		System.out.println("EN_ES COSINE: " + en_es_cosine);
		System.out.println("ES_RU COSINE: " + es_ru_cosine);
	}
}