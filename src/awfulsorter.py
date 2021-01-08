"""
Awful Sorter by David Malášek - Licensed under the MIT License.
See all versions in VERSIONS.md 
"""
import os, shutil, colorama
from colorama import Fore

SETTINGS = {
    "general": {
        "sortToSubdirectories": False,
        "overWriteDuplicates": False,
    },
    "supportedExtensions": {
        "Documents": ["txt", "docx", "doc", "pdf"],
        "Spreadsheets": ["xls", "xlsx"],
        "Scripts":
        ["py", "js", "php", "cpp", "cs", "html", "css", "jsx", "json"],
        "Images": ["png", "jpg", "jpeg", "gif", "svg"],
        "Videos": ["mp4", "mov"],
        "Compressed files": ["rar", "zip"],
        "Others": [],
    },
    "restricted": [""],
}

generateTestFiles = False

FILENAME = os.path.basename(__file__)
CURRENT_PATH = os.path.dirname(__file__)

currentFiles = os.listdir(CURRENT_PATH)

generalSettings = SETTINGS["general"]
supportedExtensions = SETTINGS["supportedExtensions"]
restricted = SETTINGS["restricted"]

colorama.init(autoreset=True)


def getDirectoryName(fileExtension):
    returnList = []
    for i in supportedExtensions:
        for e in supportedExtensions[i]:
            if e == fileExtension.lower():
                returnList.append(i)
    if len(returnList) == 1:
        return returnList[0]
    else:
        return list(supportedExtensions.keys())[-1]


def createDirectory(path, directoryName):
    if not os.path.isdir(os.path.join(path, directoryName)):
        os.makedirs(os.path.join(path, directoryName))


def moveFile(basePath, targetPath, overWrite=False):
    if overWrite:
        shutil.copy(basePath, targetPath)
        os.remove(basePath)
    else:
        shutil.move(basePath, targetPath)


currentFiles.remove(FILENAME)  # Remove this module from file list

if generateTestFiles:
    totalFiles = 0
    for i in supportedExtensions:
        for e in supportedExtensions[i]:
            if not os.path.isfile(os.path.join(CURRENT_PATH, "test." + e)):
                with open(os.path.join(CURRENT_PATH, "test." + e), "w"):
                    pass
                totalFiles += 1
    if totalFiles != 0:
        print(
            (Fore.GREEN + "\nSUCCESS" + Fore.WHITE + " - Generated total of " +
             Fore.GREEN + "{} files" + Fore.WHITE + ".").format(totalFiles))
    else:
        print(Fore.YELLOW + "\nWARNING" + Fore.WHITE +
              " - Test files already generated, please set " + Fore.YELLOW +
              "generateTestFiles" + Fore.WHITE + " to " + Fore.LIGHTCYAN_EX +
              "False" + Fore.WHITE + ".")
else:
    sortIndex = 0  # Keeps track of how many files have been sorted
    directoryList = [  # Its length keeps track of how many directories files have been sorted to
    ]
    duplicateIndex = 0  # Keeps track of how many duplicates have been found

    for i in currentFiles:
        if os.path.isfile(os.path.join(CURRENT_PATH,
                                       i)) and i not in restricted:
            fileExtension = i.split(".")[-1].lower()
            directoryName = getDirectoryName(fileExtension)
            createDirectory(CURRENT_PATH, directoryName)
            basePath = os.path.join(CURRENT_PATH, i)

            if generalSettings["sortToSubdirectories"]:
                createDirectory(os.path.join(CURRENT_PATH, directoryName),
                                fileExtension)
                targetPath = os.path.join(CURRENT_PATH, directoryName,
                                          fileExtension)
                directoryName = fileExtension
            else:
                targetPath = os.path.join(CURRENT_PATH, directoryName)

            if generalSettings["overWriteDuplicates"]:
                moveFile(basePath, targetPath, overWrite=True)
                sortIndex += 1
            elif not os.path.isfile(os.path.join(targetPath, i)):
                moveFile(basePath, targetPath)
                sortIndex += 1
            else:
                duplicateIndex += 1

            if directoryName not in directoryList:
                directoryList.append(directoryName)

        elif os.path.isdir(os.path.join(CURRENT_PATH,
                                        i)) and i not in restricted:
            currentDirectoryFiles = os.listdir(os.path.join(CURRENT_PATH, i))
            for e in currentDirectoryFiles:
                if os.path.isfile(os.path.join(CURRENT_PATH, i, e)):
                    fileExtension = e.split(".")[-1].lower()
                    basePath = os.path.join(CURRENT_PATH, i, e)
                    targetPath = os.path.join(CURRENT_PATH, i, fileExtension)
                    if generalSettings["sortToSubdirectories"]:
                        createDirectory(os.path.join(CURRENT_PATH, i),
                                        fileExtension)
                        if generalSettings["overWriteDuplicates"]:
                            moveFile(basePath, targetPath, overWrite=True)
                        else:
                            moveFile(basePath, targetPath)
                        sortIndex += 1

    print((Fore.LIGHTGREEN_EX + "\nCURRENT WORKING DIRECTORY: " + Fore.YELLOW +
           "{}").format(CURRENT_PATH))

    for i in range(len(generalSettings)):
        print(("   => {}: {}").format(
            list(generalSettings.keys())[i],
            Fore.GREEN + str(list(generalSettings.values())[i])
            if list(generalSettings.values())[i] else Fore.RED +
            str(list(generalSettings.values())[i])))

    if sortIndex + len(directoryList) + duplicateIndex == 0:
        print(Fore.YELLOW + "\nWARNING" + Fore.WHITE +
              " - Nothing changed => No files to sort.")
    else:
        if sortIndex != 0 and len(directoryList) != 0:
            print((Fore.GREEN + "\nSUCCESS" + Fore.WHITE +
                   " - Successfully sorted " + Fore.GREEN + "{} file(s)" +
                   Fore.WHITE + " into " + Fore.GREEN + "{} directory(s)" +
                   Fore.WHITE + ".").format(sortIndex, len(directoryList)))
        if duplicateIndex != 0 and sortIndex == 0:
            print((Fore.RED + "\nDUPLICATE" + Fore.WHITE + " - Found " +
                   Fore.RED + "{} duplicate(s)" + Fore.WHITE +
                   ", nothing changed.").format(duplicateIndex))
        elif duplicateIndex != 0:
            print((Fore.RED + "\nDUPLICATE" + Fore.WHITE + " - Found " +
                   Fore.RED + "{} duplicate(s)" + Fore.WHITE +
                   ".").format(duplicateIndex))
