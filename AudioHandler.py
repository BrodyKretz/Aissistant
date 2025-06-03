"""
Audio handler for continuous listening and transcription
"""
import speech_recognition as sr
from PyQt6.QtCore import QThread, pyqtSignal
import queue
import numpy as np

class AudioListenerThread(QThread):
    """Thread for continuous audio listening"""
    transcription_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = queue.Queue()
        self.is_running = False
        self.is_visualization_mode = False
        
        # Adjust recognizer settings for better performance
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        self.recognizer.pause_threshold = 0.8
        self.recognizer.operation_timeout = None
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
    
    def run(self):
        """Main thread loop"""
        self.is_running = True
        
        with self.microphone as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
        # Start background listening
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, 
            self.audio_callback,
            phrase_time_limit=None
        )
        
        # Process audio queue
        while self.is_running:
            try:
                audio = self.audio_queue.get(timeout=0.5)
                self.process_audio(audio)
            except queue.Empty:
                continue
            except Exception as e:
                self.error_occurred.emit(f"Error processing audio: {str(e)}")
    
    def audio_callback(self, recognizer, audio):
        """Callback for background listening"""
        try:
            self.audio_queue.put(audio)
        except Exception as e:
            self.error_occurred.emit(f"Error in audio callback: {str(e)}")
    
    def process_audio(self, audio):
        """Process audio and transcribe"""
        try:
            # Try Google Speech Recognition first (free, no API key needed)
            text = self.recognizer.recognize_google(audio)
            
            if text:
                self.transcription_ready.emit(text)
                
        except sr.UnknownValueError:
            # Speech not understood, ignore
            pass
        except sr.RequestError as e:
            self.error_occurred.emit(f"Speech recognition error: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"Unexpected error: {str(e)}")
    
    def stop(self):
        """Stop the thread"""
        self.is_running = False
        if hasattr(self, 'stop_listening'):
            self.stop_listening(wait_for_stop=False)
        self.wait()

class VisualizationListenerThread(QThread):
    """Thread for visualization mode listening"""
    visualization_request = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_running = False
        self.is_recording = False
    
    def run(self):
        """Main thread loop for visualization"""
        self.is_running = True
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.is_running:
                if self.is_recording:
                    try:
                        # Listen until silence
                        audio = self.recognizer.listen(
                            source,
                            timeout=None,
                            phrase_time_limit=10
                        )
                        
                        # Transcribe
                        text = self.recognizer.recognize_google(audio)
                        if text:
                            self.visualization_request.emit(text)
                        
                        self.is_recording = False
                        
                    except sr.WaitTimeoutError:
                        pass
                    except Exception as e:
                        self.error_occurred.emit(f"Visualization error: {str(e)}")
                        self.is_recording = False
                else:
                    self.msleep(100)
    
    def start_recording(self):
        """Start recording for visualization"""
        self.is_recording = True
    
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
    
    def stop(self):
        """Stop the thread"""
        self.is_running = False
        self.is_recording = False
        self.wait()

class AudioHandler:
    """Main audio handler class"""
    def __init__(self):
        self.listener_thread = None
        self.viz_thread = None
        self.transcription_ready = None
        self.visualization_request = None
    
    def start_listening(self):
        """Start continuous listening"""
        if not self.listener_thread or not self.listener_thread.isRunning():
            self.listener_thread = AudioListenerThread()
            if self.transcription_ready:
                self.listener_thread.transcription_ready.connect(self.transcription_ready)
            self.listener_thread.start()
    
    def stop_listening(self):
        """Stop listening"""
        if self.listener_thread and self.listener_thread.isRunning():
            self.listener_thread.stop()
    
    def start_visualization_mode(self):
        """Start visualization mode"""
        if not self.viz_thread or not self.viz_thread.isRunning():
            self.viz_thread = VisualizationListenerThread()
            if self.visualization_request:
                self.viz_thread.visualization_request.connect(self.visualization_request)
            self.viz_thread.start()
            self.viz_thread.start_recording()
    
    def stop_visualization_mode(self):
        """Stop visualization mode"""
        if self.viz_thread and self.viz_thread.isRunning():
            self.viz_thread.stop()
