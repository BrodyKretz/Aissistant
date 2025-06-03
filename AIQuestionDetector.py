"""
Question detection module
"""
import re
from typing import List, Set

class QuestionDetector:
    """Detects questions in transcribed text"""
    
    def __init__(self):
        # Question words
        self.question_words = {
            'what', 'when', 'where', 'who', 'whom', 'whose', 'which', 'why', 'how',
            'is', 'are', 'was', 'were', 'do', 'does', 'did', 'can', 'could', 
            'will', 'would', 'should', 'shall', 'may', 'might', 'must',
            'am', 'has', 'have', 'had'
        }
        
        # Question patterns
        self.question_patterns = [
            r'\?$',  # Ends with question mark
            r'^(what|when|where|who|whom|whose|which|why|how)\s+',  # Starts with question word
            r'^(is|are|was|were|do|does|did|can|could|will|would|should)\s+',  # Starts with auxiliary
            r'^(tell me|explain|describe|define|calculate|solve)\s+',  # Command-like questions
            r'(what|how|why|when|where)\s+.*\?*$',  # Contains question word
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.question_patterns]
    
    def is_question(self, text: str) -> bool:
        """
        Determine if the text is a question
        
        Args:
            text: The transcribed text to check
            
        Returns:
            bool: True if text is likely a question
        """
        if not text or len(text.strip()) < 3:
            return False
        
        text = text.strip()
        
        # Check for question mark
        if text.endswith('?'):
            return True
        
        # Check patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True
        
        # Check if starts with question word
        first_word = text.split()[0].lower()
        if first_word in self.question_words:
            return True
        
        # Check for inverted sentence structure (auxiliary before subject)
        words = text.lower().split()
        if len(words) >= 2:
            if words[0] in {'is', 'are', 'was', 'were', 'do', 'does', 'did', 
                           'can', 'could', 'will', 'would', 'should', 'shall',
                           'may', 'might', 'must', 'have', 'has', 'had'}:
                return True
        
        return False
    
    def extract_questions(self, text: str) -> List[str]:
        """
        Extract all questions from a longer text
        
        Args:
            text: Text that may contain multiple sentences
            
        Returns:
            List of detected questions
        """
        questions = []
        
        # Split by common sentence delimiters
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and self.is_question(sentence):
                # Add back question mark if missing
                if not sentence.endswith('?'):
                    sentence += '?'
                questions.append(sentence)
        
        return questions
    
    def get_question_type(self, question: str) -> str:
        """
        Categorize the type of question
        
        Args:
            question: The question text
            
        Returns:
            Type of question (e.g., 'what', 'how', 'yes/no', etc.)
        """
        question_lower = question.lower().strip()
        
        # Check for specific question words
        for q_word in ['what', 'when', 'where', 'who', 'whom', 'whose', 'which', 'why', 'how']:
            if question_lower.startswith(q_word):
                return q_word
        
        # Check for yes/no questions
        yes_no_starters = {'is', 'are', 'was', 'were', 'do', 'does', 'did', 
                          'can', 'could', 'will', 'would', 'should', 'shall',
                          'may', 'might', 'must', 'have', 'has', 'had'}
        
        first_word = question_lower.split()[0] if question_lower.split() else ''
        if first_word in yes_no_starters:
            return 'yes/no'
        
        # Check for command-like questions
        if any(question_lower.startswith(cmd) for cmd in ['tell me', 'explain', 'describe', 'define']):
            return 'explanation'
        
        if any(question_lower.startswith(cmd) for cmd in ['calculate', 'solve', 'compute']):
            return 'calculation'
        
        return 'other'
