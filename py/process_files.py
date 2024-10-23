#!/usr/bin/env python3
import os
import re
from pathlib import Path

def clean_content(content):
    """Clean the content by removing header and replacing 'User' with 'teilomillet'."""
    # Remove the header section
    header_pattern = r'# Conversation\n-[^#]*?(?=\n## History|\Z)'
    content = re.sub(header_pattern, '', content, flags=re.DOTALL)
    
    # Replace User with teilomillet
    replacements = [
        (r'\*\*User\*\*', '**teilomillet**'),
        (r'>> User:', '>> teilomillet:'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Clean up any extra newlines that might be left
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip() + '\n'

def rename_and_process_file(file_path):
    """Process a single file and rename it to remove underscore."""
    try:
        # Read the input file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Clean and modify content
        modified_content = clean_content(content)
        
        # Generate new filename (remove underscore)
        new_path = Path(str(file_path).replace('_', '', 1))
        
        # Write to new file
        with open(new_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
            
        # Remove old file
        file_path.unlink()
        
        print(f"Processed and renamed: {file_path} -> {new_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def process_current_directory():
    """Process all matching files in the current directory."""
    # Get current directory
    current_dir = Path.cwd()
    
    # Find all files matching the pattern (_DATE.md or _DATE.txt)
    pattern = re.compile(r'^_\d+\.(md|txt)$')
    matching_files = [f for f in current_dir.iterdir() 
                     if f.is_file() and pattern.match(f.name)]
    
    if not matching_files:
        print("No matching files found in current directory.")
        print("Looking for files matching pattern: _DATE.md or _DATE.txt")
        return
    
    successful = 0
    failed = 0
    
    # Process each file
    for file_path in matching_files:
        if rename_and_process_file(file_path):
            successful += 1
        else:
            failed += 1
    
    # Print summary
    print("\nProcessing Complete!")
    print(f"Successfully processed: {successful} files")
    print(f"Failed to process: {failed} files")

if __name__ == "__main__":
    process_current_directory()