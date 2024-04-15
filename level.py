# -*- coding: utf-8 -*-

import unreal


# # 加载地图关卡
# load_map_path = '/Game/StarterContent/Maps/StarterMap.StarterMap'
# loaded = unreal.EditorLevelLibrary.load_level(load_map_path)
# if not loaded:
#     unreal.EditorDialog.show_message('Load Map Failed!', f"Can't load {load_map_path}", unreal.AppMsgType.OK)



# 添加actor
cube_path = '/Engine/BasicShapes/Cube.Cube'
cube_obj = unreal.load_asset(cube_path)
cube_position = unreal.Vector(640.0, 1680.0, 50.0)
unreal.EditorLevelLibrary.spawn_actor_from_object(cube_obj, cube_position)

# spawn_actor_from_class
mat = unreal.load_asset('/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial')
sphere_path = '/Engine/BasicShapes/Sphere.Sphere'
sphere_obj = unreal.load_asset(sphere_path)
sphere_position = unreal.Vector(640.0, 1500.0, 50.0)
sphere_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, sphere_position)
mesh_component: unreal.StaticMeshComponent = sphere_actor.get_component_by_class(unreal.StaticMeshComponent)
mesh_component.set_static_mesh(sphere_obj)
mesh_component.set_material(0, unreal.MaterialInterface.cast(mat))
sphere_actor.set_actor_label('Sphere')



# # 关卡添加usd，不是导入而是直接在关卡预览
# try:
#     unreal.load_module('USDStageImporter')
# except KeyError:
#     unreal.EditorDialog.show_message('Usd Plugin', 'Please load the USD Plugin!', unreal.AppMsgType.OK)

# import pathlib
# import inspect

# dir_path = pathlib.Path(inspect.getfile(inspect.currentframe())).parent.absolute()
# usd_path = str(dir_path.joinpath('assets', 'UsdSkelExamples', 'HumanFemale', 'HumanFemale.walk.usd'))

# usd_actor_position = unreal.Vector(550.0, 1600.0, 50.0)
# usd_stage_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.UsdStageActor, usd_actor_position)
# usd_stage_actor.set_editor_property('root_layer', unreal.FilePath(usd_path))


# from pxr import Ar, UsdUtils
# stage_cache = UsdUtils.StageCache.Get()
# stages = stage_cache.GetAllStages()
# # stage = stages[0]
# unreal.log(stages)

