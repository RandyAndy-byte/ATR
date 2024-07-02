import os
import re
from collections import defaultdict

def read_file_contents(file_path):
    """
    Reads all text from a given file and returns it as a string.

    Parameters:
    - file_path (str): The path to the file to be read.

    Returns:
    - str: The contents of the file as a single string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"An error occurred: {e}"


def find_files(directory, extension):
    """Recursively find all files with the given extension in the directory."""
    matches = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                matches.append(os.path.join(root, file))
    return matches

def parse_component_file(file_path):
    """Parse an Angular component file to extract the component's selector."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    selector_match = re.search(r'selector:\s*\'([^\']+)\'', content)
    if selector_match:
        return selector_match.group(1)
    return None

def parse_app_module(app_module_path):
    """Parse app.module.ts to find components listed in it."""
    components = set()
    with open(app_module_path, 'r') as file:
        content = file.read()
    
    component_matches = re.findall(r'\b(\w+Component)\b', content)
    components.update(component_matches)
    
    return components

def build_component_graph(project_directory):
    """Build a component graph for an Angular project."""
    component_graph = defaultdict(list)
    component_files = find_files(project_directory, '.ts')
    html_files = find_files(project_directory, '.html')
    
    # Map of component selectors to their file paths
    selector_to_component = {}
    component_to_selector = {}
    
    # Extract selectors from component files
    for component_file in component_files:
        selector = parse_component_file(component_file)
        if selector:
            component_name = os.path.basename(component_file).replace('.ts', '')
            selector_to_component[selector] = component_name
            component_to_selector[component_name] = selector
    
    # Build the component graph by parsing HTML templates
    for html_file in html_files:
        with open(html_file, 'r') as file:
            content = file.read()
        
        parent_component = os.path.basename(html_file).replace('.html', '')
        for selector, component_name in selector_to_component.items():
            if f'<{selector}' in content:
                component_graph[parent_component].append(component_name)
    
    return component_graph

def print_component_graph(component_graph):
    """Print the component graph in a readable format."""
    for parent, children in component_graph.items():
        if parent == 'app':
            continue
        print(f'{parent}:')
        for child in children:
            print(f'  - {child}')

def determine_pages(angular_project_dir, react_project_dir):
    """Determine the pages of an Angular project based on the component graph."""
    component_graph = build_component_graph(angular_project_dir)
    child_components_dir = set()
    
    for parent in component_graph.keys():
        for child in component_graph[parent]:
            child_components_dir.add(react_project_dir + '/src/app/' + child.split('.')[0])
            
    return list(child_components_dir)