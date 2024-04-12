# -*- coding: utf-8 -*-



import pathlib
import inspect

import unreal

'''
USD 资产可以去官方下载
'''


def importFBXDemo():
    dir_path = pathlib.Path(inspect.getfile(inspect.currentframe())).parent.absolute()
    cube_fbx = dir_path.joinpath('assets', 'cube.fbx')

    if not cube_fbx.exists():
        unreal.log_error('cube.fbx not found')
        return
    
    content_path = "/Game/Assets/cube"

    assetTools = unreal.AssetToolsHelpers.get_asset_tools()

    # 使用automated导入，无导入设置窗口
    importData = unreal.AutomatedAssetImportData()
    importData.destination_path = content_path
    importData.replace_existing = True
    importData.filenames = [str(cube_fbx)]
    assets = assetTools.import_assets_automated(importData)

    # unreal.log(assets)

    # 重命名
    # renameData = unreal.AssetRenameData(assets[0], content_path, 'the_cube')
    # asset_new_names = unreal.Array(unreal.AssetRenameData)
    # asset_new_names.append(renameData)

    # assetTools.rename_assets(asset_new_names)

    # 在编辑器中打开导入的资产
    # assetTools.open_editor_for_assets(assets)


def importUsdDemo():
    dir_path = pathlib.Path(inspect.getfile(inspect.currentframe())).parent.absolute()
    usd_path = dir_path.joinpath('assets', 'UsdSkelExamples', 'HumanFemale', 'HumanFemale.walk.usd')

    if not usd_path.exists():
        unreal.log_error('UsdSkelExamples not found')
        return
    
    content_path = "/Game/Assets/usd"

    try:
        usd_factory = unreal.UsdStageImportFactory()
    except:
        unreal.EditorDialog.show_message(
            'USD Importer plugin',
            'Plugin not loaded, load it and retry.',
            unreal.AppMsgType.OK
        )
        return

    # 使用task导入
    # 这会打开导入设置窗口，需要手动点导入才完成
    task = unreal.AssetImportTask()
    task.set_editor_property('filename', str(usd_path))
    task.set_editor_property('destination_path', content_path)
    usd_factory.asset_import_task = task

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

    # 使用automated导入，无导入设置窗口
    # importData = unreal.AutomatedAssetImportData()
    # importData.destination_path = content_path
    # importData.replace_existing = True
    # importData.filenames = [str(usd_path)]
    # assets = unreal.AssetToolsHelpers.get_asset_tools().import_assets_automated(importData)


importFBXDemo()
importUsdDemo()

