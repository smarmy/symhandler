# symhandler.py

A little tool to manage symlinks. Reads a json config file and creates or
deletes symlinks.

## Example

```json
{
  "dotfiles/vimrc": "$HOME/.vimrc",
  "dotfiles/xinitrc": "$HOME/.xinitrc",
  "emacs/init.el": "$HOME/.emacs/init.el"
}
```

## TODO

Support for folders

