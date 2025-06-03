"""
Main window UI for the Audio Q&A Assistant
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QGroupBox,
    QDialog, QListWidget, QDialogButtonBox, QMessageBox,
    QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QPalette, QColor
from audio.audio_handler import AudioHandler
from ai.llm_handler import LLMHandler
from ai.question_detector import QuestionDetector

class SubjectSelectionDialog(QDialog):
    """Dialog for selecting the subject at startup"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Subject")
        self.setModal(True)
        self.setFixedSize(400, 500)
        
        layout = QVBoxLayout()
        
        # Instructions
        label = QLabel("Please select a subject for your Q&A session:")
        label.setWordWrap(True)
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)
        layout.addWidget(label)
        
        # Subject list
        self.subject_list = QListWidget()
        self.subject_list.setFont(QFont("Arial", 11))
        subjects = [
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "Computer Science",
            "History",
            "English Literature",
            "Geography",
            "Economics",
            "Psychology"
        ]
        self.subject_list.addItems(subjects)
        self.subject_list.setCurrentRow(0)
        layout.addWidget(self.subject_list)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_selected_subject(self):
        current_item = self.subject_list.currentItem()
        return current_item.text() if current_item else "General"

class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.selected_subject = None
        self.current_question = None
        self.current_answer = None
        self.is_listening = False
        
        # Initialize handlers
        self.audio_handler = AudioHandler()
        self.llm_handler = LLMHandler()
        self.question_detector = QuestionDetector()
        
        # Connect signals
        self.audio_handler.transcription_ready.connect(self.on_transcription)
        self.llm_handler.answer_ready.connect(self.on_answer_ready)
        
        # Setup UI
        self.setup_ui()
        
        # Show subject selection dialog
        self.show_subject_dialog()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Audio Q&A Assistant")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Audio Q&A Assistant")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont("Arial", 20, QFont.Weight.Bold)
        header.setFont(header_font)
        main_layout.addWidget(header)
        
        # Subject label
        self.subject_label = QLabel("Subject: Not Selected")
        self.subject_label.setFont(QFont("Arial", 12))
        self.subject_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.subject_label)
        
        # Control buttons
        control_group = QGroupBox("Audio Controls")
        control_layout = QHBoxLayout()
        
        self.listen_button = QPushButton("Start Listening")
        self.listen_button.setCheckable(True)
        self.listen_button.setFont(QFont("Arial", 12))
        self.listen_button.setMinimumHeight(50)
        self.listen_button.clicked.connect(self.toggle_listening)
        self.listen_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:checked {
                background-color: #f44336;
            }
            QPushButton:checked:hover {
                background-color: #da190b;
            }
        """)
        control_layout.addWidget(self.listen_button)
        
        self.visualize_button = QPushButton("Visualize")
        self.visualize_button.setCheckable(True)
        self.visualize_button.setFont(QFont("Arial", 12))
        self.visualize_button.setMinimumHeight(50)
        self.visualize_button.clicked.connect(self.toggle_visualization)
        self.visualize_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:checked {
                background-color: #ff9800;
            }
            QPushButton:checked:hover {
                background-color: #e68900;
            }
        """)
        control_layout.addWidget(self.visualize_button)
        
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        # Status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        main_layout.addWidget(self.status_label)
        
        # Transcription area
        trans_group = QGroupBox("Live Transcription")
        trans_layout = QVBoxLayout()
        
        self.transcription_area = QTextEdit()
        self.transcription_area.setReadOnly(True)
        self.transcription_area.setFont(QFont("Consolas", 10))
        self.transcription_area.setMaximumHeight(150)
        trans_layout.addWidget(self.transcription_area)
        
        trans_group.setLayout(trans_layout)
        main_layout.addWidget(trans_group)
        
        # Q&A area
        qa_group = QGroupBox("Question & Answer")
        qa_layout = QVBoxLayout()
        
        # Answer notification area
        self.answer_notification = QFrame()
        self.answer_notification.setVisible(False)
        self.answer_notification.setFrameStyle(QFrame.Shape.Box)
        self.answer_notification.setStyleSheet("""
            QFrame {
                background-color: #fff3cd;
                border: 2px solid #ffeaa7;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        notif_layout = QHBoxLayout(self.answer_notification)
        
        notif_label = QLabel("New answer available!")
        notif_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        notif_layout.addWidget(notif_label)
        
        notif_layout.addStretch()
        
        self.answer_button = QPushButton("ANSWER")
        self.answer_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.answer_button.clicked.connect(self.show_answer)
        self.answer_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        notif_layout.addWidget(self.answer_button)
        
        self.ignore_button = QPushButton("Ignore")
        self.ignore_button.setFont(QFont("Arial", 12))
        self.ignore_button.clicked.connect(self.ignore_question)
        self.ignore_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        notif_layout.addWidget(self.ignore_button)
        
        qa_layout.addWidget(self.answer_notification)
        
        # Q&A display area
        self.qa_display = QScrollArea()
        self.qa_content = QWidget()
        self.qa_content_layout = QVBoxLayout(self.qa_content)
        self.qa_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.qa_display.setWidget(self.qa_content)
        self.qa_display.setWidgetResizable(True)
        self.qa_display.setMinimumHeight(200)
        qa_layout.addWidget(self.qa_display)
        
        qa_group.setLayout(qa_layout)
        main_layout.addWidget(qa_group)
        
        # Apply dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
    
    def show_subject_dialog(self):
        """Show subject selection dialog"""
        dialog = SubjectSelectionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.selected_subject = dialog.get_selected_subject()
            self.subject_label.setText(f"Subject: {self.selected_subject}")
            self.llm_handler.set_subject(self.selected_subject)
        else:
            # If cancelled, exit application
            QMessageBox.warning(self, "No Subject Selected", 
                              "A subject must be selected to continue.")
            sys.exit()
    
    @pyqtSlot()
    def toggle_listening(self):
        """Toggle audio listening"""
        if self.listen_button.isChecked():
            self.listen_button.setText("Stop Listening")
            self.status_label.setText("Status: Listening...")
            self.audio_handler.start_listening()
            self.is_listening = True
        else:
            self.listen_button.setText("Start Listening")
            self.status_label.setText("Status: Stopped")
            self.audio_handler.stop_listening()
            self.is_listening = False
    
    @pyqtSlot()
    def toggle_visualization(self):
        """Toggle visualization mode"""
        if self.visualize_button.isChecked():
            self.visualize_button.setText("Stop Visualization")
            self.status_label.setText("Status: Listening for visualization...")
            self.audio_handler.start_visualization_mode()
        else:
            self.visualize_button.setText("Visualize")
            self.status_label.setText("Status: Ready")
            self.audio_handler.stop_visualization_mode()
    
    @pyqtSlot(str)
    def on_transcription(self, text):
        """Handle new transcription"""
        self.transcription_area.append(text)
        
        # Check if it's a question
        if self.is_listening and self.question_detector.is_question(text):
            self.current_question = text
            self.status_label.setText("Status: Processing question...")
            self.llm_handler.get_answer(text)
    
    @pyqtSlot(str)
    def on_answer_ready(self, answer):
        """Handle answer from LLM"""
        self.current_answer = answer
        self.answer_notification.setVisible(True)
        self.status_label.setText("Status: Answer ready!")
    
    @pyqtSlot()
    def show_answer(self):
        """Display the current Q&A"""
        if self.current_question and self.current_answer:
            # Create Q&A widget
            qa_widget = self.create_qa_widget(self.current_question, self.current_answer)
            self.qa_content_layout.addWidget(qa_widget)
            
            # Clear current Q&A
            self.current_question = None
            self.current_answer = None
            self.answer_notification.setVisible(False)
            self.status_label.setText("Status: Listening...")
    
    @pyqtSlot()
    def ignore_question(self):
        """Ignore the current question"""
        self.current_question = None
        self.current_answer = None
        self.answer_notification.setVisible(False)
        self.status_label.setText("Status: Listening...")
    
    def create_qa_widget(self, question, answer):
        """Create a widget for displaying Q&A"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.Box)
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        
        # Question
        q_label = QLabel("Question:")
        q_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(q_label)
        
        q_text = QLabel(question)
        q_text.setWordWrap(True)
        q_text.setFont(QFont("Arial", 10))
        q_text.setStyleSheet("padding-left: 10px;")
        layout.addWidget(q_text)
        
        # Answer
        a_label = QLabel("Answer:")
        a_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(a_label)
        
        a_text = QLabel(answer)
        a_text.setWordWrap(True)
        a_text.setFont(QFont("Arial", 10))
        a_text.setStyleSheet("padding-left: 10px;")
        layout.addWidget(a_text)
        
        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: widget.deleteLater())
        ok_button.setMaximumWidth(100)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        return widget
    
    def closeEvent(self, event):
        """Clean up when closing"""
        self.audio_handler.stop_listening()
        event.accept()
