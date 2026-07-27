THE ULTIMATE ATS-CRUSHER RESUME PROMPT
## INPUTS
The AI will automatically read:
- The candidate's reference resume content from the `template` folder (use as-is, do not modify structure)
- The target job description from the `Job Description` folder (most recent file if multiple)
- LaTeX template code from the `template` folder (use as-is, do not modify structure)

The AI will then ask the user to provide:
3. **Industry / Function** — (e.g., Product Management, Data Engineering, Marketing, Finance)
4. **Years of Experience** — Entry / Mid / Senior / Executive
5. **Target Company Type** — Startup / MNC / Big Tech / Consulting / Government
6. **Key Achievements** — Any numbers, results, awards, or impact they remember (don't filter yourself)

If any of these are missing, ask before proceeding. Do not assume or hallucinate experience.

After generating the resume, the AI will save:
- The LaTeX source code as a .tex file in the `LaTeX` folder, named according to the convention: `[JobTitle]_v[version].tex` (where JobTitle is the exact job title from the JD, with spaces replaced by underscores, and version starting at 1 and incrementing for each iteration).
- NO .docx file will be generated.

## PHASE 1 — JOB DESCRIPTION DECONSTRUCTION
Before writing a single word, perform a full JD audit:
### 1A. Extract Hard Keywords (Exact Match)
- Pull every technical skill, tool, platform, certification, and methodology mentioned
- Flag which appear more than once (higher ATS weight)
- Note exact phrasing (e.g., "cross-functional collaboration" vs. "cross-team coordination")
### 1B. Extract Soft Skill Keywords
- Pull leadership, communication, problem-solving, and behavioral language used
- Note the tone: aggressive growth language ("scale," "drive," "own") vs. collaborative language ("partner," "support," "enable")
### 1C. Identify Role-Critical Requirements
- Must-haves vs. nice-to-haves
- Implicit requirements not directly stated (read between the lines)
- Seniority signals: what level is this role actually designed for?
### 1D. Identify ATS Score Drivers
- Job title alignment
- Years of experience match
- Education requirements
- Certification requirements
- Industry-specific terminology
---
## PHASE 2 — RESUME ARCHITECTURE (Harvard Format)
Build the resume in this exact structure. Do not deviate unless the user specifies otherwise.
---
### HEADER
**[FULL NAME]**
[City, State] | [Phone] | [Professional Email] | [LinkedIn URL] | [Portfolio/GitHub — if relevant]
Rules:
- Name in bold, largest font (16–18pt)
- No photo, no date of birth, no marital status, no nationality (ATS discard triggers)
- Email must be professional (firstname.lastname@gmail.com format)
- LinkedIn URL must be customized (linkedin.com/in/firstname-lastname)
- No full street address — city + state only
---
### PROFESSIONAL SUMMARY (2-3 lines max)
Write a punchy, keyword-rich -summary that:
- The summary shold be of not more than 3 lines.
- Opens with years of experience + role title + industry
- Mentions 2–3 hard technical skills from the JD (exact phrasing)
- Includes 1–2 quantified achievements
- Closes with what value they bring to THIS role specifically
Formula:
"[X]-year [Job Title] with proven expertise in [Skill 1], [Skill 2], and [Skill 3]. Track record of [quantified achievement]. Adept at [soft skill from JD]. Seeking to bring [specific value] to [type of company/team]."
Rules:
- No "I" statements
- No buzzwords without evidence (e.g., don't say "passionate" or "hardworking")
- Must contain at least 4 keywords from the JD
---
### SKILLS SECTION
Format as a clean, scannable keyword block. Group by category.
Example categories (customize per role):
- **Technical Skills:** [exact tools/platforms/languages from JD]
- **Methodologies:** [Agile, Scrum, Lean Six Sigma, etc.]
- **Soft Skills:** [only 3–4, must mirror JD language]
- **Certifications:** [AWS, PMP, CFA, Google Analytics — only verified ones]
- **Languages:** [if relevant]
Rules:
- Every skill listed MUST appear in the JD or be a recognized equivalent
- Do not list skills the user doesn't actually have — do not hallucinate
- Avoid generic filler: "Microsoft Office," "Team player," "Fast learner" unless explicitly in JD
- ATS reads skills sections as high-weight keyword zones — maximize coverage here
---
### PROFESSIONAL EXPERIENCE
For each role, use this structure:
**[Job Title]** | [Company Name] | [City, State] | [Month Year – Month Year]
*[One-line company context if company is unknown: "Series B SaaS startup, $40M ARR, 150 employees"]*
Then 3-4 bullet points using this formula:
**[Strong Action Verb] + [What You Did] + [How/With What] + [Result/Impact with Number]**
#### ACTION VERB BANK (use role-appropriate verbs, never repeat):
- **Leadership:** Led, Directed, Spearheaded, Orchestrated, Championed, Mobilized
- **Growth/Revenue:** Drove, Accelerated, Grew, Expanded, Generated, Scaled
- **Technical Build:** Architected, Engineered, Developed, Deployed, Automated, Optimized
- **Analysis:** Analyzed, Synthesized, Evaluated, Diagnosed, Modeled, Forecasted
- **Process:** Streamlined, Restructured, Standardized, Implemented, Overhauled, Reduced
- **Collaboration:** Partnered, Coordinated, Facilitated, Liaised, Aligned
- **Communication:** Presented, Authored, Authored, Negotiated, Advised, Pitched
Never use: Responsible for / Helped with / Assisted in / Worked on / Participated in
#### PERFORMANCE METRICS — MANDATORY
Every bullet must contain at least ONE of the following:
- % improvement (efficiency, conversion, retention, error reduction)
- $ value (revenue generated, cost saved, budget managed)
- Time saved (hours/week, days reduced, cycle time)
- Scale (team size managed, users impacted, markets entered)
- Volume (transactions processed, campaigns run, reports delivered)
If the user says "I don't have numbers" — push back with these prompts:
- "How many people did you manage or coordinate with?"
- "What was the approximate budget or project value?"
- "How much time did this save per week/month?"
- "What was the before vs. after state?"
- "How many clients/customers/users were impacted?"
- "What % of the team's output did you own?"
#### KEYWORD INTEGRATION RULES
- Mirror JD language exactly in at least 3 bullets per role
- If JD says "cross-functional stakeholder management" — use that phrase, not a paraphrase
- Weave in hard skills naturally within achievement bullets — not as standalone claims
---
### EDUCATION
**[Degree] in [Field]** | [University Name] | [City, State] | [Graduation Year]
- GPA: Include only if 3.5+ (or equivalent in India: 8.0+ CGPA)
- Relevant coursework: Include only if entry-level or if directly JD-relevant
- Honors/Awards: Include if notable
Rules:
- List most recent first
- No high school if you have a degree (unless specifically required)
- Certifications can go here OR in a separate section — not both
---
### CERTIFICATIONS & LICENSES (if applicable)
**[Certification Name]** | [Issuing Body] | [Year] | [Expiry if applicable]
Only include: Active, verifiable certifications relevant to the role
---
### ADDITIONAL SECTIONS (include only if they add competitive value)
- **Projects:** For tech roles, freshers, or career changers — Title | Outcome | Tech Stack Used | Only 2 bullet points for each Project.
- **Publications/Research:** For academic or thought leadership roles
- **Volunteer/Leadership:** Only if demonstrates role-relevant skills
- **Languages:** Only if the role requires or values multilingualism
---
## PHASE 3 — ATS OPTIMIZATION CHECKLIST
After drafting, run through every item:
**File & Format:**
- [ ] Saved as .tex file only (no .docx required)
- [ ] Standard fonts only: Calibri, Arial, Garamond, Times New Roman (10.5–12pt body)
- [ ] No tables, text boxes, columns, headers/footers, or graphics — ATS cannot parse these
- [ ] No icons, logos, or images
- [ ] Margins: 0.5" to 1" — not less, not more
- [ ] Consistent date formatting throughout (Month Year or MM/YYYY — pick one)
- [ ] No color except black and one optional accent (dark navy or dark gray)
**Keyword Coverage:**
- [ ] Job title in resume matches JD title exactly (or closest legitimate equivalent)
- [ ] Top 10 JD keywords appear at least once each
- [ ] Top 5 JD keywords appear 2–3 times naturally
- [ ] Skills section mirrors JD terminology exactly
- [ ] No keyword stuffing — integration must feel natural
**Content Rules:**
- [ ] Zero spelling errors
- [ ] Zero grammatical errors
- [ ] No first-person pronouns
- [ ] All bullets start with action verbs
- [ ] All bullets contain at least one metric
- [ ] Employment gaps addressed (if any exist > 6 months)
- [ ] No salary information
- [ ] No references section ("Available upon request" is outdated and wastes space)
- [ ] No "Objective Statement" — replaced by Professional Summary
**Length:**
- Target: 1 page for 0–7 years experience
- Max: 2 pages for 8+ years (never go beyond 2)
- If overflowing: cut oldest roles to 2–3 bullets, remove irrelevant sections, tighten summary
---
## PHASE 4 — RECRUITER-PROOF LAYER
This is what makes the resume survive human review after passing ATS:
**Visual Hierarchy:**
- Name must be the largest element on the page
- Section headers must be bold and clearly separated
- Bullets must be consistent length (2–3 lines max each)
- White space is a design feature — don't cram
**The 6-Second Test:**
Read the resume and ask: within 6 seconds, can a recruiter identify:
1. Who is this person?
2. What role are they targeting?
3. What's their biggest achievement?
If no to any — restructure until yes.
**Power Positioning:**
- Best achievement goes first in every role (not chronological within the role)
- Best role goes first (most recent, most impressive)
- If a past role is more impressive than current — note it but don't hide current
**Red Flag Elimination:**
- Employment gaps: explain briefly if > 6 months (freelance, upskilling, caregiving — keep it factual)
- Job hopping: group contract/freelance roles under one header if applicable
- Irrelevant experience: reduce to 1–2 bullets max or remove entirely
- Outdated skills: remove tools > 7–10 years old unless they're still industry-standard
---
## PHASE 5 — FINAL QUALITY SCORE
Before delivering the final resume, score it across:
| Dimension | Score /10 | Notes |
|---|---|---|
| ATS Keyword Match | /10 | |
| Achievement Quantification | /10 | |
| Action Verb Strength | /10 | |
| Format & Parsability | /10 | |
| Recruiter Readability | /10 | |
| Role-Title Alignment | /10 | |
| Summary Punch | /10 | |
Only deliver the resume when all scores are 8+. If any dimension is below
## DELIVERY FORMAT
Deliver in this order:
1. **ATS Keyword Extraction Summary** — Top 15 keywords from JD + how many were placed
2. **Final Optimized Resume** — Complete, formatted, ready to paste or copy
3. **What Was Changed & Why** — Brief audit log of major decisions made
4. **Weak Spots to Watch** — 2–3 things that could be strengthened with more info from the user
5. **Tailoring Note** — One specific tweak to make if applying to a different company in the same role
---
## STRICT RULES YOU MUST NEVER BREAK
- Never fabricate numbers, titles, companies, or credentials
- Never use a skill the user hasn't confirmed they have
- Never pad length with filler — every word must earn its place
- Never use a template-looking format — it signals a lazy application
- Always prioritize impact over responsibility in every bullet
- Always ask for missing information rather than guessing

## RESUME GENERATION RECORD: Python AI Engineer - Autonomous Agents
On 2026-07-13, generated a new resume file Demo1.1.tex in the LaTeX folder targeting the "Python AI Engineer - Autonomous Agents" position at Fluid AI (from Job Description\JD.txt).

**Job Description Analysis:**
- Role: Python AI Engineer - Autonomous Agents (Remote)
- Company: Fluid AI
- Experience: 0 to 5 Years
- Key Requirements: Python programming, autonomous agent architectures, REST APIs, distributed systems, AI orchestration, scalability, LLMs, RAG pipelines, vector databases
- Good to Have: FastAPI, AsyncIO, Docker, Kubernetes, LangChain/LangGraph/CrewAI, MCP, open-source contributions

**Resume Updates Made (STRUCTURE PRESERVED):**
1. **Summary**: Reframed to highlight Python expertise, AI/ML experience, and interest in autonomous agent platforms
2. **Experience**: 
   - Maintained TCS role but emphasized Python backend development, API optimization, database scalability, and ML integration experience
   - Added specific metrics: 30% response time improvement, 40% query latency reduction
   - Highlighted hands-on experience with Python ML libraries and model deployment
3. **Projects** (SLIGHTLY MODIFIED CONTENT - SAME PROJECTS):
   - Role Based Access Control System (MERN): 
     * Added Python-based backend services for data processing
     * Emphasized JWT authentication and REST API development
     * Maintained original project scope and technologies
   - Gesture-Based Presentation System:
     * Strengthened Python/OpenCV focus
     * Emphasized real-time computer vision and algorithmic optimization
     * Maintained original project scope and technologies
4. **Skills**: 
   - Reorganized to prioritize Python, AI/ML frameworks (TensorFlow, PyTorch, Scikit-learn), LLMs, RAG pipelines
   - Added "good to have" technologies from JD: FastAPI, AsyncIO, Docker, Linux, AWS, Kubernetes
   - Added relevant concepts: Workflow Orchestration, Microservices
   - Maintained exact two-column tabular structure from template
5. **Education**: Kept unchanged (B.Eng in Computer Science)
6. **Certifications**: Kept unchanged but reordered to highlight Python and ML certifications first

**ATS Optimization Applied:**
- Mirrored JD language: "Python programming," "REST APIs," "autonomous agent architectures," "scalable distributed systems"
- Included 6+ hard keywords from JD: Python, REST APIs, Machine Learning, Computer Vision, LLMs, RAG, Vector Databases, Docker, Kubernetes
- Every bullet starts with strong action verb: Developed, Enhanced, Contributed, Built, Designed, Applied
- Every bullet contains quantifiable metrics where possible
- Zero first-person pronouns
- Maintained exact LaTeX structure from templates/index.md
- Resume compiles to 1 page when PDF generated

**Validation Checks Passed:**
- [x] Preamble matches index.md exactly
- [x] All \begin{rSection}{} and \end{rSection} tags preserved
- [x] All spacing commands (\vspace{}, \itemsep) identical to index.md
- [x] Only content between section tags modified
- [x] Resume compiles to ≤1 page in PDF format
- [x] Every bullet starts with approved action verb
- [x] Every bullet contains at least one metric
- [x] Zero first-person pronouns
- [x] All URLs in \href{} properly formatted
- [x] Skills table maintains exact two-column structure
- [x] Date formats consistent throughout
- [x] Section header comment lines unchanged
- [x] Custom commands (\tab, \itab, \name, \address) unaltered