---
title: 概述
description: 将 LangGraph 代理渲染到前端
---

构建可实时可视化 LangGraph 流水线的前端。这些模式展示了如何渲染多步骤图形执行，包括每个节点的状态和来自自定义 `StateGraph` 工作流程的流式内容。

## 架构

LangGraph 图形由通过边连接的有名称节点组成。每个节点执行一个步骤（分类、研究、分析、综合）并将输出写入特定的状态键。在前端，`useStream` 提供对节点输出、流式 Token 和图形元数据的响应式访问，以便您可以将每个节点映射到 UI 卡片。

```mermaid
%%{
  init: {
    "fontFamily": "monospace",
    "flowchart": {
      "curve": "curve"
    }
  }
}%%
graph LR
  FRONTEND["useStream()"]
  GRAPH["StateGraph"]
  N1["节点 A"]
  N2["节点 B"]
  N3["节点 C"]

  GRAPH --"stream"--> FRONTEND
  FRONTEND --"submit"--> GRAPH
  GRAPH --> N1
  N1 --> N2
  N2 --> N3

  classDef blueHighlight fill:#DBEAFE,stroke:#2563EB,color:#1E3A8A;
  classDef greenHighlight fill:#DCFCE7,stroke:#16A34A,color:#14532D;
  classDef orangeHighlight fill:#FEF3C7,stroke:#D97706,color:#92400E;
  class FRONTEND blueHighlight;
  class GRAPH greenHighlight;
  class N1,N2,N3 orangeHighlight;
```

:::python

```python
from langgraph.graph import StateGraph, MessagesState, START, END

class State(MessagesState):
    classification: str
    research: str
    analysis: str

graph = StateGraph(State)
graph.add_node("classify", classify_node)
graph.add_node("research", research_node)
graph.add_node("analyze", analyze_node)
graph.add_edge(START, "classify")
graph.add_edge("classify", "research")
graph.add_edge("research", "analyze")
graph.add_edge("analyze", END)

app = graph.compile()
```

:::

:::js

```ts
import { StateGraph, StateSchema, MessagesValue, START, END } from "@langchain/langgraph";
import * as z from "zod";

const State = new StateSchema({
  messages: MessagesValue,
  classification: z.string(),
  research: z.string(),
  analysis: z.string(),
});

const graph = new StateGraph(State)
  .addNode("classify", classifyNode)
  .addNode("research", researchNode)
  .addNode("analyze", analyzeNode)
  .addEdge(START, "classify")
  .addEdge("classify", "research")
  .addEdge("research", "analyze")
  .addEdge("analyze", END)
  .compile();
```

:::

在前端，`useStream` 暴露 `stream.values` 用于已完成的节点输出，以及 `getMessagesMetadata` 用于识别每个流式 Token 是由哪个节点产生的。

```ts
import { useStream } from "@langchain/react";

function Pipeline() {
  const stream = useStream<typeof graph>({
    apiUrl: "http://localhost:2024",
    assistantId: "pipeline",
  });

  const classification = stream.values?.classification;
  const research = stream.values?.research;
  const analysis = stream.values?.analysis;
}
```

## 模式

<CardGroup cols={2}>
  <Card title="图形执行" icon="chart-dots" href="/oss/langgraph/frontend/graph-execution">
    可视化多步骤图形流水线，包括每个节点的状态和流式内容。
  </Card>
</CardGroup>

## 相关模式

[LangChain 前端模式](/oss/langchain/frontend/overview) — Markdown 消息、工具调用、乐观更新等 — 可与任何 LangGraph 图形配合使用。无论您使用 `createAgent`、`createDeepAgent` 还是自定义 `StateGraph`，`useStream` hook 都提供相同的核心 API。