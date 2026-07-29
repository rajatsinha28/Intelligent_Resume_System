"""
Orchestrator for the Resume Optimizer MVP.

This is a minimal skeleton that coordinates the workflow between agents.
In this MVP phase, it handles:
1. Loading input file paths (resume and job description)
2. Preparing output directories
3. Orchestrating the flow between agents (Extractor, JD Analyzer, Role Researcher implemented)
"""

import os
import json
from pathlib import Path
import sys


class ResumeOptimizerOrchestrator:
    """Orchestrates the resume optimization workflow."""

    def __init__(self):
        """Initialize the orchestrator and set up directories."""
        from config import INPUT_DIR, OUTPUT_DIR

        self.input_dir = Path(INPUT_DIR)
        self.output_dir = Path(OUTPUT_DIR)
        self.temp_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'temp'))

        # Ensure directories exist
        self._setup_directories()

        # Initialize data containers
        self.resume_data = None
        self.job_description = None
        self.job_description_analysis = None
        self.role_research = None
        self.gap_analysis = None
        self.optimized_resume = None
        self.critique = None

    def _setup_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

    def load_input_files(self, resume_filename: str = "resume.pdf",
                        jd_filename: str = "jd.txt") -> bool:
        """
        Load the resume and job description files.

        Args:
            resume_filename: Name of the resume file in input directory
            jd_filename: Name of the job description file in input directory

        Returns:
            bool: True if files loaded successfully, False otherwise
        """
        resume_path = self.input_dir / resume_filename
        jd_path = self.input_dir / jd_filename

        # Load job description (text file)
        if jd_path.exists():
            self.job_description = self._read_text_file(str(jd_path))
        else:
            print(f"Warning: Job description file not found: {jd_path}")
            self.job_description = ""

        # For resume, we'll just note the path exists - actual parsing
        # will be done by the extractor agent
        if resume_path.exists():
            self.resume_path = str(resume_path)
        else:
            print(f"Error: Resume file not found: {resume_path}")
            return False

        return True

    def _read_text_file(self, file_path: str) -> str:
        """
        Read text content from a file.

        Args:
            file_path: Path to the text file

        Returns:
            str: File contents
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Could not read file {file_path}: {e}")
            return ""

    def run_pipeline(self) -> bool:
        """
        Run the complete resume optimization pipeline.

        In this MVP, this implements:
        Step 1: Extractor Agent (resume data extraction)
        Step 2: JD Analyzer Agent (job description analysis)
        Step 3: Role Research Agent (role research based on JD analysis)
        Steps 4-6 are stubbed for future implementation.

        Returns:
            bool: True if pipeline completed successfully
        """
        print("Starting resume optimization pipeline...")

        # Step 1: Extract resume data (Extractor Agent)
        print("Step 1: Extracting resume data...")
        try:
            # Add agents directory to path so we can import extractor
            agents_dir = os.path.dirname(os.path.abspath(__file__))
            if agents_dir not in sys.path:
                sys.path.insert(0, agents_dir)

            # Import extractor here to avoid circular imports
            from extractor import extract_resume
            self.resume_data = extract_resume(self.resume_path)

            # Save the extracted resume data to output/resume.json
            output_path = self.output_dir / "resume.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.resume_data, f, indent=2)
            print(f"  -> Saved extracted resume data to {output_path}")
        except Exception as e:
            print(f"  -> Error in resume extraction: {e}")
            return False

        # Step 2: Analyze job description (JD Analyzer Agent)
        print("Step 2: Analyzing job description...")
        try:
            # Import jd_analyzer
            from jd_analyzer import analyze_jd
            self.job_description_analysis = analyze_jd(self.job_description)

            # Save the analyzed JD data to output/jd_analysis.json
            output_path = self.output_dir / "jd_analysis.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.job_description_analysis, f, indent=2)
            print(f"  -> Saved analyzed job description to {output_path}")
        except Exception as e:
            print(f"  -> Error in JD analysis: {e}")
            return False

        # Step 3: Research the role (Role Research Agent)
        print("Step 3: Researching the role...")
        try:
            # Import role_researcher
            from role_research import research_role
            self.role_research = research_role(self.job_description_analysis)

            # Save the role research data to output/role_analysis.json
            output_path = self.output_dir / "role_analysis.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.role_research, f, indent=2)
            print(f"  -> Saved role research data to {output_path}")
        except Exception as e:
            print(f"  -> Error in role research: {e}")
            return False

        # Step 4: Perform gap analysis (Gap Analyzer Agent) - TODO
        print("Step 4: Performing gap analysis...")
        # self.gap_analysis = gap_analyzer.analyze_gaps(
        #     self.resume_data,
        #     self.job_description_analysis,
        #     self.role_research
        # )

        # Step 5: Rewrite resume (Writer Agent) - TODO
        print("Step 5: Rewriting resume...")
        # self.optimized_resume = writer.rewrite_resume(
        #     self.resume_data,
        #     self.gap_analysis
        # )

        # Step 6: Critique the resume (Critic Agent) - TODO
        print("Step 6: Critiquing the resume...")
        # self.critique = critic.review_resume(self.optimized_resume)

        # Step 7: Save results - TODO
        print("Step 7: Saving results...")
        # self._save_results()

        print("Pipeline completed (extractor, JD analyzer, and role researcher implemented).")
        return True

    def _save_results(self) -> None:
        """Save the results of each stage to files in the output directory."""
        # This will be implemented in later phases
        pass

    def get_results(self) -> dict:
        """
        Get the results from each stage of the pipeline.

        Returns:
            Dict containing results from each stage
        """
        return {
            "resume_data": self.resume_data,
            "job_description": self.job_description,
            "job_description_analysis": self.job_description_analysis,
            "role_research": self.role_research,
            "gap_analysis": self.gap_analysis,
            "optimized_resume": self.optimized_resume,
            "critique": self.critique
        }


def main():
    """Main entry point for the resume optimizer."""
    print("Resume Optimizer MVP - Initializing...")

    # Initialize orchestrator
    orchestrator = ResumeOptimizerOrchestrator()

    # Load input files
    if not orchestrator.load_input_files():
        print("Failed to load input files. Please check the input directory.")
        return 1

    # Run the pipeline
    success = orchestrator.run_pipeline()

    if success:
        print("Resume optimization completed successfully!")
        # In a real implementation, we would save and display results here
    else:
        print("Resume optimization failed.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())