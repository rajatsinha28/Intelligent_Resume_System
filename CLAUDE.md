# AI-Powered Tailored Resume Generator

## Project Overview
Build an AI-powered Resume Tailoring System that transforms an individual's existing resume into a highly ATS-optimized, job-specific resume based on a provided Job Description.

The final application should function like a professional resume optimization platform rather than a simple prompt wrapper.

## Existing Resources
- `index.md` file contains the complete LaTeX structure that every generated resume must follow
- Treat this file as the source of truth for formatting
- The AI should preserve this layout while only changing the content
- No new formatting should be invented unless explicitly instructed

## Core Requirements
- Input: Job Description (text or PDF) + Current Resume (PDF)
- Output: New tailored resume (PDF using provided LaTeX template)
- Must be:
  - ATS optimized
  - Keyword optimized
  - Truthful (no fabricated experience, companies, projects, certifications, education, achievements, or years of experience)
  - Professionally written
  - Properly formatted
- Everything added must be inferred from the existing resume or explicitly approved by the user

## Long-Term Vision
Build as a modular, production-grade, multi-agent AI system where:
- Specialized agents collaborate under an orchestrator
- Each agent has clearly defined responsibility and operates independently
- Agents produce structured outputs consumable by downstream agents
- Orchestrator coordinates workflow, validates intermediate outputs, assembles final resume
- Architecture is scalable, maintainable, and extensible for future additions

## Expected User Workflow
1. Open web application
2. Upload resume PDF
3. Upload or paste Job Description
4. Click "Generate Tailored Resume"
5. Receive:
   - Professionally tailored resume
   - Formatted using provided LaTeX template
   - Compiled into PDF
   - Optionally: supporting insights (ATS score, keyword analysis, change summary)

## Guiding Principles
Prioritize throughout design:
- Modularity
- Production readiness
- Maintainability
- Scalability
- Clear separation of responsibilities
- Structured communication between agents
- High-quality prompt engineering
- Deterministic workflows where appropriate
- Minimal hallucinations
- Fact preservation
- ATS optimization
- Clean software architecture

## Important Implementation Notes
- DO NOT propose architecture, implementation plan, agent design, code, prompts, workflows, or technologies yet
- ONLY absorb and understand the complete project context
- WAIT for next instructions before producing any design or implementation details
- DO NOT generate any code at this stage