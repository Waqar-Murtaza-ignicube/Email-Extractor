"""modules"""
import os
import re
import csv
import argparse
from pdfminer.high_level import extract_text

class EmailExtractor:
    """class to pair up functionalities"""
    def __init__(self, path, filename):
        self.output_file = filename
        self.resume_directory = path

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
                if extracted_emails:
                    all_emails.append(extracted_emails)
        return all_emails

    def write_csv(self, unique_emails):
        """writing emails in csv file"""
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Email'])
            for email in unique_emails:
                writer.writerow([email])

def main():
    """main function"""

    parser = argparse.ArgumentParser(description="Generate weather reports.")
    parser.add_argument("-O", "--output", type=str, help="output file name")
    parser.add_argument("path", type=str, help="Path to the weather data folder")

    args = parser.parse_args()

    if args.output:
        extractor = EmailExtractor(args.path, args.output)
        email = extractor.read_pdf()
        unique_emails = list(set(email))
        extractor.write_csv(unique_emails)
        print("Emails extracted and saved to:", extractor.output_file)

if __name__ == "__main__":
    main()
