
import os
import json
import argparse

def add_repo(repo_name, repo_url=None):
    # Find project root (assuming script is in 'scripts/' folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    
    # 1. Create directory
    # Use 'repositories' directory to keep root clean
    base_dir = 'repositories'
    repo_dir = os.path.join(project_root, base_dir, repo_name)
    os.makedirs(repo_dir, exist_ok=True)
    
    # 2. Create index.mdx
    index_mdx_content = f"""---
title: "{repo_name}"
description: "Documentation for {repo_name}"
---

# {repo_name}

Welcome to the documentation for **{repo_name}**.

## Getting Started

To get started with this repository via the newly created documentation, edit this file at `{base_dir}/{repo_name}/index.mdx`.
"""
    if repo_url:
        index_mdx_content += f"\nRepository URL: [{repo_url}]({repo_url})\n"
        
    with open(os.path.join(repo_dir, 'index.mdx'), 'w') as f:
        f.write(index_mdx_content)
    
    print(f"Created documentation structure for '{repo_name}' at '{repo_dir}'.")
    
    # 3. Update docs.json
    docs_json_path = os.path.join(project_root, 'docs.json')
    try:
        with open(docs_json_path, 'r') as f:
            docs_data = json.load(f)
            
        # Add to navigation
        # Helper to find if existing group
        new_nav_item = {
            "group": repo_name,
            "pages": [
                f"{base_dir}/{repo_name}/index"
            ]
        }
        
        # Determine where to add. Let's add it to a new tab called "Repositories" if it doesn't exist.
        # Check if navigation has tabs
        if 'navigation' not in docs_data:
            docs_data['navigation'] = {}
            
        navigation = docs_data['navigation']
        
        # Handle 'tabs' vs 'groups' (if no tabs used currently, might need to restructure, 
        # but Mintlify supports mixing or just tabs. Existing docs.json uses tabs)
        if 'tabs' in navigation:
            repositories_tab = None
            for tab in navigation['tabs']:
                if tab.get('tab') == 'Repositories':
                    repositories_tab = tab
                    break
            
            if not repositories_tab:
                repositories_tab = {
                    "tab": "Repositories",
                    "groups": []
                }
                navigation['tabs'].append(repositories_tab)
                
            # Check if group already exists to avoid duplicates
            group_exists = False
            for group in repositories_tab['groups']:
                if group.get('group') == repo_name:
                    group_exists = True
                    break
            
            if not group_exists:
                repositories_tab['groups'].append(new_nav_item)
                print(f"Added '{repo_name}' to 'Repositories' tab in docs.json.")
            else:
                print(f"'{repo_name}' already exists in 'Repositories' tab.")
        else:
            # Fallback if no tabs, just add to root groups? 
            # But the existing validation shows tabs are used. 
            pass

        with open(docs_json_path, 'w') as f:
            json.dump(docs_data, f, indent=2)
            
    except FileNotFoundError:
        print("Error: docs.json not found in current directory.")
    except json.JSONDecodeError:
        print("Error: Failed to parse docs.json.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a new repository to the documentation.")
    parser.add_argument("repo_name", help="Name of the repository")
    parser.add_argument("--url", help="URL of the repository (optional)")
    
    args = parser.parse_args()
    add_repo(args.repo_name, args.url)
