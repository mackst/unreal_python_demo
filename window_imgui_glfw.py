# -*- coding: utf-8 -*-


#
# 能运行也能显示界面，不能使用while循环来进入界面循环，会导致unreal编辑器无法操作
# 需要通过unreal.register_slate_post_tick_callback来注册一个回调函数，
# 在回调函数中调用绘制界面的函数
# 

import os
import site
import sys


# 把site-packages加入到python路径中
spp = site.getsitepackages()

if spp:
    _p = os.path.abspath(spp[0])
    if _p not in sys.path:
        sys.path.append(_p)
        unreal.log(f"add site path: {_p}")

from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
import glfw
import imgui

import unreal


# 独属于我们自己的编辑器类
@unreal.uclass()
class MyEditorUtility(unreal.GlobalEditorUtilityBase):
    pass


class Demo(object):

    def __init__(self) -> None:
        width, height = 1280, 720
        window_name = "minimal ImGui/GLFW3 example"

        if not glfw.init():
            # pass
            unreal.log_error("Could not initialize OpenGL context")

        # OS X supports only forward-compatible core profiles from 3.2
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(int(width), int(height), window_name, None, None)
        glfw.make_context_current(self.window)

        if not self.window:
            glfw.terminate()
            unreal.log_error("Could not initialize Window")

        glfw.set_window_close_callback(self.window, self.destory)

        self.editor = MyEditorUtility()


    def destory(self, window):
        unreal.log("destory window")
        unreal.unregister_slate_post_tick_callback(self.__TickHandle)
        self.__TickHandle = None

        glfw.destroy_window(window)

        # 如果调用imgui shutdown会导致第二次运行时，imgui报错而无法显示界面
        # 也无法关闭glfw窗口
        # self.impl.shutdown()
        # 如果调用，工具第二次运行时出错
        # 如果有多个glfw窗口同时运行，会导致所有窗口都关闭
        # 而且不会触发窗口的关闭事件，导致注册的slate_post_tick_callback
        # 无法反注册，导致输出日志界面无限循环python错误信息
        # glfw.terminate()

    # demo window显示当前关卡选择actor的名字和位移信息
    def actor_move_info_window(self):
        actor_name = 'No selection'
        tx = '0'
        ty = '0'
        tz = '0'
        if self.editor:
            selActors = self.editor.get_selection_set()
            if selActors:
                actor = selActors[0]
                actor_name = actor.get_name()
                translate = actor.get_actor_location()
                tx = str(translate.x)
                ty = str(translate.y)
                tz = str(translate.z)
        
        is_expand, show_window = imgui.begin("Actor Move Info", True)
        if is_expand:
            imgui.text_colored(text=actor_name, r=1.0, g=1.0, b=0.0, a=1.0)
            imgui.text('x : ')
            imgui.same_line()
            imgui.text_colored(text=tx, r=1.0, g=0.0, b=0.0, a=1.0)
            imgui.text('y : ')
            imgui.same_line()
            imgui.text_colored(text=ty, r=0.0, g=1.0, b=0.0, a=1.0)
            imgui.text('z : ')
            imgui.same_line()
            imgui.text_colored(text=tz, r=0.0, g=0.0, b=1.0, a=1.0)
        imgui.end()

    # 显示窗口
    def run (self):
        # 把glfw窗口和unreal关联
        hwnd = glfw.get_win32_window(self.window)
        unreal.parent_external_window_to_slate(hwnd)

        # 创建imgui上下文和后端渲染器
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        # 注册一个回调函数，在回调函数中调用绘制界面
        self.__TickHandle = unreal.register_slate_post_tick_callback(self._run)

    # 这实际就是正常imgui和glfw的 while 循环
    def _run(self, delta_seconds):
        if glfw.window_should_close(self.window):
            return
        
        show_custom_window = True

        glfw.poll_events()
        self.impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                # 可以有菜单栏但不要向这样设计关闭窗口，我的测试是
                # 窗口可以关闭但，第二次运行时，glfw窗口会显示但imgui无法绘制界面
                # 或是窗口会显示但无法关闭，需要重启unreal编辑器
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                # if clicked_quit:
                #     print('quit clicked......')
                #     glfw.set_window_should_close(self.window, True)
                #     # glfw.destroy_window(self.window)
                #     # self.destory(self.window)
                #     return

                imgui.end_menu()
            imgui.end_main_menu_bar()

        if show_custom_window:
            is_expand, show_custom_window = imgui.begin("Custom window", True)
            if is_expand:
                imgui.text("Bar")
                imgui.text_ansi("B\033[31marA\033[mnsi ")
                imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1.0, 0.0)
                imgui.extra.text_ansi_colored("Eggs", 0.2, 1.0, 0.0)
            imgui.end()

        imgui.show_demo_window()
        self.actor_move_info_window()

        gl.glClearColor(1.0, 1.0, 1.0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        self.impl.render(imgui.get_draw_data())
        glfw.swap_buffers(self.window)



if __name__ == "__main__":
    demo = Demo()
    demo.run()

