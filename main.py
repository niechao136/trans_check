from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# 初始化 FastAPI 应用
app = FastAPI()

# 读取 Excel 文件并构建翻译字典
excel_file = "i18n_RAG.xlsx"
df = pd.read_excel(excel_file)  # 自动识别列头
translation_map = {
    row["zh-TW"]: {
        "zh-TW": str(row.get("zh-TW", "")).strip(),
        "zh-CN": str(row.get("zh-CN", "")).strip(),
        "en-US": str(row.get("en-US", "")).strip(),
        "ja-JP": str(row.get("ja-JP", "")).strip(),
        "ko-KR": str(row.get("ko-KR", "")).strip()
    }
    for _, row in df.iterrows()
}

# 输入结构
class LookupRequest(BaseModel):
    phrases: list


# POST 接口：批量翻译查找
@app.post("/lookup")
async def lookup(request: LookupRequest):
    matched = []
    unmatched = []

    for phrase in request.phrases:
        translation = translation_map.get(phrase)
        if translation:
            matched.append({
                "o": phrase,
                "t": translation
            })
        else:
            unmatched.append({
                "o": phrase
            })

    return {
        "matched": matched,
        "unmatched": unmatched
    }
