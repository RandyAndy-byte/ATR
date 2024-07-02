from setup import check_node_version, set_directories, create_nextjs_project
from convert import create_react_components, convert_child_components


if __name__ == '__main__':
    print("\n")
    if check_node_version() == False:
        exit(1)
    angular_project_dir, angular_project_name, react_project_dir, react_project_name = set_directories()
    create_nextjs_project(react_project_dir)
    
    parents_components_dir, child_components_dir = create_react_components(angular_project_dir, react_project_dir)
    convert_child_components(angular_project_dir, react_project_dir, child_components_dir)
    
    
        
        