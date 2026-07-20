# Communicating with Agents

This is a readme intended for human consumption covering the core topics of the lesson we are working on.

## Formats

- **JSON**: Structured, compactable, hard to read for humans.
- **YAML**: Structured, easier for humans to read.
- **Markdown**: Unstructured, easier for humans to read.

## Where do things go wrong with larger projects?

- Agents default to being eager.
- Agents don't have any memory at all.  If it's not in their context, it doesn't exist.
- Agents can be inconsistent in their approach
- Agents can have trouble with larger projects because parts fall out of the context
- Communication can be hard!
- Without a core design document agents can give wildly different results between runs.

## How can we avoid these things going wrong?

- Define rules for the agent to follow.
- Build out an architectural design document.
- Build out user flows to explain to the agent what something is being used for.
- Define out data types.

## Memory Banks

- These allow us to create a persistent memory for the agent
- They also allow us to break this memory up into smaller pieces that fit in the context window better.
