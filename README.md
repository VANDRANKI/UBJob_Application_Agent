# 🤖 UB Job Application Agent, Built from Scratch

> **"Automating my job search with precision and zero effort."**

---

## 🌟 Overview  
I built a fully automated agent that logs into the University at Buffalo job portal, scans newly posted jobs, analyzes each description, selects the best-fit resume, generates a tailored cover letter, fills out the job application form, uploads all required documents, and submits the application.

This is my **UB Job Application Agent**; end-to-end automation for job applications at UB.

---

## 🏗️ How I Built It  

I constructed this system step by step, ensuring every module works independently and together.

### **1. Scraper (Job Reader) 👀**
- Opens UB Jobs using **Playwright**.
- Extracts job titles, departments, posting dates, and descriptions.
- Filters jobs to only include those posted within the last **7 days**.

### **2. Classifier (Keyword Matcher) 🧠**
- Reads each job description.
- Counts relevant keywords.
- Matches the job to the correct resume type:
  - **DATA Resume**
  - **RESEARCH Resume**
  - **ADMIN Resume**

### **3. Writer (Cover Letter Generator) ✍️**
- Loads my prepared template.
- Inserts job-specific details (title, department, skills).
- Saves each cover letter in `generated_docs/`.

### **4. Form Filler (Applicant Bot) 🖐️**
- Types all required personal information.
- Fills Education → Experience → Skills → References.
- Uploads the selected resume and generated letter.
- Clicks **Submit** after validation.

---

## 🗺️ Workflow Diagram --> Full Blueprint

```mermaid
flowchart TD
    %% Nodes
    Start([🚀 Start Agent])
    Login[🔐 Phase 1: Login]
    Search[🔎 Phase 2: Search Jobs]
    
    %% Decisions
    CheckLogin{Login Successful?}
    CheckDate{Posted Within 7 Days?}
    CheckMatch{Resume Match?}
    
    %% Actions
    Scrape[📄 Scrape Job Details]
    Gen[📝 Generate Cover Letter]
    Fill[✍️ Fill Application Form]
    Upload[📤 Upload Documents]
    Submit[✅ Submit Application]
    Log[💾 Log Application]
    
    %% Flow
    Start --> Login
    Login --> CheckLogin
    CheckLogin -- No --> End([❌ Stop: Login Failed])
    CheckLogin -- Yes --> Search
    
    Search --> Scrape
    Scrape --> CheckDate
    CheckDate -- No --> Log
    CheckDate -- Yes --> Analyze[🧠 Phase 3: Analyze Job]
    
    Analyze --> CheckMatch
    CheckMatch -->|Data/SQL| R1[Use DATA Resume]
    CheckMatch -->|Research/Lab| R2[Use RESEARCH Resume]
    CheckMatch -->|Admin/Office| R3[Use ADMIN Resume]
    
    R1 & R2 & R3 --> Gen
    Gen --> Fill
    
    subgraph FormFilling [Phase 4: Application Filling]
    Fill --> F1[Personal Info]
    F1 --> F2[Education]
    F2 --> F3[Experience]
    F3 --> F4[References]
    end
    
    F4 --> Upload
    Upload --> Submit
    Submit --> Log
    Log --> Loop{More Jobs?}
    Loop -- Yes --> Search
    Loop -- No --> Finish([🏁 Task Complete])
