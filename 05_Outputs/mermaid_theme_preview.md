# Mermaid 主题预览

本文档展示所有可用的 Mermaid 主题效果。

---

## 1. Default 主题（默认）

```mermaid
%%{init: {'theme':'default'} }%%
graph TD
    A[开始] --> B{判断}
    B -->|是| C[处理A]
    B -->|否| D[处理B]
    C --> E[结束]
    D --> E

    style A fill:#e1f5ff
    style B fill:#fff4e6
    style C fill:#e8f5e9
    style D fill:#fce4ec
    style E fill:#e8f6f3
```

**特点**: 清爽明亮，适合日常文档

---

## 2. Dark 主题（深色）

```mermaid
%%{init: {'theme':'dark'} }%%
graph TD
    A[开始] --> B{判断}
    B -->|是| C[处理A]
    B -->|否| D[处理B]
    C --> E[结束]
    D --> E
```

**特点**: 深色背景，适合夜间模式

---

## 3. Forest 主题（森林）

```mermaid
%%{init: {'theme':'forest'} }%%
graph TD
    A[开始] --> B{判断}
    B -->|是| C[处理A]
    B -->|否| D[处理B]
    C --> E[结束]
    D --> E
```

**特点**: 绿色调，自然清新

---

## 4. Neutral 主题（中性）

```mermaid
%%{init: {'theme':'neutral'} }%%
graph TD
    A[开始] --> B{判断}
    B -->|是| C[处理A]
    B -->|否| D[处理B]
    C --> E[结束]
    D --> E
```

**特点**: 灰色调，专业商务

---

## 如何切换主题

### VSCode 设置

在 `.vscode/settings.json` 中：

```json
{
  "mermaid.theme": "forest"  // default/dark/forest/neutral
}
```

### 在 Markdown 中局部指定

```mermaid
%%{init: {'theme':'dark'} }%%
graph LR
    A --> B
```

---

**生成日期**: 2026-01-16
