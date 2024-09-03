from .NltkVariablesExtractor import NltkVariablesExtractor

def get_relevant_variables_nltk(query):
    nlp_engine = NltkVariablesExtractor()
    return nlp_engine.find_relevant_variables(query)
