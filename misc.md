# Miscellaneous Information
- This section contains additional information that may not fit into the other categories.
- It can include tips, tricks, or other relevant details that one should be aware of.

## Building AI-powered Solution - Workflows vs Agents

You can build an AI-powered solution by either creating Workflows or Agents
- ⁠Workflows are structured pipelines where LLMs and tools are orchestrated through predefined code paths.
    
    <img src="images/workflow.png" alt="workflow" width="600"/>

    Each step is explicit, like a recipe, with clear inputs, processes, and outputs.
- Agents, on the other hand, are systems where LLMs decides the next steps, selects tools, and maintains full control over how they accomplish tasks.

    <img src="images/agent.png" alt="agent" width="580"/>

    Agents operate in a loop, reasoning, acting, and adapting based on environmental feedback

When building applications with LLMs, find the simplest solution possible - increase complexity only when needed. This might mean not building agentic systems at all!

- Workflows are deterministic, making them predictable, testable, and cost-efficient.
- Agents offer flexibility but introduce complexity.

<img src="images/workflow_vs_agent.png" alt="agent" width="580"/>

**Rule of thumb** - Start thinking with workflows first as they offer predictability and consistency, switch to agents only when the problem cannot be solved with workflows.

### References
- https://www.anthropic.com/engineering/building-effective-agents
- https://langchain-ai.github.io/langgraph/tutorials/workflows
- https://medium.com/@neeldevenshah/ai-workflows-vs-ai-agents-vs-multi-agentic-systems-a-comprehensive-guide-f945d5e2e991

