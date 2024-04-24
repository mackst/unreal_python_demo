# -*- coding: utf-8 -*-

#
# 开启编辑菜单命令
# Cmd: ToolMenus.Edit 1
# 执行该命令后，编辑器菜单栏会显示，可以通过它来获取菜单栏路径
#


import unreal


def add_menu_to_main_menu():
    # 获取ToolMenus对象，用于管理编辑器菜单
    tool_menus = unreal.ToolMenus.get()

    # 获取编辑器菜单栏
    # main_menu_path = "MainFrame.MainMenu"  # 这是最顶层的菜单栏
    main_menu_path = "LevelEditor.MainMenu" # 这个和上面的差不多，多了Actor等菜单
    # main_menu_path = "LevelEditor.MainMenu.Window" # 你还可以指定到某个菜单栏
    main_menu = tool_menus.find_menu(main_menu_path)
    
    # 检查菜单栏是否存在
    # 5.3.2 版本，无法找到，一直返回None
    # 具体创建菜单可以看下面的
    # add_menu_to_ContentBrowser_context_menu
    if not main_menu:
        unreal.log_error("Cannot find the main menu")
        return
    
    section_name = "MyMenu"

    # 创建一个子菜单
    sub_menu = main_menu.add_sub_menu(main_menu.get_name(), section_name, "My Menus", "My Tools", "My Custom Menus")

    menu_section_name_1 = "MyMenu1"
    # 华丽的分界线
    sub_menu.add_section(
        menu_section_name_1,
        "华丽的分界线",
        insert_type=unreal.ToolMenuInsertType.FIRST
    )

    # 菜单
    menu_entry_1 = unreal.ToolMenuEntry(
        name="Tool1",
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert(menu_section_name_1)#, unreal.ToolMenuInsertType.FIRST)
    )

    menu_entry_1.set_label("My Custom Tool Menu 1")
    menu_entry_1.set_tool_tip("My Custom Tool Menu 1 Tool Tip")
    # 菜单要执行的py命令
    menu_entry_1.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '', 'unreal.log("My Custom Tool Menu 1")')

    sub_menu.add_menu_entry(menu_section_name_1, menu_entry_1)

    # 华丽的分界线
    menu_section_name_2 = "MyMenu2"
    sub_menu.add_section(
        menu_section_name_2,
        "华丽的分界线 2",
        insert_type=unreal.ToolMenuInsertType.FIRST
    )

    # 菜单
    menu_entry_2 = unreal.ToolMenuEntry(
        name="Tool2",
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert(menu_section_name_2)#, unreal.ToolMenuInsertType.FIRST)
    )

    menu_entry_2.set_label("My Custom Tool Menu 2")
    menu_entry_2.set_tool_tip("My Custom Tool Menu 2 Tool Tip")
    # 菜单要执行的py命令
    menu_entry_2.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '', 'unreal.log("My Custom Tool Menu 2")')

    sub_menu.add_menu_entry(menu_section_name_2, menu_entry_2)

    tool_menus.refresh_all_widgets()


def add_menu_to_ContentBrowser_context_menu():
    # 获取ToolMenus对象，用于管理编辑器菜单
    tool_menus = unreal.ToolMenus.get()

    # 获取编辑器菜单栏
    # 这是ContentBrowser左边显示文件夹层级结构的右键菜单
    # 以及选择文件夹时的右键菜单
    folder_menu_path = "ContentBrowser.FolderContextMenu"
    # 这是ContentBrowser右边显示文件夹和资产的右键菜单
    addNew_menu_path = "ContentBrowser.AddNewContextMenu"
    # 还有资产右键菜单 ContentBrowser.AssetContextMenu.[资产类型]

    folder_menu = tool_menus.find_menu(folder_menu_path)

    my_menu_separator_name = "MyMenuSeparator"
    my_menu_separator_display_name = "My Menus"
    my_menu_section = "MyMenuSection"

    # 检查菜单栏是否存在
    if folder_menu:

        # 创建新的分界线
        # 分界线是section，添加菜单时也需要提供section_name
        folder_menu.add_section(
            section_name=my_menu_section,
            label=my_menu_separator_name,
            # insert_name='test_test',

            # insert_type是unreal.ToolMenuInsertType.FIRST的话
            # 会在最前面插入，循序是从上到下的，所以菜单会在最上方
            insert_type=unreal.ToolMenuInsertType.DEFAULT
        )

        # 添加一个菜单项
        my_folder_menu_entry = unreal.ToolMenuEntry(
            name="MyFolderMenu",
            type=unreal.MultiBlockType.MENU_ENTRY,
            insert_position=unreal.ToolMenuInsert(my_menu_separator_name, unreal.ToolMenuInsertType.FIRST)
        )

        my_folder_menu_entry.set_label("My Custom Folder Menu")
        my_folder_menu_entry.set_tool_tip("My Custom Folder Menu Tool Tip")
        # 菜单要执行的py命令
        my_folder_menu_entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '', 'unreal.log("My Custom Folder Menu")')

        my_folder_menu = folder_menu.add_sub_menu(folder_menu.get_name(), my_menu_section, "MyFolderMenu", "My Custom Folder Menu 2")
        my_folder_menu.add_menu_entry(my_menu_section, my_folder_menu_entry)



    tool_menus.refresh_all_widgets()


def add_tool_to_user_toolbar():
    # 获取ToolMenus对象，用于管理编辑器菜单
    tool_menus = unreal.ToolMenus.get()

    # ToolBar其实也是ToolMenu，所以需要路径
    folder_menu_path = "LevelEditor.LevelEditorToolBar.User"
    
    user_toolbar = tool_menus.find_menu(folder_menu_path)

    if not user_toolbar:
        unreal.log_error("Cannot find the user toolbar")
        return
    
    section1 = "MyToolbarSection1"
    section1_name = "My Toolbar Section Name 1"

    user_toolbar.add_section(
        section_name=section1,
        label=section1_name
    )

    # 和菜单一样，但需要使用
    # unreal.MultiBlockType.TOOL_BAR_BUTTON
    # 添加一个按钮
    my_tool_entry1 = unreal.ToolMenuEntry(
        name="MyToolbarEntry1",
        type=unreal.MultiBlockType.TOOL_BAR_BUTTON,
        insert_position=unreal.ToolMenuInsert(section1, unreal.ToolMenuInsertType.FIRST)
    )

    my_tool_entry1.set_label("My Custom Tool 1")
    my_tool_entry1.set_tool_tip("My Custom Tool 1 Tool Tip")
    my_tool_entry1.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '', 'unreal.log("My Custom Tool 1")')

    user_toolbar.add_menu_entry(section1, my_tool_entry1)

    section2 = "MyToolbarSection2"
    section2_name = "My Toolbar Section Name 2"
    section2_entry_name = "MyToolbarEntry2"

    user_toolbar.add_section(
        section_name=section2,
        label=section2_name
    )

    # 使用
    # unreal.MultiBlockType.TOOL_BAR_COMBO_BUTTON
    # 添加一个下拉菜单的组合按钮
    my_tool_entry2 = unreal.ToolMenuEntry(
        name=section2_entry_name,
        type=unreal.MultiBlockType.TOOL_BAR_COMBO_BUTTON,
        insert_position=unreal.ToolMenuInsert(section2, unreal.ToolMenuInsertType.FIRST)
    )

    # 图标
    # 内置图标
    # https://github.com/EpicKiwi/unreal-engine-editor-icons
    # 样式
    # https://docs.unrealengine.com/4.26/en-US/API/Editor/EditorStyle/
    my_tool_entry2.set_icon("EditorStyle", "Editor.AppIcon")

    my_tool_entry2.set_label("My Custom Tool 2")
    my_tool_entry2.set_tool_tip("My Custom Tool 2 Tool Tip")
    my_tool_entry2.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '', 'unreal.log("My Custom Tool 2")')

    user_toolbar.add_menu_entry(section2, my_tool_entry2)

    # 需要继续添加子菜单则跟菜单添加一样
    section2_menu_path = folder_menu_path + "." + section2_entry_name
    section2_menu = tool_menus.find_menu(section2_menu_path)

    if section2_menu:
        my_tool_entry2 = unreal.ToolMenuEntry(
            name="MyToolbarEntry2_1",
            type=unreal.MultiBlockType.MENU_ENTRY,
            insert_position=unreal.ToolMenuInsert(section2, unreal.ToolMenuInsertType.FIRST)
        )

        my_tool_entry2.set_label("My Custom Tool 2_1")
        my_tool_entry2.set_tool_tip("My Custom Tool 2_1 Tool Tip")
        my_tool_entry2.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '', 'unreal.log("My Custom Tool 2_1")')

        section2_menu.add_menu_entry(section2, my_tool_entry2)

    tool_menus.refresh_all_widgets()



add_menu_to_main_menu()
add_menu_to_ContentBrowser_context_menu()
add_tool_to_user_toolbar()


