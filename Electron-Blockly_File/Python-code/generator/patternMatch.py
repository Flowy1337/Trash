import json
import re
import shutil
import os
from tree_sitter import Language, Parser
import tree_sitter_python
import sys
from BlockFunction import FunctionType

# Load the Tree-sitter language for Python
PY_LANGUAGE = Language(tree_sitter_python.language())
parser = Parser()
parser.set_language(PY_LANGUAGE)

# File paths
src_file_to_copy = os.path.join(os.path.dirname(__file__), '../../projectsrc/projectsrc.py')
destination_file_path = os.path.join(os.path.dirname(__file__), '../../projectsrc/projectskeleton.py')

# Copy the src file to generate the skeleton
shutil.copy(src_file_to_copy, destination_file_path)
print(f"File '{src_file_to_copy}' has been copied to '{destination_file_path}'.")


def read_file(file_path):
    """Reads the contents of a file and returns it as a string."""

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Function to write to a file
def write_file(file_path, content):
    """Writes the given content to a file specified by file_path."""

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def extract_function_name(node):
    """Extracts the name of a function or method from the provided AST node."""

    if node.type == "attribute":
        attribute_node = node.child_by_field_name('attribute')
        if attribute_node.type == "identifier":
            return src[attribute_node.start_byte:attribute_node.end_byte].strip()
    if node.type == "call":
        attribute_node = node.child_by_field_name('function')
        if attribute_node.type == "attribute":
            identifier_node = attribute_node.child_by_field_name('attribute')
            if identifier_node.type == "identifier":
                return src[identifier_node.start_byte:identifier_node.end_byte].strip()
    return ""


def is_simple_value(node):
    """
      Checks if the given node represents a simple value like a number, string,
      or basic arithmetic expression. This helps in identifying basic assignments
      and simple expressions.
      """
    # Add more conditions to capture arithmetic or other operations
    """functionNode = node.child_by_field_name('function');
    if (functionNode):
        attributeNode = functionNode.child_by_field_name('attribute')
        if (attributeNode):
            functionName = src[attributeNode.start_byte:attributeNode.end_byte].strip()
            if is_function_in_enum(
                    functionName) == False:  # Function which is not in enum is most likely a custom function

                return True"""
    isClass = node.child_by_field_name('function');
    if (isClass):
        attributeNode = isClass.child_by_field_name('identifier')
        if (attributeNode):
            functionName = src[attributeNode.start_byte:attributeNode.end_byte].strip()
            if is_function_in_enum(
                    functionName) == False:  # Function which is not in enum is most likely a custom function

                return True

    return node.type in {"integer", "float", "string", "true", "false", "none", "attribute", "list"}


def extract_class_attribute(node):
    """
        Extracts class attributes (e.g., d_model: int) from an expression statement
        or assignment. It handles both type annotations and simple assignments.
        """
    if node.type in {"expression_statement", "assignment"}:
        left_node = node.child_by_field_name("left")
        right_node = node.child_by_field_name("right")

        # Handle class attributes with type annotations
        if node.type == "expression_statement" and left_node:
            # Extract attribute name and type annotation
            left_text = src[left_node.start_byte:left_node.end_byte].strip()
            # Type annotations might be part of the expression
            # For simplicity, we'll treat everything as a potential attribute
            attribute_name = left_text.split(":")[0].strip()  # Get the name before ":"
            attribute_type = left_text.split(":")[1].strip() if ":" in left_text else ""  # Get the type after ":"
            return {
                'function': attribute_name,
                'parameters': attribute_type,
                'assigned': "",
                'index': node.start_point[0] + 1
            }

        elif node.type == "assignment" and left_node and right_node:
            # Extract attribute name and type from assignment
            attribute_name = src[left_node.start_byte:left_node.end_byte].strip()
            attribute_type = src[right_node.start_byte:right_node.end_byte].strip()  # This may need improvement
            return {
                'function': attribute_name,
                'parameters': attribute_type,
                'assigned': "",
                'index': node.start_point[0] + 1
            }

    return None


# Use the file path defined above to read the file
src = read_file(src_file_to_copy)

# Convert the source code to bytes
src_bytes = src.encode("utf-8")

# Parse the source code
tree = parser.parse(src_bytes)

refiller = 0
if len(sys.argv) > 1:
    refiller = int(sys.argv[1])
    print(f"Received parameter: {refiller}")
else:
    print("No parameter received")
# Function to find functions, their calls, and assignments
# Function to find functions, their calls, and assignments
def find_functions_and_calls(root_node):
    """
      Traverses the AST to find functions, their calls, and assignments.
      It categorizes them by their scope (class or global) and collects relevant data.
      """
    scope_data = []
    current_function = None
    loop_context = {}  # To keep track of the current loop context
    cheat_block_count = refiller

    def traverse(node, current_scope=None, current_class=None):
        """
             Recursively traverses the AST nodes to extract function and class information.
             """
        cheatscope = current_scope
        nonlocal current_function
        nonlocal loop_context
        nonlocal cheat_block_count
        token = 1
        rowcheck = 0

        if node.type in {"class_definition", "function_definition"}:
            scope_name_node = node.child_by_field_name("name")
            if scope_name_node:
                scope_name = src[scope_name_node.start_byte:scope_name_node.end_byte]
            else:
                scope_name = src[node.start_byte:node.end_byte].strip()

            row_number = node.start_point[0] + 1
            start_byte = node.start_byte
            end_byte = node.end_byte

            has_return_statement = False
            return_value = None

            if node.type == "class_definition":
                current_class = scope_name
                parameters_node = node.child_by_field_name("parameters")
                base_classes = []

                base_class_node = node.child_by_field_name("superclasses")
                if base_class_node:
                    base_classes = src[base_class_node.start_byte:base_class_node.end_byte].strip()

                if parameters_node:
                    parameters = src[parameters_node.start_byte:parameters_node.end_byte].strip()
                else:
                    parameters = ""
                declaration_calls = []
                attributes = []
                child = node.child_by_field_name("body")
                if child.type == 'block':
                    for e in child.children:

                        if e.type == 'decorated_definition':
                            print("FOUND NNCOMPACT")
                            declaration = ""
                            for j in e.children:
                                if j.type == "decorator":
                                    declaration = src[j.start_byte:j.end_byte].strip()
                            declaration_call = {
                                'function': "Declaration",
                                'parameters': declaration,
                                'assigned': node.start_point[0] + 1,

                            }
                            declaration_calls.append(declaration_call)
                for children in child.children:
                    if children.type == "expression_statement":

                        # member = src[children.start_byte:children.end_byte].strip()
                        # attributes.append(member)
                        for e in children.children:
                            if (e.type == "assignment"):
                                left = e.child_by_field_name("left")
                                right = e.child_by_field_name("type")

                                member = {
                                    'function': "member",
                                    'parameters': src[right.start_byte:right.end_byte].strip(),
                                    'assigned': src[left.start_byte:left.end_byte].strip(),
                                    'index': node.start_point[0] + 1,
                                    # Initialize list for function calls within the loop
                                }
                                attributes.append(member)
                        # print(member)

                class_data = {
                    "scope": current_class,
                    "attributes": attributes,
                    "class_declaration": declaration_calls,  # Add attributes list above functions
                    "functions": [],
                    "translate": True,
                    "row_number": row_number,
                    "parameters": parameters,
                    "base_classes": base_classes,
                    "start_byte": start_byte,
                    "end_byte": end_byte
                }

                scope_data.append(class_data)

            elif node.type == "function_definition":
                for child in node.children:
                    if child.type == "block":
                        return_info = find_return_statements(child)
                        if return_info["has_return"]:
                            has_return_statement = True
                            return_value = return_info['return_value']

                current_scope = scope_name
                parameters_node = node.child_by_field_name("parameters")

                if parameters_node:
                    parameters = src[parameters_node.start_byte:parameters_node.end_byte].strip()
                else:
                    parameters = ""

                function_data = {
                    "functionName": current_scope,
                    "parameters": parameters,
                    "functionCalls": [],
                    "scope": current_class if current_class else "global",  # Handle global functions
                    "row": str(row_number),
                    "returns": return_value,
                    "translate": True,
                    "start_byte": start_byte,
                    "end_byte": end_byte
                }

                if current_class:
                    class_entry = next((item for item in scope_data if item["scope"] == current_class), None)
                    if class_entry:
                        class_entry['functions'].append(function_data)
                else:
                    # Handle global functions or methods outside a class
                    global_entry = next((item for item in scope_data if item["scope"] == "global"), None)
                    if not global_entry:
                        global_entry = {
                            "scope": "global",
                            "functions": [],
                            "translate": False
                        }
                        scope_data.append(global_entry)
                    global_entry['functions'].append(function_data)

                # Set the current function
                current_function = function_data



        if node.type == 'for_statement' and (current_function or current_class):
            iterable_node = node.child_by_field_name('right')
            walker_node = node.child_by_field_name('left')
            element = "element"
            if walker_node:
                element = src[walker_node.start_byte:walker_node.end_byte].strip()
            value = src[iterable_node.start_byte:iterable_node.end_byte].strip()

            loop_entry = {
                'function': "python_loop",
                'parameters': value,
                'assigned': element,
                'index': node.start_point[0] + 1,
                'functionCallsLoop': []  # Initialize list for function calls within the loop
            }

            # Update the loop context
            loop_context = loop_entry

            if current_function:
                current_function['functionCalls'].append(loop_entry)

            # Traverse children of the loop
            for child in node.children:
                traverse(child, current_scope, current_class)

            # Clear loop context after processing
            loop_context = {}

            return  # Skip further processing for the loop node

        if node.type == "assignment" and (current_function or current_class):
            assigned_variable_node = node.child_by_field_name("left")
            assigned_value_node = node.child_by_field_name("right")
            if assigned_variable_node and assigned_value_node:
                isClass = assigned_value_node.child_by_field_name('function')

                if isClass:
                    if isClass.type == "identifier":  # Check if assignment is a class name/class member
                        parametersnode = assigned_value_node.child_by_field_name('arguments')
                        parameters = ""
                        if parametersnode:
                            parameters = src[parametersnode.start_byte:parametersnode.end_byte].strip()
                        className = src[isClass.start_byte:isClass.end_byte].strip()
                        variable_name = src[assigned_variable_node.start_byte:assigned_variable_node.end_byte].strip()
                        row_number = node.start_point[0] + 1
                        variable_assignment_call = {
                            'function': "Variable",
                            'parameters': className  + parameters,
                            'assigned': variable_name,
                            'index': row_number
                        }
                        if loop_context:
                            loop_context['functionCallsLoop'].append(variable_assignment_call)
                        elif current_function:
                            current_function['functionCalls'].append(variable_assignment_call)
                        token = 0

            if assigned_variable_node and assigned_value_node:
                variable_name = src[assigned_variable_node.start_byte:assigned_variable_node.end_byte].strip()
                assigned_value = src[assigned_value_node.start_byte:assigned_value_node.end_byte].strip()

                if is_simple_value(assigned_value_node):
                    row_number = node.start_point[0] + 1
                    rowcheck = row_number
                    variable_assignment_call = {
                        'function': "Variable",
                        'parameters': assigned_value,
                        'assigned': variable_name,
                        'index': row_number
                    }

                    if loop_context:
                        loop_context['functionCallsLoop'].append(variable_assignment_call)
                    elif current_function:
                        current_function['functionCalls'].append(variable_assignment_call)
                    token = 0
        if node.type == "call" and (current_function or current_class):
            called_function_node = node.child_by_field_name("function")

            # function: call
            special_input_text = ""
            function_name = ""
            parameters_text = ""
            assigned_variable = ""
            parameter_node = node.child_by_field_name('arguments')
            function_name = extract_function_name(called_function_node)
            if parameter_node.type == "argument_list":
                parameters_text = src[parameter_node.start_byte:parameter_node.end_byte].strip()
            if called_function_node.type == "call":  # function: call
                special_parameter_node = called_function_node.child_by_field_name('arguments')
                if special_parameter_node.type == "argument_list":
                    special_input_text = src[special_parameter_node.start_byte:special_parameter_node.end_byte].strip()

            assigned_variable = find_assignment_for_call(node)
            row_number = node.start_point[0] + 1

            if is_function_in_enum(function_name):
                function_call = {
                    'function': function_name,
                    'parameters': special_input_text + parameters_text,
                    'assigned': assigned_variable,
                    'index': row_number
                }

                if function_name != "":
                    token = 0
                    if loop_context:
                        loop_context['functionCallsLoop'].append(function_call)
                    elif current_function:
                        current_function['functionCalls'].append(function_call)

            if not is_function_in_enum(function_name) and node.parent.type != "return_statement":

                parent = node.parent
                function_call = {
                    'function': "cheatblock",
                    'parameters': src[parent.start_byte:parent.end_byte].strip(),
                    'assigned': assigned_variable,
                    'index': row_number,
                    # If replace is true, we cheeck how many functions are present as "cheat blocks"
                }
                if function_name != "":
                    token = 0
                    if loop_context:
                        loop_context['functionCallsLoop'].append(function_call)
                    elif current_function:
                        current_function['functionCalls'].append(function_call)
                if cheat_block_count == 0:
                    if loop_context:
                        loop_context['functionCallsLoop'].append(function_call)
                    elif current_function:
                        current_function['functionCalls'].append(function_call)
                    current_function['translate'] = False

                    if current_class:
                        class_entry = next((item for item in scope_data if item["scope"] == current_class),
                                           None)
                        if class_entry:
                            class_entry['translate'] = False
                    else:
                        global_entry = next((item for item in scope_data if item["scope"] == "global"), None)
                        if global_entry:
                            global_entry['translate'] = False
                if cheatscope == current_scope:
                    cheat_block_count = cheat_block_count - 1

        if cheatscope != current_scope:
            cheat_block_count = refiller # Set count back to when we exit scope
        for child in node.children:
            traverse(child, current_scope, current_class)

    traverse(root_node)
    return scope_data

    # This ensures that functions in the global scope are assigned to "global".

    def filter_translatable_scopes(scope_data):
        """
         Filters the scope data to include only those scopes and functions
         that are marked as translatable.
         Returns a list of scopes containing only translatable functions.
         """
        filtered_scope_data = []
        for scope in scope_data:
            if scope['scope'] == "global":
                # Set global translate to True if there are any translatable functions
                if any(func['translate'] for func in scope['functions'] if 'translate' in func):
                    scope['translate'] = True
                else:
                    scope['translate'] = False

            # Keep only translatable functions
            translatable_functions = [
                func for func in scope['functions'] if func['translate']
            ]
            if translatable_functions or scope['scope'] == "global":
                # If there are translatable functions, include the scope
                filtered_scope_data.append({
                    **scope,
                    'functions': translatable_functions
                })
        return filtered_scope_data

    traverse(root_node)
    return filter_translatable_scopes(scope_data)


def find_return_statements(node):
    """Find return statements in the AST node and capture their values.

    Args:
        node: The AST node to traverse.

    Returns:
        dict: A dictionary containing whether a return statement was found and its value.
    """
    has_return = False  # Flag to indicate if a return statement is found
    return_value = None  # Variable to store the return value

    def traverse_returns(n):
        """Recursively traverse nodes to find return statements."""
        nonlocal has_return, return_value  # Access outer function's variables

        if n.type == "return_statement":
            has_return = True  # Mark that a return statement was found
            # The return statement usually contains an expression as its first child
            if len(n.children) > 1:
                return_value_node = n.children[1]  # Get the return expression
                # Extract the return value from the source code using its byte range
                return_value = src[return_value_node.start_byte:return_value_node.end_byte].strip()

        # Recursively traverse all child nodes
        for child in n.children:
            traverse_returns(child)

    # Start the traversal from the given node
    traverse_returns(node)
    return {
        "has_return": has_return,  # Indicate if a return statement was found
        "return_value": return_value  # Capture the return value
    }


def extract_function_and_parameters(full_call_text):
    """Extract the function name and parameters from a full call text.

    Args:
        full_call_text (str): The full text of the function call.

    Returns:
        tuple: A tuple containing the function name and its parameters.
    """
    # Find the position of the opening parenthesis
    function_name_end = full_call_text.find('(')
    if function_name_end != -1:
        function_name = full_call_text[:function_name_end].strip()  # Get the function name
        parameters_text = full_call_text[function_name_end:].strip()  # Get the parameters
    else:
        function_name = full_call_text.strip()  # No parameters, return the full text
        parameters_text = ""

    # Remove any leading module or class name prefixes
    function_name = function_name.split('.')[-1]  # Get the last part after '.'

    return function_name, parameters_text  # Return function name and parameters


def find_assignment_for_call(node):
    """Find the variable to which a function call is assigned.

    Args:
        node: The AST node representing the function call.

    Returns:
        str: The name of the variable assigned to the function call, or an empty string.
    """
    parent = node.parent  # Start from the parent node of the function call
    while parent:
        if parent.type == "assignment":  # Check if the parent node is an assignment
            assigned_to_node = parent.child_by_field_name("left")  # Get the left-hand side of the assignment
            if assigned_to_node:
                return src[assigned_to_node.start_byte:assigned_to_node.end_byte].strip()  # Return the variable name
        parent = parent.parent  # Move up the AST to the parent node
    return ""  # Return an empty string if no assignment is found

def is_function_in_enum(function_name):
    """Check if a function name exists in the defined enumeration.

    Args:
        function_name (str): The name of the function to check.

    Returns:
        bool: True if the function exists in the enumeration, otherwise False.
    """
    try:
        # Attempt to access the function type in the enumeration
        FunctionType[function_name.upper()]
        return True  # Return True if the function exists in the enum
    except KeyError:
        return False  # Return False if the function does not exist


# Find functions and calls categorized by their parent nodes
scope_data = find_functions_and_calls(tree.root_node)

# Write the output data to a JSON file
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(scope_data, json_file, indent=4)

print("JSON file 'output.json' has been created with the translatable class and function data.")

# Read the copied skeleton file
skeleton_src = read_file(destination_file_path)

# Initialize an empty string to store the modified skeleton
modified_skeleton = ""
last_index = 0

# Insert #Doable comments at the head of translatable functions and classes, and remove the translatable part
for scope in scope_data:
    if scope:
        if scope['scope'] != 'global' and scope['translate']:
            # Check if any function in the class is not translatable
            class_translatable = all(function['translate'] for function in scope['functions'])

            if class_translatable:
                # If the class is translatable, remove the entire class definition
                start_byte = scope['start_byte']  # Start byte of the class definition
                end_byte = scope['end_byte']  # End byte of the class definition

                # Append the source code up to the start of the class definition
                modified_skeleton += skeleton_src[last_index:start_byte]

                # Insert the #Doable comment at the head of the class
                modified_skeleton += f"#{scope['scope']}+\n"
                modified_skeleton += f"#{scope['scope']}-\n"
                # Update last_index to skip the entire class definition
                last_index = end_byte
        elif scope['scope'] == 'global':


            # If the scope is global, handle functions within the global scope
            for function in scope['functions']:
                if function['translate']:
                    start_byte = function['start_byte']  # Start byte of the function definition
                    end_byte = function['end_byte']  # End byte of the function definition

                    # Append the source code up to the start of the function definition
                    modified_skeleton += skeleton_src[last_index:start_byte]

                    # Insert the #Doable comment at the head of the function
                    modified_skeleton += f"#{function['functionName']}+\n"
                    modified_skeleton += f"#{function['functionName']}-\n"
                    # Update last_index to skip the translatable function
                    last_index = end_byte


# Add the remaining part of the file after the last processed scope
modified_skeleton += skeleton_src[last_index:]

# Write the modified skeleton back to the file
write_file(destination_file_path, modified_skeleton)

print(
    f"Translatable scopes and return statements have been marked with #Doable and removed from '{destination_file_path}'.")
