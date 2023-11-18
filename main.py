import keyboard
import time
import random
import threading


class StringDisplayTimer:
    def __init__(self):
        self.stringSet = ["SS1", "SS2"]
        self.root = ["R/1", "R/2", "R/3", "R/4", "R/5"]
        self.lastTwoOutputs = []
        self.maxTimeLimit = 30  # seconds
        self.userInputWaitTime = 60  # seconds
        self.running = True
        self.waiting_for_key = True

    def randomElement(self, elements):
        return random.choice(elements)

    def generateString(self):
        string = (
            self.randomElement(self.stringSet) + " " + self.randomElement(self.root)
        )
        while string in self.lastTwoOutputs:
            string = (
                self.randomElement(self.stringSet) + " " + self.randomElement(self.root)
            )
        if len(self.lastTwoOutputs) >= 2:
            self.lastTwoOutputs.pop(0)
        self.lastTwoOutputs.append(string)
        return string

    def display(self, message):
        print(message)

    def startTimerAndListen(self):
        while self.running:
            self.display(self.generateString())
            self.start_time = time.time()
            self.waiting_for_key = True

            while (
                self.waiting_for_key
                and time.time() - self.start_time < self.maxTimeLimit
            ):
                time.sleep(0.1)

            if not self.waiting_for_key:  # Spacebar pressed
                elapsed_time = time.time() - self.start_time
                self.display(f"Elapsed time: {elapsed_time} seconds")

            elif self.waiting_for_key:  # Max time limit reached
                elapsed_time = time.time() - self.start_time
                self.display(
                    f"Max time limit of {self.maxTimeLimit} seconds elapsed. Elapsed time: {elapsed_time} seconds"
                )

            self.promptForContinue()

    def promptForContinue(self):
        self.display("Would you like to go again? (space to continue, escape to exit)")
        start_time = time.time()
        self.waiting_for_key = True

        while (
            self.waiting_for_key and time.time() - start_time < self.userInputWaitTime
        ):
            time.sleep(0.1)

        if self.waiting_for_key:  # No response received
            self.display("No input received...terminating program.")
            self.running = False

    def listenForKey(self):
        while self.running:
            if keyboard.is_pressed("space"):
                self.waiting_for_key = False
                time.sleep(0.2)  # Prevent multiple detections
            elif keyboard.is_pressed("esc"):
                self.running = False
                self.waiting_for_key = False
                self.display("Terminating program...")
                time.sleep(0.2)  # Prevent multiple detections
            time.sleep(0.1)

    def run(self):
        self.display("Starting program...")
        key_listener_thread = threading.Thread(target=self.listenForKey)
        key_listener_thread.start()
        self.startTimerAndListen()


# Initialize and run the program
program = StringDisplayTimer()
program.run()
