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

<h1 align="center">
  <img src="https://github.com/user-attachments/assets/99abd1a7-7e99-4d20-b72c-892e0d7804d8" alt="Auto Dashboards logo" height="64" valign="middle">
  <span>Auto Dashboards</span>
</h1>
<p align="center">
  Convert Jupyter notebooks to dashboards in one click and preview side-by-side.
</p>

[![auto-dashboards](https://marketplace.orbrx.io/api/badge/auto-dashboards?metric=downloads-month&leftColor=%23555&rightColor=%23F37620&style=flat)](https://marketplace.orbrx.io/extensions/auto-dashboards)

**New in version 0.3.0**: Create Dash dashboards.

**New in version 0.2.1**: Support for OpenAI-compatible and local LLMs like Ollama!

**New in version 0.2.0**: Create Solara dashboards.

https://github.com/user-attachments/assets/f7b040e5-a137-454f-bcb2-4c7b46b45288

## Features

Supported output formats:
- [Streamlit](https://github.com/streamlit/streamlit)
- [Solara](https://github.com/widgetti/solara)
- [Dash](https://github.com/plotly/dash)

Coming soon:
- [Gradio](https://github.com/gradio-app/gradio)

## Requirements

- JupyterLab >= 4.2
- OpenAI or OpenAI-compatible LLM
    - For OpenAI:
    ```bash
    export OPENAI_API_KEY="your-api-key"
    ```
    - For OpenRouter:
    ```bash
    export OPENAI_API_KEY="openrouter-api-key"
    export OPENAI_API_BASE="https://openrouter.ai/api/v1"
    export OPENAI_API_MODEL="openrouter/horizon-beta" # or any other model you have access to
    ```
    - For local LLMs (like Ollama):
    ```bash
    export OPENAI_API_URL="http://localhost:11434/v1"
    export OPENAI_MODEL="gpt-oss:20b"  # or any other model you have pulled
    ```

## Install

To install the extension, execute:

```bash
pip install auto-dashboards
```

This installs the extension with just the core dependencies. To use dashboard conversion, install one or more framework extras:

```bash
# Install with a specific framework
pip install auto-dashboards[streamlit]
pip install auto-dashboards[solara]
pip install auto-dashboards[dash]

# Install with multiple frameworks
pip install auto-dashboards[streamlit,dash]

# Install with all supported frameworks
pip install auto-dashboards[all]
```

If you installed the core extension without frameworks, you can add them later:

```bash
pip install streamlit solara dash
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

## Dash script authoring

When launching Dash through Auto Dashboards, keep the script as plain Dash.
The managed runner loads your script and starts the app for you.

Rules:
- Use standard Dash app creation (`app = Dash(__name__)`).
- Expose either a top-level `app` or a `create_app(...)` function that returns a Dash app.
- Define `app.layout` as usual.
- You may keep a local `if __name__ == "__main__": app.run()` block for direct Python runs.
- Do not parse `--port`, `--proxy-path`, or `--no-browser` in your script when using Auto Dashboards.
- Keep the file valid Python with no notebook magics.

```python
from dash import Dash, html

app = Dash(__name__)
app.layout = html.Div("Hello from Dash")

if __name__ == "__main__":
    app.run()
```

Auto Dashboards injects managed runtime defaults for Jupyter proxy compatibility
(port, host, and proxy pathname prefix).

## Acknowledgments

This extension is initially based on the Elyra AI Toolkit's [Streamlit extension](https://github.com/elyra-ai/streamlit-extension) that provides Streamlit execution and preview functionality.

This extension is inspired by the POC from a wonderful BreakThrough AI Team during the Fall 2024 session: [@anikaguin](https://github.com/anikaguin), [@mpate154](https://github.com/mpate154), [@z3yn3p-alta](https://github.com/z3yn3p-alta). Check out their [project](https://github.com/anikaguin/Axle-Informatics/tree/main).

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

#### Setup a fresh development environment

We recommend creating a fresh development environment to avoid conflicts with existing installations.

**Option 1: Using uv (recommended for faster setup)**

Note: Requires Node.js 22 to be installed separately.

```bash
# Create a virtual environment with Python 3.13
uv venv --python 3.13

# Install JupyterLab and framework dependencies
uv pip install jupyterlab==4.4.10 streamlit

# Activate the virtual environment
source .venv/bin/activate
```

**Option 2: Using conda**

```bash
# Create a new conda environment with all dependencies
conda create -n auto-dashboards -c conda-forge python=3.13 jupyterlab=4.4.10 nodejs=22

# Activate the environment
conda activate auto-dashboards

# Install framework dependencies
pip install streamlit
```

**Build and install the extension (applies to any environment):**

```bash
# Install Node.js dependencies
jlpm install

# Build the extension
jlpm build

# Install package in development mode (use 'uv pip install' for uv or 'pip install' for conda)
pip install -e .

# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite

# Server extension must be manually installed in develop mode
jupyter server extension enable auto_dashboards

# Rebuild extension Typescript source after making changes
jlpm build
```

Start JupyterLab:

```bash
jupyter lab
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

#### Cleaning build artifacts

If you encounter build errors or want to rebuild from scratch, clean the build artifacts first:

```bash
# WARNING: This removes ALL git-ignored files (like node_modules, .venv, build artifacts)
# Use with caution - make sure you've committed any important work!
git clean -Xdf

# Or clean only specific build outputs
jlpm clean            # Clean TypeScript build outputs
jlpm clean:all        # Complete clean (including labextension)
```

Then rebuild:

```bash
jlpm build
```

### Development uninstall

**For uv users:**

```bash
# Uninstall the package
uv pip uninstall auto-dashboards

# Optionally, remove the virtual environment
deactivate
rm -rf .venv
```

**For conda users:**

```bash
# Uninstall the package
pip uninstall auto-dashboards

# Optionally, remove the entire environment
conda deactivate
conda env remove -n auto-dashboards
```

### Packaging the extension

See [RELEASE](RELEASE.md)
