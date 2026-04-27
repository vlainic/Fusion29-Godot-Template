extends Node

func load_scene(scene_path: String) -> void:
	if scene_path.is_empty():
		return
	get_tree().change_scene_to_file(scene_path)

func reload_current_scene() -> void:
	get_tree().reload_current_scene()
