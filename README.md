# mrgreengenes

A colorscheme for anyone who loves their eyes, their code, and a touch of green.

This repository mainly provides Jinja2 templates that can be used to generate theme
configurations and plugins for various applications.

## Configuration

Colors and theme settings are defined in **`theme.yaml`**. The Jinja2 templates reference
these settings to generate the final configurations. Any changes to the theme should
generally be made in this file. Template-specific mappings determine how these settings
are applied in each generated output.

## Template generation

Templates are used to generate colorscheme files for the following supported applications:

- Alacritty
- fish
- Lazygit
- Neovim
- tmux

Running the templates produces ready-to-use theme configurations for these applications.

## Workflow

Version tags (`v*`) trigger workflows for generating and updating plugin repositories
or configuration outputs. This is designed to automate distribution of the generated
themes across supported platforms.

## Generating Locally

All outputs can be generated locally by running:

```bash
python generate.py
```
