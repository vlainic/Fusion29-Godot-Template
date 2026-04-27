class_name GlobalState
extends Node

const SAVE_STATE_PATH = "user://global_state.tres"
const NO_VERSION_NAME = "0.0.0"
const LEGACY_STATE_SCRIPT_PATH = "res://scenes/runtime_template/base/nodes/state/global_state_data.gd"
const CURRENT_STATE_SCRIPT_PATH = "res://scenes/base/state/global_state_data.gd"

static var current : GlobalStateData
static var current_version : String

static func _ensure_open() -> void:
	if current is GlobalStateData:
		return
	open()

static func _log_opened() -> void:
	if current is GlobalStateData:
		current.last_unix_time_opened = int(Time.get_unix_time_from_system())

static func _log_version() -> void:
	if current is GlobalStateData:
		current_version = ProjectSettings.get_setting("application/config/version", NO_VERSION_NAME)
		if current_version.is_empty():
			current_version = NO_VERSION_NAME
		if not current.first_version_opened:
			current.first_version_opened = current_version
		current.last_version_opened = current_version

static func _load_current_state() -> void:
	if FileAccess.file_exists(SAVE_STATE_PATH):
		current = ResourceLoader.load(SAVE_STATE_PATH)
		if not current:
			_migrate_legacy_save_and_retry()
	if not current:
		current = GlobalStateData.new()

static func _migrate_legacy_save_and_retry() -> void:
	var file := FileAccess.open(SAVE_STATE_PATH, FileAccess.READ)
	if file == null:
		return
	var contents := file.get_as_text()
	file.close()
	if not contents.contains(LEGACY_STATE_SCRIPT_PATH):
		return
	contents = contents.replace(LEGACY_STATE_SCRIPT_PATH, CURRENT_STATE_SCRIPT_PATH)
	file = FileAccess.open(SAVE_STATE_PATH, FileAccess.WRITE)
	if file == null:
		return
	file.store_string(contents)
	file.close()
	current = ResourceLoader.load(SAVE_STATE_PATH)

static func open() -> void:
	_load_current_state()
	_log_opened()
	_log_version()
	save()

static func save() -> void:
	if current is GlobalStateData:
		ResourceSaver.save(current, SAVE_STATE_PATH)

static func has_state(state_key : String) -> bool:
	_ensure_open()
	if current is not GlobalStateData: return false
	return current.has_state(state_key)

static func get_or_create_state(state_key : String, state_type_path : String) -> Resource:
	_ensure_open()
	if current is not GlobalStateData: return
	return current.get_or_create_state(state_key, state_type_path)

static func reset() -> void:
	_ensure_open()
	if current is not GlobalStateData: return
	current.states.clear()
	save()
