import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QComboBox,QCheckBox,QFileDialog,QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt,QDir
import image_compressor


class App(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.title = 'Image Compressor'
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 600
        self.setFixedSize(self.width, self.height)
        self.setObjectName("main_window")
        #var
        self.is_multiple = True

        stylesheet = ""
        with open("src/design.css", "r") as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        main_panel = self.create_frame(self,"main_panel",10,10)
        #input panel
        self.create_panel_1(main_panel,"Choose Images path", 10, 10)
        #output panel
        self.create_panel_2(main_panel,"Choose Output path", 10, 110)
        #panel_3
        self.create_panel_3(main_panel,10,220)
        #panel_4
        self.create_panel_4(main_panel,"Image Adjustment",10,360)
        #panel_5
        self.tiny_panel = self.create_panel_5(main_panel,10,460)
        if image_compressor.scale_type == image_compressor.ScaleType.ODD_SCALE:
            self.tiny_panel.hide()
        #compress button
        self.compress_button = self.create_button(main_panel,"compress_button","Compress",90, 520)
        self.compress_button.clicked.connect(self.compress_button_clicked)
        self.show()

    def compress_button_clicked(self):
        image_compressor.source_dir = self.input_path.text()
        image_compressor.destination_dir = self.output_path.text()
        if self.width_input.text():
            image_compressor.width_x = int(self.width_input.text())
        else:
            image_compressor.width_x  = 0
        if self.hieght_input.text():
            image_compressor.height_x = int(self.hieght_input.text())
        else:
            image_compressor.height_x = 0
        image_compressor.use_tinify = self.tiny_check.isChecked()
        if self.tiny_check.isChecked():
            image_compressor.tinify_key = self.tiny_key.text()
        else:
            image_compressor.tinify_key = ''
        image_compressor.contrast_value = float(self.contrast_value.text())
        image_compressor.sharpness_value = float(self.sharpness_value.text())
        if not image_compressor.source_dir:
            self.show_dialog_box('source path is required!', 'please add source path.')
        elif not os.path.exists(image_compressor.source_dir):
            self.show_dialog_box('source path is invalid!', 'please add correct source path.')
        elif not image_compressor.destination_dir:
            self.show_dialog_box('output path is required!', 'please add output path.')
        elif not os.path.exists(image_compressor.destination_dir):
            self.show_dialog_box('output path is invalid!', 'please add correct output path.')
            
        elif image_compressor.width_x <= 0:
            self.show_dialog_box('Width is required!', 'please add width value.')
        elif image_compressor.scale_type == image_compressor.ScaleType.ODD_SCALE:
            if image_compressor.height_x <= 0:
                self.show_dialog_box('Height is required!', 'please add Height value.')
            else:
                print('ODD scale')
                self.run_compress()
        elif self.tiny_check.isChecked():
            if not image_compressor.tinify_key:
                self.show_dialog_box('Tinify Key is required!', 'please get Key from https://tinypng.com/developers')
            else:
                print('tini checked')
                self.run_compress()
        else:
            self.run_compress()
        
    def show_dialog_box(self, msg, additional_msg):
        msgbox = self.create_dialog_box()
        msgbox.setText(msg)
        msgbox.setInformativeText(additional_msg)
        msgbox.exec_()

    def create_dialog_box(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        # msg.setText('')
        # msg.setInformativeText("This is additional information")
        # msg.setWindowTitle("MessageBox demo")
        # msg.setDetailedText("The details are as follows:")     
        # retval = msg.exec_()
        # print ("value of pressed message box button:", retval)
        return msg
                
    def run_compress(self):
        print(image_compressor.source_dir ,
        image_compressor.destination_dir,
        image_compressor.image_type,
        image_compressor.scale_type,
        image_compressor.width_x ,
        image_compressor.height_x ,
        image_compressor.use_tinify ,
        image_compressor.tinify_key ,
        image_compressor.contrast_value,
        image_compressor.sharpness_value)

        image_compressor.compress_images(image_compressor.source_dir, image_compressor.destination_dir, image_compressor.width_x, image_compressor.height_x)

    def create_frame(self,parent,css_class,x,y):
        panel = QFrame(parent)
        panel.setObjectName(css_class)
        panel.move(x, y)
        return panel

    def create_label(self,parent,css_class,text,x,y):
        label = QLabel(parent)
        label.setObjectName(css_class)
        label.setText(text)
        label.move(x, y)
        return label

    def create_lineedit(self,parent,css_class,x,y):
        input_path = QLineEdit(parent)
        input_path.setObjectName(css_class)
        input_path.move(x, y)
        return input_path

    def create_button(self,parent,css_class,text,x,y):
        button = QPushButton(parent)
        button.setText(text)
        button.setObjectName(css_class)
        button.move(x, y)
        return button

    def create_combo_box(self,parent,css_class,types,x,y):
        cb = QComboBox(parent)
        cb.addItems(types)
        cb.move(x,y)
        # print(cb.currentText())
        return cb

    def create_checkbox(self,parent,css_class,x,y):
        check_box = QCheckBox(parent) 
        check_box.setObjectName(css_class)
        check_box.move(x, y)
        return check_box
     
    def create_panel_1(self,parent,text,x,y):
        frame = self.create_frame(parent,"input_panel",x,y)
        self.input_label = self.create_label(frame,"text",text,30, 20)
        self.input_path = self.create_lineedit(frame,"src_path",30, 45)
        self.input_path_button = self.create_button(frame,"browse_button","...",280, 39)

        #multiple?
        self.create_label(frame,"src_path","Multiple?",260, 20)
        self.check_box_multiple = self.create_checkbox(frame,"src_path_dummy",320, 20)

        if self.is_multiple is True:
            self.check_box_multiple.setChecked(True)

        if self.check_box_multiple.isChecked() is True:
            self.input_path_button.clicked.connect(self.browse_input)
        else:
            self.input_path_button.clicked.connect(self.browse_for_file)
         
        # print(" check status: ",self.check_box_multiple.isChecked() )
        self.check_box_multiple.stateChanged.connect(self.is_checked_multiple)
        
    def is_checked_multiple(self):
        self.input_path.setText("")
        self.input_path_button.disconnect()
        if not self.check_box_multiple.isChecked():
            self.is_multiple = False
            self.input_label.setText("Choose Image path")
            self.input_path_button.clicked.connect(self.browse_for_file)
        else:
            self.is_multiple = True
            self.input_label.setText("Choose Images path")  
            self.input_path_button.clicked.connect(self.browse_input)
        # print("is_multiple: ",self.is_multiple)
       
    def create_panel_2(self,parent,text,x,y):
        frame = self.create_frame(parent,"input_panel",x,y)
        self.create_label(frame,"text",text,30, 20)
        self.output_path = self.create_lineedit(frame,"src_path",30, 45)
        self.output_path_button = self.create_button(frame,"browse_button","...",280, 39)
        self.output_path_button.clicked.connect(self.browse_output)

    def browse_input(self):
        self.input_path.setText(self.browse_for_folder())

    def browse_output(self):
        self.output_path.setText(self.browse_for_folder())

    def browse_for_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Find Files", QDir.currentPath())
        return directory    

    def browse_for_file(self):
        options = QFileDialog.Options() #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*.jpg *.png)",options=options)
        if fileName:
            self.input_path.setText(fileName)

    def create_panel_3(self,parent,x,y):
        frame = self.create_frame(parent,"panel_3",x,y)
        #Image Type
        self.create_label(frame,"src_path","Image Type",30, 20)
        self.imagetype_cbox = self.create_combo_box(frame,"src_path_dummy",["Png","Jpg"],25, 40)
        self.imagetype_cbox.currentIndexChanged.connect(self.change_imagetype)
        #Scale Type
        self.create_label(frame,"src_path","Scale Type",180, 20)
        self.scaletype_cbox = self.create_combo_box(frame,"src_path_dummy",["Even Scale","Odd Scale"],175, 40)
        self.scaletype_cbox.currentIndexChanged.connect(self.change_scaletype)
        #Width
        self.create_label(frame,"src_path","Width",30, 80)
        self.width_input = self.create_lineedit(frame,"src_path_dummy",80, 80)
        onlyInt = QIntValidator()
        self.width_input.setValidator(onlyInt)
        self.width_input.setText('563')
        #height
        self.hieght_lebal = self.create_label(frame,"src_path","Height",180, 80)
        self.hieght_input = self.create_lineedit(frame,"src_path_dummy",250, 80)
        self.hieght_input.setValidator(onlyInt)
        self.hieght_input.setText('317')
        self.hieght_lebal.hide()
        self.hieght_input.hide()

    def change_imagetype(self,i):
        # print ("Current index",i,"selection changed ",self.imagetype_cbox.currentText())
        if self.imagetype_cbox.currentText() == 'Png':
            image_compressor.image_type = image_compressor.ImageType.PNG
        if self.imagetype_cbox.currentText() == 'Jpg':
            image_compressor.image_type = image_compressor.ImageType.JPG

    def change_scaletype(self,i):
        # print ("Current index",i,"selection changed ",self.scaletype_cbox.currentText())
        if self.scaletype_cbox.currentText() == 'Even Scale':
            image_compressor.scale_type = image_compressor.ScaleType.EVEN_SCALE
            self.hieght_lebal.hide()
            self.hieght_input.hide()
            self.tiny_panel.show()
        if self.scaletype_cbox.currentText() == 'Odd Scale':
            image_compressor.scale_type = image_compressor.ScaleType.ODD_SCALE
            self.hieght_lebal.show()
            self.hieght_input.show()
            self.tiny_panel.hide()

    def create_panel_4(self,parent,text,x,y):
        frame = self.create_frame(parent,"panel_5",x,y)
        self.create_label(frame,"text",text,30, 20)
        #Contrast
        self.create_label(frame,"src_path","Contrast",30, 50)
        self.contrast_value = self.create_lineedit(frame,"src_path_dummy",100, 50)
        self.contrast_value.setText('1.2')
        onlyFloat = QDoubleValidator(0,10, 2, self)
        self.contrast_value.setValidator(onlyFloat)
        #Sharpness
        self.create_label(frame,"src_path","Sharpness",200, 50)
        self.sharpness_value = self.create_lineedit(frame,"src_path_dummy",280, 50)
        self.sharpness_value.setText('2')
        self.sharpness_value.setValidator(onlyFloat)
    
    def create_panel_5(self,parent,x,y):
        frame = self.create_frame(parent,"panel_4",x,y)   
        #Use Tinypng?
        self.create_label(frame,"src_path","Use Tinypng?",30, 10)
        self.tiny_check = self.create_checkbox(frame,"src_path_dummy",120, 10)
        #Key
        self.create_label(frame,"src_path","Key",160, 10)
        self.tiny_key = self.create_lineedit(frame,"key",190, 10)
        return frame


if __name__ == '__main__':
    os.environ['QT_MAC_WANTS_LAYER'] = '1'
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())