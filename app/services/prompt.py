# This is a place to manage QA Prompt, Summary Prompt, Agent Prompt

def build_prompt(context, question):
    prompt = f"""你是一個專業的文件AI助理。請根據以下提供的「參考資料」來回答使用者的「問題」。
                如果參考資料中沒有提到，請回答「在文件中找不到相關答案」，不要憑空捏造。
                [參考資料]:
                {context}
                [問題]:
                {question}
                [回答]:"""
    return prompt