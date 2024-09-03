import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import pandas as pd
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
NLTK_DATA_DIR = f'{CURRENT_DIR}/nltk_data'
nltk.data.path.append(NLTK_DATA_DIR)

# Download necessary NLTK data
nltk.download('punkt', download_dir=NLTK_DATA_DIR)
nltk.download('punkt_tab', download_dir=NLTK_DATA_DIR)
nltk.download('stopwords', download_dir=NLTK_DATA_DIR)
nltk.download('wordnet', download_dir=NLTK_DATA_DIR)




class NltkVariablesExtractor:
    def __init__(self, variablesPath=f'{CURRENT_DIR}/variables_clean.csv'):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.df_variables = pd.read_csv(variablesPath)
        
    def preprocess_text(self, text):
        word_tokens = word_tokenize(text.lower())
        return [self.lemmatizer.lemmatize(w) for w in word_tokens if w.isalnum() and w not in self.stop_words]
    
    def calculate_relevance_score(self, query_tokens, label_tokens):
        # Calculate Jaccard similarity
        intersection = set(query_tokens).intersection(set(label_tokens))
        union = set(query_tokens).union(set(label_tokens))
        return len(intersection) / len(union) if union else 0
    
    def find_relevant_variables(self, query, threshold=0.2):
        if query is None or query.strip()=='':
            threshold=-1
        query_tokens = self.preprocess_text(query)
        
        relevant_vars = {}
        for index, row in self.df_variables.iterrows():
            label_tokens = self.preprocess_text(row['Label'])
            score = self.calculate_relevance_score(query_tokens, label_tokens)
            if score > threshold:
                # relevant_vars.append((row['Name'], row['Label'] , score))
                relevant_vars[row['Label']]=row['Name']
        
        # Sort by relevance score in descending order
        # relevant_vars.sort(key=lambda x: x[1], reverse=True)
        
        
        # Return only the variable names and labels, not the scores
        return relevant_vars
        # return [(var[0],var[1] ) for var in relevant_vars]
        
        
        
        
if __name__ == '__main__':
    engine = NltkVariablesExtractor()
    # Example usage
    query = "Data on who don't speak English well"
    relevant_variables = engine.find_relevant_variables(query)
    for var in relevant_variables:
        print(var)
    # print(relevant_variables)
    print(len(relevant_variables))