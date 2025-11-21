import os
from datetime import datetime

def generate_cover_letter(job_data, resume_type, personal_info, template_prompt=None):
    """
    Generates a cover letter based on the job and resume type.
    
    Args:
        job_data (dict): Contains Job_Title, Job_ID, Department, Description.
        resume_type (str): DATA, RESEARCH, or ADMIN.
        personal_info (dict): User's contact details.
        template_prompt (str): Optional custom prompt/template.
        
    Returns:
        str: The generated cover letter text.
    """
    
    # Default Template Structure
    date_str = datetime.now().strftime("%B %d, %Y")
    
    # Extract key info
    title = job_data.get("Job_Title", "Position")
    job_id = job_data.get("Job_ID", "")
    dept = job_data.get("Department", "Hiring Committee")
    
    # Basic customization based on Resume Type
    skills_highlight = ""
    if resume_type == "DATA":
        skills_highlight = "My background in data analysis, Python, and SQL allows me to transform complex datasets into actionable insights."
    elif resume_type == "RESEARCH":
        skills_highlight = "My experience in laboratory research, experimental design, and technical documentation aligns well with the scientific rigor required for this role."
    elif resume_type == "ADMIN":
        skills_highlight = "My strong organizational skills, project management experience, and ability to coordinate across departments make me an ideal candidate."
    
    # Construct the letter
    # Note: In a real production agent with LLM access, we would call the LLM here.
    # Since I am a code-generation agent building a script, I will create a robust template.
    
    letter = f"""{date_str}

Hiring Committee
{dept}
University at Buffalo
Buffalo, NY

Re: Application for {title} (Job ID: {job_id})

Dear Hiring Committee,

I am writing to express my enthusiastic interest in the {title} position within the {dept} at the University at Buffalo. As a driven professional with a strong commitment to academic and operational excellence, I am eager to contribute my skills to your team.

{skills_highlight} I have carefully reviewed the job description and am confident that my experience aligns perfectly with the requirements of this role. I am particularly drawn to this opportunity because of UB's reputation for innovation and community impact.

In my previous roles, I have demonstrated the ability to adapt quickly, solve complex problems, and collaborate effectively with diverse stakeholders. I am eager to bring this same level of dedication and performance to the {dept}.

Thank you for your time and consideration. I look forward to the possibility of discussing how my background and skills would be a great fit for your team.

Sincerely,

{personal_info.get('first_name', 'Prabhu')} {personal_info.get('last_name', 'Kiran')}
{personal_info.get('email', '[Email]')}
{personal_info.get('phone', '[Phone]')}
"""
    return letter

def save_cover_letter(letter, job_id, output_dir):
    filename = os.path.join(output_dir, f"Cover_Letter_{job_id}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(letter)
    return filename
