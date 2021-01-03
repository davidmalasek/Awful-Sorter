# Awful Sorter

Awful Sorter is an example of a **Automate The Boring Stuff** project. Reason why is this tool so useful is because the main algorithm depends on a bunch of **settings** which give you a full control over sorting your files!

---

## General settings ⚙️

|          Name          | Value  | When `True`                                                                                                                           |
| :--------------------: | :----: | -------------------------------------------------------------------------------------------------------------------------------------- |
| `createSubDirectories` | `bool` | Files will be sorted into directories depending on their type and subdirectories depending on their file extension.       |
| `overWriteDuplicates`  | `bool` | Original file already existing inside a directory will be overwritted by its duplicate file existing in a root directory. |
|    `sortDuplicates`    | `bool` | Every duplicate will be sorted into **_Duplicates_** directory.                                                           |

### Important notes ⚠️

##### Please note that some variations of settings above can affect the sorting algorithm in a way you might not expect. 

For example, `createSubDirectories` set to `True` allows algorithm go 1 extra level below the 1. level directory. Once you set this to `False`, 2. level directory is out of reach and some functions like overwriting might not work.

When `createSubDirectories` is set to `True`, algorithm will try to sort files inside 1. level directories to subdirectories based on their file extension even if there are no files in the root directory.

Both `overWriteDuplicates` and `sortDuplicates` cannot be set to `True` at the same time, the way algorithm is dealing with this is setting `sortDuplicates` to `False`. 

Note that duplicates inside **_Duplicates_** directory cannot be overwritten or sorted to subdirectories.

---

## Supported extensions

Supported file extensions are stored in key-value pairs inside a dictionary. The key of the pair refers to directory where all files with file extension stored inside the value should go.

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

---

## Restricted files

Sometimes things should stay just in one place. That's why you can list all the files you don't want algorithm to move with.

```python
"restrictedFiles": ["notpasswords.txt"]
# Those files won't move a inch
```

---

## Final words

If you want to test this tool, feel free to use built-in test file generator. In the main file, search for a variable named `generateTestFiles`. Setting it to `True` will generate 1 test file for each file extension listed under **_supportedExtensions_** and will turn off the main algorithm.

---

## License

Licensed under the [MIT License](LICENSE).
