import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw


class CustomSpinBox(qw.QLineEdit):
    int_spinbox = 0
    double_spinbox = 1

    def __init__(self, spinbox_type, value=0):
        super(CustomSpinBox, self).__init__()

        if spinbox_type == CustomSpinBox.int_spinbox:
            self.setValidator(qg.QIntValidator(parent=self))
        else:
            self.setValidator(qg.QDoubleValidator(parent=self))
        self.spinbox_type = spinbox_type
        self.min = None
        self.max = None
        self.steps = 1
        self.value_at_press = None
        self.pos_at_press = None

        self.setMinimumWidth(100)
        self.setMaximumWidth(100)

        self.set_value(value)

    def wheelEvent(self, event):
        super(CustomSpinBox, self).wheelEvent(event)
        steps_mult = self.get_steps_multiplier(event)
        if event.delta() > 0:
            self.set_value(self.value() + self.steps * steps_mult)
        else:
            self.set_value(self.value() - self.steps * steps_mult)

    def mousePressEvent(self, event):
        if event.buttons() == qc.Qt.MiddleButton:
            self.value_at_press = self.value()
            self.pos_at_press = event.pos()
            self.setCursor(qg.QCursor(qc.Qt.SizeHorCursor))
        else:
            super(CustomSpinBox, self).mousePressEvent(event)
            self.selectAll()

    def mouseReleaseEvent(self, event):
        if event.buttons() == qc.Qt.MiddleButton:
            self.value_at_press = None
            self.pos_at_press = None
            self.setCursor(qg.QCursor(qc.Qt.IBeamCursor))
            return
        super(CustomSpinBox, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() != qc.Qt.MiddleButton:
            return
        if self.pos_at_press is None:
            return
        steps_mult = self.get_steps_multiplier(event)

        delta = event.pos().x() - self.pos_at_press.x()
        delta /= 6
        delta *= self.steps * steps_mult

        value = self.value_at_press + delta
        self.set_value(value)

        super(CustomSpinBox, self).mouseMoveEvent(event)

    def get_steps_multiplier(self, event):
        steps_mult = 1

        if event.modifiers() == qc.Qt.CTRL:
            steps_mult = 10

        elif event.modifiers() == qc.Qt.SHIFT:
            steps_mult = 0.1

        return steps_mult

    def set_minimum(self, value):
        self.min = value

    def set_maximum(self, value):
        self.max = value

    def set_steps(self, steps):
        if self.spinbox_type == CustomSpinBox.int_spinbox:
            self.steps = max(steps, 1)
        else:
            self.steps = steps

    def value(self):
        if self.spinbox_type == CustomSpinBox.int_spinbox:
            return int(self.text())
        else:
            return float(self.text())

    def set_value(self, value):
        if self.min is not None:
            value = max(value, self.min)
        if self.max is not None:
            value = min(value, self.max)
        if self.spinbox_type == CustomSpinBox.int_spinbox:
            self.setText(str(int(value)))
        else:
            self.setText(str(float(value)))
