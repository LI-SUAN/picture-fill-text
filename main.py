from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QSettings, QCoreApplication, QRect
from PySide6.QtGui import QScreen
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# 准备模板图片和字体
template_image_path = "注册页面.png"
font_path = "等线.ttf"
image = Image.open(template_image_path)

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

    def initUI(self):  # 这里将initUI定义移到了__init__方法的外部
        self.setWindowTitle('填写信息')
        self.layout = QVBoxLayout()

        # 文本位置预设
        self.text_positions = [
            ("账号：", (465, 250), 20),
            ("密码：", (465, 285), 20),
            ("姓名：", (465, 360), 20),
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

        # 调整窗口大小和位置
        self.adjustSize()  # 调整窗口大小以适应内容
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        width = screen.width() // 3
        height = self.height()  # 获取调整后的窗口高度
        self.setGeometry(QRect(screen.width() // 2 - width // 2, screen.height() // 2 - height // 2, width, height))

    def on_submit(self):
        last_path = self.settings.value("lastPath", "")
        save_path = QFileDialog.getExistingDirectory(self, "选择保存路径", last_path)

        if save_path:
            self.settings.setValue("lastPath", save_path)
            for i, (_, position, font_size) in enumerate(self.text_positions):
                user_input_text = self.inputs[i].text()
                if user_input_text:  # 如果用户输入了文本
                    create_text_box(image, user_input_text, position, font_path, font_size)

            # 获取当前时间并格式化为YYYYMMDDHHmmss的格式
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            # 使用格式化的时间作为文件名保存图片
            output_image_path = f"{save_path}/{current_time}.png"
            image.save(output_image_path)
            QMessageBox.information(self, "保存成功", f"图片已保存至：{output_image_path}")
            self.close()
        else:
            QMessageBox.warning(self, "保存失败", "未选择保存路径。")

if __name__ == '__main__':
    QCoreApplication.setOrganizationName("MyCompany")
    QCoreApplication.setApplicationName("MyApp")
    app = QApplication([])
    window = FormWindow()
    window.show()
    app.exec()
