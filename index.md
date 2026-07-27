%-------------------------
% Resume in LaTeX
% Based on the classic "Jake's Resume" style structure
% Compile with pdflatex
%-------------------------

\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{multicol}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large\bfseries
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure PDF is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    #1 \vspace{-2pt}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=0.15in]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%

\begin{document}

%----------HEADING----------
\begin{center}
    \textsc{\Huge \scshape Rajat Sinha} \\ \vspace{1pt}
    \small Lucknow, Uttar Pradesh \\ \vspace{1pt}
    \small \Mobilefone\ +918896647475 ~
    \href{mailto:rajatsinhaa28@gmail.com}{\Letter\ \underline{rajatsinhaa28@gmail.com}} ~
    \href{https://www.linkedin.com/in/rajatsinha28}{\underline{LinkedIn}}  ~
    \href{https://github.com/rajatsinha28}{\underline{GitHub}}
    \vspace{-8pt}
\end{center}

% SUMMARY
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section*{Summary}

Software Engineer with 2 years of experience across test automation and full-stack frontend development at TCS, now building React interfaces and exploring applied AI/LLM systems — including a multi-agent research pipeline built with LangGraph and LangChain. Comfortable owning work end-to-end, from automation frameworks to production UI to agentic AI tooling.

%-----------EDUCATION-----------
\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {Chandigarh University}{Oct 2020 -- Jun 2024}
      {Bachelor of Engineering in Computer Science}{Mohali, Punjab}
  \resumeSubHeadingListEnd

%-----------EXPERIENCE-----------
\section{Experience}
  \resumeSubHeadingListStart

    \resumeSubheading
      {Tata Consultancy Services}{June 2025 -- Present}
      {Software Engineer (Frontend Developer)}{Bhubaneswar, Odisha}
      \resumeItemListStart
        \resumeItem{Built and integrated REST APIs for React-based interfaces, cutting UI latency by nearly 25\% through component optimization and asynchronous data loading.}
        \resumeItem{Resolved production defects and kept the codebase CI-ready using Git, working directly with QA and product teams to ship reliable releases.}
        \resumeItem{Built reusable, responsive React components across features, reducing duplicate UI logic across views.}
      \resumeItemListEnd

    \resumeSubheading
      {Tata Consultancy Services}{July 2024 -- May 2025}
      {Automation Tester}{Bhubaneswar, Odisha}
      \resumeItemListStart
        \resumeItem{Led full regression testing across 100+ automated test scenarios covering country-specific workflows, ensuring release-readiness across markets.}
        \resumeItem{Designed and built a Selenium WebDriver automation framework from scratch using Cucumber, TestNG, JUnit, and Maven, reducing regression execution time by 20-25\%.}
        \resumeItem{Owned framework architecture within a QA team, coordinating scenario coverage and execution across releases.}
      \resumeItemListEnd

  \resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
    \resumeSubHeadingListStart
      \resumeProjectHeading
          {\textbf{\href{https://github.com/rajatsinha28/Multi-Agent-Research-System-Basic}{Multi-Agent-Research \& Report Generation System}} $|$ \emph{Python, LangGraph, LangChain, Tavily API}}{}
          \resumeItemListStart
            \resumeItem{Designed 8 specialized agents (Planner, Research, Search, Web Scraper, Citation, Writer, Reviewer, Critic) with LangGraph, cutting manual research-to-report time from hours to minutes per topic.}
            \resumeItem{Built a RAG pipeline combining the Tavily Search API, web scraping, and LLM synthesis to auto-generate a detailed, citation-backed research paper as a final PDF, including facts, figures, tables, and references.}
            \resumeItem{Implemented shared-state orchestration across agents so failures at one stage (e.g., scraping) trigger automatic retries without restarting the full pipeline.}
          \resumeItemListEnd
      \resumeProjectHeading
          {\textbf{Personal Portfolio} $|$ \emph{Claude, Claude Code, Framer Motion, 21st.dev}}{}
          \resumeItemListStart
            \resumeItem{Designed and built a personal portfolio site using an AI-assisted development workflow with Claude and Claude Code.}
            \resumeItem{Used Framer Motion for interaction/animation design and 21st.dev for UI component composition.}
          \resumeItemListEnd
      \resumeProjectHeading
          {\textbf{\href{https://github.com/rajatsinha28/Task-Management}{Role-Based Access Control System}} $|$ \emph{MongoDB, Express.js, React.js, Node.js}}{}
          \resumeItemListStart
            \resumeItem{Built a full-stack MERN app with JWT authentication and role-based access control for user and task management.}
            \resumeItem{Designed RESTful APIs and indexed MongoDB schemas, improving query response times on core task-lookup endpoints.}
            \resumeItem{Built reusable React components in a modular frontend architecture, cutting time to add new task views by reusing shared UI logic.}
          \resumeItemListEnd
    \resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
 \begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
     \textbf{Languages}{: Python, Java, JavaScript (ES6+), SQL} \\
     \textbf{AI \& LLM}{: LangGraph, LangChain, Prompt Engineering, Retrieval-Augmented Generation (RAG), Multi-Agent Orchestration} \\
     \textbf{Frontend}{: React.js, HTML5, CSS3, Responsive Web Design} \\
     \textbf{Backend}{: Node.js, Express.js, REST API Design} \\
     \textbf{Automation Testing}{: Selenium WebDriver, Cucumber, TestNG, JUnit, Maven, Regression Testing} \\
     \textbf{Developer Tools}{: Git, GitHub, Docker, Linux, Postman, CI/CD}
    }}
 \end{itemize}
 \vspace{-6pt}
%-------------------------------------------
\end{document}