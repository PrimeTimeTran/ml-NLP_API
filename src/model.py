from transformers import pipeline

class Model():
    def __init__(self):
      print('Init')
      self.classifier_sentiment = pipeline('sentiment-analysis')
      self.classifier_subject = pipeline('zero-shot-classification')
      self.generator = pipeline("text-generation")

      self.ner = pipeline("ner", grouped_entities=True)
    
    def sentiment_analysis(self, prompt):
      return self.classifier_sentiment(prompt)
    
    def subject_analysis(self, prompt):
      return self.classifier_subject(prompt, candidate_labels=["education", "politics", "business"],)
    
    def generate(self, prompt):
      return self.generator(prompt)
