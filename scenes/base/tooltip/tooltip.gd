class_name Tooltip
extends PanelContainer
## Reusable hover tooltip. Parent sets content via meta and calls toggle().
##
## On the hover target:
##   set_meta(&"tooltip_bbcode", "[b]Title[/b]\nDescription")
##   # or set_meta(&"tooltip_text", "Plain text")
## On mouse_entered / mouse_exited call $Tooltip.toggle(true/false).

@onready var _content: RichTextLabel = $Content
@onready var _delay_timer: Timer = $DelayTimer

@export var default_text: String = ""
@export var extra_offset: Vector2 = Vector2(0, -10)
@export var delay_seconds: float = 0.5:
	set(value):
		delay_seconds = value
		if _delay_timer:
			_delay_timer.wait_time = delay_seconds

var _opacity_tween: Tween
var _hover_active: bool = false


func _ready() -> void:
	_delay_timer.wait_time = delay_seconds
	visible = false


func _process(_delta: float) -> void:
	if visible:
		global_position = get_global_mouse_position() + _get_screen_offset()


func toggle(on: bool) -> void:
	if on:
		_hover_active = true
		_delay_timer.start()
		await _delay_timer.timeout

		if not _hover_active:
			return

		if not _update_content():
			return

		modulate.a = 0.0
		show()
		await get_tree().process_frame
		await _tween_opacity(1.0).finished
	else:
		_hover_active = false
		modulate.a = 1.0
		await _tween_opacity(0.0).finished
		_delay_timer.stop()
		hide()


func _tween_opacity(to: float) -> Tween:
	if _opacity_tween:
		_opacity_tween.kill()

	_opacity_tween = create_tween()
	_opacity_tween.tween_property(self, "modulate:a", to, 0.3)
	return _opacity_tween


func _update_content() -> bool:
	var parent := get_parent()
	if parent == null:
		_content.text = default_text
		return not default_text.is_empty()

	if parent.has_meta(&"tooltip_bbcode"):
		_content.text = str(parent.get_meta(&"tooltip_bbcode"))
	elif parent.has_meta(&"tooltip_text"):
		_content.text = str(parent.get_meta(&"tooltip_text"))
	elif not default_text.is_empty():
		_content.text = default_text
	else:
		return false

	return true


func _get_screen_offset() -> Vector2:
	return Vector2(-size.x / 2.0, -size.y) + extra_offset
