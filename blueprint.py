# -*- coding: utf-8 -*-

import unreal


asset_tools = unreal.AssetToolsHelpers.get_asset_tools()


asset_path = "/Game/Assets/BP_test"

package_name, asset_name = asset_tools.create_unique_asset_name(asset_path, "")
asset_path, asset_name = package_name.rsplit("/", 1)

# 蓝图工厂和父类
bp_factory = unreal.BlueprintFactory()
bp_factory.set_editor_property("ParentClass", unreal.Actor)

bp_asset: unreal.Blueprint = asset_tools.create_asset(
    asset_name, asset_path, 
    unreal.Blueprint, 
    bp_factory
)


# 使用SubobjectDataSubsystem来添加组件
subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
root_data_handle = subsystem.k2_gather_subobject_data_for_blueprint(bp_asset)[0]

sub_handle, fail_reson = subsystem.add_new_subobject(
    unreal.AddNewSubobjectParams(
        root_data_handle,
        unreal.StaticMeshComponent,
        bp_asset
    )
)

# 修改组件名称
subsystem.rename_subobject(sub_handle, unreal.Text("Mesh"))

# 获取组件
BFL = unreal.SubobjectDataBlueprintFunctionLibrary
mesh_component: unreal.StaticMeshComponent = BFL.get_object(BFL.get_data(sub_handle))

# 设置组件属性
mat = unreal.load_asset('/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial')
sphere_path = '/Engine/BasicShapes/Sphere.Sphere'
mesh_component.set_static_mesh(unreal.load_asset(sphere_path))
mesh_component.set_material(0, unreal.MaterialInterface.cast(mat))


unreal.BlueprintEditorLibrary.compile_blueprint(bp_asset)
unreal.EditorAssetLibrary.save_loaded_asset(bp_asset)



