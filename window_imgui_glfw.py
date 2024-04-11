# -*- coding: utf-8 -*-


#
# 能运行也能显示界面，但会卡在界面的while循环
# 而导致unreal编辑器无法操作
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

        hwnd = glfw.get_win32_window(self.window)
        unreal.parent_external_window_to_slate(hwnd)

    def destory(self, window):
        self.impl.shutdown()
        glfw.terminate()
    def run(self):
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        show_custom_window = True

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()

            imgui.new_frame()

            if imgui.begin_main_menu_bar():
                if imgui.begin_menu("File", True):

                    clicked_quit, selected_quit = imgui.menu_item(
                        "Quit", "Cmd+Q", False, True
                    )

                    if clicked_quit:
                        glfw.set_window_should_close(self.window, True)

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

            gl.glClearColor(1.0, 1.0, 1.0, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)



if __name__ == "__main__":
    demo = Demo()
    demo.run()
