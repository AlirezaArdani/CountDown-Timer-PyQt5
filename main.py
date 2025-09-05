from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QPushButton, QLabel, QSpinBox
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5 import uic
import sys
import os.path
import resource


class CountdownTimer(QMainWindow):
    def __init__(self):
        super(CountdownTimer, self).__init__()
        # Setup ui
        self.setup_ui()
        # Create sound object
        self.sound_player = QSoundEffect()
        # Timer states variables
        self.total_seconds = 0
        self.is_running = False
        self.is_paused = False
        self.timer = QTimer(self)

        # Define Widgets
        self.timeLabel = self.findChild(QLabel, "counterLabel")
        # Set default label
        self.timeLabel.setText("00:00:00")
        self.startButton = self.findChild(QPushButton, "startCounterPushButton")
        self.stopButton = self.findChild(QPushButton, "stopCounterPushButton")
        self.resetButton = self.findChild(QPushButton, "resetCounterPushButton")
        self.hourNumber = self.findChild(QSpinBox, "hourSpinBox")
        self.minutesNumber = self.findChild(QSpinBox, "minuteSpinBox")
        self.secondsNumber = self.findChild(QSpinBox, "secondSpinBox")
        self.soundBox = self.findChild(QComboBox, "soundBox")

        # Connect signals
        self.connect_signals()

        # Show App
        self.show()

    # Setup ui
    def setup_ui(self):
        # Load UI
        uic.loadUi("countdown_timer.ui", self)
        self.setWindowTitle("Countdown Timer")

        # Add sounds and Apply style
        self.read_and_add_sounds()
        self.apply_style()

    # Connect signal
    def connect_signals(self):
        self.startButton.clicked.connect(self.start_timer)
        self.stopButton.clicked.connect(self.stop_resume_timer)
        self.resetButton.clicked.connect(self.reset_timer)
        # Connect the timer's 'tick' to the update function
        self.timer.timeout.connect(self.update_timer)

    # Start counter
    def start_timer(self):
        # Calculate total seconds to pass to the timer
        if not self.is_running and not self.is_paused:
            hours = self.hourNumber.value()
            minutes = self.minutesNumber.value()
            seconds = self.secondsNumber.value()

            self.total_seconds = (hours * 3600) + (minutes * 60) + seconds
            print(self.total_seconds)
            if self.total_seconds > 0:
                # Change state to running
                self.is_running = True
                print(self.is_running)
                # Start timer to tick every 1000ms
                self.timer.start(1000)
                # Disable Spins
                self.set_inputs_state(False)

    # Stop the Counter
    def stop_resume_timer(self):
        if self.is_running:
            # Change state of running
            self.is_running = False
            self.is_paused = True
            # print(self.is_running)
            # stop timer
            self.timer.stop()
            # print(self.timer.remainingTime()) # if timer is inactive, return -1
            self.stopButton.setText("Resume")
            # Enable Spins
            self.set_inputs_state(True)
        elif self.is_paused:
            self.set_inputs_state(False)
            self.is_running = True
            self.is_paused = False
            self.timer.start(1000)
            self.stopButton.setText("Stop")


    # Stop timer and Reset display stuff
    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.timer.stop()
        # Recalculate total seconds
        hours = self.hourNumber.value()
        minutes = self.minutesNumber.value()
        seconds = self.secondsNumber.value()
        self.total_seconds = (hours * 3600) + (minutes * 60) + seconds
        self.update_display()
        self.set_inputs_state(True)
        self.stopButton.setText("Stop")

    # Decrement timer and Update display
    def update_timer(self):
        if self.total_seconds > 0:
            self.total_seconds -= 1
            self.update_display()
        else:
            # When total_s equal to 0 and time's up
            self.is_running = False
            self.is_paused = False
            self.timer.stop()
            self.set_inputs_state(True)
            self.stopButton.setText("Stop")
            self.play_sound(self.soundBox.currentText())
            print(self.soundBox.currentText())
            QMessageBox.about(self, "Timer's Up!!!....", " The countdown has finished  ")
            self.sound_player.stop()

    def update_display(self):
        h = self.total_seconds // 3600
        m = (self.total_seconds % 3600) // 60
        s = self.total_seconds  % 60
        self.timeLabel.setText(f"{h:02d}:{m:02d}:{s:02d}") # 01:07:10

    # Change Spins enabled or disabled
    def set_inputs_state(self, enabled):
        self.hourNumber.setEnabled(enabled)
        self.minutesNumber.setEnabled(enabled)
        self.secondsNumber.setEnabled(enabled)

    # Add sounds
    def read_and_add_sounds(self):
        sound_directory = "sounds"
        # store sounds
        sounds = []
        # clear if there is any item in combo
        self.soundBox.clear()
        # check if exists
        if os.path.exists(sound_directory):
            # get list of files in sound dir
            for file_name in os.listdir(sound_directory):
                # print(os.listdir(sound_directory))
                if file_name.endswith(".wav"):
                    # its get filename and filename extension
                    sound_name = os.path.splitext(file_name)[0]
                    # print(sound_name)
                    sounds.append(sound_name)

            self.soundBox.addItems(sounds)
            print(sounds)
        else:
            QMessageBox.about(self, "Not Found", "No Directory named  \"sounds\"")

    # Play sound
    def play_sound(self, sound_name):
        # set sounds directory/path
        sound_path = f"sounds/{sound_name}.wav"
        print(sound_path)
        if os.path.exists(sound_path):
            # set source of player for playing sound using QUrl
            self.sound_player.setSource(QUrl.fromLocalFile(sound_path))
            # Set Sound to loop till stopped
            self.sound_player.setLoopCount(QSoundEffect.Infinite)
            # play
            self.sound_player.play()
        else:
            # if there is no path
            QMessageBox.about(self, "Error Finding File", f"Warning: Sound file not found at {sound_path}")

    # Apply style
    def apply_style(self):
        try:
            with open("style.qss", "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except FileNotFoundError:
            print("Warning: style.qss not found. Using default styles.")


# Initialize App
if __name__ == '__main__':
    app = QApplication(sys.argv)
    counter = CountdownTimer()
    sys.exit(app.exec_())
