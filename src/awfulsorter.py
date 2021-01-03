# Awful Sorter 2.0 by David Malášek
import os
import shutil
import sys

SETTINGS = {
    "general": {
        "createSubDirectories": True,
        "overWriteDuplicates": False,
        "sortDuplicates": False,
        "showDevTools": False,
    },
    "supportedExtensions": {
        "Documents": ["txt", "docx", "doc", "pdf"],
        "Spreadsheets": ["xls", "xlsx"],
        "Scripts": ["py", "js", "php", "cpp", "cs", "html", "css", "jsx", "json"],
        "Images": ["png", "jpg", "jpeg", "gif", "svg"],
        "Videos": ["mp4", "mov"],
        "Compressed files": ["rar", "zip"],
        "Others": [],
    },
    "restrictedFiles": [],
}

generateTestFiles = False

FILENAME = os.path.basename(__file__)

currentPath = os.path.dirname(__file__)
currentFiles = os.listdir(currentPath)

generalSettings = SETTINGS["general"]
supportedExtensions = SETTINGS["supportedExtensions"]

restrictedFiles = SETTINGS["restrictedFiles"]


def getFolderName(fileExtension):
    returnList = []
    for i in supportedExtensions:
        for e in supportedExtensions[i]:
            if e == fileExtension.lower():
                returnList.append(i)
    if len(returnList) == 1:
        return returnList[0]
    else:
        return list(supportedExtensions.keys())[-1]


def createFolder(fileExtension, createDirectly=False, parentDirectoryName=""):
    if createDirectly:
        targetPath = os.path.join(
            currentPath, parentDirectoryName, fileExtension.lower()
        )
    else:
        targetPath = os.path.join(currentPath, getFolderName(fileExtension.lower()))

    if not os.path.isdir(targetPath):
        os.makedirs(targetPath)


def correctEnding(word, number, reversedEnding=False):
    if number < 2:
        if reversedEnding:
            return word + "s"
        else:
            return word
    else:
        if reversedEnding:
            return word
        else:
            if word.endswith("y"):
                return word[: len(word) - 1] + "ies"
            else:
                return word + "s"


if FILENAME in currentFiles:
    currentFiles.remove(FILENAME)  # Remove this file from file list

folders = []
for i in currentFiles:  # Append folder names to folders list
    if os.path.isdir(os.path.join(currentPath, i)):
        folders.append(i)

for i in folders:  # Remove folders from currentFiles list
    currentFiles.remove(i)

if generateTestFiles:
    totalFiles = 0
    for i in supportedExtensions:
        for e in supportedExtensions[i]:
            totalFiles += 1
            with open(os.path.join(currentPath, "test." + e), "w"):
                pass
    print("\n" + "🔨  Generated total of " + str(totalFiles) + " test files.")

else:
    if len(currentFiles) == 0:
        if generalSettings["createSubDirectories"]:
            registeredDirectories = []
            sortIndex = 0
            directoryIndex = 0
            duplicatesFound = 0

            _currentFiles = []

            for i in folders:
                for e in os.listdir(os.path.join(currentPath, i)):
                    if os.path.isfile(os.path.join(currentPath, i, e)):
                        _currentFiles.append(e)

            for i in folders:
                for e in os.listdir(os.path.join(currentPath, i)):  # Node LEVEL 1
                    if os.path.isfile(os.path.join(currentPath, i, e)):  # Node LEVEL 2
                        fileExtension = e.split(".")[-1]
                        folderName = getFolderName(fileExtension)
                        basePath = os.path.join(currentPath, i, e)
                        createFolder(
                            fileExtension,
                            createDirectly=True,
                            parentDirectoryName=folderName,
                        )
                        targetPath = os.path.join(
                            currentPath, folderName, fileExtension
                        )
                        if not os.path.isfile(os.path.join(targetPath, e)):
                            shutil.move(basePath, targetPath)
                            sortIndex += 1
                        else:
                            duplicatesFound += 1

                        if targetPath not in registeredDirectories:
                            directoryIndex += 1
                        registeredDirectories.append(targetPath)

            if sortIndex != 0 and duplicatesFound == 0:
                if generalSettings["showDevTools"]:
                    print("OUTPUT 1")
                print(
                    "\n"
                    + "✅  Successfuly sorted "
                    + str(sortIndex)
                    + " "
                    + correctEnding("file", sortIndex)
                    + " into "
                    + str(directoryIndex)
                    + " "
                    + correctEnding("subdirectory", directoryIndex)
                    + "."
                )
            elif sortIndex != 0 and duplicatesFound != 0:
                if generalSettings["showDevTools"]:
                    print("OUTPUT 2")
                print(
                    "\n"
                    + "✅  Successfuly sorted "
                    + str(sortIndex)
                    + " "
                    + correctEnding("file", sortIndex)
                    + " into "
                    + str(directoryIndex)
                    + " "
                    + correctEnding("subdirectory", directoryIndex)
                    + "\n⚠️  Found "
                    + str(duplicatesFound)
                    + " "
                    + correctEnding("duplicate", duplicatesFound)
                    + "."
                )
            elif sortIndex == 0 and duplicatesFound != 0:
                if generalSettings["showDevTools"]:
                    print("OUTPUT 3")
                print(
                    "\n⚠️  Found "
                    + str(duplicatesFound)
                    + " "
                    + correctEnding("duplicate", duplicatesFound)
                    + "."
                )
            else:
                if generalSettings["showDevTools"]:
                    print("OUTPUT 4")
                print(
                    "\n"
                    + "⚠️  Nothing changed => No files in current directory or subdirectories."
                )
            exit()
        else:
            print("\n" + "⚠️  Nothing changed => No files in current directory.")
            exit()
    else:
        print("\n" + "⚙️  CURRENT WORKING DIRECTORY: " + currentPath)
        checkSettingStatus = []
        for i in generalSettings:
            checkSettingStatus.append("✅" if generalSettings[i] else "❌")

        for i in range(len(generalSettings)):
            print(
                "   => "
                + list(generalSettings.keys())[i]
                + ": "
                + checkSettingStatus[i]
            )

        if generalSettings["overWriteDuplicates"] and generalSettings["sortDuplicates"]:
            print(
                "\n"
                + "⚠️  Settings conflict => Cannot set both 'overWriteIfDuplicate' and 'sortDuplicates' to True. This will set 'sortDuplicates' to False."
            )
            generalSettings["sortDuplicates"] = False

    didOverwrite = False
    didThrowDuplicateError = False
    multipleDuplicates = False

    sortIndex = 0
    directoryIndex = 0
    duplicateErrorIndex = 0
    multipleDuplicatesIndex = 0

    registeredDirectories = []

    # Main algorithm
    for i in currentFiles:
        if os.path.isfile(os.path.join(currentPath, i)) and i not in restrictedFiles:
            fileExtension = i.split(".")[-1]
            folderName = getFolderName(fileExtension)
            createFolder(fileExtension)
            basePath = os.path.join(currentPath, i)

            sortIndex += 1
            try:
                if generalSettings["createSubDirectories"]:
                    createFolder(
                        fileExtension,
                        createDirectly=True,
                        parentDirectoryName=folderName,
                    )
                    targetPath = os.path.join(currentPath, folderName, fileExtension)
                else:
                    targetPath = os.path.join(currentPath, folderName)

                if generalSettings["overWriteDuplicates"] and os.path.isfile(
                    os.path.join(targetPath, i)
                ):
                    didOverwrite = True
                    shutil.copy(basePath, targetPath)
                    os.remove(basePath)
                else:
                    shutil.move(basePath, targetPath)

                if targetPath not in registeredDirectories:
                    directoryIndex += 1
                registeredDirectories.append(targetPath)

            except:
                if generalSettings["sortDuplicates"]:
                    targetPath = os.path.join(currentPath, "Duplicates")
                    if not os.path.isdir(targetPath):
                        os.makedirs(targetPath)
                    if not os.path.isfile(os.path.join(targetPath, i)):
                        shutil.move(basePath, targetPath)
                    elif generalSettings["overWriteDuplicates"] and os.path.isfile(
                        os.path.join(targetPath, i)
                    ):
                        didOverwrite = True
                        shutil.copy(basePath, targetPath)
                    else:
                        multipleDuplicatesIndex += 1
                        multipleDuplicates = True

                duplicateErrorIndex += 1
                didThrowDuplicateError = True

    if (
        didThrowDuplicateError
        and generalSettings["sortDuplicates"]
        and multipleDuplicates
    ):
        if generalSettings["showDevTools"]:
            print("OUTPUT 5")
        print(
            "\n"
            + "⚠️  Found "
            + str(multipleDuplicatesIndex)
            + " "
            + correctEnding("duplicate", multipleDuplicatesIndex)
            + " that already "
            + correctEnding("exist", multipleDuplicatesIndex, reversedEnding=True)
            + " inside Duplicates folder."
        )
    elif didThrowDuplicateError and generalSettings["sortDuplicates"]:
        if generalSettings["showDevTools"]:
            print("OUTPUT 6")
        print(
            "\n"
            + "✅  Moved "
            + str(duplicateErrorIndex)
            + " files into Duplicates folder."
        )
    elif didThrowDuplicateError:
        if generalSettings["showDevTools"]:
            print("OUTPUT 7")
        print(
            "\n"
            + "⚠️  Found "
            + str(duplicateErrorIndex)
            + " "
            + correctEnding("duplicate", duplicateErrorIndex)
            + "."
        )
    elif didOverwrite:
        if generalSettings["showDevTools"]:
            print("OUTPUT 8")
        print(
            "\n"
            + "✅  Successfuly overwrited "
            + str(sortIndex)
            + " "
            + correctEnding("file", sortIndex)
            + "."
        )
    elif generalSettings["createSubDirectories"]:
        if generalSettings["showDevTools"]:
            print("OUTPUT 9")
        afterDirectory = os.listdir(currentPath)
        afterDirectory.remove(FILENAME)
        print(
            "\n"
            + "✅  Successfuly sorted "
            + str(sortIndex)
            + " "
            + correctEnding("file", sortIndex)
            + " into "
            + str(len(afterDirectory))
            + " "
            + correctEnding("directory", len(afterDirectory))
            + " and "
            + str(directoryIndex)
            + " "
            + correctEnding("subdirectory", directoryIndex)
            + "."
        )
    else:
        if generalSettings["showDevTools"]:
            print("OUTPUT 10")
        print(
            "\n"
            + "✅  Successfuly sorted "
            + str(sortIndex)
            + " "
            + correctEnding("file", sortIndex)
            + " into "
            + str(directoryIndex)
            + " "
            + correctEnding("directory", directoryIndex)
            + "."
        )
