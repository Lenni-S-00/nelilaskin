import sys
from PySide6.QtWidgets import QApplication
import laskinfrontend

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ikkuna = laskinfrontend.Laskin()
    ikkuna.resize(300, 300)

    ikkuna.show()

    sys.exit(app.exec())