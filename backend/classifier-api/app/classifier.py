from typing import List
from transformers import pipeline

class ZeroShotEmailClassifier:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    
    def classify(self, text: str, labels: List[str], multi_label: bool = False):
        result = self.classifier(text, candidate_labels=labels, multi_label=multi_label)
        return result
    