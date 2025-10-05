import os

# Define the clean redirect content template function
def get_redirect_content(page_name, redirect_path):
    return f"""import {{ redirect }} from 'next/navigation'

export default function {page_name}Page() {{
  redirect('{redirect_path}')
}}
"""

# Files to clean up
files_to_fix = [
    ("app/(dashboard)/analytics/page.tsx", "Analytics", "/search"),
    ("app/(dashboard)/compliance/page.tsx", "Compliance", "/upload"),
    ("app/(dashboard)/settings/page.tsx", "Settings", "/upload"),
    ("app/(dashboard)/users/page.tsx", "Users", "/upload"),
    ("app/(dashboard)/profile/page.tsx", "Profile", "/upload")
]

for file_path, page_name, redirect_path in files_to_fix:
    content = get_redirect_content(page_name, redirect_path)
    
    try:
        # Delete file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Write clean content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed {file_path}")
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")

print("All redirect pages have been cleaned up!")