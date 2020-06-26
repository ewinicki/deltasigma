from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QCheckBox, QComboBox, QGridLayout
from enum import Enum


FREQ = 1000
AMP = 1
WAVE = ('Sine', 'Square', 'Triangle', 'Sawtooth')
RES = 1024
DC = 0
FS = 2 * FREQ
OVER = 2 ** 6
VREF = 2.5
PER = 50
CLOCK = 1000
ORDER = ('First', 'Second')

class MainGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # input signal
        self.values = {
                'f': (QLabel('Input Frequency (Hz)'), QLineEdit(), str(FREQ)),
                'amp': (QLabel('Input Amplitude (V)'), QLineEdit(), str(AMP)),
                'wave': (QLabel('Input Waveform'), QComboBox(), WAVE),
                'samp': (QLabel('Input Samples'), QLineEdit(), str(RES)),
                'dc': (QLabel('DC Offset'), QLineEdit(), str(DC)),
                'noise': (QLabel('Noisy Input'), QCheckBox(), True),
                'fs': (QLabel('Sampling Frequency (Hz)'), QLineEdit(), str(FS)),
                'over': (QLabel('Oversampling Rate'), QLineEdit(), str(OVER)),
                'vref': (QLabel('Vref (V)'), QLineEdit(), str(VREF)),
                'per': (QLabel('Periods'), QLineEdit(), str(PER)),
                'order': (QLabel('Order'), QComboBox(), ORDER)
                }

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.set_values()

        self.setLayout(self.grid)

    def set_values(self, reset=False):
        for row, (name, data) in enumerate(self.values.items()):
            self.grid.addWidget(data[0], row, 0)
            self.grid.addWidget(data[1], row, 1)

            if isinstance(data[1], QLineEdit):
                data[1].setText(data[2])
            elif isinstance(data[1], QCheckBox):
                data[1].setChecked(data[2])
            elif isinstance(data[1], QComboBox):
                if reset is True:
                    data[1].setCurrentIndex(0)
                else:
                    for option in data[2]:
                        data[1].addItem(option)

    def reset(self):
        self.set_values(reset=True)

    @property
    def frequency(self):
        return int(self.values['f'][1].text())

    @property
    def amplitude(self):
        return int(self.values['amp'][1].text())

    @property
    def waveform(self):
        return self.values['wave'][1].currentText()

    @property
    def samples(self):
        return int(self.values['samp'][1].text())

    @property
    def dc(self):
        return float(self.values['dc'][1].text())

    @property
    def noise(self):
        return self.values['noise'][1].isChecked()

    @property
    def sampling_frequency(self):
        return int(self.values['fs'][1].text())

    @property
    def oversampling_rate(self):
        return int(self.values['over'][1].text())

    @property
    def vref(self):
        return float(self.values['vref'][1].text())

    @property
    def periods(self):
        return int(self.values['per'][1].text())

    @property
    def order(self):
        return self.values['order'][1].currentText()
