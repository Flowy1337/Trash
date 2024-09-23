import os
import re
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROJECTSRC_PATH = '../../projectsrc/projectskeleton.py'


def insert_new_comment(target_file_path, insert_string, line_number):
    try:
        with open(target_file_path, 'r') as target_file:
            target_content = target_file.readlines()

        insert_content = insert_string.splitlines(True)
        updated_content = target_content[:line_number] + insert_content + target_content[line_number:]

        with open(target_file_path, 'w') as target_file:
            target_file.writelines(updated_content)

        print(f"String inserted into {target_file_path} at line {line_number}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def log_number_and_update_projectsrc(file_path):
    try:
        base_name = os.path.basename(file_path)
        match = re.search(r'(\d+)', base_name)
        if match:
            number = int(match.group(1))
            print(f"Found number {number} in file name {base_name}")
            logging.info(f"Found number {number} in file name {base_name}")

            # Construct the strings to insert
            start_comment = f"#{extract_filename_without_extension(base_name)}+"
            end_comment = f"#{extract_filename_without_extension(base_name)}-"

            # Insert the strings into projectsrc.py
            insert_new_comment(PROJECTSRC_PATH, start_comment + '\n', number)
            insert_new_comment(PROJECTSRC_PATH, end_comment + '\n', number + 1)
        else:
            logging.info(f"No number found in file name {base_name}")
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
def extract_filename_without_extension(file_path):
    base_name = os.path.basename(file_path)
    file_name, _ = os.path.splitext(base_name)
    return file_name

def find_comment_block(file_path, start_comment, end_comment):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        start_line = None
        end_line = None
        for line_number, line in enumerate(lines, start=1):
            if start_comment in line:
                start_line = line_number
            elif end_comment in line:
                end_line = line_number
                break

        return start_line, end_line
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def insert_string_at_line(target_file_path, insert_string, start_line, end_line,bottom):
    try:
        with open(target_file_path, 'r') as target_file:
            target_content = target_file.readlines()

        insert_string += "#"+bottom + '\n'
        insert_content = insert_string.splitlines(True)

        if start_line is not None and end_line is not None:
            updated_content = target_content[:start_line] + insert_content + target_content[end_line:]
        else:
            updated_content = target_content + insert_content

        with open(target_file_path, 'w') as target_file:
            target_file.writelines(updated_content)

        print(f"String inserted into {target_file_path} at line {start_line}.")
    except Exception as e:
        print(f"An error occurred: {e}")





def read_file(file_path):
    base = extract_filename_without_extension(file_path)
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        # Determine marker type from the filename
        start_comment = base+"+"
        end_comment = base+"-"
        print("Start/END is.." + start_comment + "\n" + end_comment)
        start_line, end_line = find_comment_block('../../projectsrc/projectskeleton.py', start_comment, end_comment)

        if start_line is not None and end_line is not None:
            insert_string_at_line('../../projectsrc/projectskeleton.py', code, start_line, end_line, end_comment)
        else:
            print("Markers not found.")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

class Watcher:
    def __init__(self, directory_to_watch):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            read_file(event.src_path)

    @staticmethod
    def on_created(event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")
            log_number_and_update_projectsrc(event.src_path)


    @staticmethod
    def on_deleted(event):
        if not event.is_directory:
            logging.info(f"File deleted: {event.src_path}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_to_watch>")
        sys.exit(1)

    directory_to_watch = sys.argv[1]

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    w = Watcher(directory_to_watch)
    w.run()