"""modules"""
import os
import re
import csv
import argparse
from pdfminer.high_level import extract_text

class EmailExtractor:
    """class to pair up functionalities"""
    def __init__(self, path, filename, not_found_path):
        self.output_file = filename
        self.resume_directory = path
        self.not_found_path = not_found_path

    def extract_emails(self, text):
        """extracting emails using regex from pdf pages"""
        email_pattern = r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+(?<![0-9])'
        match = re.search(email_pattern, text)
        if not match:
            return None
        return match.group()

    def read_pdf(self):
        """getting directory and reading pdfs"""
        all_emails = []
        for filename in os.listdir(self.resume_directory):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.resume_directory, filename)
                text = extract_text(file_path)
                extracted_emails = self.extract_emails(text)
                print(extracted_emails, file_path)
                if extracted_emails is None:
                    dest_path = os.path.join(self.not_found_path, filename)
                    os.rename(file_path, dest_path)
                all_emails.append(extracted_emails)
            else:
                dest_path = os.path.join(self.not_found_path, filename)
                os.rename(file_path, dest_path)
        return all_emails

    def write_csv(self, unique_emails):
        """writing emails in csv file"""
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Email'])
            for email in unique_emails:
                writer.writerow([email])

    def format_emails(self, emails):
        """formatting emails"""
        for i, email in enumerate(emails):
            if email is not None:
                parts = email.split('.')
                if parts[-1] == 'c' or parts[-1] == 'co' or parts[-1] == '':
                    parts[-1] = 'com'
                    emails[i] = '.'.join(parts)
        return emails

def main():
    """main function"""

    parser = argparse.ArgumentParser(description="Extracting emails from pdf resumes.")
    parser.add_argument("-O", "--output", type=str, help="output file name")
    parser.add_argument("path", type=str, help="Path to the resume data folder")

    args = parser.parse_args()

    not_found_path = './not_found'
    if not os.path.exists(not_found_path):
        os.makedirs(not_found_path)

    if args.output:
        extractor = EmailExtractor(args.path, args.output, not_found_path)
        email = extractor.read_pdf()
        unique_emails = list(set(email))
        formatted_emails = extractor.format_emails(unique_emails)
        extractor.write_csv(formatted_emails)
        print("Emails extracted and saved to:", extractor.output_file)
        print("PDFs with no emails moved to:", not_found_path)

if __name__ == "__main__":
    main()