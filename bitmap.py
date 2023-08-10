import sys, os, cv2, pyautogui
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore

from cso_lua_export import *

try:
    from wand.image import *
    from wand.color import *
    canConvert = True
except:
    canConvert = False
    pass

checkBox = None
isPaintBtnPressed = False

class PaintButton(QPushButton):
    def enterEvent(self, event):
        super().enterEvent(event)
        if isPaintBtnPressed:
            self.click()
       
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.RightButton:
            global isPaintBtnPressed, checkBox
            isPaintBtnPressed = not isPaintBtnPressed
            checkBox.setChecked(isPaintBtnPressed)

class PaintBackground(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0, 0, 481, 481)
        self.setStyleSheet("background: white")

        self.is32x32 = False

    def set32x32(self, isOn):
        self.is32x32 = isOn

    def paintEvent(self, event):
        painter = QPainter(self)

        brush = QBrush(QColor(170, 170, 170))
        if self.is32x32 == True:
            painter.scale(0.5, 0.5)
            for i in range(96):
                for j in range(48):
                    if i % 2 == 0:
                        painter.fillRect(QRectF(20 * j, 10 * i, 10, 10), brush)
                    else:
                        painter.fillRect(QRectF(10 + 20 * j, 10 * i, 10, 10), brush)
        
            pen = QPen(Qt.black, 1)
            painter.setPen(pen)
            for i in range(32+1):
                painter.drawLine(QPoint(30 * i, 0), QPoint(30 * i, self.height() * 2))
                painter.drawLine(QPoint(0, 30 * i), QPoint(self.width() * 2, 30 * i))
        else:
            painter.scale(1.0, 1.0)
            for i in range(48):
                for j in range(24):
                    if i % 2 == 0:
                        painter.fillRect(QRectF(20 * j, 10 * i, 10, 10), brush)
                    else:
                        painter.fillRect(QRectF(10 + 20 * j, 10 * i, 10, 10), brush)
        
            pen = QPen(Qt.black, 1)
            painter.setPen(pen)
            for i in range(16+1):
                painter.drawLine(QPoint(30 * i, 0), QPoint(30 * i, self.height()))
                painter.drawLine(QPoint(0, 30 * i), QPoint(self.width(), 30 * i))

        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        about = QMessageBox()
        about.setText("【製作者】崩潰金魚燒、DestroyerI滅世I   ")
        about.setStandardButtons(QMessageBox.Ok)
        about.setWindowTitle(QCoreApplication.translate("about", u"【提醒】此程式完全免費！", None))
        about.setStyleSheet(u"font: 75 15pt NSimSun")
        about.setWindowIcon(QIcon("./icon/icon.png"))
        about = about.exec()

        self.setWindowTitle("CSO STUDIO LUA | 像素圖")
        self.setWindowIcon(QIcon("./icon/icon.png"))
        self.setFixedSize(960, 511)
        self.setStyleSheet(u"QTabWidget::pane {\n"
"	border: 1px solid #000000;\n"
"	border-radius: 2px;\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"	padding: 5px 209px 5px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(50, 50, 75);\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"	border-bottom: 2px solid rgb(250, 175, 0, 175);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"	border-bottom: 2px solid #fca311;\n"
"}")

        # 儲存顏色，未來輸出用
        self.colors = [[['0','0','0','0'] for j in range(16)] for i in range(16)]

        self.mode = 1
        self.save = True
        
        self.row = 16
        self.column = 16

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 961, 511))
        self.tabWidget.setStyleSheet(u"font: 87 10pt \"Arial Black\";")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Bitmap", u"CONVERT", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Bitmap", u"BITMAP", None))

        self.RGBA = []
        self.labels = ["R", "G", "B", "A"]
        for i in range(4):
            if i == 0:
                #r
                color = QSpinBox(self.tab_2)
                color.setObjectName(u"spinBox")
                color.setGeometry(QRect(550, 260, 171, 31))
                color.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
                color.setAlignment(Qt.AlignCenter)
                color.setMaximum(255)

            if i == 1:
                #g
                color = QSpinBox(self.tab_2)
                color.setObjectName(u"spinBox_2")
                color.setGeometry(QRect(550, 300, 171, 31))
                color.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
                color.setAlignment(Qt.AlignCenter)
                color.setMaximum(255)

            if i == 2:
                #b
                color = QSpinBox(self.tab_2)
                color.setObjectName(u"spinBox_3")
                color.setGeometry(QRect(550, 340, 171, 31))
                color.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
                color.setAlignment(Qt.AlignCenter)
                color.setMaximum(255)

            if i == 3:
                #a
                color = QSpinBox(self.tab_2)
                color.setObjectName(u"spinBox_4")
                color.setGeometry(QRect(550, 380, 171, 31))
                color.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
                color.setAlignment(Qt.AlignCenter)
                color.setMaximum(255)
                color.setValue(255)

            self.RGBA.append(color)

            color.valueChanged.connect(lambda state, info=[color, i]: self.colorvalueEvent(info))

        #draw
        self.drawbtn = QRadioButton(self.tab_2)
        self.drawbtn.setChecked(True)
        self.drawbtn.setObjectName(u"drawbtn")
        self.drawbtn.setGeometry(QRect(490, 60, 231, 41))
        self.drawbtn.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.drawbtn.clicked.connect(self.draw)

        #eraser
        self.eraserbtn = QRadioButton(self.tab_2)
        self.eraserbtn.setObjectName(u"eraserbtn")
        self.eraserbtn.setGeometry(QRect(490, 110, 231, 41))
        self.eraserbtn.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.eraserbtn.clicked.connect(self.eraser)

        #selectcolor
        self.selectcolorbtn = QRadioButton(self.tab_2)
        self.selectcolorbtn.setObjectName(u"selectcolorbtn")
        self.selectcolorbtn.setGeometry(QRect(490, 160, 231, 41))
        self.selectcolorbtn.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.selectcolorbtn.clicked.connect(self.selectcolor)

        #colorpicker
        self.btnColorPicker = QPushButton(self.tab_2)
        self.btnColorPicker.setObjectName(u"btnColorPicker")
        self.btnColorPicker.setGeometry(QRect(500, 420, 221, 41))
        self.btnColorPicker.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.btnColorPicker.clicked.connect(self.colorPicker)

        #clearcanvas
        self.btnClearCanvas = QPushButton(self.tab_2)
        self.btnClearCanvas.setObjectName(u"btnClearCanvas")
        self.btnClearCanvas.setGeometry(QRect(730, 160, 110, 41))
        self.btnClearCanvas.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.btnClearCanvas.clicked.connect(self.clearCanvas)

        #import
        self.btnImport = QToolButton(self.tab_2)
        self.btnImport.setObjectName(u"btnImport")
        self.btnImport.setGeometry(QRect(841, 160, 110, 41))
        self.btnImport.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.btnImport.clicked.connect(self.Import)

        #export
        self.exportBtn = QPushButton(self.tab_2)
        self.exportBtn.setObjectName(u"exportBtn")
        self.exportBtn.setGeometry(QRect(730, 420, 221, 41))
        self.exportBtn.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.exportBtn.clicked.connect(self.export)

        #exportname
        self.exportName = QLineEdit(self.tab_2)
        self.exportName.setObjectName(u"exportName")
        self.exportName.setGeometry(QRect(730, 260, 221, 31))
        self.exportName.setStyleSheet(u"font: 87 10pt \"Arial Black\";")
        self.exportName.setAlignment(Qt.AlignCenter)

        self.bg = PaintBackground(self.tab_2)

        #size16x16
        self.size16x16 = QPushButton(self.tab_2)
        self.size16x16.setObjectName(u"size16x16")
        self.size16x16.setGeometry(QRect(730, 60, 221, 41))
        self.size16x16.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.size16x16.clicked.connect(lambda: self.bg.set32x32(False))
        self.size16x16.clicked.connect(self.sizes16x16)

        #size32x32
        self.size32x32 = QPushButton(self.tab_2)
        self.size32x32.setObjectName(u"size32x32")
        self.size32x32.setGeometry(QRect(730, 110, 221, 41))
        self.size32x32.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.size32x32.clicked.connect(lambda: self.bg.set32x32(True))
        self.size32x32.clicked.connect(self.sizes32x32)

        self.btnconvertcf = QPushButton(self.tab)
        self.btnconvertcf.setObjectName(u"btnconvertcf")
        self.btnconvertcf.setGeometry(QRect(260, 120, 421, 61))
        self.btnconvertcf.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label")
        self.label_9.setGeometry(QRect(260, 50, 421, 71))
        self.label_9.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.convetsize32x32 = QRadioButton(self.tab)
        self.convetsize32x32.setObjectName(u"convetsize32x32")
        self.convetsize32x32.setGeometry(QRect(490, 280, 191, 41))
        self.convetsize32x32.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.convetsize16x16 = QRadioButton(self.tab)
        self.convetsize16x16.setObjectName(u"convetsize16x16")
        self.convetsize16x16.setGeometry(QRect(260, 280, 191, 41))
        self.convetsize16x16.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.convetsize16x16.setChecked(True)
        self.btnconvert = QPushButton(self.tab)
        self.btnconvert.setObjectName(u"btnconvert")
        self.btnconvert.setGeometry(QRect(260, 340, 421, 61))
        self.btnconvert.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(480, 20, 241, 31))
        self.label.setStyleSheet(u"font: 20pt \"\u83ef\u5eb7\u5137\u7279\u5713\";")
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(490, 220, 231, 31))
        self.label_2.setStyleSheet(u"font: 20pt \"\u83ef\u5eb7\u5137\u7279\u5713\";")
        self.label_3 = QLabel(self.tab_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(500, 260, 51, 31))
        self.label_3.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.label_4 = QLabel(self.tab_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(500, 300, 51, 31))
        self.label_4.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(500, 340, 51, 31))
        self.label_5.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.label_6 = QLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(500, 380, 51, 31))
        self.label_6.setStyleSheet(u"font: 87 20pt \"Arial Black\";")
        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(720, 220, 231, 31))
        self.label_7.setStyleSheet(u"font: 20pt \"\u83ef\u5eb7\u5137\u7279\u5713\";")
        self.label_8 = QLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(730, 20, 231, 31))
        self.label_8.setStyleSheet(u"font: 20pt \"\u83ef\u5eb7\u5137\u7279\u5713\";")

        self.drawbtn.setText(QCoreApplication.translate("Form", u"Draw", None))
        self.eraserbtn.setText(QCoreApplication.translate("Form", u"Eraser", None))
        self.selectcolorbtn.setText(QCoreApplication.translate("Form", u"Select Color", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u3010\u756b\u7b46\u3011", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u3010\u984f\u8272\u3011", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"R\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"G\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"B\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"A\uff1a", None))
        self.btnColorPicker.setText(QCoreApplication.translate("Form", u"Color Picker", None))
        self.btnClearCanvas.setText(QCoreApplication.translate("Form", u"Clear", None))
        self.btnImport.setText(QCoreApplication.translate("Form", u"Import", None))
        self.exportBtn.setText(QCoreApplication.translate("Form", u"Export", None))
        self.exportName.setPlaceholderText(QCoreApplication.translate("Form", u"English or Number Name", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u3010\u8f38\u51fa\u3011", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u3010\u756b\u677f\u3011", None))
        self.size16x16.setText(QCoreApplication.translate("Form", u"16x16", None))
        self.size32x32.setText(QCoreApplication.translate("Form", u"32x32", None))
        self.btnconvertcf.setText(QCoreApplication.translate("Bitmap", u"Choose File", None))
        self.label_9.setText(QCoreApplication.translate("Bitmap", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:400;\">Convert Image to *.bitmap</span></p></body></html>", None))
        self.convetsize32x32.setText(QCoreApplication.translate("Bitmap", u"Size 32x32", None))
        self.convetsize16x16.setText(QCoreApplication.translate("Bitmap", u"Size 16x16", None))
        self.btnconvert.setText(QCoreApplication.translate("Bitmap", u"Convert", None))

        self.checkBox = QCheckBox(self.tab_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(600, 10, 241, 51))
        self.checkBox.setStyleSheet(u"font: 15pt \"\u83ef\u5eb7\u5137\u7279\u5713\";")
        self.checkBox.setAutoRepeat(False)
        self.checkBox.setAutoExclusive(False)
        self.checkBox.setText(QCoreApplication.translate("Form", u"右鍵單擊\n滑動模式", None))
        self.checkBox.clicked.connect(self.checkPen)

        global checkBox
        checkBox = self.checkBox

        self.btnconvertcf.clicked.connect(self.convertChoosefile)
        self.btnconvert.clicked.connect(self.convertBtn)
        self.convetsize16x16.clicked.connect(self.convert16x16)
        self.convetsize32x32.clicked.connect(self.convert32x32)

        self.tabWidget.currentChanged.connect(self.tabChange)

        if canConvert == False:
            self.tabWidget.setCurrentIndex(1)
            error = QMessageBox()
            error.setText("    【錯誤】無法使用Convert功能\n   偵測到使用者未安裝Image Magick！   ")
            error.setStandardButtons(QMessageBox.Ok)
            error.setWindowTitle(QCoreApplication.translate("error", u"ERROR", None))
            error.setStyleSheet(u"font: 75 15pt NSimSun")
            error.setWindowIcon(QIcon("./icon/icon.png"))
            error = error.exec()

        self.convertFile = ''
        self.convertFilename = ''
        self.convertSize = 16

        self.btns = []
        for i in range(32):
            self.btns.append([])
            for j in range(32):
                btn = PaintButton(self.tab_2)
                btn.setGeometry(QRect(30 * i, 30 * j, 31, 31))
                btn.clicked.connect(lambda state, info=[btn, i, j], :self.clickedEvent(info))

                self.btns[i].append(btn)
                btn.setStyleSheet(u"QPushButton {background-color: rgba(0,0,0,0);}\nQPushButton:hover {background-color: rgba(0,0,0,255);}\nQPushButton:pressed {background-color: rgba(150,150,150,255);}")

                if i >= 16 or j >= 16:
                    btn.hide()

    def checkPen(self):
        self.checkBox.setChecked(isPaintBtnPressed)

    def convert16x16(self):
        self.convertSize = 16

    def convert32x32(self):
        self.convertSize = 32

    def convertChoosefile(self):
        file = QFileDialog()
        file.setNameFilter("Images (*.png *.jpg *.jpeg *.tiff *.psd *.bmp *.pict)")
        if file.exec_():
            file_name = file.selectedFiles()
            self.convertFilename = file_name[0]
            self.convertFile = Image(filename = file_name[0])
            fname = file_name[0].split("/")
            self.fname = fname[len(fname) - 1]

    def convertBtn(self):
        if self.convertFile != '':
            try:
                img = cv2.imread(self.convertFilename)
                if img.shape[0] > img.shape[1]:
                    img = cv2.resize(img, (int(img.shape[1] / (img.shape[0] / self.convertSize)), int(img.shape[0] / (img.shape[0] / self.convertSize))))
                if img.shape[1] > img.shape[0]:
                    img = cv2.resize(img, (int(img.shape[1] / (img.shape[1] / self.convertSize)), int(img.shape[0] / (img.shape[1] / self.convertSize))))
                if img.shape[0] == img.shape[1]:
                    img = cv2.resize(img, (self.convertSize, self.convertSize))
                cv2.imwrite('resize.png', img)
                self.convertFile = Image(filename = 'resize.png')
                self.convertFile_convert = self.convertFile.convert('txt')
                self.convertFile_convert.save(filename ='convert.txt')
                with open("convert.txt", "r", encoding="UTF-8") as f:
                    splits = []
                    for line in f:
                        if line[0:1] != '#':
                            split = line.split(": (")
                            splits.append(split)

                n = 0
                l = 0
                str_ = []
                with open(self.fname + ".bitmap", "w", encoding="UTF-8") as f:
                    f.write("")

                for split in splits:
                    split = split[1].split(')')
                    split = split[0].split(',')
                    r = split[0]
                    g = split[1]
                    b = split[2]
                    if len(split) == 3:
                        a = 255
                    elif len(split) == 4:
                        a = split[3]

                    str_.append([l])
                    str_[l] = str(str_[l]) + "-{"+str(r)+','+str(g)+','+str(b)+','+str(a)+"}"
                    
                    n = n + 1
                    if len(splits) < 512:
                        if n == img.shape[0]:
                            n = 0
                            with open(self.fname + ".bitmap", "a", encoding="UTF-8") as f:
                                f.write(str_[l][4:]+'\n')
                            l = l + 1
                    else:
                        if n == img.shape[1]:
                            n = 0
                            with open(self.fname + ".bitmap", "a", encoding="UTF-8") as f:
                                f.write(str_[l][4:]+'\n')
                            l = l + 1

                os.remove('resize.png')
                os.remove('convert.txt')
                successed = QMessageBox()
                successed.setText("【成功】轉換完成！   ")
                successed.setStandardButtons(QMessageBox.Ok)
                successed.setWindowTitle(QCoreApplication.translate("successed", u"SUCCESSED", None))
                successed.setStyleSheet(u"font: 75 15pt NSimSun")
                successed.setWindowIcon(QIcon("./icon/icon.png"))
                successed = successed.exec()
            except AttributeError:
                error = QMessageBox()
                error.setText("【錯誤】檔案名稱不能為中文及其他特殊符號！   ")
                error.setStandardButtons(QMessageBox.Ok)
                error.setWindowTitle(QCoreApplication.translate("error", u"ERROR", None))
                error.setStyleSheet(u"font: 75 15pt NSimSun")
                error.setWindowIcon(QIcon("./icon/icon.png"))
                error = error.exec()

        else:
            close = QMessageBox()
            close.setText("【錯誤】沒有找到要轉換的圖片檔案！   ")
            close.setWindowIcon(QIcon("./icon/icon.png"))
            close.setStyleSheet(u"font: 75 15pt NSimSun")
            close.setStandardButtons(QMessageBox.Ok)
            close.setWindowTitle(QCoreApplication.translate("close", u"ERROR", None))
            close = close.exec()

    def tabChange(self):
        if self.tabWidget.currentIndex() == 0:
            if canConvert == False:
                self.tabWidget.setCurrentIndex(1)
                error = QMessageBox()
                error.setText("    【錯誤】無法使用Convert功能\n   偵測到使用者未安裝Image Magick！   ")
                error.setStandardButtons(QMessageBox.Ok)
                error.setWindowTitle(QCoreApplication.translate("error", u"ERROR", None))
                error.setStyleSheet(u"font: 75 15pt NSimSun")
                error.setWindowIcon(QIcon("./icon/icon.png"))
                error = error.exec()

    def closeEvent(self, event):
        if self.save == False:
            close = QMessageBox()
            close.setText("【提醒】偵測到尚未輸出檔案，確定要關閉嗎？   ")
            close.setWindowIcon(QIcon("./icon/icon.png"))
            close.setStyleSheet(u"font: 75 15pt NSimSun")
            close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            close.setWindowTitle(QCoreApplication.translate("close", u" ", None))
            close = close.exec()
            if close == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def sizes16x16(self):
        self.row = 16
        self.column = 16
        self.clearCanvas()

        for i in range(32):
            for j in range(32):
                if i < 16 and j < 16:
                    self.btns[i][j].show()
                    self.btns[i][j].setGeometry(QRect(30 * i, 30 * j, 31, 31))
                else:
                    self.btns[i][j].hide()

    def sizes32x32(self):
        self.row = 32
        self.column = 32
        self.clearCanvas()

        for i in range(32):
            for j in range(32):
                self.btns[i][j].show()
                self.btns[i][j].setGeometry(QRect(15 * i, 15 * j, 16, 16))

    def draw(self):
        self.mode = 1
        r = str(self.RGBA[0].value())
        g = str(self.RGBA[1].value())
        b = str(self.RGBA[2].value())
        a = str(self.RGBA[3].value())
        color = r+","+g+","+b+","+a

        style1 = ''
        style2 = ''
        style3 = ''
        style4 = ''
        style5 = ''
        styleR = ''
        styleG = ''
        styleB = ''
        styleA = ''
        for row in self.btns:
            for btn in row:
                style1 = btn.styleSheet()
                style2 = style1.split('\n')
                style3 = style2[0].split(',')
                style4 = style3[0].split('(')
                styleR = style4[1]
                styleG = style3[1]
                styleB = style3[2]
                style5 = style3[3].split(')')
                styleA = style5[0]
                color1 = styleR+","+styleG+","+styleB+","+styleA
                btn.setStyleSheet(u"QPushButton {background-color: rgba("+color1+");}\nQPushButton:hover {background-color: rgba("+color+");}\nQPushButton:pressed {background-color: rgba(150,150,150,255);}")

    def eraser(self):
        self.mode = 2
        style1 = ''
        style2 = ''
        style3 = ''
        style4 = ''
        style5 = ''
        styleR = ''
        styleG = ''
        styleB = ''
        styleA = ''
        for row in self.btns:
            for btn in row:
                style1 = btn.styleSheet()
                style2 = style1.split('\n')
                style3 = style2[0].split(',')
                style4 = style3[0].split('(')
                styleR = style4[1]
                styleG = style3[1]
                styleB = style3[2]
                style5 = style3[3].split(')')
                styleA = style5[0]
                color1 = styleR+","+styleG+","+styleB+","+styleA
                btn.setStyleSheet(u"QPushButton {background-color: rgba("+color1+");}\nQPushButton:hover {background-color: rgba(0,0,0,0);}\nQPushButton:pressed {background-color: rgba(150,150,150,255);}")

    def selectcolor(self):
        self.mode = 3

    def colorPicker(self):
        color = QColorDialog().getColor()
        self.RGBA[0].setValue(color.red())
        self.RGBA[1].setValue(color.green())
        self.RGBA[2].setValue(color.blue())

    def clearCanvas(self):
        self.save = True
        for row in self.btns:
            for btn in row:
                r = str(self.RGBA[0].value())
                g = str(self.RGBA[1].value())
                b = str(self.RGBA[2].value())
                a = str(self.RGBA[3].value())
                color = r+","+g+","+b+","+a
            
                btn.setStyleSheet(u"QPushButton {background-color: rgba(0,0,0,0);}\nQPushButton:hover {background-color: rgba("+color+");}\nQPushButton:pressed {background-color: rgba(150,150,150,255);}")

        self.colors = [[['0','0','0','0'] for j in range(self.column)] for i in range(self.row)]

    def Import(self):
        open_ = False
        self.splits = []
        file = QFileDialog()
        file.setNameFilter("Bitmaps (*.bitmap)")
        if file.exec_():
            file_name = file.selectedFiles()
            if file_name[0].endswith('.bitmap'):
                with open(file_name[0], 'r', encoding="UTF-8") as f:
                    open_ = True
                    for line in f:
                        split = line.split('-')
                        split[len(split) - 1] = split[len(split) - 1].split('\n')[0]
                        self.splits.append(split)
                        if len(split) > 16:
                            self.is32x32 = True
                            self.row = 32
                            self.column = 32
                            self.clearCanvas()

                            for i in range(32):
                                for j in range(32):
                                    self.btns[i][j].show()
                                    self.btns[i][j].setGeometry(QRect(15 * i, 15 * j, 16, 16))
                        else:
                            self.is32x32 = False
                            self.row = 16
                            self.column = 16
                            self.clearCanvas()

                            for i in range(32):
                                for j in range(32):
                                    if i < 16 and j < 16:
                                        self.btns[i][j].show()
                                        self.btns[i][j].setGeometry(QRect(30 * i, 30 * j, 31, 31))
                                    else:
                                        self.btns[i][j].hide()

                        self.bg.set32x32(self.is32x32)

        if open_:
            self.save = False
            indexerror = False
            for i in range(self.row):
                for j in range(self.column):
                    try:
                        if self.splits[j][i][-2:-1] == '}':
                            self.splits[j][i] = self.splits[j][i][0:-2]

                        splits = self.splits[j][i].split(',')
                        splits[0] = splits[0][1:]
                        splits[3] = splits[3][:-1]
                        r = splits[0]
                        g = splits[1]
                        b = splits[2]
                        a = splits[3]
                        colors = [r,g,b,a]
                        self.colors[j][i] = colors
                        color = r+','+g+','+b+','+a
                        self.btns[i][j].setStyleSheet(u"QPushButton {background-color: rgba("+color+");}\nQPushButton:hover {background-color: rgba("+color+");}\nQPushButton:pressed {background-color: rgba(150,150,150,255);}")
                    except IndexError:
                        if indexerror == False:
                            error = QMessageBox()
                            error.setText(" 【錯誤】無法偵測所輸入的bitmap檔案資料\n 這「可能」會導致讀出來的像素圖有些問題！   ")
                            error.setStandardButtons(QMessageBox.Ok)
                            error.setWindowTitle(QCoreApplication.translate("error", u"ERROR", None))
                            error.setStyleSheet(u"font: 75 15pt NSimSun")
                            error.setWindowIcon(QIcon("./icon/icon.png"))
                            error = error.exec()
                        indexerror = True
                        pass
                            

        self.mode = 1
        r = str(self.RGBA[0].value())
        g = str(self.RGBA[1].value())
        b = str(self.RGBA[2].value())
        a = str(self.RGBA[3].value())
        color = r+","+g+","+b+","+a

        style1 = ''
        style2 = ''
        style3 = ''
        style4 = ''
        style5 = ''
        styleR = ''
        styleG = ''
        styleB = ''
        styleA = ''
        for row in self.btns:
            for btn in row:
                style1 = btn.styleSheet()
                style2 = style1.split('\n')
                style3 = style2[0].split(',')
                style4 = style3[0].split('(')
                styleR = style4[1]
                styleG = style3[1]
                styleB = style3[2]
                style5 = style3[3].split(')')
                styleA = style5[0]
                color1 = styleR+","+styleG+","+styleB+","+styleA
                btn.setStyleSheet(u"QPushButton {background-color: rgba("+color1+");}\nQPushButton:hover {background-color: rgba("+color+");}\nQPushButton:pressed {background-color: rgba(150,150,150,255);}")

    def clickedEvent(self, info):
        self.save = False
        btn = info[0]
        if self.mode != 3:
            if self.mode == 1:
                r = str(self.RGBA[0].value())
                g = str(self.RGBA[1].value())
                b = str(self.RGBA[2].value())
                a = str(self.RGBA[3].value())

            if self.mode == 2:
                r = str(0)
                g = str(0)
                b = str(0)
                a = str(0)

            color = r+","+g+","+b+","+a
            colors = [r,g,b,a]
        
            btn.setStyleSheet(u"QPushButton {background-color: rgba("+color+");}\nQPushButton:hover {background-color: rgba("+color+");}\nQPushButton:pressed {background-color: rgba(150,150,150,255);}")
        
            row = info[1]
            column = info[2]
            self.colors[column][row] = colors
        else:
            style1 = ''
            style2 = ''
            style3 = ''
            style4 = ''
            style5 = ''
            styleR = ''
            styleG = ''
            styleB = ''
            styleA = ''
            style1 = btn.styleSheet()
            style2 = style1.split('\n')
            style3 = style2[0].split(',')
            style4 = style3[0].split('(')
            styleR = style4[1]
            styleG = style3[1]
            styleB = style3[2]
            style5 = style3[3].split(')')
            styleA = style5[0]
            self.RGBA[0].setValue(int(styleR))
            self.RGBA[1].setValue(int(styleG))
            self.RGBA[2].setValue(int(styleB))
            self.RGBA[3].setValue(int(styleA))

    def colorvalueEvent(self, info):
        r = str(self.RGBA[0].value())
        g = str(self.RGBA[1].value())
        b = str(self.RGBA[2].value())
        a = str(self.RGBA[3].value())
        color = r+","+g+","+b+","+a

        style1 = ''
        style2 = ''
        style3 = ''
        style4 = ''
        style5 = ''
        styleR = ''
        styleG = ''
        styleB = ''
        styleA = ''
        for row in self.btns:
            for btn in row:
                style1 = btn.styleSheet()
                style2 = style1.split('\n')
                style3 = style2[0].split(',')
                style4 = style3[0].split('(')
                styleR = style4[1]
                styleG = style3[1]
                styleB = style3[2]
                style5 = style3[3].split(')')
                styleA = style5[0]
                color1 = styleR+","+styleG+","+styleB+","+styleA
                btn.setStyleSheet(u"QPushButton {background-color: rgba("+color1+");}\nQPushButton:hover {background-color: rgba("+color+");}\nQPushButton:pressed {background-color: rgba(150,150,150,255);}")

    def export(self):
        if self.save == True:
            error = QMessageBox()
            error.setText("【錯誤】無法輸出沒有進行修改的像素圖！   ")
            error.setStandardButtons(QMessageBox.Ok)
            error.setWindowTitle(QCoreApplication.translate("error", u"ERROR", None))
            error.setStyleSheet(u"font: 75 15pt NSimSun")
            error.setWindowIcon(QIcon("./icon/icon.png"))
            error = error.exec()
        else:
            varName = self.exportName.text()
            if varName == '':
                error = QMessageBox()
                error.setText("【錯誤】請輸入輸出後的檔案名稱！   ")
                error.setStandardButtons(QMessageBox.Ok)
                error.setWindowTitle(QCoreApplication.translate("error", u"ERROR", None))
                error.setStyleSheet(u"font: 75 15pt NSimSun")
                error.setWindowIcon(QIcon("./icon/icon.png"))
                error = error.exec()
            else:
                if varName[0:1] != '0'\
                and varName[0:1] != '1'\
                and varName[0:1] != '2'\
                and varName[0:1] != '3'\
                and varName[0:1] != '4'\
                and varName[0:1] != '5'\
                and varName[0:1] != '6'\
                and varName[0:1] != '7'\
                and varName[0:1] != '8'\
                and varName[0:1] != '9':
                    self.save = True
                    color_list = []
                    color_list2 = []
                    for row in self.colors:
                        color_table = []
                        for color in row:
                            color_table.append("{" + ",".join(color) + "}")
                        color_list.append("\t{" + ",".join(color_table) + "}")
                        color_list2.append("-".join(color_table))
        
                    var = varName
                    colorData_fmt = var + "_data = {\n"
                    colorData_fmt += ",\n".join(color_list)
                    colorData_fmt += "\n}\n"

                    with open(var + ".bitmap", "w", encoding="UTF-8") as f:
                        f.write("\n".join(color_list2))

                    with open("bitmap_data.lua", "a", encoding="UTF-8") as f:
                        f.write(exportColorData(var, colorData_fmt))
        
                    if not os.path.isfile("bitmap_class.lua"):
                        with open("bitmap_class.lua", "w", encoding="UTF-8") as f:
                            f.write(exprotMinifyClass())

                    successed = QMessageBox()
                    successed.setText("【成功】輸出完成！   ")
                    successed.setStandardButtons(QMessageBox.Ok)
                    successed.setWindowTitle(QCoreApplication.translate("successed", u"SUCCESSED", None))
                    successed.setStyleSheet(u"font: 75 15pt NSimSun")
                    successed.setWindowIcon(QIcon("./icon/icon.png"))
                    successed = successed.exec()
                else:
                    error = QMessageBox()
                    error.setText("【錯誤】檔案名稱字首不能為數字！   ")
                    error.setStandardButtons(QMessageBox.Ok)
                    error.setWindowTitle(QCoreApplication.translate("error", u"ERROR", None))
                    error.setStyleSheet(u"font: 75 15pt NSimSun")
                    error.setWindowIcon(QIcon("./icon/icon.png"))
                    error = error.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())