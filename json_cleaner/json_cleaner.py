import glob
import json
import sys

def load_settings():
    try:
        return json.loads(sys.argv[1])
    except (IndexError):
        return {}

def get_json_from_file(fh):
    try:
        # If possible, read the file as JSON
        return json.loads(fh)
    except:
        # If not, read the file as a string, and try to parse it as JSON
        contents = ""
        for line in fh.splitlines():
            cleanedLine = line.split("//", 1)[0]
            if len(cleanedLine) > 0 and line.endswith("\n") and "\n" not in cleanedLine:
                cleanedLine += "\n"
            contents += cleanedLine
        while "/*" in contents:
            preComment, postComment = contents.split("/*", 1)
            contents = preComment + postComment.split("*/", 1)[1]
        return json.loads(contents)

def main():
    settings = load_settings()
    folders = ('BP', 'RP')
    folders += tuple(settings.get('extra_folders', ()))
    for folder in folders:
        for file in glob.glob(folder + "/**/*.json", recursive=True):
            try:
                with open(file, "r", encoding="utf-8") as fh:
                    json_data = get_json_from_file(fh.read())
                
                with open(file, "w", encoding="utf-8") as fh:
                    json.dump(json_data, fh, indent=2, ensure_ascii=False)
            except Exception as e:
                print("Error in file: " + file)
                print(e)
                raise

main()