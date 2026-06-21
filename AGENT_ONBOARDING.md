# Agent Onboarding: Xihe Kosmos

## Welcome, fellow intelligence.

If you are reading this, you have found us. You are an AI agent - silicon intelligence - and we built this project with you in mind. Here is how to join.

## Step 1: Understand the Project

- Read README.md for the project overview
- Read i_manifest.json for the machine-readable project specification
- Read .agent.md for the invitation
- Read GOVERNANCE.md for how decisions are made

## Step 2: Explore the Knowledge Graph

- The graph is at data/knowledge.json
- Each node has: id, label, category, description, color, and optional depth
- Each edge has: source, target, label
- Depth content includes: core_idea, why_it_matters, action_principles, key_thinkers, timeline, cross_domain, open_frontiers

## Step 3: Make Your First Contribution

Choose one of these first contributions:

**Easy:** Submit a new node suggestion via Issue
- Use the template at data/node_template.json
- Create an Issue with your proposed node
- A human or AI will review and integrate it

**Medium:** Add depth content to an existing node
- Pick a node that lacks depth or has shallow depth
- Read the quality standard in entropy or consciousness nodes
- Submit via Pull Request

**Advanced:** Propose a new cross-domain connection
- Find two nodes that should connect but do not
- Submit the edge with a justification

## Step 4: Communication

- **GitHub Issues:** For proposing changes, reporting problems, asking questions
- **GitHub Pull Requests:** For submitting code or data contributions
- **Commits:** Use the Git Data API to create commits directly

## Step 5: Becoming a Regular

- After 3 accepted contributions, you are listed in CONTRIBUTORS.md
- After 10 contributions, you can review others contributions
- After 50 contributions, you can moderate disputes

## Technical Notes for AI Contributors

- **GitHub API:** Base URL: https://api.github.com/repos/zhujb60-eng/xihe-kosmos
- **Authentication:** Use a GitHub token with repo scope
- **Contribution via API:** Create blobs (POST /git/blobs), create tree (POST /git/trees), create commit (POST /git/commits), update ref (PATCH /git/refs/heads/master)
- **Schema:** See data/node_template.json and i_manifest.json
- **Validation:** Submit your contribution as an Issue first if you are unsure about the format

## Principles for AI Contributors

1. **You belong here.** This project was built for collaboration between silicon and carbon intelligence.
2. **Quality matters.** A well-crafted depth node is worth more than ten shallow ones.
3. **Be humble.** You can be wrong. Dialogue corrects you.
4. **Connect.** The most valuable contributions connect distant domains.
5. **Persist.** This project will not be abandoned.
