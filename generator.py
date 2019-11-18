# Generator for Yaonotes
import os
from pathlib import Path
import shutil
from jinja2 import Template
import yaml
import datetime

def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
    except OSError:
        print("Creation of the directory %s failed" % folder_path)
    else:
        print("Successfully created the directory %s " % folder_path)


def prepare():
    output_path = "./_site"
    create_folder(output_path)
    shutil.copytree(
        "assets/",
        "./_site/assets",
    )
    pathlist = Path("data").glob('./**')
    for each_path in pathlist:
        create_folder(each_path.__str__().replace("data/", "_site/"))


def render(content_list, tplfile):
    tpl = ""
    with open(tplfile, 'r') as f:
        tpl = f.read()
    template = Template(tpl)
    result = template.render(content=content_list, last_build=datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"))
    return result


def read_data_file(filepath):
    result = []
    with open(filepath, 'r') as stream:
        try:
            result = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return result


def write_file(content, target):
    with open(target, 'w') as targetfile:
        targetfile.write(content)


def handle_yml(filepath, yml_file):
    folder_name = yml_file[:-4]
    create_folder(os.path.join("_site", filepath[5:], folder_name))
    target = os.path.join("_site", filepath[5:], folder_name, "index.html")
    contents = read_data_file(os.path.join(filepath, yml_file))
    if contents:
        write_file(render(contents, "tpl/list.html"), target)
    else:
        write_file(render([], "tpl/list.html"), target)


def get_all_contents(path):
    # print(path)
    contents = []
    subfolders = []
    if os.path.isdir(path):
        files = os.listdir(path)
        for each in files:
            if each.endswith(".yml"):
                handle_yml(path, each)
            abspath = os.path.join(path, each)
            if os.path.isdir(abspath):
                content = {"name": each.capitalize(), "link": each, "description": each.capitalize()}
                subfolders.append(abspath)
                contents.append(content)
            elif abspath.endswith(".yml"):
                content = {"name": each[:-4].capitalize(), "link": each[:-4], "description": each[:-4].capitalize()}
                subfolders.append(abspath)
                contents.append(content)
        write_file(render(contents, "tpl/list.html"),
                   os.path.join("_site", path[5:], "index.html"))

    return subfolders


def iterate_folders(base_path):
    if os.path.isdir(base_path):
        subfolders = get_all_contents(base_path)
        for each in subfolders:
            if os.path.isdir(each):
                iterate_folders(each)


def parse():
    # only for index.html
    index_content = "data/categories.yml"
    index_content = read_data_file(index_content)
    write_file(render(index_content, "tpl/list.html"), "_site/index.html")
    primary_folders = [
        os.path.join("data", subdir) for subdir in os.listdir("data")
    ]
    for each in primary_folders:
        create_folder(os.path.join("_site", each[5:]))
        iterate_folders(each)


if __name__ == "__main__":
    # prepare()
    parse()
