import os, ffmpeg
from PyQt5 import QtCore, QtGui, QtWidgets

AppVersion = "1.1.0"
AppEdition = "py38"

os.environ['path'] = "ffmpeg/"

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtWidgets.QStyleFactory, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(241, 211)
        MainWindow.setWindowIcon(QtGui.QIcon("img/icon.png"))
        MainWindow.setWindowFlags(MainWindow.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        MainWindow.setWindowFlags(MainWindow.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LabelInput = QtWidgets.QLabel(self.centralwidget)
        self.LabelInput.setGeometry(QtCore.QRect(10, 0, 111, 31))
        self.LabelInput.setObjectName("LabelInput")
        self.LineInput = QtWidgets.QLineEdit(self.centralwidget)
        self.LineInput.setGeometry(QtCore.QRect(10, 30, 181, 20))
        self.LineInput.setObjectName("LineInput")
        self.ButtonChooseInput = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonChooseInput.setGeometry(QtCore.QRect(200, 29, 32, 22))
        self.ButtonChooseInput.setObjectName("ButtonChooseInput")
        self.LabelCurrentSize = QtWidgets.QLabel(self.centralwidget)
        self.LabelCurrentSize.setGeometry(QtCore.QRect(10, 100, 201, 31))
        self.LabelCurrentSize.setObjectName("LabelCurrentSize")
        self.LabelNewSize = QtWidgets.QLabel(self.centralwidget)
        self.LabelNewSize.setGeometry(QtCore.QRect(55, 129, 151, 21))
        self.LabelNewSize.setObjectName("LabelNewSize")
        self.LineNewSize = QtWidgets.QLineEdit(self.centralwidget)
        self.LineNewSize.setGeometry(QtCore.QRect(10, 130, 41, 20))
        self.LineNewSize.setObjectName("LineNewSize")
        self.ButtonCompress = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonCompress.setGeometry(QtCore.QRect(9, 160, 223, 41))
        self.ButtonCompress.setObjectName("ButtonCompress")
        self.ButtonCompress.setIcon(QtGui.QIcon("img/compress.png"))
        self.ButtonCompress.setIconSize(QtCore.QSize(24, 24))
        self.LineOutput = QtWidgets.QLineEdit(self.centralwidget)
        self.LineOutput.setGeometry(QtCore.QRect(10, 80, 181, 20))
        self.LineOutput.setObjectName("LineOutput")
        self.LabelOutput = QtWidgets.QLabel(self.centralwidget)
        self.LabelOutput.setGeometry(QtCore.QRect(10, 50, 111, 31))
        self.LabelOutput.setObjectName("LabelOutput")
        self.ButtonChooseOutput = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonChooseOutput.setGeometry(QtCore.QRect(200, 79, 32, 22))
        self.ButtonChooseOutput.setObjectName("ButtonChooseOutput")
        self.ButtonLang = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonLang.setGeometry(QtCore.QRect(176, 4, 23, 23))
        self.ButtonLang.setText("")
        self.ButtonLang.setObjectName("ButtonLang")
        self.ButtonLang.hide()
        self.ButtonInfo = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonInfo.setGeometry(QtCore.QRect(209, 4, 23, 23))
        self.ButtonInfo.setText("")
        self.ButtonInfo.setIcon(QtGui.QIcon("img/info.png"))
        self.ButtonInfo.setObjectName("ButtonInfo")
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.ButtonChooseInput.clicked.connect(self.ChooseInputPath)
        self.ButtonChooseOutput.clicked.connect(self.ChooseOutputPath)
        self.ButtonCompress.clicked.connect(self.Compress)
        self.LineInput.textChanged.connect(self.SeeInputSize)
        self.ButtonInfo.clicked.connect(self.AboutWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SlavicClamp {}".format(AppVersion)))
        self.LabelInput.setText(_translate("MainWindow", "Input path:"))
        self.ButtonChooseInput.setText(_translate("MainWindow", "..."))
        self.LabelCurrentSize.setText(_translate("MainWindow", "(original file size will show up here)"))
        self.LabelNewSize.setText(_translate("MainWindow", " - new file size (in megabytes)"))
        self.ButtonCompress.setText(_translate("MainWindow", " Compress"))
        self.LabelOutput.setText(_translate("MainWindow", "Output path:"))
        self.ButtonChooseOutput.setText(_translate("MainWindow", "..."))
    
    def ChooseInputPath(self, MainWindow):
        InputPath = QtWidgets.QFileDialog.getOpenFileName(self, "Choose video file", os.getcwd(), "All Files (*)")
        if InputPath[0] == "":
            return
        else:
            self.LineInput.setText(InputPath[0])
    
    def ChooseOutputPath(self, MainWindow):
        ChooseOutputPathAppearAt = os.getcwd()
        if not os.path.isdir(self.RemoveAfterLastSlash(self, self.LineInput.text())):
            pass
        else:
            ChooseOutputPathAppearAt = self.RemoveAfterLastSlash(self, self.LineInput.text())
            
        ChooseOutputPathCurrentFormat = ""
        if not os.path.isfile(self.LineInput.text()):
            ChooseOutputPathChooseFormat = "MP4 file (*.mp4);;WMV file (*.wmv);;AVI file (*.avi);;Specify other format (*)".format()
        else:
            ChooseOutputPathChooseFormat = "Current file format (*.{});;MP4 file (*.mp4);;WMV file (*.wmv);;AVI file (*.avi);;Specify other format (*)".format(self.FindFormat(self, self.LineInput.text()))
        
        OutputPath = QtWidgets.QFileDialog.getSaveFileName(self, "Choose where to save, and what name & format/extension to use", ChooseOutputPathAppearAt, ChooseOutputPathChooseFormat)
        if OutputPath[0] == "":
            return
        else:
            self.LineOutput.setText(OutputPath[0])
    
    def SeeInputSize(self, MainWindow):
        if os.path.isfile(self.LineInput.text()):
            self.LabelCurrentSize.setText("{} MB - current file size".format(str(round(os.stat(self.LineInput.text()).st_size / 1048576, 2))))
        else:
            self.LabelCurrentSize.setText("(original file size will show up here)")
    
    def EnableButtons(self, MainWindow, Boolean):
        if (Boolean == True) or (Boolean == False):
            self.LineInput.setEnabled(Boolean)
            self.LineOutput.setEnabled(Boolean)
            self.LineNewSize.setEnabled(Boolean)
            self.ButtonChooseInput.setEnabled(Boolean)
            self.ButtonChooseOutput.setEnabled(Boolean)
            self.ButtonCompress.setEnabled(Boolean)
        else:
            print("Incorrect argument for EnableButtons used: \"{}\"".format(Boolean))
    
    def RemoveAfterLastSlash(self, MainWindow, String):
        if String.rfind('/') != -1:
            return String[:String.rfind('/')]
        else:
            return String
    
    def FindFormat(self, MainWindow, FilePath):
        Parts = FilePath.rsplit('.', 1)
        if len(Parts) > 1:
            return Parts[-1]
        else:
            return ''

    
    def AboutWindow(self, MainWindow):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("About")
        msgbox.setText("SlavicClamp\nVersion: {}\nEdition: {}\nWritten by vazhka-dolya on GitHub\nLicensed under the Do What The Fuck You Want To Public License\n\nCredits:\n- Some person on Stack Overflow — code for actually compressing the video\n- FFmpeg — used for compression\n- SMO14O7 — name for the program".format(AppVersion, AppEdition))
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgbox.setIconPixmap(QtGui.QPixmap("img/icon.png"))
        msgbox.setWindowIcon(QtGui.QIcon("img/info.png"))
        runmsgbox = msgbox.exec_()
    
    def Compress(self, MainWindow):
        self.EnableButtons(self, False)
        ErrorText = ""
        Errors = 0
        #print(self.LineInput.text())
        #print(self.LineOutput.text())
        #print(self.LineNewSize.text())
        if not os.path.isfile(self.LineInput.text()):
            ErrorText += ("LineInput is not a file\n")
            Errors += 1
        if not os.path.isdir(self.RemoveAfterLastSlash(self, self.LineInput.text())):
            ErrorText += ("LineOutput is not a directory\n")
            Errors += 1
        try:
            if (float(self.LineNewSize.text()) > 10240):
                ErrorText += ("LineNewSize is bigger that 10240\n")
                Errors += 1
        except:
            ErrorText += ("Error with LineNewSize\n")
            Errors += 1
        if Errors > 0:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setWindowTitle("Error!")
            msgbox.setText(ErrorText)
            msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgbox.setIcon(QtWidgets.QMessageBox.Critical)
            msgbox.setWindowIcon(QtGui.QIcon("img/icon.png"))
            runmsgbox = msgbox.exec_()
            self.LineInput.setText("")
            self.LineOutput.setText("")
            self.LineNewSize.setText("")
            self.EnableButtons(self, True)
            return
        self.compress_video(self, self.LineInput.text(), self.LineOutput.text(), float(self.LineNewSize.text()) * 1000)
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Finished")
        msgbox.setText("The video has been successfully compressed.\nPath to video: {}".format(self.LineOutput.text()))
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgbox.setIcon(QtWidgets.QMessageBox.Information)
        msgbox.setWindowIcon(QtGui.QIcon("img/icon.png"))
        runmsgbox = msgbox.exec_()
        self.EnableButtons(self, True)

    # function below written by some person on stack overflow
    def compress_video(self, MainWindow, video_full_path, output_file_name, target_size):
        # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
        min_audio_bitrate = 32000
        max_audio_bitrate = 256000

        probe = ffmpeg.probe(video_full_path)
        # Video duration, in s.
        duration = float(probe['format']['duration'])
        # Audio bitrate, in bps.
        audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
        # Target total bitrate, in bps.
        target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

        # Target audio bitrate, in bps
        if 10 * audio_bitrate > target_total_bitrate:
            audio_bitrate = target_total_bitrate / 10
            if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                audio_bitrate = min_audio_bitrate
            elif audio_bitrate > max_audio_bitrate:
                audio_bitrate = max_audio_bitrate
        # Target video bitrate, in bps.
        video_bitrate = target_total_bitrate - audio_bitrate

        i = ffmpeg.input(video_full_path)
        ffmpeg.output(i, os.devnull,
                    **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                    ).overwrite_output().run()
        ffmpeg.output(i, output_file_name,
                    **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                    ).overwrite_output().run()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
