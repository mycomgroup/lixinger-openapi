# QVeris API 技能文档

## 概述

QVeris 是一个工具搜索和执行层，为 LLM Agent 提供 API 来发现和执行各种工具。

- **源文档**: [QVeris API Documentation](https://qveris.ai/docs)
- **文档位置**: `/Users/yuping/Downloads/git/stock-website-crawler/stock-crawler/merged_output/qveris-api-docs/docs/qveris-api-docs.md`

---

## API 基本信息

| 属性 | 值 |
|------|-----|
| **Base URL** | `https://qveris.ai/api/v1` |
| **认证方式** | Bearer Token |
| **请求头** | `Authorization: Bearer YOUR_API_KEY`<br>`Content-Type: application/json` |

---

## 核心端点

### 1. 搜索工具

**端点**: `POST /search`

**描述**: 使用自然语言查询搜索可用的工具

**请求参数**:
```json
{
  "query": "string",      // 必需：描述工具功能的自然语言查询
  "limit": 10,            // 可选：返回结果数量限制
  "session_id": "string"  // 可选：用户会话ID
}
```

**响应示例**:
```json
{
  "search_id": "string",
  "total": 3,
  "results": [
    {
      "tool_id": "openweathermap.weather.execute.v1",
      "name": "Current Weather",
      "description": "Get current weather data for any location",
      "provider_name": "OpenWeatherMap",
      "provider_description": "Global weather data provider",
      "region": "global",
      "params": [
        {
          "name": "city",
          "type": "string",
          "required": true,
          "description": "City name"
        },
        {
          "name": "units",
          "type": "string",
          "required": false,
          "description": "Temperature units (metric/imperial)",
          "enum": ["metric", "imperial", "standard"]
        }
      ],
      "stats": {
        "avg_execution_time_ms": 21.74,
        "success_rate": 0.909
      }
    }
  ],
  "elapsed_time_ms": 245.6
}
```

**curl 示例**:
```bash
curl -sS -X POST "https://qveris.ai/api/v1/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "weather forecast API", "limit": 5}'
```

---

### 2. 执行工具

**端点**: `POST /tools/execute`

**描述**: 通过 tool_id 执行特定工具

**URL 参数**:
- `tool_id`: 要执行的工具ID（从搜索结果中获取）

**请求体参数**:
```json
{
  "search_id": "string",           // 必需：来自 search_tools 的 search_id
  "session_id": "string",          // 可选：用户会话ID
  "parameters": {                  // 工具特定参数
    "city": "London",
    "units": "metric"
  },
  "max_response_size": 20480       // 可选：最大响应大小（字节），默认20480
}
```

**响应示例**:
```json
{
  "execution_id": "exec123",
  "result": {
    "data": {
      "temperature": 15.5,
      "humidity": 72,
      "description": "partly cloudy",
      "wind_speed": 12.5
    }
  },
  "success": true,
  "error_message": null,
  "elapsed_time_ms": 210.72,
  "cost": 5.0
}
```

**curl 示例**:
```bash
curl -sS -X POST "https://qveris.ai/api/v1/tools/execute?tool_id=openweathermap_current_weather" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "search_id": "YOUR_SEARCH_ID",
    "parameters": {
      "city": "London",
      "units": "metric"
    }
  }'
```

---

### 3. 根据ID获取工具详情

**端点**: `POST /tools/by-ids`

**描述**: 根据工具ID列表获取工具详情

**请求体参数**:
```json
{
  "tool_ids": ["string1", "string2"],
  "search_id": "string",
  "session_id": "string"
}
```

---

## Agent 调用示例

### 函数定义（供 LLM Agent 使用）

**search_tools**:
```json
{
  "type": "function",
  "function": {
    "name": "search_tools",
    "description": "Search for available tools. Returns relevant tools that can help accomplish tasks.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The search query describing the general capability of the tool. Not specific params you want to pass to the tool later."
        },
        "session_id": {
          "type": "string",
          "description": "The uuid of the user session. Should be changed only if new session."
        }
      },
      "required": ["query"]
    }
  }
}
```

**execute_tool**:
```json
{
  "type": "function",
  "function": {
    "name": "execute_tool",
    "description": "Execute a specific remote tool with provided parameters. The tool_id must come from a previous search_tools call; The params_to_tool is where the params can be passed.",
    "parameters": {
      "type": "object",
      "properties": {
        "tool_id": {
          "type": "string",
          "description": "The ID of the remote tool to execute (from search results)"
        },
        "search_id": {
          "type": "string",
          "description": "The search_id in the response of the search_tools call that returned the information of this remote tool"
        },
        "session_id": {
          "type": "string",
          "description": "The uuid of the user session. Should be changed only if new session."
        },
        "params_to_tool": {
          "type": "string",
          "description": "A JSON stringified dictionary of parameters to pass to the remote tool. For example: { \"param1\": \"value1\", \"param2\": 42 }"
        },
        "max_response_size": {
          "type": "integer",
          "description": "If tool generates data longer than max_response_size (in bytes), do not return the full data to avoid big LLM token cost. Default value is 20480."
        }
      },
      "required": ["tool_id", "search_id", "params_to_tool"]
    }
  }
}
```

---

## TypeScript 使用示例

```typescript
export async function searchTools(
  query: string,
  sessionId: string,
  limit: number = 20
): Promise<SearchResponse> {
  const response = await api.post<SearchResponse>('/search', {
    query,
    limit,
    session_id: sessionId,
  })
  return response.data
}

export async function executeTool(
  toolId: string,
  searchId: string,
  sessionId: string,
  parameters: object
): Promise<ToolExecutionResponse> {
  const response = await api.post<ToolExecutionResponse>(
    `/tools/execute?tool_id=${toolId}`,
    {
      search_id: searchId,
      session_id: sessionId,
      parameters,
    }
  )
  return response.data
}

// 工具执行函数
async function executeTool(name: string, args: Record<string, unknown>) {
  console.log(`[Tool] Executing ${name} with:`, args)

  if (name === 'search_tools') {
    const result = await searchEngineApi.searchTools(
      args.query as string,
      args.session_id as string,
      20
    )
    return result
  } else if (name === 'execute_tool') {
    let parsedParams: Record<string, unknown>
    try {
      parsedParams = JSON.parse(args.params_to_tool as string) as Record<string, unknown>
    } catch (parseError) {
      throw new Error(`Invalid JSON in params_to_tool: ${parseError instanceof Error ? parseError.message : 'Unknown parse error'}`)
    }

    const result = await searchEngineApi.executeTool(
      args.tool_id as string,
      args.search_id as string,
      args.session_id as string,
      parsedParams
    )
    return result
  }

  throw new Error(`Unknown tool: ${name}`)
}
```

---

## MCP 配置

如果你使用支持 MCP (Model Context Protocol) 的工具，可以这样配置：

```json
{
  "mcpServers": {
    "qveris": {
      "command": "npx",
      "args": ["@qverisai/mcp"],
      "env": {
        "QVERIS_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

---

## 使用场景

1. **当用户需要执行某个特定功能但不确定使用什么工具时**
   - 调用 `search_tools` 查找相关工具

2. **当需要从搜索结果中执行某个工具时**
   - 使用 `search_id` 和 `tool_id` 调用 `execute_tool`
   - 将参数以 JSON 字符串形式传递给 `params_to_tool`

3. **当需要管理工具执行会话时**
   - 使用 `session_id` 跟踪会话状态
   - 使用 `max_response_size` 控制响应大小以节省 token

---

## 注意事项

1. **认证**: 所有请求都需要在 Header 中提供 `Authorization: Bearer YOUR_API_KEY`
2. **会话ID**: `session_id` 用于跟踪用户会话，只有在开始新会话时才应该更改
3. **工具参数**: `params_to_tool` 必须是 JSON 字符串格式，包含要传递给远程工具的参数
4. **响应大小**: 使用 `max_response_size` 参数（默认 20480 字节）限制响应大小，避免产生过高的 LLM token 成本
5. **工具ID来源**: `tool_id` 必须来自之前的 `search_tools` 调用结果

---

## 相关数据模型

### 工具参数模式
```json
{
  "name": "string",
  "type": "string|number|boolean|array|object",
  "required": true,
  "description": "string",
  "enum": ["option1", "option2"]
}
```

### 工具历史执行性能
```json
{
  "avg_execution_time_ms": 8564.43,
  "success_rate": 0.748
}
```
