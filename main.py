from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QSettings, QCoreApplication, QRect
from PySide6.QtGui import QScreen
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os


# 准备模板图片和字体
template_image_path = "注册页面.png"
font_path = "等线.ttf"
image = Image.open(template_image_path)

# 获取原图片的文件扩展名
original_extension = os.path.splitext(template_image_path)[1]

# 创建一个透明的文本框并填充文本的函数
def create_text_box(image, text, position, font_path, font_size):
    drawing = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    drawing.text(position, text, fill=(0,0,0), font=font)
    return image

class FormWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("MyCompany", "MyApp")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('填写信息')
        self.layout = QVBoxLayout()

        # 创建文件路径及浏览按钮的水平布局
        path_layout = QHBoxLayout()
        self.layout.addLayout(path_layout)  # 将这个水平布局添加到主垂直布局中

        # 在这个水平布局中放置标签、文本框和浏览按钮
        path_layout.addWidget(QLabel("保存路径："))
        self.path_edit = QLineEdit(self.settings.value("lastPath", ""))
        path_layout.addWidget(self.path_edit)
        browse_button = QPushButton('浏览...')
        browse_button.clicked.connect(self.on_browse)
        path_layout.addWidget(browse_button)

        # 文本位置预设
        self.text_positions = [
            ("账号：", (465, 248), 20),
            ("密码：", (465, 285), 20),
            ("确认密码：", (465, 322), 20),
            ("姓名：", (465, 359), 20),
            ("邮箱：", (465, 396), 20),
            ("手机：", (580, 432), 20),
            ("电话：", (465, 470), 20),
            ("留言：", (465, 506), 20),
            # 根据需要添加更多
        ]

        self.inputs = []
        for prompt, _, _ in self.text_positions:
            self.layout.addWidget(QLabel(prompt))
            line_edit = QLineEdit()
            self.layout.addWidget(line_edit)
            self.inputs.append(line_edit)

        submit_button = QPushButton('提交')
        submit_button.clicked.connect(self.on_submit)
        self.layout.addWidget(submit_button)
        self.setLayout(self.layout)

        self.adjustSize()
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        width = screen.width() // 3
        height = self.height()
        self.setGeometry(QRect(screen.width() // 2 - width // 2, screen.height() // 2 - height // 2, width, height))

    def on_browse(self):
        directory = QFileDialog.getExistingDirectory(self, "选择保存路径", self.path_edit.text())
        if directory:
            self.path_edit.setText(directory)

    def on_submit(self):
        save_path = self.path_edit.text()
        if save_path:
            self.settings.setValue("lastPath", save_path)
            for i, (_, position, font_size) in enumerate(self.text_positions):
                user_input_text = self.inputs[i].text()
                if user_input_text:
                    create_text_box(image, user_input_text, position, font_path, font_size)

            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            output_image_path = f"{save_path}/{current_time}{original_extension}"
            image.save(output_image_path)
            QMessageBox.information(self, "保存成功", f"图片已保存至：{output_image_path}")
            self.close()
        else:
            QMessageBox.warning(self, "保存失败", "未指定保存路径。")

if __name__ == '__main__':
    QCoreApplication.setOrganizationName("MyCompany")
    QCoreApplication.setApplicationName("MyApp")
    app = QApplication([])
    window = FormWindow()
    window.show()
    app.exec()
