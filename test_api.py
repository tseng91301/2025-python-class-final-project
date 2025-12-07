import api_connect as api
api.init("測試 0")
api.write_note("我今天去騎車，好開心!", mood_test=True)
api.export_notes()