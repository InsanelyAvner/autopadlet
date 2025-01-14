import sys
import json
import os
import random
import threading
import traceback
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import concurrent.futures


# ---------- Core Selenium Logic ---------- #

def run_autopadlet(logger_callback, link, mode, threads):
    """
    Runs the autopadlet logic with the given parameters.

    :param logger_callback: a function to call for logging output (e.g. in the UI)
    :param link: The Padlet link to target
    :param mode: "like" or any other mode (to post random comments)
    :param threads: Number of parallel threads
    """
    # Comments for random usage
    comments = [
        "Great job!",
        "Well done!",
        "Fantastic work!",
        "Impressive effort!",
        "Keep it up!",
        "Brilliant!",
        "You nailed it!",
        "That's exactly right!",
        "Outstanding performance!",
        "You're doing a great job!",
        "That was first-class work!",
        "You've got this!",
        "Amazing progress!",
        "Superb!",
        "You exceeded expectations!"
    ]

    # Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    logger_callback("--- AUTOPADLET LOG ---")

    # Worker function used per thread
    def slave(n, stop_event):
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        count = 0  # to track the number of likes/comments added
        wait = WebDriverWait(driver, 10)

        while not stop_event.is_set():
            try:
                driver.get(link)

                # Like logic
                if mode.lower() == "like":
                    # Preliminary short delay to let the page load fully
                    import time
                    time.sleep(1)  # Adjust as needed

                    try:
                        # Wait for the like button to be clickable
                        like_button = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Like post"]'))
                        )
                        time.sleep(1)  # allow animations to settle
                        # Scroll element into center of view
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", like_button)

                        # Attempt normal click, fallback to JS click
                        try:
                            like_button.click()
                        except Exception as e_click:
                            logger_callback(f"[INSTANCE {n}] Normal click intercepted: {e_click}\nTrying JS click.")
                            driver.execute_script("arguments[0].click();", like_button)

                    except Exception as e:
                        logger_callback(f"[INSTANCE {n}] No Like Button Found or not clickable: {e}")

                    # Attempt the Done button if it exists
                    try:
                        time.sleep(1)
                        done_button = wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="app"]/div[4]/div/div/div/div/form/div[2]/button')
                            )
                        )
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", done_button)
                        time.sleep(0.5)

                        # Normal click, then fallback
                        try:
                            done_button.click()
                        except Exception as e_click:
                            logger_callback(f"[INSTANCE {n}] Normal 'Done' click intercepted: {e_click}\nTrying JS click.")
                            driver.execute_script("arguments[0].click();", done_button)

                        time.sleep(4)
                    except Exception as e:
                        logger_callback(f"[INSTANCE {n}] No Done Button Found: {e}")

                # Comment logic
                else:
                    comment_box = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/div/div/div/div/p')
                        )
                    )
                    comment_box.send_keys(random.choice(comments))

                    comment_button = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/button')
                        )
                    )
                    comment_button.click()

                count += 1
                logger_callback(
                    f"[INSTANCE {n}] {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} "
                    f"| Total {mode.capitalize()}s Added: {count}"
                )

                # Reset cookies
                driver.delete_all_cookies()

            except Exception as ex:
                logger_callback(f"[INSTANCE {n}] Error: {ex}")
                break

        driver.quit()

    # We use a stop_event to tell threads to stop gracefully
    stop_event = threading.Event()

    # We store threads in an executor, so we can cancel them if needed
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(slave, i + 1, stop_event) for i in range(threads)]
        return stop_event, futures


class AutoPadletWorker(QtCore.QObject):
    """
    A worker object to handle the autopadlet logic in a background thread
    so it doesn't block the main GUI.
    """
    log_signal = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self, link, mode, threads):
        super().__init__()
        self.link = link
        self.mode = mode
        self.threads = threads
        self.stop_event = None
        self.futures = []

    def run(self):
        """
        This function will run in a background thread:
        It starts the autopadlet code, spawns multiple threads,
        and waits for them to finish or be stopped.
        """
        try:
            self.stop_event, self.futures = run_autopadlet(
                logger_callback=self.log_message,
                link=self.link,
                mode=self.mode,
                threads=self.threads
            )

            # Wait for all futures to complete or to be stopped
            for future in self.futures:
                # If any exception occurs in a worker, it'll appear here
                future.result()

        except Exception:
            self.log_signal.emit(f"ERROR: {traceback.format_exc()}")
        finally:
            # Signal that we are fully finished
            self.finished.emit()

    def stop(self):
        """
        Stops the worker's ongoing threads.
        """
        if self.stop_event is not None:
            self.log_signal.emit("Stopping threads...")
            self.stop_event.set()

    @QtCore.pyqtSlot(str)
    def log_message(self, msg):
        """
        Receives log messages from autopadlet code and forwards them via signal
        """
        self.log_signal.emit(msg)


# ---------- The Main Window (UI) ---------- #

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Basic window setup
        self.setWindowTitle("AutoPadlet")
        self.resize(600, 700)  # Adjusted size
        
        # Central widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add padding around edges
        main_layout.setSpacing(20)  # Space between widgets
        
        # Title label with proper styling
        title_label = QtWidgets.QLabel("AutoPadlet")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 600;
            color: white;
            margin: 20px 0;
            padding: 20px;
            background-color: rgba(45, 45, 45, 0.7);
            border-radius: 12px;
        """)
        main_layout.addWidget(title_label)
        
        # Input container frame
        input_frame = QtWidgets.QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QtWidgets.QFormLayout(input_frame)
        input_layout.setContentsMargins(30, 30, 30, 30)  # Interior padding
        input_layout.setSpacing(20)  # Space between form rows
        main_layout.addWidget(input_frame)
        
        # Link input with label
        link_label = QtWidgets.QLabel("Link:")
        self.link_edit = QtWidgets.QLineEdit()
        self.link_edit.setPlaceholderText("Enter Padlet link...")
        input_layout.addRow(link_label, self.link_edit)
        
        # Mode input with label
        mode_label = QtWidgets.QLabel("Mode:")
        self.mode_combo = QtWidgets.QComboBox()
        self.mode_combo.addItems(["like", "comment"])
        input_layout.addRow(mode_label, self.mode_combo)
        
        # Threads input with label
        threads_label = QtWidgets.QLabel("Threads:")
        self.thread_spin = QtWidgets.QSpinBox()
        self.thread_spin.setMinimum(1)
        self.thread_spin.setMaximum(50)
        self.thread_spin.setValue(1)
        input_layout.addRow(threads_label, self.thread_spin)
        
        # Button container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        button_layout.setSpacing(15)
        main_layout.addWidget(button_container)
        
        # Buttons
        self.start_button = QtWidgets.QPushButton("Start")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        
        # Log output
        self.log_output = QtWidgets.QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(200)  # Ensure sufficient height
        main_layout.addWidget(self.log_output)
        
        # Apply stylesheet
        self.apply_stylesheet()
        
        # Load config
        self.load_config()
        
        # Connect buttons
        self.start_button.clicked.connect(self.handle_start)
        self.stop_button.clicked.connect(self.handle_stop)
        
    def apply_stylesheet(self):
        """
        Enhanced stylesheet with fixed alignments and modern design
        """
        self.setStyleSheet("""
            QMainWindow {
                background: #1a1b1e;
            }
            
            #inputFrame {
                background-color: rgba(45, 45, 45, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: 500;
                padding: 5px 0;
                min-width: 80px;
            }
            
            QLineEdit {
                background-color: rgba(30, 30, 30, 0.7);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 12px 15px;
                color: #ffffff;
                font-size: 14px;
                selection-background-color: #7289da;
                min-width: 400px;
            }
            
            QLineEdit:focus {
                border: 2px solid #7289da;
                background-color: rgba(40, 40, 40, 0.8);
            }
            
            QLineEdit:hover {
                background-color: rgba(40, 40, 40, 0.7);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            
            QComboBox {
                background-color: rgba(30, 30, 30, 0.7);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 12px 15px;
                color: #ffffff;
                font-size: 14px;
                min-width: 400px;
            }
            
            QComboBox:hover {
                background-color: rgba(40, 40, 40, 0.7);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border: solid 2px #ffffff;
                border-width: 0 2px 2px 0;
                padding: 3px;
                transform: rotate(45deg);
                margin-right: 10px;
            }
            
            QSpinBox {
                background-color: rgba(30, 30, 30, 0.7);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 12px 15px;
                color: #ffffff;
                font-size: 14px;
                min-width: 400px;
            }
            
            QSpinBox:hover {
                background-color: rgba(40, 40, 40, 0.7);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: transparent;
                border: none;
                width: 20px;
                margin: 3px;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #7289da,
                                          stop:1 #5865f2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 14px;
                font-weight: 600;
                min-width: 150px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #5865f2,
                                          stop:1 #7289da);
            }
            
            QPushButton:disabled {
                background: #4f545c;
                color: rgba(255, 255, 255, 0.5);
            }
            
            QTextEdit {
                background-color: rgba(30, 30, 30, 0.7);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 15px;
                color: #dcddde;
                font-family: 'Consolas', monospace;
                font-size: 13px;
                line-height: 1.5;
            }
            
            QScrollBar:vertical {
                background-color: transparent;
                width: 16px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: rgba(114, 137, 218, 0.3);
                border-radius: 8px;
                min-height: 30px;
                margin: 2px 4px 2px 4px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: rgba(114, 137, 218, 0.5);
            }
            
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

    def load_config(self):
        """
        Loads the configuration using QSettings and sets the UI fields.
        If no settings are found, default values are used.
        """
        settings = QSettings("AutoPadlet", "AutoPadletApp")
        link = settings.value("link", "")
        mode = settings.value("mode", "like")
        threads = int(settings.value("threads", 1))

        self.link_edit.setText(link)
        if mode.lower() in ["like", "comment"]:
            self.mode_combo.setCurrentText(mode.lower())
        else:
            self.mode_combo.setCurrentIndex(0)
        self.thread_spin.setValue(threads)

    def save_config(self):
        """
        Saves the current settings using QSettings.
        """
        settings = QSettings("AutoPadlet", "AutoPadletApp")
        settings.setValue('link', self.link_edit.text().strip())
        settings.setValue('mode', self.mode_combo.currentText().strip())
        settings.setValue('threads', self.thread_spin.value())

    def handle_start(self):
        """
        Starts the autopadlet worker in a background thread.
        """
        link = self.link_edit.text().strip()
        mode = self.mode_combo.currentText().strip()
        threads = self.thread_spin.value()

        if not link:
            self.log_output.append("ERROR: Please enter a valid link.")
            return

        # Save the current settings
        self.save_config()

        # Disable Start button, enable Stop button
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.log_output.append(f"Starting AutoPadlet with link={link}, mode={mode}, threads={threads}...")

        # Create the worker and move it to a QThread
        self.worker = AutoPadletWorker(link, mode, threads)
        self.thread = QtCore.QThread()

        self.worker.moveToThread(self.thread)

        # Connect signals
        self.thread.started.connect(self.worker.run)
        self.worker.log_signal.connect(self.on_log_received)
        self.worker.finished.connect(self.on_worker_finished)
        self.thread.finished.connect(self.thread.deleteLater)

        # Start the thread
        self.thread.start()

    def handle_stop(self):
        """
        Stops the worker's threads.
        """
        if hasattr(self, 'worker') and self.worker:
            self.worker.stop()
            self.log_output.append("Stop signal sent.")

    def on_log_received(self, message):
        """
        Receives log messages from the worker and appends them to the log output.
        """
        self.log_output.append(message)
        # Auto-scroll
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )

    def on_worker_finished(self):
        """
        Called when the worker completes or is stopped.
        """
        self.log_output.append("Worker finished.")
        self.thread.quit()

        # Re-enable start and disable stop
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)


# ---------- Main Entry Point ---------- #

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
