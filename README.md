# Awful Sorter

#### Awful Sorter is a tool for sorting files to directories. How? You decide!

This is an example of a **Automate The Boring Stuff** project. Reason why is this tool so useful is because the main algorithm depends on a bunch of **settings** which give you a full control over sorting your files!

## General settings ⚙️

|          Name          |  Type  | When `True`                                                                                                                                       |
| :--------------------: | :----: | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sortToSubdirectories` | `bool` | Files will be sorted to additional subdirectories depending on their file extensions.                                                             |
| `overWriteDuplicates`  | `bool` | Duplicate files inside the root directory will overwrite original files inside 1. and 2. level directories (depending on `sortToSubdirectories`). |

- `sortToSubdirectories` modifies the reach of the algorithm
- when `sortToSubdirectories` is `True`, algorithm will attempt to sort files inside 1. level directories to subdirectories inside 2. level directories even if there are no files inside the root directory

## Supported extensions

Supported file extensions are stored in key-value pairs inside a dictionary. The key of the pair refers to directory where all files with a file extension stored inside the value should go.

```python
"supportedExtensions": {
        "Documents": ["txt", "docx", "doc", "pdf"],
        "Spreadsheets": ["xls", "xlsx"],
        "Scripts": ["py", "js", "php", "cpp", "cs", "html", "css", "jsx", "json"],
        "Images": ["png", "jpg", "jpeg", "gif", "svg"],
        "Videos": ["mp4", "mov"],
        "Compressed files": ["rar", "zip"],
        "Others": [],
}
# For example, test.txt file would be sorted into Documents directory
```

Feel free to add as many file extension as you want. Notice the key named **_Others_** with an empty list as a value at the bottom of the dictionary. This refers to directory where all files with unsupported file extensions should go.

## Restricted files

Sometimes things should stay just in one place. That's why you can list all the files and folders you don't want algorithm to move with.

```python
# This is case-sensitive!
"restrictedFiles": ["document.txt, Myfolder"]
# Those files won't move a inch
```

## Final words

If you want to test this tool, feel free to use built-in test file generator. Search for a variable named `generateTestFiles`. Setting this to `True` will generate 1 test file for each file extension listed under **_supportedExtensions_** and will turn off the main algorithm.

## Versions

See [VERSIONS](VERSIONS.md) for a list of versions and changes made.

## License

Licensed under the [MIT License](LICENSE).
