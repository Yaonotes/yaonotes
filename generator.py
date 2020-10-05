# coding:utf-8
# Generator for Yaonotes
import os
from pathlib import Path
import shutil
from jinja2 import Template, Environment, PackageLoader
import yaml
import datetime
import requests
import json

# Global parameters for statistics
counts = {}
all_contents = []

def get_commits():
    g = requests.get("https://api.github.com/repos/xzyaoi/yaonotes/commits", headers={"Accept":"application/vnd.github.v3+json"})
    result = json.loads(g.text)
    return result

def generate_history():
    commits = get_commits()
    contents = []
    for each in commits:
        content = {
            "name":each["sha"][0:8],
            "status":"Merged",
            "link":'https://github.com/xzyaoi/yaonotes/commit/'+each["sha"],
            "description":each['commit']['message'],
            "lastUpdate": each['commit']['author']['date'],
        }
        contents.append(content)
    write_file(render("History", contents, "tpl/list.html"), "_site/history.html")

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
    except OSError:
        print("Creation of the directory %s failed" % folder_path)
    else:
        # print("Successfully created the directory %s " % folder_path)
        pass


def prepare():
    output_path = "./_site"
    try:
        shutil.rmtree(
            "./_site/assets",
        )
    except:
        pass
    create_folder(output_path)
    shutil.copytree(
        "assets/",
        "./_site/assets",
    )
    pathlist = Path("data").glob('./**')
    for each_path in pathlist:
        create_folder(each_path.__str__().replace("data/", "_site/"))


def render_stats(total_count, counts, tplfile):
    tpl = ""
    with open(tplfile, 'r') as f:
        tpl = f.read()
    template = Template(tpl)
    result = template.render(title="Statistics", total_count=total_count, counts=counts, last_build=datetime.datetime.now(
    ).strftime("%b %d %Y %H:%M:%S"))
    return result


def render(title, content_list, tplfile):
    tpl = ""
    with open(tplfile, 'r') as f:
        tpl = f.read()
    template = Template(tpl)
    result = template.render(title=title, content=content_list, last_build=datetime.datetime.now(
    ).strftime("%b %d %Y %H:%M:%S"))
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
        write_file(render(folder_name, contents, "tpl/list.html"), target)
    else:
        write_file(render(folder_name, [], "tpl/list.html"), target)
    if(contents is not None):
        counts[folder_name] = len(contents)
    return contents


def get_all_contents(path):
    contents = []
    subfolders = []
    if os.path.isdir(path):
        files = os.listdir(path)
        for each in files:
            if each.endswith(".yml"):
                result = handle_yml(path, each)
                if result is not None:
                    all_contents.extend(result)
            abspath = os.path.join(path, each)
            if os.path.isdir(abspath):
                content = {"name": each.capitalize(), "link": each,
                           "description": each.capitalize()}
                subfolders.append(abspath)
                contents.append(content)
            elif abspath.endswith(".yml"):
                content = {
                    "name": each[:-4].capitalize(), "link": each[:-4], "description": each[:-4].capitalize()}
                subfolders.append(abspath)
                contents.append(content)
        write_file(render(path, contents, "tpl/list.html"),
                   os.path.join("_site", path[5:], "index.html"))

    return subfolders


def iterate_folders(base_path):
    if os.path.isdir(base_path):
        subfolders = get_all_contents(base_path)
        for each in subfolders:
            if os.path.isdir(each):
                iterate_folders(each)


def generate_stats():
    write_file(render_stats(len(all_contents)-1, counts, "tpl/stats.html"),
               os.path.join("_site", "stats.html"))


def parse():
    # only for index.html
    index_content = "data/categories.yml"
    index_content = read_data_file(index_content)
    write_file(render("Categories", index_content, "tpl/list.html"), "_site/index.html")
    primary_folders = [
        os.path.join("data", subdir) for subdir in os.listdir("data")
    ]
    for each in primary_folders:
        if each == os.path.join("data", "blogs"):
            create_folder(os.path.join("_site", each[5:]))
        else:
            create_folder(os.path.join("_site", each[5:]))
            iterate_folders(each)
    generate_history()
    generate_stats()


if __name__ == "__main__":
    prepare()
    parse()
