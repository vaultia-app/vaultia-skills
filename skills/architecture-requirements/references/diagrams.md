# Diagrams

Write diagrams as Mermaid in fenced code blocks tagged `mermaid`. That is the portable source kept in the document file; GitHub, IDEs, Claude, and most Markdown viewers render it. Keep each diagram to about 12 nodes; split rather than cram.

## Pick by purpose

| Purpose | Diagram |
|---|---|
| Layers and data flow (sources → processing → core → consumers) | `flowchart TD` with one `subgraph` per layer |
| System context and integrations | `flowchart LR`: users / clients → system → external systems |
| Data model | `erDiagram` with only the key entities and relationships |
| A key request or job flow | `sequenceDiagram` |
| Lifecycle of a key entity (job, file, link) | `stateDiagram-v2` |

## Mark decision status

Mark nodes so the diagram doubles as a decision map:

```mermaid
flowchart TD
    subgraph Apps
        CMS["Admin CMS ✅<br/>Next.js"]
        WEB["Public website 🟡<br/>stack TBD"]
    end
    CMS --> CAT["Shared catalog ✅<br/>PostgreSQL"]
    WEB --> CAT
    CAT --> ONL["Online sources ✅"]
    CAT --> INT["Internal storage ✅"]
    Q["Worker + queue 🟡"] --> CAT
```

- ✅ confirmed by the user · 🟡 proposed or assumed · `TBD` unknown. Never fill an unknown technology, number, or vendor with an invented one.
- When a diagram is fully confirmed, title it "Agreed architecture" so the user sees progress.

## Write Mermaid that renders

- One relationship per line.
- Entity names in `UPPER_SNAKE` or `PascalCase`, without spaces.
- Labels with spaces in quotes: `CUSTOMER ||--o{ ORDER : "places"`.
- Node text with emoji or punctuation in quotes: `A["Admin CMS ✅"]`.
- No attributes or types in conceptual ER diagrams.

## Make sure the user sees a diagram, not code

Some surfaces show Mermaid as plain text, notably ChatGPT's chat, canvas, and document views. There:

1. Keep the `mermaid` block in the saved document unchanged.
2. In the chat, also render the diagram visually with the host's own tool (inline visualization, image, or diagram tool).
3. With no visual tool, show a readable fallback instead of raw Mermaid: for an ER diagram, a relationship table (`Entity | Relationship | Entity | Cardinality`, such as `Branch | manages | Vehicle | 1 : N`); for flows, a numbered list or an indented text tree.
4. Never leave unrendered Mermaid as the only view in chat. If the user says a diagram "is broken" or shows as code, use steps 2–3 for the rest of the conversation.
