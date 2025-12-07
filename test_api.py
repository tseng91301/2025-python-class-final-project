import api_connect as api

api.init("測試 1", force=False)
api.write_note("我今天去騎車，好開心！", mood_test=True)

api.conversation_bg("你好嗎？")  # 立即返回，不會卡住

api.conversation_bg("其實我今天報告快做不完，要爆炸了...")  # 立即返回，不會卡住
api.conversation_bg("但我今天有去騎車，其實還是挺開心的")  # 立即返回，不會卡住

# 等一段時間…
print(api.genai_waiting)         # False
print(api.genai_response)        # <-- 顯示回答

# 等一下想看的時候再匯出
api.export_notes()