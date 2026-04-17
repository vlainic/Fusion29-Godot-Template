@tool
extends Control

@onready var credits_label : RichTextLabel = %CreditsLabel

@export var input_scroll_speed : float = 10.0

var _line_number : float = 0

func _on_visibility_changed() -> void:
	if visible:
		_sync_credits_width()
		credits_label.scroll_to_line(0)
		credits_label.grab_focus()

func _sync_credits_width() -> void:
	credits_label.custom_minimum_size.x = size.x

func _on_resized() -> void:
	_sync_credits_width()

func _ready() -> void:
	credits_label.focus_mode = Control.FOCUS_ALL
	visibility_changed.connect(_on_visibility_changed)
	resized.connect(_on_resized)
	_sync_credits_width()
	call_deferred("_sync_credits_width")

func _process(delta : float) -> void:
	if Engine.is_editor_hint() or not visible:
		return
	var input_axis = Input.get_axis("ui_up", "ui_down")
	if abs(input_axis) > 0.5:
		_line_number += input_axis * delta * input_scroll_speed
		var max_lines = credits_label.get_line_count() - credits_label.get_visible_line_count()
		if _line_number < 0:
			_line_number = 0
		if _line_number > max_lines:
			_line_number = max_lines
		credits_label.scroll_to_line(round(_line_number))
