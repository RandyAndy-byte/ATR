import os
from route_utils import determine_pages, read_file_contents

def gather_angular_components(angular_app_dir, react_app_dir):
    # List all entries in the specified directory
    entries = os.listdir(angular_app_dir)
    
    # Filter out entries that are directories
    folders = [entry for entry in entries if os.path.isdir(os.path.join(angular_app_dir, entry))]
    print(f"Number of Components: {len(folders)}")
    
    components_dir = []
    for folder in folders:
        components_dir.append(os.path.join(react_app_dir, folder))
        
    return components_dir

def create_react_components(angular_project_dir, react_project_dir):
    components_dir = gather_angular_components(angular_project_dir + "/src/app/", react_project_dir + "/src/app/")
    
    child_components_dir = determine_pages(angular_project_dir, react_project_dir)
    parent_components_dir = []
    
    for i in range(len(components_dir)):
        if components_dir[i] not in child_components_dir:
            parent_components_dir.append(components_dir[i])

    print("\n ----------- Analyzing Parent Components -----------")
    for parent_component_dir in parent_components_dir:
        if os.path.isdir(parent_component_dir) == False:
            os.makedirs(parent_component_dir, exist_ok=True)
            print(f"Creating {parent_component_dir}")
        else:
            print(f"{parent_component_dir} already exists")
    
    print("\n ----------- Analyzing Subcomponents -----------")
    for i in range(len(child_components_dir)):
        child_components_dir[i] = child_components_dir[i].replace("app", "components")
    for child_component_dir in child_components_dir:
        if os.path.isdir(child_component_dir) == False:
            os.makedirs(child_component_dir, exist_ok=True)
            print(f"Creating {child_component_dir}")
        else:
            print(f"{child_component_dir} already exists")
            
    return [parent_components_dir, child_component_dir]
    
    
from ai import get_codex_completion

def convert_child_components(angular_project_dir, react_project_dir, child_components_dir):
    
    for component_dir in child_components_dir:
        angular_component_dir = component_dir.replace("-react", "")
        angular_code = read_file_contents(angular_component_dir)
        prompt = """
        Please change this current Angular JS code into code compatible with React JS. This prompt contains the javascript/typescript
        and html to make an angular component. Your goal is to combine this code into a single .tsx file for a react component. Keep in mind
        that components are small parts of large applications. They can include other components inside of them and they use 'ng' template functions
        that don't translate directly to other frameworks.
        """
        get_codex_completion(prompt)