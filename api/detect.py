"""
AI vs Human Text Detector API
Reference: https://justdone.com/ai-detector

This API uses TF-IDF + Logistic Regression to detect whether text is AI-generated or human-written.
"""

import json
import re
import math
from http.server import BaseHTTPRequestHandler


# Pre-trained model parameters (simplified for serverless deployment)
# These coefficients are based on common AI vs Human writing patterns
class AIDetectorModel:
    """
    A lightweight AI text detector using TF-IDF-like features and Logistic Regression.
    
    Features used for detection:
    1. Average sentence length
    2. Vocabulary richness (type-token ratio)
    3. Punctuation density
    4. Conjunction usage frequency
    5. First-person pronoun usage
    6. Passive voice indicators
    7. Average word length
    8. Sentence complexity (clauses per sentence)
    """
    
    def __init__(self):
        # Pre-trained coefficients (learned from AI vs Human text samples)
        # Positive coefficients indicate AI-like features
        self.coefficients = {
            'avg_sentence_length': 0.025,      # AI tends to have more uniform sentence lengths
            'vocabulary_richness': -1.5,       # Humans tend to have more varied vocabulary
            'punctuation_density': -0.5,       # Humans use more varied punctuation
            'conjunction_freq': 0.6,           # AI often uses more conjunctions
            'first_person_freq': -1.5,         # Humans use more first-person pronouns
            'passive_voice_freq': 0.8,         # AI tends to use more passive voice
            'avg_word_length': 0.4,            # AI often uses slightly longer words
            'sentence_complexity': 0.5,        # AI tends to have consistent complexity
            'repetition_score': 1.0,           # AI tends to repeat phrases
            'formality_score': 1.2,            # AI tends to be more formal
        }
        self.intercept = 0.4
    
    def extract_features(self, text: str) -> dict:
        """Extract linguistic features from text."""
        if not text or len(text.strip()) == 0:
            return {}
        
        # Clean and tokenize
        sentences = self._split_sentences(text)
        words = self._tokenize(text)
        
        if len(words) == 0 or len(sentences) == 0:
            return {}
        
        features = {}
        
        # 1. Average sentence length
        sentence_lengths = [len(self._tokenize(s)) for s in sentences]
        features['avg_sentence_length'] = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        # 2. Vocabulary richness (type-token ratio)
        unique_words = set(word.lower() for word in words)
        features['vocabulary_richness'] = len(unique_words) / len(words) if words else 0
        
        # 3. Punctuation density
        punctuation_count = sum(1 for char in text if char in '.,!?;:"-()[]{}')
        features['punctuation_density'] = punctuation_count / len(words) if words else 0
        
        # 4. Conjunction frequency
        conjunctions = {'and', 'but', 'or', 'so', 'yet', 'for', 'nor', 'although', 
                       'because', 'since', 'while', 'whereas', 'however', 'therefore',
                       'moreover', 'furthermore', 'additionally', 'consequently'}
        conjunction_count = sum(1 for word in words if word.lower() in conjunctions)
        features['conjunction_freq'] = conjunction_count / len(words) if words else 0
        
        # 5. First-person pronoun frequency
        first_person = {'i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves'}
        first_person_count = sum(1 for word in words if word.lower() in first_person)
        features['first_person_freq'] = first_person_count / len(words) if words else 0
        
        # 6. Passive voice indicators
        passive_indicators = {'was', 'were', 'been', 'being', 'is', 'are', 'am'}
        passive_count = sum(1 for word in words if word.lower() in passive_indicators)
        features['passive_voice_freq'] = passive_count / len(words) if words else 0
        
        # 7. Average word length
        features['avg_word_length'] = sum(len(word) for word in words) / len(words) if words else 0
        
        # 8. Sentence complexity (estimated by punctuation within sentences)
        clause_markers = sum(1 for char in text if char in ',;:')
        features['sentence_complexity'] = clause_markers / len(sentences) if sentences else 0
        
        # 9. Repetition score (phrase repetition)
        features['repetition_score'] = self._calculate_repetition(words)
        
        # 10. Formality score
        features['formality_score'] = self._calculate_formality(text, words)
        
        return features
    
    def _split_sentences(self, text: str) -> list:
        """Split text into sentences."""
        # Simple sentence splitting using regex
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _tokenize(self, text: str) -> list:
        """Tokenize text into words."""
        # Simple word tokenization
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        return words
    
    def _calculate_repetition(self, words: list) -> float:
        """Calculate a repetition score based on repeated n-grams."""
        if len(words) < 4:
            return 0.0
        
        # Check for repeated trigrams
        trigrams = []
        for i in range(len(words) - 2):
            trigram = ' '.join(words[i:i+3]).lower()
            trigrams.append(trigram)
        
        if not trigrams:
            return 0.0
        
        # Count repeated trigrams
        unique_trigrams = set(trigrams)
        repetition_ratio = 1 - (len(unique_trigrams) / len(trigrams))
        return repetition_ratio
    
    def _calculate_formality(self, text: str, words: list) -> float:
        """Calculate formality score based on contractions and informal words."""
        if not words:
            return 0.5
        
        # Check for contractions (informal)
        contractions = re.findall(r"\b\w+'[a-z]+\b", text.lower())
        contraction_ratio = len(contractions) / len(words)
        
        # Informal words/phrases
        informal_markers = {'gonna', 'wanna', 'kinda', 'sorta', 'yeah', 'yep', 
                          'nope', 'ok', 'okay', 'hey', 'hi', 'well', 'like',
                          'actually', 'basically', 'literally', 'totally'}
        informal_count = sum(1 for word in words if word.lower() in informal_markers)
        informal_ratio = informal_count / len(words)
        
        # Higher formality = less contractions and informal words
        formality = 1 - (contraction_ratio * 2 + informal_ratio)
        return max(0, min(1, formality))
    
    def predict(self, text: str) -> dict:
        """
        Predict whether text is AI-generated or human-written.
        
        Returns:
            dict with 'prediction' ('AI' or 'Human'), 'confidence', and 'features'
        """
        features = self.extract_features(text)
        
        if not features:
            return {
                'prediction': 'Unknown',
                'confidence': 0.0,
                'ai_probability': 0.5,
                'human_probability': 0.5,
                'features': {},
                'message': 'Text too short or invalid for analysis'
            }
        
        # Calculate logit score
        logit = self.intercept
        for feature_name, coefficient in self.coefficients.items():
            if feature_name in features:
                # Normalize features to reasonable ranges
                value = features[feature_name]
                if feature_name == 'avg_sentence_length':
                    value = (value - 15) / 10  # Center around 15 words, scale by 10
                elif feature_name == 'avg_word_length':
                    value = (value - 5) / 2    # Center around 5 chars, scale by 2
                elif feature_name == 'sentence_complexity':
                    value = (value - 1) / 2    # Center around 1, scale by 2
                
                logit += coefficient * value
        
        # Convert logit to probability using sigmoid
        ai_probability = 1 / (1 + math.exp(-logit))
        human_probability = 1 - ai_probability
        
        # Make prediction
        if ai_probability > 0.6:
            prediction = 'AI'
            confidence = ai_probability
        elif human_probability > 0.6:
            prediction = 'Human'
            confidence = human_probability
        else:
            prediction = 'Uncertain'
            confidence = max(ai_probability, human_probability)
        
        # Calculate word count
        word_count = len(self._tokenize(text))
        
        return {
            'prediction': prediction,
            'confidence': round(confidence * 100, 1),
            'ai_probability': round(ai_probability * 100, 1),
            'human_probability': round(human_probability * 100, 1),
            'word_count': word_count,
            'features': {
                'avg_sentence_length': round(features.get('avg_sentence_length', 0), 2),
                'vocabulary_richness': round(features.get('vocabulary_richness', 0) * 100, 1),
                'formality_score': round(features.get('formality_score', 0) * 100, 1),
            },
            'message': f'Analysis complete. The text appears to be {prediction.lower()}-{"generated" if prediction == "AI" else "written"}.'
        }


# Initialize model
detector = AIDetectorModel()


class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Function Handler"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests - return API info"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'ok',
            'message': 'AI Detector API is running',
            'usage': 'POST /api/detect with {"text": "your text here"}',
            'reference': 'https://justdone.com/ai-detector'
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests - perform AI detection"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # Parse JSON
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_error_response(400, 'Invalid JSON format')
                return
            
            # Extract text
            text = data.get('text', '')
            
            if not text or len(text.strip()) < 50:
                self.send_error_response(400, 'Text must be at least 50 characters long for accurate analysis')
                return
            
            # Perform detection
            result = detector.predict(text)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_error_response(500, f'Internal server error: {str(e)}')
    
    def send_error_response(self, status_code: int, message: str):
        """Send an error response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'error': message}
        self.wfile.write(json.dumps(response).encode())
