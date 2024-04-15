# -*- coding: utf-8 -*-

import unreal



# 创建一个材质
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

material_path = "/Game/Assets/M_test"

package_name, asset_name = asset_tools.create_unique_asset_name(material_path, "")
asset_path, asset_name = package_name.rsplit("/", 1)

material = asset_tools.create_asset(asset_name, asset_path, 
                                    unreal.Material, unreal.MaterialFactoryNew())


node_x = -500
node_y = 0
# color sampler
is_rgba = False
color_texture_path = "/Game/Assets/color"
color_sampler = unreal.MaterialEditingLibrary.create_material_expression(
    material, unreal.MaterialExpressionTextureSample,
    node_x, node_y
)
color_sampler.set_editor_property('Desc', "Color")
if unreal.EditorAssetLibrary.does_asset_exist(color_texture_path):
    color_sampler.texture = unreal.load_asset(color_texture_path)

unreal.MaterialEditingLibrary.connect_material_property(
    color_sampler, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)

if is_rgba:
    unreal.MaterialEditingLibrary.connect_material_property(
        color_sampler, "A", unreal.MaterialProperty.MP_OPACITY)
    
    material.set_editor_property('blend_mode', unreal.BlendMode.BLEND_TRANSLUCENT)

# smoothness -> roughness
node_y += 200
roughness_sampler = unreal.MaterialEditingLibrary.create_material_expression(
    material, unreal.MaterialExpressionTextureSample,
    node_x, node_y + 100
)

one_minus = unreal.MaterialEditingLibrary.create_material_expression(
    material, unreal.MaterialExpressionOneMinus,
    node_x + 250, node_y + 200
)

unreal.MaterialEditingLibrary.connect_material_expressions(
    roughness_sampler, "R", one_minus, '')
unreal.MaterialEditingLibrary.connect_material_property(
    one_minus, "", unreal.MaterialProperty.MP_ROUGHNESS)


# 
unreal.EditorAssetLibrary.save_asset(material.get_path_name(), True)
