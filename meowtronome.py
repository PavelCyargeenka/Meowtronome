from pathlib import Path
from time import sleep
from os import path, environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

ROOT = Path(__file__).resolve().parent


class Meowtronome:
    """
    Simple metronome that supports various time signatures and a wide BPM range.
    Supports 2 sound configurations: normal and funny (dog/cat sounds)
    """

    def __init__(self):
        """
        Initializes the Meowtronome instance
        - Sets the file paths for the audio files.
        - Prompts the user to select a time signature.
        - Prompts the user to enter the BPM (metronome speed).
        - Calculates the beat length based on the BPM.
        - Prompts the user to choose the sound configuration.
        - Initializes the pygame mixer.
        - Calls the manage() method to start the metronome loop.
        - Stops the session with a message when the user quits Meowtronome.
        """
        self.downbeat = path.join(ROOT, 'audio/db.wav')
        self.upbeat = path.join(ROOT, 'audio/ub.wav')
        self.downdog = path.join(ROOT, 'audio/dog.wav')
        self.upcat = path.join(ROOT, 'audio/upcat.mp3')
        self.available_time_signatures = [
            '1/4', '2/4', '3/4', '4/4', '5/4', '6/4', '3/8', '5/8', '6/8', '9/8'
        ]

        try:
            self.show_time_signatures()
            self.time_signature = self.get_time_signature()
            self.bmp = self.get_bpm()
            self.beat_length = 60 / self.bmp
            self.sound_config = self.sound_config()
            mixer.init()
            self.manage()

        except KeyboardInterrupt:
            mixer.quit()
            print('\nThanks for choosing the Meowtronome!')
            return

    def show_time_signatures(self):
        """
        Shows the available time signatures to the user.
        """
        print(f"Available time signatures: {', '.join(self.available_time_signatures)}")

    def get_time_signature(self):
        """
        Prompts the user to select a valid time signature.
        Returns str: The selected time signature.
        Raises ValueError: If there are too many invalid inputs.
        """
        for i in range(3):
            ts = input('Please select a time signature: ')
            if ts in self.available_time_signatures:
                return ts
            print('Invalid input')
        raise ValueError('Too many invalid inputs, the session is over.')

    def get_bpm(self):
        """
        Prompts the user to enter a valid BPM (metronome speed).
        Returns int: The selected BPM.
        Raises ValueError: If there are too many invalid inputs.
        """
        for attempt in range(3):
            try:
                if self.time_signature in self.available_time_signatures[:6]:
                    bpm = int(input('Enter the BPM (30-300): '))
                else:
                    bpm = int(input('Enter a dotted crotchet BPM (30-300): '))
                if 30 <= bpm <= 300:
                    return bpm
                if attempt < 2:
                    print('Please enter a value between 30 and 300.')
            except ValueError:
                if attempt < 2:
                    print('Invalid input. Please enter an integer.')
        raise ValueError('Too many invalid inputs, the session is over.')

    @staticmethod
    def sound_config():
        """
        Prompts the user to choose one of two sound configurations: normal or funny (animal sounds).
        Returns str: The selected sound configuration.
        The default sound configuration is activated after 3 invalid inputs.
        """
        ans = '2'
        for _ in range(3):
            ans = input('For dogs and cats sounds configuration press 1, for normal press 2: ')
            if ans in ['1', '2']:
                return ans
            if _ < 2:
                print('Enter 1 or 2')
            else:
                print('Default sound configuration is activated')
        return ans

    def manage(self):
        """
        Manages the metronome loop.
        - Checks the chosen sound configuration.
        - Loads the necessary sounds into pygame mixer.
        - Runs the metronome loop
        """
        beat_type = 'crotchet' if self.time_signature[2] == '4' else 'quaver'
        print(f'Here we go! Remember, one bit = one {beat_type}.')
        sleep(self.beat_length)
        while True:
            for i in range(int(self.time_signature[0])):
                if i == 0:
                    mixer.music.load(self.downbeat) if self.sound_config == '2' else mixer.music.load(self.downdog)
                else:
                    mixer.music.load(self.upbeat) if self.sound_config == '2' else mixer.music.load(self.upcat)
                mixer.music.play()
                sleep(self.beat_length)


session = Meowtronome()
