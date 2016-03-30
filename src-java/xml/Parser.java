package xml;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public class Parser {
	
	private final String outputFolder = "C:/Users/jmcaninl/Documents/Workspace/Biases/data/processed/";
	
	public String parseSingleExportFromFile(String filename) throws IOException {
		
		String plainText = "";
		
		System.out.println(filename);
		BufferedReader br = new BufferedReader(new FileReader(filename));
		
		BufferedWriter bw = new BufferedWriter(new FileWriter(outputFolder + filename.substring(filename.lastIndexOf("/"))));
		
		String line = null;
		/*
		int wordCount = 0;
		boolean hasNextPage = true, wordFound = false;
		*/
		
		while((line = br.readLine()) != null) {
			
			line.replaceAll("&quot", "");
			line.replaceAll("===", "");
			line.replaceAll("&lt", "");
			line.replaceAll("&rt", "");
			
			/*
			int lineCount = 0;
			wordFound = false;
			int startIndex = 0;
			
			for(int i = 0; i < line.length(); i++) {
				
				if(line.charAt(i) == ' ') {
					if(wordFound) {
					  lineCount++;
					  String word = line.substring(startIndex, i);
					  if(words.containsKey(word)) {
						  words.put(word, words.get(word)+1);
					  }
					  else {
						  words.put(word, 1);
					  }
					  wordFound = false;
					  startIndex = i+1;
					}
				} else {
					wordFound = true;
				}
			}
			
			wordCount += lineCount;
			
			*/
			plainText += line;
			
			bw.write(line);
		}
		
		bw.close();
		
		return plainText;
	}

	public void wordCount() throws IOException {
		
		HashMap<String, Integer> words = new HashMap<String, Integer>();
		
		String line = null;
		int wordCount = 0;
		boolean hasNextPage = true, wordFound = false;
		
		long start = System.currentTimeMillis();
		
		BufferedReader br = new BufferedReader(new FileReader("../../../../Downloads/Wikipedia-20160203050807.xml"));
		
		while((line = br.readLine()) != null) {
			
			int lineCount = 0;
			wordFound = false;
			int startIndex = 0;
			
			for(int i = 0; i < line.length(); i++) {
				
				if(line.charAt(i) == ' ') {
					if(wordFound) {
					  lineCount++;
					  String word = line.substring(startIndex, i);
					  if(words.containsKey(word)) {
						  words.put(word, words.get(word)+1);
					  }
					  else {
						  words.put(word, 1);
					  }
					  wordFound = false;
					  startIndex = i+1;
					}
				} else {
					wordFound = true;
				}
			}
			
			wordCount += lineCount;
			
			/*
			while(!(line.contains("<page>"))) {
			
				line = br.readLine();
				if(line == null) {
					hasNextPage = false;
					break;
				}
			}
		
			if(hasNextPage) {
				while(!(line.contains("<title>"))) {
			
					line = br.readLine();
				}
			
				System.out.println(line.substring(line.indexOf("<title>") + 7, line.indexOf("</title>")));
		
				count++;
			}
			*/
		}
		
		words = (HashMap<String, Integer>) sortByValue(words);
		for(Entry<String, Integer> w : words.entrySet()) {
			System.out.println(w.getKey() + " " + w.getValue());
		}
		System.out.println("Count: " + wordCount);
		long time = System.currentTimeMillis() - start;
		System.out.println("Runtime: " + time / 60000 + "m " + (time / 1000) % 60 + "s");
		
	}
	
	public <K, V extends Comparable<? super V>> Map<K, V> sortByValue(Map<K, V> map) {
    
		List<Map.Entry<K, V>> list = new LinkedList<Map.Entry<K, V>>(map.entrySet());
		
		Collections.sort(list, new Comparator<Map.Entry<K, V>>()
			{
				public int compare( Map.Entry<K, V> o1, Map.Entry<K, V> o2 )
				{
					return (o1.getValue()).compareTo( o2.getValue() );
				}
			}
		);

		Map<K, V> result = new LinkedHashMap<K, V>();
		
		for (Map.Entry<K, V> entry : list)
		{
			result.put( entry.getKey(), entry.getValue() );
		}
		return result;
    }
}