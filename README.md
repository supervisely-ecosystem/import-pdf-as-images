<div align="center" markdown>
<img src="https://github.com/supervisely-ecosystem/import-pdf-as-images/assets/119248312/11e644d7-4491-4fbe-ba3b-d77370938c00"/>  

# Import PDF as Images

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> 
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-pdf-as-images)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-pdf-as-images)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/import-pdf-as-images.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/import-pdf-as-images.png)](https://supervise.ly)

</div>

# Overview

This app allows you to download pages of PDF files as PNG images.

❗ Be aware that "Remove temporary files after successful import" flag is enabled by default, it will automatically remove source directory after import. 

# How To Run

App can be launched from Ecosystem, Team Files, Images Project and Images Dataset
* [running the app from ecosystem](#run-from-ecosystem) you will be given options to create new project, upload images to existing project or existing dataset
* [running the app from team files](#run-from-team-files) will result in new project
* [running the app from images project](#run-from-images-project) will upload images to existing project, from which it was launched
* [running the app from images dataset](#run-from-images-dataset) will upload images to existing dataset, from which it was launched

### Run from Ecosystem:

**Step 1.** Go to Ecosystem page and find the app [Import PDF as Images](https://ecosystem.supervisely.com/apps/import-pdf-as-images).

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-pdf-as-images" src="XXX" width="500px" style='padding-bottom: 20px'/> 

<br>

<img src="XXX"/>

**Step 2.** Drag & drop your data, or select already uploaded folder with data from `Team Files`, select options in the modal window and press the `Run` button, you will be redirected to the `Workspace tasks` page.

<img src="XXX"/>

**Step 3.** Wait for the app to process your data, once done, link to your project will become available.

<img src="XXX"/>

**Step 4.** Go to `Team Files` -> `Supervisely Agent` and find your folder there.

### Import to existing Images Project:

**Step 1.** Open context menu of images project -> `Run app` -> `Import`  -> `Import PDF as Images`.

<img src="XXX"/>

**Step 2.** Drag & drop your data, or select already uploaded folder with data from `Team Files`, select options in the modal window and press the `Run` button, you will be redirected to the `Workspace tasks` page.

<img src="XXX"/>

**Step 3.** Wait for the app to process your data, once done, link to your project will become available.

<img src="XXX"/>

### Import to existing Images Dataset:

**Step 1.** Open context menu of images dataset -> `Run app` -> `Import`  -> `Import PDF as Images`.

<img src="XXX"/>

**Step 2.** Drag & drop your data, or select already uploaded folder with data from `Team Files`, select options in the modal window and press the `Run` button, you will be redirected to the `Workspace tasks` page.

<img src="XXX"/>

**Step 3.** Wait for the app to process your data, once done, link to your project will become available.

<img src="XXX"/>


## Input files structure

Directories define dataset names. Images in root directory will be moved to dataset with name "`ds0`".
 
```
.
my_images_project
├── img_01.png
├── ...
├── img_09.png
├── my_folder1
│   ├── img_01.png
│   ├── img_02.png
│   └── my_folder2
│       ├── img_13.png
│       ├── ...
│       └── img_9999.png
└── my_folder3
    ├── img_01.png
    ├── img_02.png
    └── img_03.png
```

As a result we will get project with 3 datasets with the names: `ds0`, `my_folder1`, `my_folder3`. Dataset `my_folder1` will also contain images from `my_folder2` directory.

