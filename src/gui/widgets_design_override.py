"""
Модуль отвечает за изменение методов отрисовки у виджетов. 

Поскольку дизайнер переписывает код окон,
нам будет необходимо при каждом изменении дизайна
запускать "[debug] quick_gui_override.py".
"""

from PyQt5 import QtCore, QtGui, QtWidgets

from genetic.point import Point


class Colors:
    background = QtGui.QColor(255, 255, 255)
    graph_node = QtGui.QColor(0, 0, 0)


class PlainBackground(QtWidgets.QWidget): 
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()
      
    def drawWidget(self, qp):
        size = self.size()

        w = size.width()
        h = size.height()

        qp.setPen(Colors.background)
        qp.setBrush(Colors.background)
        qp.drawRect(0, 0, w, h)


class GraphWidget(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def mousePressEvent(self, event):
        left_mouse_button = 1
        if event.button() != left_mouse_button:
            return
        
        x = event.localPos().x()# / self.size().width()
        y = event.localPos().y()# / self.size().height()

        self.add_point(Point(x, y))
      
    def drawWidget(self, qp):
        size = self.size()

        w = size.width()
        h = size.height()

        qp.save()

        qp.setBrush(Colors.background)
        qp.drawRect(0, 0, w, h)

        qp.setBrush(Colors.graph_node)
        qp.setPen(Colors.graph_node)

        radius = 2
        for point in self.genetic_master.points:
            center_x = point.x# * w
            center_y = point.y# * h
            qp.drawEllipse(
                center_x - radius,
                center_y - radius,
                radius*2,
                radius*2
            )
        
        for i, point_a in enumerate(self.genetic_master.super_genome):
            point_b = self.genetic_master.super_genome[(i + 1) % len(self.genetic_master.super_genome)]
            qp.drawLine(point_a.x * w, point_a.y * h, point_b.x * w, point_b.y * h)

        qp.restore()

    def add_point(self, point: Point):
        self.genetic_master.points.append(point)
        self.update_graph()
    
    def update_graph(self):
        self.repaint()

class ButtonOverride(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.hovered = False

    def event(self, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            self.hovered = True
        if event.type() == QtCore.QEvent.HoverLeave:
            self.hovered = False
        return super().event(event)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()
        full_rect = QtCore.QRect(0, 0, w, h)
        margin_size = 4
        margins = QtCore.QMargins(
            *([margin_size]*4)
        )
        rect = full_rect.marginsRemoved(margins)
        qp.save()

        border_color, background_color = None, None

        icon_state = QtGui.QIcon.Off

        if self.hovered and not self.isDown():
            border_color = Colors.primary
            background_color = Colors.highlighted
            icon_state = QtGui.QIcon.On
        elif self.isDown() or self.isChecked():
            border_color = Colors.primary
            background_color = Colors.secondary
            icon_state = QtGui.QIcon.On
        elif not self.isFlat():
            border_color = Colors.secondary
            background_color = Colors.primary

        if border_color and background_color:
            pen = QtGui.QPen(border_color)
            pen.setWidth(2)
            brush = QtGui.QBrush(background_color)

            qp.setPen(pen)

            qp.setBrush(brush)
            qp.drawRect(full_rect)

        icon_rect = QtCore.QRect()

        icon = self.icon()
        text = self.text()

        if not icon.isNull():
            icon_rect = QtCore.QRect(rect)
            h = rect.height()
            icon_rect.setWidth(icon_rect.height())
            if not text:
                icon_rect.moveCenter(rect.center())
            pixmap = icon.pixmap(h, h, QtGui.QIcon.Normal, icon_state)
            qp.drawPixmap(
                icon_rect,
                pixmap,
                pixmap.rect()
                )

        if text:
            text_rect = QtCore.QRect(rect)
            text_rect.setLeft(icon_rect.right() + margin_size)
            qp.setFont(self.font())
            qp.setPen(Colors.font)
            qp.drawText(text_rect, QtCore.Qt.AlignLeft, text)

        qp.restore()
