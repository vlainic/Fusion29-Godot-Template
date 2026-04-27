@tool
class_name LevelLoader
extends Node
## Loads level scenes into a configured container.

signal level_load_started
signal level_loaded
signal level_ready

@export var level_container: Node
@export var level_loading_screen: LoadingScreen
@export_group("Debugging")
@export var current_level: Node

var current_level_path: String
var is_loading: bool = false

func _attach_level(level_resource: Resource) -> Node:
	assert(level_container != null, "level_container is null")
	var instance: Node = level_resource.instantiate()
	level_container.call_deferred("add_child", instance)
	return instance

func load_level(level_path: String) -> void:
	if is_loading:
		return
	if is_instance_valid(current_level):
		current_level.queue_free()
		await current_level.tree_exited
		current_level = null

	current_level_path = level_path
	is_loading = true
	if level_loading_screen:
		level_loading_screen.reset()
	level_load_started.emit()

	var level_resource := load(current_level_path)
	if level_resource == null:
		push_error("Failed to load level: %s" % current_level_path)
		is_loading = false
		if level_loading_screen:
			level_loading_screen.close()
		return

	is_loading = false
	current_level = _attach_level(level_resource)
	if level_loading_screen:
		level_loading_screen.close()
	level_loaded.emit()
	await current_level.ready
	level_ready.emit()
