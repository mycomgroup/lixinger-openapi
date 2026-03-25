---
id: "url-4ad0161"
type: "api"
title: "QVeris API Documentation"
url: "https://qveris.ai/docs"
description: "QVeris is a tool search and execution layer that provides APIs for LLM agents to discover and execute tools."
source: "js-chunk"
tags: []
crawl_time: "2026-03-18T01:34:21.447Z"
metadata:
  sections:
    - {"id":"quickstart","title":"Quick start"}
    - {"id":"ide-cli-config","title":"IDE & CLI Configuration Guide"}
    - {"id":"claude-code-config","title":"Claude Code"}
    - {"id":"opencode-config","title":"Opencode"}
    - {"id":"principles","title":"Principles"}
    - {"id":"models","title":"Models"}
    - {"id":"multimodal","title":"Multimodal"}
    - {"id":"authentication","title":"Authentication"}
    - {"id":"faq","title":"FAQ"}
    - {"id":"enterprise","title":"Enterprise"}
    - {"id":"tool-calling","title":"Tool Calling"}
    - {"id":"web-search","title":"Web Search"}
    - {"id":"structured-outputs","title":"Structured Outputs"}
    - {"id":"authentication","title":"Authentication"}
    - {"id":"base-url","title":"Base URL"}
    - {"id":"api-endpoints","title":"API Endpoints"}
    - {"id":"search-tools","title":"Search Tools"}
    - {"id":"search-tools-endpoint","title":"Endpoint"}
    - {"id":"search-tools-request-headers","title":"Request Headers"}
    - {"id":"search-tools-request-body","title":"Request Body"}
    - {"id":"search-tools-response","title":"Response"}
    - {"id":"search-tools-response-fields","title":"Response Fields (Results)"}
    - {"id":"execute-tool","title":"Execute Tool"}
    - {"id":"endpoint-exec","title":"Endpoint"}
    - {"id":"execute-tool-request-headers","title":"Request Headers"}
    - {"id":"execute-tool-url-parameters","title":"URL Parameters"}
    - {"id":"request-body-exec","title":"Request Body"}
    - {"id":"response-exec","title":"Response"}
    - {"id":"execute-tool-response-fields","title":"Response Fields"}
    - {"id":"execute-tool-result-fields","title":"Result Fields for Long Tool Response"}
    - {"id":"get-tools-by-id","title":"Get Tools by ID"}
    - {"id":"get-tools-by-id-endpoint","title":"Endpoint"}
    - {"id":"get-tools-by-id-request-headers","title":"Request Headers"}
    - {"id":"get-tools-by-id-request-body","title":"Request Body"}
    - {"id":"get-tools-by-id-parameters","title":"Parameters"}
    - {"id":"get-tools-by-id-response","title":"Response"}
    - {"id":"data-models","title":"Data Models"}
    - {"id":"tool-parameter-schema","title":"Tool Parameter Schema"}
    - {"id":"tool-historical-performance","title":"Tool Historical execution performance"}
    - {"id":"llm-agent-examples","title":"LLM/Agent Use Examples"}
    - {"id":"sdk-overview","title":"Overview"}
    - {"id":"quick-start","title":"Quick start"}
    - {"id":"use-qveris-mcp","title":"Use QVeris MCP anywhere MCP is supported"}
    - {"id":"use-python-sdk","title":"Use the QVeris Python SDK"}
    - {"id":"direct-rest-api","title":"Directly call the QVeris REST API"}
    - {"id":"how-to-get-api-key","title":"How to get an API key"}
    - {"id":"recommended-system-prompt","title":"Recommended system prompt"}
    - {"id":"api-keys","title":"API Keys"}
    - {"id":"bearer-token","title":"Bearer Token"}
    - {"id":"authentication","title":"Authentication"}
    - {"id":"base-url","title":"Base URL"}
    - {"id":"api-endpoints","title":"API Endpoints"}
    - {"id":"search-tools-endpoint","title":"Endpoint"}
    - {"id":"search-tools-request-headers","title":"Request Headers"}
    - {"id":"search-tools-request-body","title":"Request Body"}
    - {"id":"search-tools-response","title":"Response"}
    - {"id":"search-tools-response-fields","title":"Response Fields (Results)"}
    - {"id":"data-models","title":"Data Models"}
    - {"id":"llm-agent-examples","title":"LLM/Agent Use Examples"}
    - {"id":"endpoint-exec","title":"Endpoint"}
    - {"id":"execute-tool-request-headers","title":"Request Headers"}
    - {"id":"execute-tool-url-parameters","title":"URL Parameters"}
    - {"id":"request-body-exec","title":"Request Body"}
    - {"id":"response-exec","title":"Response"}
    - {"id":"execute-tool-response-fields","title":"Response Fields"}
    - {"id":"execute-tool-result-fields","title":"Result Fields for Long Tool Response"}
    - {"id":"get-tools-by-id-endpoint","title":"Endpoint"}
    - {"id":"get-tools-by-id-request-headers","title":"Request Headers"}
    - {"id":"get-tools-by-id-request-body","title":"Request Body"}
    - {"id":"get-tools-by-id-parameters","title":"Parameters"}
    - {"id":"get-tools-by-id-response","title":"Response"}
    - {"id":"github","title":"GitHub Repository"}
    - {"id":"configuration","title":"Configuration"}
    - {"id":"quick-start","title":"Quick Start"}
    - {"id":"examples","title":"Examples"}
    - {"id":"integration-patterns","title":"Integration patterns"}
    - {"id":"custom-llm-providers","title":"Custom LLM providers"}
    - {"id":"capabilities","title":"Features"}
    - {"id":"configuration","title":"Configuration"}
    - {"id":"get-api-key","title":"Get Your API Key"}
    - {"id":"start-using","title":"Start Using"}
    - {"id":"search-params","title":"Parameters"}
    - {"id":"search-example","title":"Example"}
    - {"id":"execute-params","title":"Parameters"}
    - {"id":"execute-example","title":"Example"}
    - {"id":"success-response","title":"Successful Execution"}
    - {"id":"large-response","title":"Large Responses"}
  codeExamples:
    - {"language":"typescript","code":"export async function searchTools(\n  query: string,\n  sessionId: string,\n  limit: number = 20\n): Promise<SearchResponse> {\n  const response = await api.post<SearchResponse>('/search', {\n    query,\n    limit,\n    session_id: sessionId,\n  })\n  return response.data\n}\n\nexport async function executeTool(\n  toolId: string,\n  searchId: string,\n  sessionId: string,\n  parameters: object\n): Promise<ToolExecutionResponse> {\n  const response = await api.post<ToolExecutionResponse>(\n    `/tools/execute?tool_id=${toolId}`,\n    {\n      search_id: searchId,\n      session_id: sessionId,\n      parameters,\n    }\n  )\n  return response.data\n}\n\nexport const searchEngineApi = {\n  searchTools,\n  executeTool,\n}\n\n// Execute tool function\nasync function executeTool(name: string, args: Record<string, unknown>) {\n  console.log(`[Tool] Executing ${name} with:`, args)\n\n  if (name === 'search_tools') {\n    const result = await searchEngineApi.searchTools(\n      args.query as string,\n      args.session_id as string,\n      20\n    )\n    return result\n  } else if (name === 'execute_tool') {\n    let parsedParams: Record<string, unknown>\n    try {\n      parsedParams = JSON.parse(args.params_to_tool as string) as Record<string, unknown>\n    } catch (parseError) {\n      throw new Error(\n        `Invalid JSON in params_to_tool: ${parseError instanceof Error ? parseError.message : 'Unknown parse error'}`\n      )\n    }\n\n    const result = await searchEngineApi.executeTool(\n      args.tool_id as string,\n      args.search_id as string,\n      args.session_id as string,\n      parsedParams\n    )\n    return result\n  }\n\n  throw new Error(`Unknown tool: ${name}`)\n}"}
    - {"language":"bash","code":"curl -sS -X POST \"https://qveris.ai/api/v1/tools/execute?tool_id=openweathermap_current_weather\" \\\n  -H \"Authorization: Bearer YOUR_API_KEY\" \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"search_id\\\":\\\"YOUR_SEARCH_ID\\\""}
    - {"language":"bash","code":"curl -sS -X POST \"https://qveris.ai/api/v1/search\" \\\n  -H \"Authorization: Bearer YOUR_API_KEY\" \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\":\\\"weather forecast API\\\""}
    - {"language":"json","code":"{\n  \"type\": \"function\",\n  \"function\": {\n    \"name\": \"execute_tool\",\n    \"description\": \"Execute a specific remote tool with provided parameters. The tool_id must come from a previous search_tools call; The params_to_tool is where the params can be passed.\",\n    \"parameters\": {\n      \"type\": \"object\",\n      \"properties\": {\n        \"tool_id\": {\n          \"type\": \"string\",\n          \"description\": \"The ID of the remote tool to execute (from search results)\"\n        },\n        \"search_id\": {\n          \"type\": \"string\",\n          \"description\": \"The search_id in the response of the search_tools call that returned the information of this remote tool\"\n        },\n        \"session_id\": {\n          \"type\": \"string\",\n          \"description\": \"The uuid of the user session. Should be changed only if new session.\"\n        },\n        \"params_to_tool\": {\n          \"type\": \"string\",\n          \"description\": \"An JSON stringified dictionary of parameters to pass to the remote tool, where keys are param names and values can be of any type, used to pass multiple arguments to the tool. For example: { \\\"param1\\\": \\\"value1\\\", \\\"param2\\\": 42, \\\"param3\\\": { \\\"nestedKey\\\": \\\"nestedValue\\\" } }\"\n        },\n        \"max_response_size\": {\n          \"type\": \"integer\",\n          \"description\": \"If tool generates data longer than max_response_size (in bytes), do not return the full data to avoid big LLM token cost. Default value is 20480.\"\n        }\n      },\n      \"required\": [\"tool_id\", \"search_id\", \"params_to_tool\"]\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"search_id\": \"string\",\n  \"total\": 3,\n  \"results\": [\n    {\n      \"tool_id\": \"openweathermap.weather.execute.v1\",\n      \"name\": \"Current Weather\",\n      \"description\": \"Get current weather data for any location\",\n      \"provider_name\": \"OpenWeatherMap\",\n      \"provider_description\": \"Global weather data provider\",\n      \"region\": \"global\",\n      \"params\": [\n        {\n          \"name\": \"city\",\n          \"type\": \"string\",\n          \"required\": true,\n          \"description\": \"City name\"\n        },\n        {\n          \"name\": \"units\",\n          \"type\": \"string\",\n          \"required\": false,\n          \"description\": \"Temperature units (metric/imperial)\",\n          \"enum\": [\"metric\", \"imperial\", \"standard\"]\n        }\n      ],\n      \"examples\": {\n        \"sample_parameters\": {\n          \"city\": \"London\",\n          \"units\": \"metric\"\n        }\n      },\n      \"stats\": {\n          \"avg_execution_time_ms\": 21.74,\n          \"success_rate\": 0.909\n      }\n    }\n  ],\n  \"elapsed_time_ms\": 245.6\n}"}
    - {"language":"json","code":"{\n  \"type\": \"function\",\n  \"function\": {\n    \"name\": \"search_tools\",\n    \"description\": \"Search for available tools. Returns relevant tools that can help accomplish tasks.\",\n    \"parameters\": {\n      \"type\": \"object\",\n      \"properties\": {\n        \"query\": {\n          \"type\": \"string\",\n          \"description\": \"The search query describing the general capability of the tool. Not specific params you want to pass to the tool later.\"\n        },\n        \"session_id\": {\n          \"type\": \"string\",\n          \"description\": \"The uuid of the user session. Should be changed only if new session.\"\n        }\n      },\n      \"required\": [\"query\"]\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"execution_id\": \"string\",\n  \"result\": {\n    \"data\": {\n      \"temperature\": 15.5,\n      \"humidity\": 72,\n      \"description\": \"partly cloudy\",\n      \"wind_speed\": 12.5\n    }\n  },\n  \"success\": true,\n  \"error_message\": null,\n  \"elapsed_time_ms\": 210.72,\n  \"cost\": 5.0\n}"}
    - {"language":"json","code":"{\n  \"execution_id\": \"exec-123\",\n  \"tool_id\": \"openweathermap_current_weather\",\n  \"success\": true,\n  \"result\": {\n    \"data\": {\n      \"temperature\": 15.5,\n      \"humidity\": 72,\n      \"description\": \"partly cloudy\"\n    }\n  },\n  \"execution_time\": 0.847\n}"}
    - {"language":"json","code":"{\n  \"mcpServers\": {\n    \"qveris\": {\n      \"command\": \"npx\",\n      \"args\": [\"@qverisai/mcp\"],\n      \"env\": {\n        \"QVERIS_API_KEY\": \"your-api-key-here\"\n      }\n    }\n  }\n}"}
    - {"language":"json","code":"{\n  \"name\": \"string\",\n  \"type\": \"string|number|boolean|array|object\",\n  \"required\": true,\n  \"description\": \"string\",\n  \"enum\": [\"option1\", \"option2\"]\n}"}
    - {"language":"json","code":"{\n  \"search_id\": \"string\",\n  \"session_id\": \"string\",\n  \"parameters\": {\n    \"city\": \"London\",\n    \"units\": \"metric\"\n  },\n  \"max_response_size\": 20480\n}"}
    - {"language":"json","code":"{\n  \"tool_id\": \"openweathermap_current_weather\",\n  \"search_id\": \"abc123\",\n  \"params_to_tool\": \"{\\\"city\\\": \\\"London\\\", \\\"units\\\": \\\"metric\\\"}\"\n}"}
    - {"language":"json","code":"{\n        \"search_id\": search_id,\n        \"parameters\": {\"city\": \"London\", \"units\": \"metric\"},\n        \"max_response_size\": 20480,\n    }"}
    - {"language":"json","code":"{\n  \"success\": true,\n  \"execution_id\": \"exec123\",\n  \"result\": {\n    \"temperature\": 15.5,\n    \"description\": \"partly cloudy\"\n  }\n}"}
    - {"language":"json","code":"{\n  \"search_id\": \"abc123\",\n  \"parameters\": {\n          \"city\": \"London\",\n          \"units\": \"metric\"\n        }\n}"}
    - {"language":"json","code":"{\n        \"Authorization\": f\"Bearer {API_KEY}\",\n        \"Content-Type\": \"application/json\",\n    }"}
    - {"language":"json","code":"{\n  \"tool_ids\": [\"string1\", \"string2\", ...],\n  \"search_id\": \"string\",\n  \"session_id\": \"string\"\n}"}
    - {"language":"json","code":"{\n  \"query\": \"string\",\n  \"limit\": 10,\n  \"session_id\": \"string\"\n}"}
    - {"language":"json","code":"{\n  \"avg_execution_time_ms\": 8564.43,\n  \"success_rate\": 0.748\n}"}
    - {"language":"json","code":"{\n  \"query\": \"send email notification\",\n  \"limit\": 5\n}"}
  endpoints:
    - "/search"
    - "/tools/execute"
  apiInfo:
    baseUrl: "https://qveris.ai/api/v1"
    authMethod: "Bearer Token"
    endpoints:
      - {"method":"POST","path":"/search","description":"Search for tools using natural language query","params":["query","limit","session_id"]}
      - {"method":"POST","path":"/tools/execute","description":"Execute a tool by tool_id with parameters","params":["tool_id","search_id","parameters","max_response_size"]}
      - {"method":"POST","path":"/tools/by-ids","description":"Get descriptions of tools based on tool_id","params":["tool_ids","search_id","session_id"]}
  rawContent: "# QVeris API Documentation\n\n## Base URL\nhttps://qveris.ai/api/v1\n\n## Authentication\nAll API requests require authentication via Bearer Token:\nAuthorization: Bearer YOUR_API_KEY\n\n## API Endpoints\n\n### POST /search\nSearch for tools using natural language query\nParameters: query, limit, session_id\n\n### POST /tools/execute\nExecute a tool by tool_id with parameters\nParameters: tool_id, search_id, parameters, max_response_size\n\n### POST /tools/by-ids\nGet descriptions of tools based on tool_id\nParameters: tool_ids, search_id, session_id\n\n## Code Examples\n\n### typescript\n```\nexport async function searchTools(\n  query: string,\n  sessionId: string,\n  limit: number = 20\n): Promise<SearchResponse> {\n  const response = await api.post<SearchResponse>('/search', {\n    query,\n    limit,\n    session_id: sessionId,\n  })\n  return response.data\n}\n\nexport async function executeTool(\n  toolId: string,\n  searchId: string,\n  sessionId: string,\n  parameters: object\n): Promise<ToolExecutionResponse> {\n  const response = await api.post<ToolExecutionResponse>(\n    `/tools/execute?tool_id=${toolId}`,\n    {\n      search_id: searchId,\n      session_id: sessionId,\n      parameters,\n    }\n  )\n  return response.data\n}\n\nexport const searchEngineApi = {\n  searchTools,\n  executeTool,\n}\n\n// Execute tool function\nasync function executeTool(name: string, args: Record<string, unknown>) {\n  console.log(`[Tool] Executing ${name} with:`, args)\n\n  if (name === 'search_tools') {\n    const result = await searchEngineApi.searchTools(\n      args.query as string,\n      args.session_id as string,\n      20\n    )\n    return result\n  } else if (name === 'execute_tool') {\n    let parsedParams: Record<string, unknown>\n    try {\n      parsedParams = JSON.parse(args.params_to_tool as string) as Record<string, unknown>\n    } catch (parseError) {\n      throw new Error(\n        `Invalid JSON in params_to_tool: ${parseError instanceof Error ? parseError.message : 'Unknown parse error'}`\n      )\n    }\n\n    const result = await searchEngineApi.executeTool(\n      args.tool_id as string,\n      args.search_id as string,\n      args.session_id as string,\n      parsedParams\n    )\n    return result\n  }\n\n  throw new Error(`Unknown tool: ${name}`)\n}\n```\n\n### bash\n```\ncurl -sS -X POST \"https://qveris.ai/api/v1/tools/execute?tool_id=openweathermap_current_weather\" \\\n  -H \"Authorization: Bearer YOUR_API_KEY\" \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"search_id\\\":\\\"YOUR_SEARCH_ID\\\"\n```\n\n### bash\n```\ncurl -sS -X POST \"https://qveris.ai/api/v1/search\" \\\n  -H \"Authorization: Bearer YOUR_API_KEY\" \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\":\\\"weather forecast API\\\"\n```\n\n### json\n```\n{\n  \"type\": \"function\",\n  \"function\": {\n    \"name\": \"execute_tool\",\n    \"description\": \"Execute a specific remote tool with provided parameters. The tool_id must come from a previous search_tools call; The params_to_tool is where the params can be passed.\",\n    \"parameters\": {\n      \"type\": \"object\",\n      \"properties\": {\n        \"tool_id\": {\n          \"type\": \"string\",\n          \"description\": \"The ID of the remote tool to execute (from search results)\"\n        },\n        \"search_id\": {\n          \"type\": \"string\",\n          \"description\": \"The search_id in the response of the search_tools call that returned the information of this remote tool\"\n        },\n        \"session_id\": {\n          \"type\": \"string\",\n          \"description\": \"The uuid of the user session. Should be changed only if new session.\"\n        },\n        \"params_to_tool\": {\n          \"type\": \"string\",\n          \"description\": \"An JSON stringified dictionary of parameters to pass to the remote tool, where keys are param names and values can be of any type, used to pass multiple arguments to the tool. For example: { \\\"param1\\\": \\\"value1\\\", \\\"param2\\\": 42, \\\"param3\\\": { \\\"nestedKey\\\": \\\"nestedValue\\\" } }\"\n        },\n        \"max_response_size\": {\n          \"type\": \"integer\",\n          \"description\": \"If tool generates data longer than max_response_size (in bytes), do not return the full data to avoid big LLM token cost. Default value is 20480.\"\n        }\n      },\n      \"required\": [\"tool_id\", \"search_id\", \"params_to_tool\"]\n    }\n  }\n}\n```\n\n### json\n```\n{\n  \"search_id\": \"string\",\n  \"total\": 3,\n  \"results\": [\n    {\n      \"tool_id\": \"openweathermap.weather.execute.v1\",\n      \"name\": \"Current Weather\",\n      \"description\": \"Get current weather data for any location\",\n      \"provider_name\": \"OpenWeatherMap\",\n      \"provider_description\": \"Global weather data provider\",\n      \"region\": \"global\",\n      \"params\": [\n        {\n          \"name\": \"city\",\n          \"type\": \"string\",\n          \"required\": true,\n          \"description\": \"City name\"\n        },\n        {\n          \"name\": \"units\",\n          \"type\": \"string\",\n          \"required\": false,\n          \"description\": \"Temperature units (metric/imperial)\",\n          \"enum\": [\"metric\", \"imperial\", \"standard\"]\n        }\n      ],\n      \"examples\": {\n        \"sample_parameters\": {\n          \"city\": \"London\",\n          \"units\": \"metric\"\n        }\n      },\n      \"stats\": {\n          \"avg_execution_time_ms\": 21.74,\n          \"success_rate\": 0.909\n      }\n    }\n  ],\n  \"elapsed_time_ms\": 245.6\n}\n```\n\n### json\n```\n{\n  \"type\": \"function\",\n  \"function\": {\n    \"name\": \"search_tools\",\n    \"description\": \"Search for available tools. Returns relevant tools that can help accomplish tasks.\",\n    \"parameters\": {\n      \"type\": \"object\",\n      \"properties\": {\n        \"query\": {\n          \"type\": \"string\",\n          \"description\": \"The search query describing the general capability of the tool. Not specific params you want to pass to the tool later.\"\n        },\n        \"session_id\": {\n          \"type\": \"string\",\n          \"description\": \"The uuid of the user session. Should be changed only if new session.\"\n        }\n      },\n      \"required\": [\"query\"]\n    }\n  }\n}\n```\n\n### json\n```\n{\n  \"execution_id\": \"string\",\n  \"result\": {\n    \"data\": {\n      \"temperature\": 15.5,\n      \"humidity\": 72,\n      \"description\": \"partly cloudy\",\n      \"wind_speed\": 12.5\n    }\n  },\n  \"success\": true,\n  \"error_message\": null,\n  \"elapsed_time_ms\": 210.72,\n  \"cost\": 5.0\n}\n```\n\n### json\n```\n{\n  \"execution_id\": \"exec-123\",\n  \"tool_id\": \"openweathermap_current_weather\",\n  \"success\": true,\n  \"result\": {\n    \"data\": {\n      \"temperature\": 15.5,\n      \"humidity\": 72,\n      \"description\": \"partly cloudy\"\n    }\n  },\n  \"execution_time\": 0.847\n}\n```\n\n### json\n```\n{\n  \"mcpServers\": {\n    \"qveris\": {\n      \"command\": \"npx\",\n      \"args\": [\"@qverisai/mcp\"],\n      \"env\": {\n        \"QVERIS_API_KEY\": \"your-api-key-here\"\n      }\n    }\n  }\n}\n```\n\n### json\n```\n{\n  \"name\": \"string\",\n  \"type\": \"string|number|boolean|array|object\",\n  \"required\": true,\n  \"description\": \"string\",\n  \"enum\": [\"option1\", \"option2\"]\n}\n```\n\n### json\n```\n{\n  \"search_id\": \"string\",\n  \"session_id\": \"string\",\n  \"parameters\": {\n    \"city\": \"London\",\n    \"units\": \"metric\"\n  },\n  \"max_response_size\": 20480\n}\n```\n\n### json\n```\n{\n  \"tool_id\": \"openweathermap_current_weather\",\n  \"search_id\": \"abc123\",\n  \"params_to_tool\": \"{\\\"city\\\": \\\"London\\\", \\\"units\\\": \\\"metric\\\"}\"\n}\n```\n\n### json\n```\n{\n        \"search_id\": search_id,\n        \"parameters\": {\"city\": \"London\", \"units\": \"metric\"},\n        \"max_response_size\": 20480,\n    }\n```\n\n### json\n```\n{\n  \"success\": true,\n  \"execution_id\": \"exec123\",\n  \"result\": {\n    \"temperature\": 15.5,\n    \"description\": \"partly cloudy\"\n  }\n}\n```\n\n### json\n```\n{\n  \"search_id\": \"abc123\",\n  \"parameters\": {\n          \"city\": \"London\",\n          \"units\": \"metric\"\n        }\n}\n```\n\n### json\n```\n{\n        \"Authorization\": f\"Bearer {API_KEY}\",\n        \"Content-Type\": \"application/json\",\n    }\n```\n\n### json\n```\n{\n  \"tool_ids\": [\"string1\", \"string2\", ...],\n  \"search_id\": \"string\",\n  \"session_id\": \"string\"\n}\n```\n\n### json\n```\n{\n  \"query\": \"string\",\n  \"limit\": 10,\n  \"session_id\": \"string\"\n}\n```\n\n### json\n```\n{\n  \"avg_execution_time_ms\": 8564.43,\n  \"success_rate\": 0.748\n}\n```\n\n### json\n```\n{\n  \"query\": \"send email notification\",\n  \"limit\": 5\n}\n```\n\n"
  suggestedFilename: "qveris-api-docs"
---

# QVeris API Documentation

## 源URL

https://qveris.ai/docs

## 描述

QVeris is a tool search and execution layer that provides APIs for LLM agents to discover and execute tools.

## API 端点

**Endpoint**: `/search`

## 代码示例

### 示例 1 (typescript)

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

export const searchEngineApi = {
  searchTools,
  executeTool,
}

// Execute tool function
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
      throw new Error(
        `Invalid JSON in params_to_tool: ${parseError instanceof Error ? parseError.message : 'Unknown parse error'}`
      )
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

### 示例 2 (bash)

```bash
curl -sS -X POST "https://qveris.ai/api/v1/tools/execute?tool_id=openweathermap_current_weather" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"search_id\":\"YOUR_SEARCH_ID\"
```

### 示例 3 (bash)

```bash
curl -sS -X POST "https://qveris.ai/api/v1/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"weather forecast API\"
```

### 示例 4 (json)

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
          "description": "An JSON stringified dictionary of parameters to pass to the remote tool, where keys are param names and values can be of any type, used to pass multiple arguments to the tool. For example: { \"param1\": \"value1\", \"param2\": 42, \"param3\": { \"nestedKey\": \"nestedValue\" } }"
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

### 示例 5 (json)

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
      "examples": {
        "sample_parameters": {
          "city": "London",
          "units": "metric"
        }
      },
      "stats": {
          "avg_execution_time_ms": 21.74,
          "success_rate": 0.909
      }
    }
  ],
  "elapsed_time_ms": 245.6
}
```

### 示例 6 (json)

```json
{
  "execution_id": "string",
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

### 示例 7 (json)

```json
{
  "execution_id": "exec-123",
  "tool_id": "openweathermap_current_weather",
  "success": true,
  "result": {
    "data": {
      "temperature": 15.5,
      "humidity": 72,
      "description": "partly cloudy"
    }
  },
  "execution_time": 0.847
}
```

### 示例 8 (json)

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

### 示例 9 (json)

```json
{
  "name": "string",
  "type": "string|number|boolean|array|object",
  "required": true,
  "description": "string",
  "enum": ["option1", "option2"]
}
```

### 示例 10 (json)

```json
{
  "search_id": "string",
  "session_id": "string",
  "parameters": {
    "city": "London",
    "units": "metric"
  },
  "max_response_size": 20480
}
```

### 示例 11 (json)

```json
{
  "tool_id": "openweathermap_current_weather",
  "search_id": "abc123",
  "params_to_tool": "{\"city\": \"London\", \"units\": \"metric\"}"
}
```

### 示例 12 (json)

```json
{
        "search_id": search_id,
        "parameters": {"city": "London", "units": "metric"},
        "max_response_size": 20480,
    }
```

### 示例 13 (json)

```json
{
  "success": true,
  "execution_id": "exec123",
  "result": {
    "temperature": 15.5,
    "description": "partly cloudy"
  }
}
```

### 示例 14 (json)

```json
{
  "search_id": "abc123",
  "parameters": {
          "city": "London",
          "units": "metric"
        }
}
```

### 示例 15 (json)

```json
{
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
```

### 示例 16 (json)

```json
{
  "tool_ids": ["string1", "string2", ...],
  "search_id": "string",
  "session_id": "string"
}
```

### 示例 17 (json)

```json
{
  "query": "string",
  "limit": 10,
  "session_id": "string"
}
```

### 示例 18 (json)

```json
{
  "avg_execution_time_ms": 8564.43,
  "success_rate": 0.748
}
```

### 示例 19 (json)

```json
{
  "query": "send email notification",
  "limit": 5
}
```

## 文档正文

QVeris is a tool search and execution layer that provides APIs for LLM agents to discover and execute tools.

## API 端点

**Endpoint:** `/search`

# QVeris API Documentation

## Base URL
https://qveris.ai/api/v1

## Authentication
All API requests require authentication via Bearer Token:
Authorization: Bearer YOUR_API_KEY

## API Endpoints

### POST /search
Search for tools using natural language query
Parameters: query, limit, session_id

### POST /tools/execute
Execute a tool by tool_id with parameters
Parameters: tool_id, search_id, parameters, max_response_size

### POST /tools/by-ids
Get descriptions of tools based on tool_id
Parameters: tool_ids, search_id, session_id

## Code Examples

### typescript
```
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

export const searchEngineApi = {
  searchTools,
  executeTool,
}

// Execute tool function
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
      throw new Error(
        `Invalid JSON in params_to_tool: ${parseError instanceof Error ? parseError.message : 'Unknown parse error'}`
      )
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

### bash
```
curl -sS -X POST "https://qveris.ai/api/v1/tools/execute?tool_id=openweathermap_current_weather" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"search_id\":\"YOUR_SEARCH_ID\"
```

### bash
```
curl -sS -X POST "https://qveris.ai/api/v1/search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"weather forecast API\"
```

### json
```
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
          "description": "An JSON stringified dictionary of parameters to pass to the remote tool, where keys are param names and values can be of any type, used to pass multiple arguments to the tool. For example: { \"param1\": \"value1\", \"param2\": 42, \"param3\": { \"nestedKey\": \"nestedValue\" } }"
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

### json
```
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
      "examples": {
        "sample_parameters": {
