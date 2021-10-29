# Build A 3D Mesh Search Using jina

Game Developers should pay attention: This example shows how you can search for similar
3D objects using Jina. You can input a 3D mesh and the search system will return similar 3D meshes.

**Table of Contents**
- [Overview](#overview)
- [🐍 Build the app with Python](#-build-the-app-with-python)
- [🌀 Flow diagram](#-flow-diagram)
- [🔮 Overview of the files](#-overview-of-the-files)
- [🌀 Flow diagram](#-flow-diagram)
- [⏭️ Next steps](#-next-steps)
- [👩‍👩‍👧‍👦 Community](#-community)
- [🦄 License](#-license)


## Overview
| About this example: |  |
| ------------- | ------------- |
| Learnings | How to search through 3D meshes. |
| Used for indexing | 3D meshes in `.glb` files. |
| Used for querying | Another `.glb` file |
| Dataset used | Custom collection of 1000 `.glb` files |
| Model used | [Pointnet Model](https://github.com/jina-ai/executor-pn-encoder) |

In this example, we create a 3D mesh search system that enables users to search through a large collection of 3D objects.

We choose to use PointNet model to encode the 3D meshes.

Jina searches the collection of indexed 3D objects and returns the path to the matches.

_____

## 🐍 Build the app with Python

These instructions explain how to build the example yourself and deploy it with Python.


### 🗝️ Requirements

1. You have a working Python 3.7 or 3.8 environment and a installation of [Docker](https://docs.docker.com/get-docker/). Ensure that you set enough memory resources(more than 6GB) to docker. You can set it in settings/resources/advanced in Docker.
2. We recommend creating a [new Python virtual environment](https://docs.python.org/3/tutorial/venv.html) to have a clean installation of Jina and prevent dependency conflicts.   
3. You have at least 5 GB of free space on your hard drive. 

### 👾 Step 1. Clone the repo and install Jina

Begin by cloning the repo, so you can get the required files and datasets.

```sh
git clone https://github.com/jina-ai/example-3D-model
cd example-3D-model
````
In your terminal, you should now be located in the *example-3D-model* folder. Let's install Jina and the other required Python libraries. For further information on installing Jina check out [our documentation](https://docs.jina.ai/chapters/core/setup/).

```sh
pip install -r requirements.txt
```

### 🏃 Step 2. Index your data
To quickly get started, you can the dataset we provided. Later, we recommend you try out your own datasets.

To index our dataset, run
```bash
python app.py -t index
```

### 🔎 Step 4: Query your data
After indexing, you can run a quick test query using:
```bash
python app.py -t query
```
This runs one query using a 3D object containing a laptop.  
If you want to visualize the results and matches, you can use our simple visualization funcionality:
```bash
python app.py -t query -v True
```
Alternatively, you can use [online tools](https://gltf-viewer.donmccurdy.com/) to visualize in better quality.

Alternatively, you can start a REST Api waiting for queries:
```bash
python app.py -t query_restful
```

Afterwards, you can query with
```bash
curl -X 'POST' 'localhost:45678/search' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"data": [{"uri": "/workspace/toy_data/laptop_laptop_computer_17.glb"}]}'
```

You can also add more parameters to the query:
```sh
curl -X POST -d '{"parameters":{"limit": 5}, "data": [{"uri": "/workspace/toy_data/laptop_laptop_computer_17.glb"}]}' -H 'accept: application/json' -H 'Content-Type: application/json' 'http://localhost:45678/search'
```

## 🌀 Flow diagram
This diagram provides a visual representation of the Flow in this example; Showing which executors are used in which order.
Remember, our goal is to compare vectors representing the 3D objects.

![](.github/flow.png)  
As you can see, the Flow that indexes and searches the 3D objects is pretty simple: 
- Crafter: reads the .glb files into the Document
- Encoder: Encodes the 3D object and creates the embedding vector
- Indexer: 
  - Stores the Documents with the embeddings persistently during indexing.
  - Compares the search vector with the saved vectors to find matches during query time. 


## 🔮 Overview of the files

|                      |                                                                                                                  |
| -------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 📃 `flow.yml`  | YAML file to configure the Flow |
| 📂 `workspace/`      | Folder to store indexed files (embeddings and documents). Automatically created after the first indexing   |
| 📂 `toy-data/`       | Folder to store the toy dataset for the example  |
| 📃 `app.py`          | Main file that runs the example  |
| 📂 `.github/`        | Documentation files for the README and github |
| 📃 `requirements.txt`  | Python Package Requirements |


## ⏭️ Next steps

Did you like this example and are you interested in building your own? For a detailed tutorial on how to build your Jina app check out [How to Build Your First Jina App](https://docs.jina.ai/chapters/my_first_jina_app/#how-to-build-your-first-jina-app) guide in our documentation.  

To learn more about Jina concepts, check out the [documentation](https://docs.jina.ai/).  

If you have any issues following this guide, you can always get support from our [Slack community](https://slack.jina.ai) .

## 👩‍👩‍👧‍👦 Community

- [Slack channel](https://slack.jina.ai) - a communication platform for developers to discuss Jina.
- [LinkedIn](https://www.linkedin.com/company/jinaai/) - get to know Jina AI as a company and find job opportunities.
- [![Twitter Follow](https://img.shields.io/twitter/follow/JinaAI_?label=Follow%20%40JinaAI_&style=social)](https://twitter.com/JinaAI_) - follow us and interact with us using hashtag `#JinaSearch`.  
- [Company](https://jina.ai) - know more about our company, we are fully committed to open-source!

## 🦄 License

Copyright (c) 2021 Jina AI Limited. All rights reserved.

Jina is licensed under the Apache License, Version 2.0. See [LICENSE](https://github.com/jina-ai/jina/blob/master/LICENSE) for the full license text.