<!--
{% comment %}
Copyright 2017-2023 Elyra Authors
Copyright 2025 Orange Bricks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
{% endcomment %}
-->

# Auto Dashboards

[![Github Actions Status](https://github.com/orbrx/auto-dashboards/workflows/Build/badge.svg)](https://github.com/orbrx/auto-dashboards/actions/workflows/build.yml)

Convert Jupyter notebooks to dashboards in one click and preview side-by-side.

https://github.com/user-attachments/assets/aa2c25e1-c95a-470d-8879-0b4fb3c5e158


## Requirements

- JupyterLab >= 4.2
- OpenAI
    - you are required to provide your OpenAI API key to use the extension. Export it before starting JupyterLab:
    ```bash
    export OPENAI_API_KEY="your-api-key"
    ```

## Install

To install the extension, execute:

```bash
pip install auto-dashboards
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall auto-dashboards
```

## Troubleshoot

If you are seeing the frontend extension, but it is not working, check
that the server extension is enabled:

```bash
jupyter server extension list
```

If the server extension is installed and enabled, but you are not seeing
the frontend extension, check the frontend extension is installed:

```bash
jupyter labextension list
```

## Acknowledgments

This extension is initially based on the Elyra AI Toolkit's [Streamlit extension](https://github.com/elyra-ai/streamlit-extension) that provides Streamlit execution and preview functionality.

This extension is inspired by the POC from a wonderful BreakThrough AI Team during the Fall 2023 session: [@anikaguin](https://github.com/anikaguin), [@mpate154](https://github.com/mpate154), [@z3yn3p-alta](https://github.com/z3yn3p-alta). Check out their [project](https://github.com/anikaguin/Axle-Informatics/tree/main).

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the auto_dashboards directory
# Install package in development mode
pip install -e .
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Server extension must be manually installed in develop mode
jupyter server extension enable auto_dashboards
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
# Server extension must be manually disabled in develop mode
jupyter server extension disable auto_dashboards
pip uninstall auto-dashboards
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `@orbrx/auto-dashboards` within that folder.

### Packaging the extension

See [RELEASE](RELEASE.md)
