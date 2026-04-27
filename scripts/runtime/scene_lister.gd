@tool
class_name SceneLister
extends Node
## Lists scene files from a configured directory.

@export var files: Array[String] = []
@export_dir var directory: String = ""
@export var include_subdirectories: bool = false

func _ready() -> void:
	if Engine.is_editor_hint():
		_refresh_files()

func _refresh_files() -> void:
	if directory.is_empty():
		return
	var result: Array[String] = []
	_collect_scene_files(directory, result)
	files = result

func _collect_scene_files(dir_path: String, out: Array[String]) -> void:
	var dir_access := DirAccess.open(dir_path)
	if dir_access == null:
		return
	if dir_access.list_dir_begin() != OK:
		return
	var file_name := dir_access.get_next()
	while file_name != "":
		var full_path := dir_path.path_join(file_name)
		if dir_access.current_is_dir():
			if include_subdirectories and file_name != "." and file_name != "..":
				_collect_scene_files(full_path, out)
		elif file_name.ends_with(".tscn"):
			out.append(full_path)
		file_name = dir_access.get_next()
	out.sort()
