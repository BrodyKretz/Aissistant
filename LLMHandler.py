"""
Language Model handler for answering questions
"""
from PyQt6.QtCore import QThread, pyqtSignal
import openai
import os
from typing import Optional

class LLMThread(QThread):
    """Thread for LLM API calls"""
    answer_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, question: str, subject: str, api_key: str):
        super().__init__()
        self.question = question
        self.subject = subject
        self.api_key = api_key
    
    def run(self):
        """Run LLM query"""
        try:
            # Set up OpenAI client
            openai.api_key = self.api_key
            
            # Create the prompt with subject context
            system_prompt = f"""You are a helpful educational assistant specializing in {self.subject}. 
            Answer questions clearly and concisely, providing accurate information relevant to the subject.
            Keep answers educational but easy to understand."""
            
            # Make API call
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # You can change to "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": self.question}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message['content'].strip()
            self.answer_ready.emit(answer)
            
        except Exception as e:
            self.error_occurred.emit(f"LLM Error: {str(e)}")

class VisualizationThread(QThread):
    """Thread for visualization requests"""
    visualization_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, request: str, subject: str, api_key: str):
        super().__init__()
        self.request = request
        self.subject = subject
        self.api_key = api_key
    
    def run(self):
        """Process visualization request"""
        try:
            openai.api_key = self.api_key
            
            # Create visualization prompt
            system_prompt = f"""You are a visualization assistant for {self.subject}.
            When asked to visualize something, provide a detailed description of what the visualization would show.
            If possible, provide ASCII art or text-based diagrams.
            For mathematical functions, describe the graph characteristics."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Visualize: {self.request}"}
                ],
                max_tokens=800,
                temperature=0.5
            )
            
            result = response.choices[0].message['content'].strip()
            self.visualization_ready.emit(result)
            
        except Exception as e:
            self.error_occurred.emit(f"Visualization Error: {str(e)}")

class LLMHandler:
    """Main LLM handler class"""
    def __init__(self):
        self.api_key = None
        self.subject = "General"
        self.answer_ready = None
        self.visualization_ready = None
        
        # Try to get API key from environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # TODO: If no API key in environment, you'll need to set it manually
        # For now, using a placeholder - YOU NEED TO REPLACE THIS
        if not self.api_key:
            self.api_key = "YOUR_OPENAI_API_KEY_HERE"  # <-- REPLACE THIS
    
    def set_subject(self, subject: str):
        """Set the subject for context"""
        self.subject = subject
    
    def get_answer(self, question: str):
        """Get answer to a question"""
        if not self.api_key or self.api_key == "YOUR_OPENAI_API_KEY_HERE":
            if self.answer_ready:
                self.answer_ready.emit("Error: OpenAI API key not configured. Please set your API key.")
            return
        
        thread = LLMThread(question, self.subject, self.api_key)
        if self.answer_ready:
            thread.answer_ready.connect(self.answer_ready)
        thread.start()
    
    def get_visualization(self, request: str):
        """Get visualization for a request"""
        if not self.api_key or self.api_key == "YOUR_OPENAI_API_KEY_HERE":
            if self.visualization_ready:
                self.visualization_ready.emit("Error: OpenAI API key not configured.")
            return
        
        thread = VisualizationThread(request, self.subject, self.api_key)
        if self.visualization_ready:
            thread.visualization_ready.connect(self.visualization_ready)
        thread.start()

# Alternative LLM Handler using Hugging Face (free alternative)
class HuggingFaceLLMHandler:
    """Alternative handler using Hugging Face models (free)"""
    def __init__(self):
        self.subject = "General"
        self.answer_ready = None
        
        # Note: This would require transformers library
        # from transformers import pipeline
        # self.qa_pipeline = pipeline("question-answering")
    
    def set_subject(self, subject: str):
        """Set the subject for context"""
        self.subject = subject
    
    def get_answer(self, question: str):
        """Get answer using local model"""
        # TODO: Implement Hugging Face integration
        # This is a placeholder for local model integration
        if self.answer_ready:
            self.answer_ready.emit(
                "Hugging Face integration not yet implemented. "
                "Please configure OpenAI API key for now."
            )
