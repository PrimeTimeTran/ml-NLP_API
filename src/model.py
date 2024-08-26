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

# Does anyone know where I can find a list of the best kung fu schools in HCMC? 

# Would love to be able to move to SG and continue my training... that'd be dope.

# TIA~!
# https://www.facebook.com/reel/1456874645176248



# Langflow
# Haystack, Gradio
# Vercel AI SDK
