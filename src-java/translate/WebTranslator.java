package translate;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashSet;

public class WebTranslator {
	
	private String key = "trnsl.1.1.20160302T004242Z.7161c8aebd4b02f4.2305e50205506efda15504b7f7e1a350a955cc1a";
	private String urlString = "https://translate.yandex.net/api/v1.5/tr/translate";
	
	public String translate(String fromLanguage, String toLanguage, String text) {
		
		String urlWithParams 
			= urlString + "?"
			+ "key="	+ key 
			+ "&lang=" 	+ fromLanguage + "-" + toLanguage
			+ "&text=";
				
		String textTranslated = "";
		int begin = 0, end = 0;
		
		while(end < text.length()) {
			
			if(text.length()-end < 10000-urlWithParams.length()) {
				end = text.length();
			} else {
				end = text.lastIndexOf(". ", begin + 10000 - urlWithParams.length()) + 2;
			}
			String snippet = text.substring(begin, end);
			begin = end;
			
			URL url = null;
			try {
				url = new URL(urlWithParams + snippet);
			} catch (MalformedURLException e1) {
				e1.printStackTrace();
			}
			
			try (BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream(), "UTF-8"))) {
				for (String line; (line = reader.readLine()) != null;) {
					textTranslated += line;
			    }
			} catch (Exception e) {
				e.printStackTrace();
			}
		}		
		
		return textTranslated;
	}
}