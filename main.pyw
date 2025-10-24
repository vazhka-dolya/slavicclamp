import os, ffmpeg, sys
from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser
from datetime import datetime
import json
import configparser
import subprocess

AppVersion = "1.4.0"
AppEdition = "py38"

ConfigPath = "settings.json"
global ConfigData
ConfigData = {
    "language": "english",
    "default_size": 0,
	"path_mode": 0,
	"path_last_used": "",
	"path_custom": ""
}
global ResetConfigData
ResetConfigData = ConfigData.copy()

def UpdateTranslation():
    global CurrentTranslation
    if ConfigData["language"] == "english":
        CurrentTranslation = Translation_English
    elif ConfigData["language"] == "latvian":
        CurrentTranslation = Translation_Latvian
    elif ConfigData["language"] == "russian":
        CurrentTranslation = Translation_Russian
    elif ConfigData["language"] == "ukrainian":
        CurrentTranslation = Translation_Ukrainian
    else:
        CurrentTranslation = Translation_English

Translation_English = {
    "MainWindow_LabelInput": "Choose a video:",
    "MainWindow_LabelNewSize": " – new file size (in megabytes).",
    "MainWindow_ButtonCompress": " Compress",
    "MainWindow_LabelOutput": "Where to save the result:",
    "MainWindow_CurrentFileSizeEmpty": "<current file size>",
    "MainWindow_CurrentFileSize": " MB – current file size.",
    "AboutWindow_Title": "About",
    "AboutWindow_Text": f"SlavicClamp\nVersion: {AppVersion}\nEdition: {AppEdition}\nWritten by vazhka-dolya on GitHub\nLicensed under the Do What The Fuck You Want To Public License\n\nCredits:\n• Some person on Stack Overflow – code for actually compressing the video.\n• FFmpeg – used for compression.\n• @SMO14O7 – name for the program.",
    "InputDialog_Title": "Select a video file",
    "InputDialog_Format": "All files (*)",
    "OutputDialog_Text": "MP4 file (*.mp4);;WMV file (*.wmv);;AVI file (*.avi);;Specify other format (*)",
    "OutputDialog_TextWithInput1": "Current file format (*.",
    "OutputDialog_TextWithInput2": ");;MP4 file (*.mp4);;WMV file (*.wmv);;AVI file (*.avi);;Specify other format (*)",
    "OutputDialog_Title": "Choose where to save, and what name & format/extension to use",
    "Error_Title": "Error!",
    "Error_Text": "The following errors occured while trying to compress:\n",
    "Error_LineInputIsNotAFile": "Selected input path is not a file.\n",
    "Error_LineOutputIsNotADirectory": "Selected output path does not contain the specified directory.\n",
    "ExportDialog_Title": "Finished",
    "ExportDialog_Text1": "The video has successfully been compressed and exported to:\n\n“",
    "ExportDialog_Text2": "”\n\nWould you like to see it in the file manager?",
    "SettingsWindow_Title": "Settings",
    "SettingsWindow_GroupDefaultSize": "Size",
    "SettingsWindow_LabelDefaultSize": "Default size:",
    "SettingsWindow_GroupDefaultPath": "Default path",
    "SettingsWindow_LabelDefaultPath": "Default path to open:",
    "SettingsWindow_RadioPathLastUsed": "Last used path",
    "SettingsWindow_RadioPathRoot": "SlavicClamp's root folder",
    "SettingsWindow_GroupLanguage": "Language",
    "SettingsWindow_actionSaveAndClose": "Save && Close",
    "SettingsWindow_actionClose": "Close"
}

Translation_Latvian = {
    "MainWindow_LabelInput": "Izvēlieties video:",
    "MainWindow_LabelNewSize": " – jauns izmērs (MB).",
    "MainWindow_ButtonCompress": " Saspiediet",
    "MainWindow_LabelOutput": "Kur saglabāt rezultātu:",
    "MainWindow_CurrentFileSizeEmpty": "<pašreizējais izmērs>",
    "MainWindow_CurrentFileSize": " MB – pašreizējais izmērs.",
    "AboutWindow_Title": "Par programmu",
    "AboutWindow_Text": f"SlavicClamp\nVersija: {AppVersion}\nRedakcija: {AppEdition}\nNo vazhka-dolya GitHub\nLicencēts saskaņā ar Do What The Fuck You Want To Public License\n\nPateicība:\n• kāds no StackOverflow — pats video saspiešanas kods;\n• FFmpeg — izmantots saspiešanai;\n• @SMO14O7 — izdomāja programmas nosaukumu.",
    "InputDialog_Title": "Izvēlieties videofailu",
    "InputDialog_Format": "Visi faili (*)",
    "OutputDialog_Text": "MP4 fails (*.mp4);;WMV fails (*.wmv);;AVI fails (*.avi);;Norādīt citu formātu (*)",
    "OutputDialog_TextWithInput1": "Pašreizējais formāts (*.",
    "OutputDialog_TextWithInput2": ");;MP4 fails (*.mp4);;WMV fails (*.wmv);;AVI fails (*.avi);; Norādīt citu formātu (*)",
    "OutputDialog_Title": "Izvēlieties, kur saglabāt, kā arī kādu nosaukumu un formātu/paplašinājumu izmantot",
    "Error_Title": "Kļūda!",
    "Error_Text": "Mēģinot saspiest, radās šādas kļūdas:\n",
    "Error_LineInputIsNotAFile": "Izvēlētais sākotnējā faila ceļš neved uz failu.\n",
    "Error_LineOutputIsNotADirectory": "Izvēlētajā ceļā nav direktorija, kur saglabāt rezultātu.\n",
    "ExportDialog_Title": "Pabeigts",
    "ExportDialog_Text1": "Video ir veiksmīgi saspiests un eksportēts uz:\n\n“",
    "ExportDialog_Text2": "”\n\nVai vēlaties to atvērt failu pārvaldniekā?",
    "SettingsWindow_Title": "Iestatījumi",
    "SettingsWindow_GroupDefaultSize": "Izmērs",
    "SettingsWindow_LabelDefaultSize": "Noklusējuma izmērs:",
    "SettingsWindow_GroupDefaultPath": "Noklusējuma ceļš",
    "SettingsWindow_LabelDefaultPath": "Noklusējumā izmantot:",
    "SettingsWindow_RadioPathLastUsed": "pēdējais izmantotais ceļš",
    "SettingsWindow_RadioPathRoot": "SlavicClamp sakņu mape",
    "SettingsWindow_GroupLanguage": "Valoda",
    "SettingsWindow_actionSaveAndClose": "Saglabāt un aizvērt",
    "SettingsWindow_actionClose": "Aizvērt"
}

Translation_Russian = {
    "MainWindow_LabelInput": "Выберите видео:",
    "MainWindow_LabelNewSize": " – новый размер (в МБ).",
    "MainWindow_ButtonCompress": " Сжать",
    "MainWindow_LabelOutput": "Куда сохранить результат:",
    "MainWindow_CurrentFileSizeEmpty": "<текущий размер>",
    "MainWindow_CurrentFileSize": " МБ – текущий размер.",
    "AboutWindow_Title": "О программе",
    "AboutWindow_Text": f"SlavicClamp\nВерсия: {AppVersion}\nРедакция: {AppEdition}\nОт vazhka-dolya на GitHub\nЛицензировано под Do What The Fuck You Want To Public License\n\nБлагодарность:\n• кто-то на StackOverflow — сам код для сжатия видео;\n• FFmpeg — используется для сжатия;\n• @SMO14O7 — придумал имя программы.",
    "InputDialog_Title": "Выберите видеофайл",
    "InputDialog_Format": "Все файлы (*)",
    "OutputDialog_Text": "MP4-файл (*.mp4);;WMV-файл (*.wmv);;AVI-файл (*.avi);;Указать другой формат (*)",
    "OutputDialog_TextWithInput1": "Текущий формат (*.",
    "OutputDialog_TextWithInput2": ");;MP4-файл (*.mp4);;WMV-файл (*.wmv);;AVI-файл (*.avi);;Указать другой формат (*)",
    "OutputDialog_Title": "Выберите, куда сохранить, а также какое имя и формат/расширение использовать",
    "Error_Title": "Ошибка!",
    "Error_Text": "Произошли следующие ошибки во время попытки сжать:\n",
    "Error_LineInputIsNotAFile": "Выбранный путь для исходного файла не ведёт на файл.\n",
    "Error_LineOutputIsNotADirectory": "Не существует директории в выбранном пути для сохранения результата.\n",
    "ExportDialog_Title": "Закончено",
    "ExportDialog_Text1": "Видео было успешно сжато и экспортировано в:\n\n«",
    "ExportDialog_Text2": "»\n\nХотите открыть его в файловом менеджере?",
    "SettingsWindow_Title": "Настройки",
    "SettingsWindow_GroupDefaultSize": "Размер",
    "SettingsWindow_LabelDefaultSize": "Размер по умолчанию:",
    "SettingsWindow_GroupDefaultPath": "Путь по умолчанию",
    "SettingsWindow_LabelDefaultPath": "По умолчанию использовать:",
    "SettingsWindow_RadioPathLastUsed": "последний использованный путь",
    "SettingsWindow_RadioPathRoot": "корневую папку SlavicClamp",
    "SettingsWindow_GroupLanguage": "Язык",
    "SettingsWindow_actionSaveAndClose": "Сохранить и закрыть",
    "SettingsWindow_actionClose": "Закрыть"
}

Translation_Ukrainian = {
    "MainWindow_LabelInput": "Виберіть відео:",
    "MainWindow_LabelNewSize": " – новий розмір (в МБ).",
    "MainWindow_ButtonCompress": " Стиснути",
    "MainWindow_LabelOutput": "Куди зберегти результат:",
    "MainWindow_CurrentFileSizeEmpty": "<поточний розмір>",
    "MainWindow_CurrentFileSize": " МБ – поточний розмір.",
    "AboutWindow_Title": "Про програму",
    "AboutWindow_Text": f"SlavicClamp\nВерсія: {AppVersion}\nРедакція: {AppEdition}\nВід vazhka-dolya на GitHub\nЛіцензовано під Do What The Fuck You Want To Public License\n\nПодяка:\n• хтось на StackOverflow — сам код для стиснення відео;\n• FFmpeg — використовується для стиснення;\n• @SMO14O7 — придумав назву програми.",
    "InputDialog_Title": "Виберіть відеофайл",
    "InputDialog_Format": "Усі файли (*)",
    "OutputDialog_Text": "MP4-файл (*.mp4);;WMV-файл (*.wmv);;AVI-файл (*.avi);;Вказати інший формат (*)",
    "OutputDialog_TextWithInput1": "Поточний формат (*.",
    "OutputDialog_TextWithInput2": ");;MP4-файл (*.mp4);;WMV-файл (*.wmv);;AVI-файл (*.avi);;Вказати інший формат (*)",
    "OutputDialog_Title": "Виберіть, куди зберегти, а також яке ім'я та формат/розширення використовувати",
    "Error_Title": "Помилка!",
    "Error_Text": "Під час спроби стиснути сталися такі помилки:\n",
    "Error_LineInputIsNotAFile": "Вибраний шлях для вихідного файлу не веде до файлу.\n",
    "Error_LineOutputIsNotADirectory": "Не існує каталогу в обраному шляху для збереження результату.\n",
    "ExportDialog_Title": "Закінчено",
    "ExportDialog_Text1": "Відео було успішно стиснуто та експортовано в:\n\n«",
    "ExportDialog_Text2": "»\n\nБажаєте відкрити його в файловому менеджері?",
    "SettingsWindow_Title": "Налаштування",
    "SettingsWindow_GroupDefaultSize": "Розмір",
    "SettingsWindow_LabelDefaultSize": "Розмір за замовчуванням:",
    "SettingsWindow_GroupDefaultPath": "Шлях за замовчуванням",
    "SettingsWindow_LabelDefaultPath": "За замовчуванням використовувати:",
    "SettingsWindow_RadioPathLastUsed": "останній використаний шлях",
    "SettingsWindow_RadioPathRoot": "кореневу папку SlavicClamp",
    "SettingsWindow_GroupLanguage": "Мова",
    "SettingsWindow_actionSaveAndClose": "Зберегти і закрити",
    "SettingsWindow_actionClose": "Закрити"
}

global CurrentTranslation
CurrentTranslation = Translation_English

os.environ['path'] = "ffmpeg/"

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtWidgets.QStyleFactory, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

os.environ["QT_ENABLE_HIGHDPI_SCALING"]   = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"]             = "1"

class Ui_MainWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        sys.exit(0)
            
    def OpenSettingsWindow(self):
        self.SettingsWindow = QtWidgets.QMainWindow()
        self.SettingsWindowUi = Ui_SettingsWindow()
        self.SettingsWindowUi.setupUi(self.SettingsWindow)
        self.SettingsWindow.show()
        
    def setupUi(self, MainWindow):
        fontsmaller = QtGui.QFont()
        fontsmaller.setPointSize(8)

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(241, 211)
        MainWindow.setWindowIcon(QtGui.QIcon("img/icon.png"))
        MainWindow.setWindowFlags(MainWindow.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        MainWindow.setWindowFlags(MainWindow.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        MainWindow.setFont(fontsmaller)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LabelInput = QtWidgets.QLabel(self.centralwidget)
        self.LabelInput.setGeometry(QtCore.QRect(10, 0, 111, 31))
        self.LabelInput.setObjectName("LabelInput")
        self.LineInput = QtWidgets.QLineEdit(self.centralwidget)
        self.LineInput.setGeometry(QtCore.QRect(10, 30, 187, 20))
        self.LineInput.setObjectName("LineInput")
        self.ButtonChooseInput = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonChooseInput.setGeometry(QtCore.QRect(200, 29, 32, 22))
        self.ButtonChooseInput.setObjectName("ButtonChooseInput")
        self.LabelCurrentSize = QtWidgets.QLabel(self.centralwidget)
        self.LabelCurrentSize.setGeometry(QtCore.QRect(10, 100, 201, 31))
        self.LabelCurrentSize.setObjectName("LabelCurrentSize")
        self.LabelNewSize = QtWidgets.QLabel(self.centralwidget)
        self.LabelNewSize.setGeometry(QtCore.QRect(75, 129, 151, 21))
        self.LabelNewSize.setObjectName("LabelNewSize")
        self.DoubleSpinNewSize = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.DoubleSpinNewSize.setGeometry(QtCore.QRect(10, 130, 64, 20))
        #self.DoubleSpinNewSize.setAlignment(QtCore.Qt.AlignCenter)
        self.DoubleSpinNewSize.setObjectName("DoubleSpinNewSize")
        self.DoubleSpinNewSize.setMaximum(9999.989999999999782)
        self.ButtonCompress = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonCompress.setGeometry(QtCore.QRect(9, 160, 223, 41))
        self.ButtonCompress.setObjectName("ButtonCompress")
        self.ButtonCompress.setIcon(QtGui.QIcon("img/compress.png"))
        self.ButtonCompress.setIconSize(QtCore.QSize(24, 24))
        self.LineOutput = QtWidgets.QLineEdit(self.centralwidget)
        self.LineOutput.setGeometry(QtCore.QRect(10, 80, 187, 20))
        self.LineOutput.setObjectName("LineOutput")
        self.LabelOutput = QtWidgets.QLabel(self.centralwidget)
        self.LabelOutput.setGeometry(QtCore.QRect(10, 50, 171, 31))
        self.LabelOutput.setObjectName("LabelOutput")
        self.ButtonChooseOutput = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonChooseOutput.setGeometry(QtCore.QRect(200, 79, 32, 22))
        self.ButtonChooseOutput.setObjectName("ButtonChooseOutput")
        self.ButtonLang = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonLang.setGeometry(QtCore.QRect(176, 4, 23, 23))
        self.ButtonLang.setText("")
        self.ButtonLang.setObjectName("ButtonLang")
        self.ButtonLang.hide()
        self.ButtonSettings = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonSettings.setGeometry(QtCore.QRect(209, 4, 23, 23))
        self.ButtonSettings.setText("")
        self.ButtonSettings.setIcon(QtGui.QIcon("img/settings.png"))
        self.ButtonSettings.setObjectName("ButtonSettings")
        self.ButtonInfo = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonInfo.setGeometry(QtCore.QRect(184, 4, 23, 23))
        self.ButtonInfo.setText("")
        self.ButtonInfo.setIcon(QtGui.QIcon("img/info.png"))
        self.ButtonInfo.setObjectName("ButtonInfo")
        self.ButtonGitHub = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonGitHub.setGeometry(QtCore.QRect(159, 4, 23, 23))
        self.ButtonGitHub.setText("")
        self.ButtonGitHub.setIcon(QtGui.QIcon("img/github.png"))
        self.ButtonGitHub.setObjectName("ButtonGitHub")
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.ButtonChooseInput.clicked.connect(self.ChooseInputPath)
        self.ButtonChooseOutput.clicked.connect(self.ChooseOutputPath)
        self.ButtonCompress.clicked.connect(self.BeforeCompress)
        self.LineInput.textChanged.connect(self.SeeInputSize)
        self.ButtonSettings.clicked.connect(self.OpenSettingsWindow)
        self.ButtonInfo.clicked.connect(self.AboutWindow)
        self.ButtonGitHub.clicked.connect(self.OpenGitHubPage)
        
        self.LoadSettings(self)
        self.DoubleSpinNewSize.setValue(ConfigData["default_size"])
        UpdateTranslation()
        self.retranslateUi()
            
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self):
        global CurrentTranslation
        MainWindow.setWindowTitle(f"SlavicClamp {AppVersion}")
        self.LabelInput.setText(CurrentTranslation["MainWindow_LabelInput"])
        self.ButtonChooseInput.setText("...")
        self.LabelCurrentSize.setText(CurrentTranslation["MainWindow_CurrentFileSizeEmpty"])
        self.LabelNewSize.setText(CurrentTranslation["MainWindow_LabelNewSize"])
        self.ButtonCompress.setText(CurrentTranslation["MainWindow_ButtonCompress"])
        self.LabelOutput.setText(CurrentTranslation["MainWindow_LabelOutput"])
        self.ButtonChooseOutput.setText("...")
    
    def LoadSettings(self, MainWindow):
        global ConfigData, ResetConfigData
        try:
            if os.path.isfile(ConfigPath):
                with open(ConfigPath, "r") as f:
                    ConfigData = json.load(f)
            else:
                self.SaveSettings(self, True)
        except:
            self.SaveSettings(self, True)
            if os.path.isfile(ConfigPath):
                with open(ConfigPath, "r") as f:
                    ConfigData = json.load(f)
    
    def SaveSettings(self, MainWindow, ResetSettings=False):
        global ConfigData, ResetConfigData
        with open(ConfigPath, "w") as f:
            if not ResetSettings:
                json.dump(ConfigData, f, indent = "\t")
            else:
                json.dump(ResetConfigData, f, indent = "\t")
            
    def ChooseInputPath(self, MainWindow):
        global CurrentTranslation
        InputPath = QtWidgets.QFileDialog.getOpenFileName(self, CurrentTranslation["InputDialog_Title"], os.getcwd(), CurrentTranslation["InputDialog_Format"])
        if InputPath[0] == "":
            return
        else:
            self.LineInput.setText(InputPath[0])
    
    def ChooseOutputPath(self, MainWindow):
        global ConfigData, ResetConfigData
        global CurrentTranslation
            
        ChooseOutputPathAppearAt = os.getcwd()
        if not os.path.isdir(self.RemoveAfterLastSlash(self, self.LineInput.text())):
            pass
        else:
            #ChooseOutputPathAppearAt = 
            ChooseOutputPathAppearAt = self.SplitFormat(self, self.LineInput.text())[0] + datetime.today().strftime('_c_%Y-%m-%d_%H-%M')
            
        ChooseOutputPathCurrentFormat = ""
            
        if not os.path.isfile(self.LineInput.text()):
            ChooseOutputPathChooseFormat = CurrentTranslation["OutputDialog_Text"]
        else:
            ChooseOutputPathChooseFormat = f"{CurrentTranslation['OutputDialog_TextWithInput1']}{self.SplitFormat(self, self.LineInput.text())[1]}{CurrentTranslation['OutputDialog_TextWithInput2']}"
        
        OutputPath = QtWidgets.QFileDialog.getSaveFileName(self, CurrentTranslation["OutputDialog_Title"], ChooseOutputPathAppearAt, ChooseOutputPathChooseFormat)
        if OutputPath[0] == "":
            return
        else:
            self.LineOutput.setText(OutputPath[0])
    
    def SeeInputSize(self, MainWindow):
        global CurrentTranslation
        try:
            size = str(round(os.stat(self.LineInput.text()).st_size / 1048576, 2))
            
            if os.path.isfile(self.LineInput.text()):
                self.LabelCurrentSize.setText(f"{size}{CurrentTranslation['MainWindow_CurrentFileSize']}")
            else:
                self.LabelCurrentSize.setText(CurrentTranslation["MainWindow_CurrentFileSizeEmpty"])
        except:
            self.LabelCurrentSize.setText(CurrentTranslation["MainWindow_CurrentFileSizeEmpty"])
    
    def EnableButtons(self, MainWindow, Boolean):
        self.LineInput.setEnabled(Boolean)
        self.LineOutput.setEnabled(Boolean)
        self.DoubleSpinNewSize.setEnabled(Boolean)
        self.ButtonChooseInput.setEnabled(Boolean)
        self.ButtonChooseOutput.setEnabled(Boolean)
        self.ButtonCompress.setEnabled(Boolean)
        self.ButtonInfo.setEnabled(Boolean)
        self.ButtonGitHub.setEnabled(Boolean)
        self.ButtonSettings.setEnabled(Boolean)
    
    def RemoveAfterLastSlash(self, MainWindow, String):
        if String.rfind('/') != -1:
            return String[:String.rfind('/')]
        else:
            return String
    
    def SplitFormat(self, MainWindow, FilePath):
        Parts = FilePath.rsplit('.', 1)
        if len(Parts) > 1:
            return Parts[0], Parts[-1]
        else:
            return ''

    
    def AboutWindow(self, MainWindow):
        global CurrentTranslation
        msgboxabo = QtWidgets.QMessageBox()
        msgboxabo.setWindowTitle(CurrentTranslation["AboutWindow_Title"])
        msgboxabo.setText(CurrentTranslation["AboutWindow_Text"])
        msgboxabo.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgboxabo.setIconPixmap(QtGui.QPixmap("img/icon.png"))
        msgboxabo.setWindowIcon(QtGui.QIcon("img/info.png"))
        runmsgboxabo = msgboxabo.exec_()
    
    def OpenGitHubPage(self, MainWindow):
        webbrowser.open("https://github.com/vazhka-dolya/slavicclamp")
    
    def BeforeCompress(self, MainWindow):
        self.EnableButtons(self, False)
        self.Compress(self)
    
    def Compress(self, MainWindow):
        global CurrentTranslation
        ErrorText = CurrentTranslation["Error_Text"]
        Errors = 0
        
        if not os.path.isfile(self.LineInput.text()):
            Errors += 1
            ErrorText += f"{Errors}. {(CurrentTranslation['Error_LineInputIsNotAFile'])}"
        if not os.path.isdir(self.RemoveAfterLastSlash(self, self.LineInput.text())):
            Errors += 1
            ErrorText += f"{Errors}. {(CurrentTranslation['Error_LineOutputIsNotADirectory'])}"
        if Errors > 0:
            msgboxerr = QtWidgets.QMessageBox()
            msgboxerr.setWindowTitle(CurrentTranslation["Error_Title"])
            msgboxerr.setText(ErrorText)
            msgboxerr.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgboxerr.setIcon(QtWidgets.QMessageBox.Critical)
            msgboxerr.setWindowIcon(QtGui.QIcon("img/icon.png"))
            runmsgboxerr = msgboxerr.exec_()
            self.LineInput.setText("")
            self.LineOutput.setText("")
            self.DoubleSpinNewSize.setValue(0)
            self.EnableButtons(self, True)
            return
        
        # We should be multiplying by a 1000, but the result video sometimes goes over the selected size, so we're gonna do 950 instead
        self.compress_video(self, self.LineInput.text(), self.LineOutput.text(), float(self.DoubleSpinNewSize.value()) * 950)
        global msgbox
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle(CurrentTranslation["ExportDialog_Title"])
        msgbox.setText(f"{CurrentTranslation['ExportDialog_Text1']}{self.LineOutput.text()}{CurrentTranslation['ExportDialog_Text2']}")
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.Yes)
        msgbox.buttonClicked.connect(self.LocateFile)
        msgbox.setIcon(QtWidgets.QMessageBox.Information)
        msgbox.setWindowIcon(QtGui.QIcon("img/icon.png"))
        runmsgbox = msgbox.exec_()
        self.EnableButtons(self, True)

    # function below written by some person on stack overflow
    def compress_video(self, MainWindow, video_full_path, output_file_name, target_size):
        # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
        min_audio_bitrate = 64000
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
    
    def LocateFile(self):
        global msgbox
        if msgbox.clickedButton().text() == "&Yes":
            if os.name == "nt":  # Check if the operating system is Windows
                try:
                    subprocess.run(['explorer', '/select,', self.LineOutput.text().replace("/", "\\")])
                except:
                    os.startfile(self.RemoveAfterLastSlash(self, self.LineOutput.text()))
            else:
                os.startfile(self.RemoveAfterLastSlash(self, self.LineOutput.text()))
        else:
            pass

class Ui_SettingsWindow(QtWidgets.QMainWindow):
    def setupUi(self, SettingsWindow):
        global ConfigData, ResetConfigData
        fontsmaller = QtGui.QFont()
        fontsmaller.setPointSize(8)
        
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName("SettingsWindow")
        # SettingsWindow.setFixedSize(251, 292)
        SettingsWindow.setFixedSize(251, 170)
        SettingsWindow.setWindowIcon(QtGui.QIcon("img/settings.png"))
        SettingsWindow.setWindowFlags(SettingsWindow.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        SettingsWindow.setWindowFlags(SettingsWindow.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        SettingsWindow.setFont(fontsmaller)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.GroupDefaultSize = QtWidgets.QGroupBox(self.centralwidget)
        self.GroupDefaultSize.setObjectName("GroupDefaultSize")
        self.GroupDefaultSize.setGeometry(QtCore.QRect(10, 70, 231, 71))
        self.LabelDefaultSize = QtWidgets.QLabel(self.GroupDefaultSize)
        self.LabelDefaultSize.setObjectName("LabelDefaultSize")
        self.LabelDefaultSize.setGeometry(QtCore.QRect(10, 20, 211, 16))
        self.DoubleSpinDefaultSize = QtWidgets.QDoubleSpinBox(self.GroupDefaultSize)
        self.DoubleSpinDefaultSize.setObjectName("DoubleSpinDefaultSize")
        #self.DoubleSpinDefaultSize.setAlignment(QtCore.Qt.AlignCenter)
        self.DoubleSpinDefaultSize.setGeometry(QtCore.QRect(60, 39, 111, 22))
        self.DoubleSpinDefaultSize.setMaximum(9999.989999999999782)
        # Too lazy to add that rn
        # self.GroupDefaultPath = QtWidgets.QGroupBox(self.centralwidget)
        # self.GroupDefaultPath.setObjectName("GroupDefaultPath")
        # self.GroupDefaultPath.setGeometry(QtCore.QRect(10, 150, 231, 111))
        # self.LabelDefaultPath = QtWidgets.QLabel(self.GroupDefaultPath)
        # self.LabelDefaultPath.setObjectName("LabelDefaultPath")
        # self.LabelDefaultPath.setGeometry(QtCore.QRect(10, 20, 211, 16))
        # self.RadioPathLastUsed = QtWidgets.QRadioButton(self.GroupDefaultPath)
        # self.RadioPathLastUsed.setObjectName("RadioPathLastUsed")
        # self.RadioPathLastUsed.setGeometry(QtCore.QRect(10, 40, 211, 20))
        # self.RadioPathRoot = QtWidgets.QRadioButton(self.GroupDefaultPath)
        # self.RadioPathRoot.setObjectName("RadioPathRoot")
        # self.RadioPathRoot.setGeometry(QtCore.QRect(10, 60, 211, 20))
        # self.RadioPathCustom = QtWidgets.QRadioButton(self.GroupDefaultPath)
        # self.RadioPathCustom.setObjectName("RadioPathCustom")
        # self.RadioPathCustom.setGeometry(QtCore.QRect(10, 80, 211, 20))
        # self.LineCustomDefaultPath = QtWidgets.QLineEdit(self.GroupDefaultPath)
        # self.LineCustomDefaultPath.setObjectName("LineCustomDefaultPath")
        # self.LineCustomDefaultPath.setGeometry(QtCore.QRect(28, 80, 158, 20))
        # self.ButtonCustomDefaultPath = QtWidgets.QPushButton(self.GroupDefaultPath)
        # self.ButtonCustomDefaultPath.setObjectName("ButtonCustomDefaultPath")
        # self.ButtonCustomDefaultPath.setGeometry(QtCore.QRect(189, 79, 32, 22))
        self.GroupLanguage = QtWidgets.QGroupBox(self.centralwidget)
        self.GroupLanguage.setObjectName("GroupLanguage")
        self.GroupLanguage.setGeometry(QtCore.QRect(10, 10, 231, 51))
        self.ComboLanguage = QtWidgets.QComboBox(self.GroupLanguage)
        self.ComboLanguage.setObjectName("ComboLanguage")
        self.ComboLanguage.setGeometry(QtCore.QRect(10, 20, 211, 22))
        SettingsWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(SettingsWindow)
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 251, 21))
        self.actionSaveAndClose = QtWidgets.QAction(self.menuBar)
        self.actionSaveAndClose.setObjectName("actionSaveAndClose")
        self.actionClose = QtWidgets.QAction(self.menuBar)
        self.actionClose.setObjectName("actionClose")
        SettingsWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.actionSaveAndClose)
        self.menuBar.addAction(self.actionClose)
        
        self.ComboLanguage.addItem("")
        self.ComboLanguage.setItemText(0, "English (United States)")
        self.ComboLanguage.setItemIcon(0, QtGui.QIcon("img/flag_us.png"))
        self.ComboLanguage.addItem("")
        self.ComboLanguage.setItemText(1, "latviešu (Latvija)")
        self.ComboLanguage.setItemIcon(1, QtGui.QIcon("img/flag_lv.png"))
        self.ComboLanguage.addItem("")
        self.ComboLanguage.setItemText(2, "русский (Россия)")
        self.ComboLanguage.setItemIcon(2, QtGui.QIcon("img/flag_ru.png"))
        self.ComboLanguage.addItem("")
        self.ComboLanguage.setItemText(3, "українська (Україна)")
        self.ComboLanguage.setItemIcon(3, QtGui.QIcon("img/flag_ua.png"))
        
        self.LoadSettings(self)
        self.retranslateUi(SettingsWindow)
        
        self.actionClose.triggered.connect(SettingsWindow.close)
        
        def SaveAndClose():
            self.SaveSettings(self)
            SettingsWindow.close()
        
        self.actionSaveAndClose.triggered.connect(SaveAndClose)

        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        global CurrentTranslation
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(CurrentTranslation["SettingsWindow_Title"])
        self.GroupDefaultSize.setTitle(CurrentTranslation["SettingsWindow_GroupDefaultSize"])
        self.LabelDefaultSize.setText(CurrentTranslation["SettingsWindow_LabelDefaultSize"])
        #self.GroupDefaultPath.setTitle(CurrentTranslation["SettingsWindow_GroupDefaultPath"])
        #self.LabelDefaultPath.setText(CurrentTranslation["SettingsWindow_LabelDefaultPath"])
        #self.RadioPathLastUsed.setText(CurrentTranslation["SettingsWindow_RadioPathLastUsed"])
        #self.RadioPathRoot.setText(CurrentTranslation["SettingsWindow_RadioPathRoot"])
        #self.RadioPathCustom.setText("")
        #self.ButtonCustomDefaultPath.setText("...")
        self.GroupLanguage.setTitle(CurrentTranslation["SettingsWindow_GroupLanguage"])

        self.actionSaveAndClose.setText(CurrentTranslation["SettingsWindow_actionSaveAndClose"])
        self.actionClose.setText(CurrentTranslation["SettingsWindow_actionClose"])
        
    def SaveSettings(self, SettingsWindow, ResetSettings=False):
        global ConfigData, ResetConfigData
        if self.ComboLanguage.currentIndex() == 0:
            ConfigData["language"] = "english"
        elif self.ComboLanguage.currentIndex() == 1:
            ConfigData["language"] = "latvian"
        elif self.ComboLanguage.currentIndex() == 2:
            ConfigData["language"] = "russian"
        elif self.ComboLanguage.currentIndex() == 3:
            ConfigData["language"] = "ukrainian"
        else:
            ConfigData["language"] = "english"
        
        ConfigData["default_size"] = self.DoubleSpinDefaultSize.value()
        
        # if self.RadioPathLastUsed.isChecked():
            # ConfigData["path_mode"] = 0
        # if self.RadioPathRoot.isChecked():
            # ConfigData["path_mode"] = 1
        # elif self.RadioPathCustom.isChecked():
            # ConfigData["path_mode"] = 2
        # else:
            # ConfigData["path_mode"] = 0
        
        # ConfigData["path_custom"] = self.LineCustomDefaultPath.text()
        
        with open(ConfigPath, "w") as f:
            if not ResetSettings:
                json.dump(ConfigData, f, indent = "\t")
            else:
                json.dump(ResetConfigData, f, indent = "\t")
        
        UpdateTranslation()
        MainWindow.retranslateUi()
    
    def LoadSettings(self, SettingsWindow):
        global ConfigData, ResetConfigData
        if os.path.isfile(ConfigPath):
            with open(ConfigPath, "r") as f:
                ConfigData = json.load(f)
            if ConfigData["language"] == "english":
                self.ComboLanguage.setCurrentIndex(0)
            elif ConfigData["language"] == "latvian":
                self.ComboLanguage.setCurrentIndex(1)
            elif ConfigData["language"] == "russian":
                self.ComboLanguage.setCurrentIndex(2)
            elif ConfigData["language"] == "ukrainian":
                self.ComboLanguage.setCurrentIndex(3)
            else:
                self.ComboLanguage.setCurrentIndex(0)
            
            self.DoubleSpinDefaultSize.setValue(ConfigData["default_size"])
        
            # if ConfigData["path_mode"] == 0:
                # self.RadioPathLastUsed.setChecked(True)
            # if ConfigData["path_mode"] == 1:
                # self.RadioPathRoot.setChecked(True)
            # elif ConfigData["path_mode"] == 2:
                # self.RadioPathCustom.setChecked(True)
            # else:
                # self.RadioPathCustom.setChecked(True)
            
            # self.LineCustomDefaultPath.setText(ConfigData["path_custom"])
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.setupUi(MainWindow)
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
