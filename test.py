import openai
import re

client = openai.OpenAI(
    api_key="sk-1234",
    base_url="http://127.0.0.1:4000"
)

response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {
            "role": "user",
            "content": "結果はマークダウンで出力して：取引件数が上位１０位の顧客のID、居住地、延滞実績有無を教えて",
            "type": "message"
        }
    ],
    tools=[
        {
            "type": "mcp",
            "server_label": "snowflake",
            "server_url": "litellm_proxy",
            "require_approval": "never",
            "allowed_tools": ["snowflake-cortex_analyst"],
            "headers": {
                "x-litellm-api-key": "Bearer sk-1234"
            }
        }
    ],
    stream=True,
    tool_choice="required"
)

table_pattern = r"(\|[^\n]+\|\n(\|[^\n]+\|\n)+)"

for event in response:
    if getattr(event, "type", None) == "response.completed":
        for output_item in event.response.output:
            if hasattr(output_item, "content"):
                for content in output_item.content:
                    if hasattr(content, "text"):
                        match = re.search(table_pattern, content.text)
                        if match:
                            print(match.group(1))