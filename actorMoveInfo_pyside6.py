# -*- coding: utf-8 -*-

import inspect
import os
import site
import sys

import unreal

# 把site-packages加入到python路径中
spp = site.getsitepackages()

if spp:
    _p = os.path.abspath(spp[0])
    if _p not in sys.path:
        sys.path.append(_p)
        unreal.log(f"add site path: {_p}")


from PySide6 import QtWidgets, QtUiTools


# 独属于我们自己的编辑器类
@unreal.uclass()
class MyEditorUtility(unreal.GlobalEditorUtilityBase):
    pass


class TestWidget(QtWidgets.QWidget):
    # 注册的句柄，窗口关闭时，需要取消注册
    # 尽量不要使用类变量，因为类变量会在类加载时初始化，
    # unreal执行.py时类似会做reload()一样的操作
    # 就会导致类变量重新初始化
    # __TickHandle = None
    
    # QUiLoader必须在QtWidgets.QApplication实例化前初始化
    # 不然会卡死unreal编辑器
    UILoader = QtUiTools.QUiLoader()

    # 这段代码是为了防止重复创建，让我们的窗口只会创建一个
    # 无论这个脚本被执行了多少遍
    def __new__(cls, *args, **kwargs):
        tlws = QtWidgets.QApplication.instance().topLevelWidgets()
        for tlw in tlws:
            if tlw.__class__.__name__ == cls.__name__:
                unreal.log_warning(f"{cls.__name__} instance already exists!")
                return tlw
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, parent=None):
        super().__init__(parent)
            
        self.setWindowTitle("Test Widget")
        
        dirPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        uiPath = os.path.join(dirPath, "actorMoveInfo.ui")
        self.widget = self.UILoader.load(uiPath)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.widget)
        self.setLayout(layout)

        # 注册一个tick回调
        self.__TickHandle = unreal.register_slate_post_tick_callback(self.update)
        self.editor = MyEditorUtility()

    def update(self, delta_seconds):
        if not self.editor: return
        selActors = self.editor.get_selection_set()
        if selActors:
            actor: unreal.Actor = selActors[0]
            self.widget.itemNameLabel.setText(actor.get_name())
            translate = actor.get_actor_location()
            self.widget.xLabel.setText(str(translate.x))
            self.widget.yLabel.setText(str(translate.y))
            self.widget.zLabel.setText(str(translate.z))
    def closeEvent(self, event):
        if self.__TickHandle:
            # 取消注册
            unreal.unregister_slate_post_tick_callback(self.__TickHandle)
            self.__TickHandle = None

        super().closeEvent(event)

    def show(self) -> None:
        super().show()
        # 把窗口整合到编辑器中，注意必须先调用show方法winId才有效
        unreal.parent_external_window_to_slate(self.winId())


# Qt 必须要一个应用程序实例
# 这中写法是为了多次运行不会报错，应用程序实例只能创建一次
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)


label = TestWidget()
label.show()


