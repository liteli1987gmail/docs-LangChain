import os
import sys

def translate_file(src_file, out_file):
    with open(src_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Translation mappings
    translations = {
        'You can invoke LangSmith Fleet agents from your applications using the [LangGraph SDK](/langsmith/reference) or the REST API. Fleet agents run on [Agent Server](/langsmith/agent-server), so you can use the same API methods as any other [LangSmith deployment](/langsmith/deployments).': '您可以使用 [LangGraph SDK](/langsmith/reference) 或 REST API 从您的应用程序调用 LangSmith Fleet 智能体。Fleet 智能体运行在 [Agent Server](/langsmith/agent-server) 上，因此您可以使用与任何其他 [LangSmith 部署](/langsmith/deployments) 相同的 API 方法。',
        'The REST API lets you call your agent from any language or platform that supports HTTP requests.': 'REST API 让您可以使用任何支持 HTTP 请求的语言或平台调用您的智能体。',
        '## Prerequisites': '## 前置条件',
        '- A LangSmith account with a Fleet agent': '- 一个带有 Fleet 智能体的 LangSmith 账户',
        '- A [Personal Access Token (PAT)](/langsmith/create-account-api-key) for authentication': '- 用于身份验证的 [个人访问令牌 (PAT)](/langsmith/create-account-api-key)',
        '- (SDK only) The [LangGraph SDK](/langsmith/reference) installed:': '- （仅 SDK）安装 [LangGraph SDK](/langsmith/reference)：',
        '## Authentication': '## 身份验证',
        'To authenticate with your agent\'s Fleet deployment, provide a LangSmith [Personal Access Token (PAT)](/langsmith/create-account-api-key) to the `api_key` argument when instantiating the LangGraph SDK client, or via the `X-API-Key` header. If using `X-API-Key`, you must also set the `X-Auth-Scheme` header to `langsmith-api-key`.': '要通过您的智能体的 Fleet 部署进行身份验证，请在实例化 LangGraph SDK 客户端时将 LangSmith [个人访问令牌 (PAT)](/langsmith/create-account-api-key) 提供给 `api_key` 参数，或通过 `X-API-Key` 头。如果您使用 `X-API-Key`，则还必须将 `X-Auth-Scheme` 头设置为 `langsmith-api-key`。',
        'If the PAT you pass is not tied to the owner of the agent, your request will be rejected with a `404 Not Found` error.': '如果您传递的 PAT 未绑定到智能体的所有者，您的请求将被拒绝并返回 `404 Not Found` 错误。',
        'If the agent you\'re trying to invoke is a <Tooltip tip="Agents shared with all members of a LangChain workspace. Private agents are only visible to the creator." cta="Learn more" href="/langsmith/fleet/manage-agent-settings">workspace agent</Tooltip> and you\'re not the owner, you can perform all the same operations as you would in the UI (read-only).': '如果您尝试调用的智能体是 <Tooltip tip="与 LangSmith 工作区所有成员共享的智能体。私有智能体仅对创建者可见。" cta="了解更多" href="/langsmith/fleet/manage-agent-settings">工作区智能体</Tooltip> 而您不是所有者，则可以执行与在 UI 中相同的所有操作（只读）。',
        '## 1. Get the agent ID and URL': '## 1. 获取智能体 ID 和 URL',
        'To get your agent\'s `agent_id` and `api_url`:': '要获取您智能体的 `agent_id` 和 `api_url`：',
        'In the [LangSmith UI](https://smith.langchain.com), navigate to your agent\'s inbox.': '在 [LangSmith UI](https://smith.langchain.com) 中，导航到您智能体的收件箱。',
        'Next to the agent name, click the <Icon icon="pencil" /> **Edit Agent** icon.': '在智能体名称旁边，点击<Icon icon="pencil" />**编辑智能体**图标。',
        'Click the <Icon icon="settings" /> **Settings** icon in the top right corner.': '点击右上角的<Icon icon="settings" />**设置**图标。',
        'Click **View code snippets** to see pre-populated values for your agent.': '点击**查看代码片段**以查看您智能体的预填充值。',
        'Copy the code below and replace `agent_id` and `api_url` with the values from your agent\'s code snippets.': '复制以下代码并用您智能体代码片段中的值替换 `agent_id` 和 `api_url`。',
        'Create a `.env` file in your project root with your [Personal Access Token](/langsmith/create-account-api-key):': '在您的项目根目录创建一个包含您 [个人访问令牌](/langsmith/create-account-api-key) 的 `.env` 文件：',
        '## 2. Fetch agent configuration': '## 2. 获取智能体配置',
        'Verify your connection by fetching your agent\'s configuration:': '通过获取您智能体的配置来验证您的连接：',
        'Use a [Personal Access Token (PAT)](/langsmith/create-account-api-key) tied to your LangSmith account. Set the `X-Auth-Scheme` header to `langsmith-api-key` for authentication. If you implemented custom authentication, pass the user\'s token in headers so the agent can use user-scoped tools. See [Add custom authentication](/langsmith/custom-auth).': '使用绑定到您 LangSmith 账户的 [个人访问令牌 (PAT)](/langsmith/create-account-api-key)。将 `X-Auth-Scheme` 头设置为 `langsmith-api-key` 进行身份验证。如果您实现了自定义身份验证，请在头中传递用户的令牌，以便智能体可以使用用户范围的工具。请参阅[添加自定义身份验证](/langsmith/custom-auth)。',
        '## 3. Invoke agent': '## 3. 调用智能体',
        'The examples below show how to send a message to your agent and receive a response. You can use either a **stateless** run (no thread, no conversation history) or a **stateful** run (with a thread to maintain conversation history across multiple turns).': '下面的示例展示了如何向您的智能体发送消息并接收响应。您可以使用**无状态**运行（无线程，无对话历史）或**有状态**运行（带线程以在多次交互中维护对话历史）。',
        '### Stateless run': '### 无状态运行',
        'A stateless run sends a single request and returns the full response. No conversation history is persisted. This is the simplest way to call your agent:': '无状态运行发送单个请求并返回完整响应。不保留对话历史记录。这是调用您智能体的最简单方式：',
        '### Stateless streaming run': '### 无状态流式运行',
        'To stream the response as it is generated rather than waiting for the full result, use the streaming endpoint:': '要流式传输生成的响应而不是等待完整结果，请使用流式端点：',
        '### Stateful run with a thread': '### 带线程的有状态运行',
        'To maintain conversation history across multiple interactions, first create a thread and then run your agent on it. Each subsequent run on the same thread has access to the full message history:': '要在多次交互中维护对话历史，请先创建一个线程，然后在该线程上运行您的智能体。同一线程上的每个后续运行都可以访问完整的消息历史：',
        '## REST API reference': '## REST API 参考',
        'The table below summarizes the key endpoints. Replace `<API_URL>` with your agent\'s deployment URL.': '下表总结了关键端点。将 `<API_URL>` 替换为您的智能体部署 URL。',
        'All endpoints require the following headers:': '所有端点都需要以下头：',
        'For the full API specification, see the [Agent Server API reference](/langsmith/server-api-ref).': '有关完整的 API 规范，请参阅 [Agent Server API 参考](/langsmith/server-api-ref)。',
        'Call agents from code': '通过代码调用智能体',
        'Invoke Fleet agents from Python, JavaScript, or any language through the REST API.': '通过 REST API 从 Python、JavaScript 或任何语言调用 Fleet 智能体。',
        'Call from code': '通过代码调用',
        'Use the `thread_id` from the response to send messages on the thread:': '使用响应中的 `thread_id` 在该线程上发送消息：',
        'Send a follow-up message on the same thread:': '在同一线程上发送后续消息：',
        'First, create a thread:': '首先，创建一个线程：',
    }

    for eng, chn in translations.items():
        content = content.replace(eng, chn)

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    src_file = sys.argv[1]
    out_file = sys.argv[2]
    translate_file(src_file, out_file)
    print(f'Translated: {src_file} -> {out_file}')
