class_name LevelManager
extends Node
## Manage level changes in games.

@export var level_loader: LevelLoader
@export_file var starting_level_path: String
@export var scene_lister: Node
@export var auto_load: bool = true

@export_group("Scenes")
@export_file("*.tscn") var main_menu_scene_path: String
@export_file("*.tscn") var ending_scene_path: String
@export var game_won_scene: PackedScene
@export var level_lost_scene: PackedScene
@export var level_won_scene: PackedScene

var current_level: Node
var current_level_path: String: set = set_current_level_path
var checkpoint_level_path: String: set = set_checkpoint_level_path

func set_current_level_path(value: String) -> void:
	current_level_path = value

func set_checkpoint_level_path(value: String) -> void:
	checkpoint_level_path = value

func _try_connecting_signal_to_node(node: Node, signal_name: String, callable: Callable) -> void:
	if node.has_signal(signal_name) and not node.is_connected(signal_name, callable):
		node.connect(signal_name, callable)

func _try_connecting_signal_to_level(signal_name: String, callable: Callable) -> void:
	_try_connecting_signal_to_node(current_level, signal_name, callable)

func get_main_menu_scene_path() -> String:
	if main_menu_scene_path.is_empty():
		return GameConfig.main_menu_scene_path
	return main_menu_scene_path

func _load_main_menu() -> void:
	get_tree().change_scene_to_file(get_main_menu_scene_path())

func _find_in_scene_lister(level_path: String) -> int:
	if not scene_lister:
		return -1
	if not scene_lister.has_method("get"):
		return -1
	var listed_files = scene_lister.get("files")
	if listed_files == null:
		return -1
	level_path = ResourceUID.ensure_path(level_path)
	return listed_files.find(level_path)

func get_relative_level_path(offset: int = 1) -> String:
	if not scene_lister:
		return ""
	var listed_files = scene_lister.get("files")
	if listed_files == null:
		return ""
	var current_level_id := _find_in_scene_lister(current_level_path)
	if current_level_id > -1:
		if current_level_id >= max(0, -offset) and current_level_id < listed_files.size() - max(0, offset):
			current_level_id += offset
			return listed_files[current_level_id]
	return ""

func get_next_level_path() -> String:
	return get_relative_level_path(1)

func get_ending_scene_path() -> String:
	if ending_scene_path.is_empty():
		return GameConfig.ending_scene_path
	return ending_scene_path

func _load_ending() -> void:
	if not get_ending_scene_path().is_empty():
		get_tree().change_scene_to_file(get_ending_scene_path())
	else:
		_load_main_menu()

func _on_level_lost() -> void:
	if level_lost_scene:
		var instance := level_lost_scene.instantiate()
		get_tree().current_scene.add_child(instance)
		_try_connecting_signal_to_node(instance, &"restart_pressed", _reload_level)
		_try_connecting_signal_to_node(instance, &"main_menu_pressed", _load_main_menu)
	else:
		_reload_level()

func get_checkpoint_level_path() -> String:
	if checkpoint_level_path.is_empty():
		if scene_lister:
			var listed_files = scene_lister.get("files")
			if listed_files != null and listed_files.size() > 0:
				return listed_files.front()
		if not starting_level_path.is_empty():
			return starting_level_path
	return checkpoint_level_path

func load_level(level_path: String) -> void:
	current_level_path = level_path
	if level_loader and level_loader.has_method("load_level"):
		level_loader.load_level(level_path)

func _load_checkpoint_level() -> void:
	load_level(get_checkpoint_level_path())

func _reload_level() -> void:
	load_level(current_level_path)

func _load_win_screen_or_ending() -> void:
	if game_won_scene:
		var instance := game_won_scene.instantiate()
		get_tree().current_scene.add_child(instance)
		_try_connecting_signal_to_node(instance, &"continue_pressed", _load_ending)
		_try_connecting_signal_to_node(instance, &"restart_pressed", _reload_level)
		_try_connecting_signal_to_node(instance, &"main_menu_pressed", _load_main_menu)
	else:
		_load_ending()

func _load_level_won_screen_or_checkpoint() -> void:
	if level_won_scene:
		var instance := level_won_scene.instantiate()
		get_tree().current_scene.add_child(instance)
		_try_connecting_signal_to_node(instance, &"continue_pressed", _load_checkpoint_level)
		_try_connecting_signal_to_node(instance, &"restart_pressed", _reload_level)
		_try_connecting_signal_to_node(instance, &"main_menu_pressed", _load_main_menu)
	else:
		_load_checkpoint_level()

func _on_level_won(next_level_path: String = "") -> void:
	if next_level_path.is_empty():
		next_level_path = get_next_level_path()
	if next_level_path.is_empty():
		_load_win_screen_or_ending()
	else:
		checkpoint_level_path = next_level_path
		_load_level_won_screen_or_checkpoint()

func _on_level_changed(next_level_path: String) -> void:
	checkpoint_level_path = next_level_path
	_load_checkpoint_level()

func _connect_level_signals() -> void:
	_try_connecting_signal_to_level(&"level_lost", _on_level_lost)
	_try_connecting_signal_to_level(&"level_won", _on_level_won)
	_try_connecting_signal_to_level(&"level_changed", _on_level_changed)

func _on_level_loader_level_loaded() -> void:
	if level_loader:
		current_level = level_loader.current_level
	if current_level == null:
		return
	await current_level.ready
	_connect_level_signals()

func _auto_load() -> void:
	if auto_load:
		_load_checkpoint_level()

func _ready() -> void:
	if Engine.is_editor_hint():
		return
	if level_loader == null:
		push_error("LevelManager: level_loader is not assigned.")
		return
	if not level_loader.level_loaded.is_connected(_on_level_loader_level_loaded):
		level_loader.level_loaded.connect(_on_level_loader_level_loaded)
	_auto_load()
