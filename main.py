import os
import zipfile
import shutil

PATH_TO_OUTPUT = "./output/"
PATH_TO_ZIPS = "./temp/zips/"
PATH_TO_TEMP_LATE = "./temp/temp_template/"
PATH_TO_TEMP_SETS = "./temp/temp_sets/"


def main():
    print("Starting MSE Set Combiner! \n All will be one.")

    #  Sanity check on template file
    if len([f for f in os.listdir("./place_template_set_here") if f == 'template.mse-set']) < 1:
        print("Make sure you put in a template file! It must be named \"template.mse-set\"")
        return
    elif len([f for f in os.listdir("./place_template_set_here") if f.endswith('.mse-set')]) > 1:
        print("Only put in a single template file and no other mse sets! Stopping.")
        return


    # check and see if output and temp are not clear, and prompt if we clear them
    # clean up output and temp as a preemptive measure
    cleanUp(log=True)

    #
    # TEMPLATE FILE
    #
    print("Handling template file")
    copyAndExtract("./place_template_set_here/template.mse-set", "template", True)

    # Get the template's top block
    setTop = getTopFromSetFile(PATH_TO_TEMP_LATE + "template/set")
    appendToOutputSetFile(setTop, overwrite=True) # Overwrite the existing file

    # copy the template's set symbol
    set_symbol = [f for f in os.listdir(PATH_TO_TEMP_LATE + "template") if f.endswith('.mse-symbol')]

    if len(set_symbol) == 0:
        print("No set symbol found!")
    else:
        if len(set_symbol) > 1:
            print("more than one set symbol found! Using: " + set_symbol[0])
        shutil.copy(PATH_TO_TEMP_LATE + "template/" + set_symbol[0], PATH_TO_OUTPUT + "/" + set_symbol[0])

    #
    # SET FILES
    #
    print("Handling set files!")

    nameCounter = 0
    for file in os.listdir("./place_mse_sets_here/"):
        if file == ".gitkeep":
            continue

        print("copying file " + file)
        try:
            copyAndExtract("./place_mse_sets_here/" + file, "setNum" + str(nameCounter))
            nameCounter += 1
        except:
            print("error with extracting " + str(file) + ". Continuing on...")
    

    imageCounter = 1 # indexing at 0 because MSE indexes at 1 and it's incredibly rude
    for setFolder in os.listdir(PATH_TO_TEMP_SETS):
        # ignore gitkeep
        if setFolder == ".gitkeep":
            continue

        setImages = [f for f in os.listdir(PATH_TO_TEMP_SETS + setFolder) if f.startswith("image")]
        mainframeImages = [f for f in os.listdir(PATH_TO_TEMP_SETS + setFolder) if f.startswith("mainframe_image")]

        # grab cards from set file
        cards = getCardsFromSetFile(PATH_TO_TEMP_SETS + setFolder + "/set")

        for imgArr in [setImages, mainframeImages]:
            # change the names of each image file and copy into output
            for img in imgArr:
                newImgName = "image" + str(imageCounter)

                # copy over the images with new name
                shutil.copy(PATH_TO_TEMP_SETS + setFolder + "/" + img, PATH_TO_OUTPUT + newImgName) # copy img over

                
                # replace old image name with temporary one
                for i in range(len(cards)):
                    # new lines and file extension checks should handle weird things
                    # like image1 and image13 bumping heads

                    # Some files have both image1.png and image1 as files, so this handles it
                    if (": " + img + "\n") in cards[i]:
                        cards[i] = cards[i].replace(": " + img + "\n",": setCondensed" + str(imageCounter) + "\n")
                        imageCounter += 1
                    

        # Then go ahead and change them back to image1-imageN format because MSE needs them named as such (stupidly)
        for n in range(imageCounter + 1):
            for i in range(len(cards)):
                cards[i] = cards[i].replace(": setCondensed" + str(n) + "\n",": image" + str(n) + "\n")

        # copy over the cards block
        appendToOutputSetFile(cards)


    #
    # FINAL TOUCHES
    #
    print("Finished copying all cards! Wrapping up.")

    # Get the template's bottom block
    setBottom = getBottomFromSetFile(PATH_TO_TEMP_LATE + "template/set")
    appendToOutputSetFile(setBottom)

    # Zip up the contents of the output folder
    zf = zipfile.ZipFile("./temp/combined.mse-set", mode="w")
    try:
        for filename in os.listdir("./output/"):
            if filename == ".gitkeep":
                continue

            # SOme error handling on my part
            try: 
                filename.index(".")
                print("File" + filename + "with not accounted for ending! This may break things; go tell Piguy about it")
            except:
                pass
            zf.write("./output/" + filename, filename, compress_type=zipfile.ZIP_DEFLATED)
    except FileNotFoundError:
        print("that's really odd; file not found despite checking for all the files here")
    finally:
        zf.close()
        shutil.move("./temp/combined.mse-set", "./output/combined.mse-set")

    cleanUp(leaveCombined=True)

    print("Done! All is now one.")
    print("file is in output/combined.mse-set")


def cleanUp(log=False, leaveCombined=False):
    if len(os.listdir("./temp/temp_sets/")) > 1:
        if log:
            print("temp_sets folder has junk in there. Cleaning it up...")
        emptyDir("./temp/temp_sets/")
        # emptyDir("./output/", ignore=["set"])    # For debugging


    if len(os.listdir("./temp/temp_template/")) > 1:
        if log:
            print("temp_template folder has junk in there. Cleaning it up...")
        emptyDir("./temp/temp_template/")

    if len(os.listdir("./temp/zips/")) > 1:
        if log:
            print("zips folder has junk in there. Cleaning it up...")
        emptyDir("./temp/zips/")

    if len(os.listdir("./output/")) > 1:
        if log:
            print("Output folder has the following files:")
            for file in os.listdir("./output/"):
                if file != ".gitkeep":
                    print(file)
            if input("\nDelete these files? Y for yes, n for no.\n") != "Y":
                raise KeyboardInterrupt("Go get everything you need out of output!") 
    
        if leaveCombined:
            emptyDir("./output/", ignore=["combined.mse-set"])
            # emptyDir("./output/", ignore=["combined.mse-set", "set"])    # For debugging
        else:
            emptyDir("./output/")



def copyAndExtract(filepath, newFilename, template=False):
    temp_path = PATH_TO_TEMP_SETS
    if template:
        temp_path = PATH_TO_TEMP_LATE

    shutil.copy(filepath, PATH_TO_ZIPS + newFilename + ".zip")

    with zipfile.ZipFile(PATH_TO_ZIPS + newFilename + ".zip", 'r') as zip_ref:
        zip_ref.extractall(temp_path + newFilename)
 
def appendToOutputSetFile(arr, overwrite=False):
    if overwrite:
        f = open("./output/set", "w", encoding="utf-8")    
    else:
        f = open("./output/set", "a", encoding="utf-8")    

    for i in arr:
        f.write(i)

# pulls text from the set file based on the start and end indicators (end indicator is not included)
def getFromSetFile(filepath, startIndicator="", endIndicator="", stopper=False):
    f = open(filepath, "r", encoding="utf-8")
    txt = f.readlines()
    f.close()

    startOfBlock = 0
    if startIndicator != "":
        startOfBlock = -1
        for i in range(len(txt)):
            if startIndicator == txt[i]:
                startOfBlock = i
                break

    endOfBlock = len(txt)
    if endIndicator != "":
        endOfBlock = -1
        for j in range(len(txt)):
            if endIndicator in txt[j]:
                endOfBlock = j
                break
    
    # could be from older versions; they didn't use underscores in "version_control" tag
    if startOfBlock == -1 or endOfBlock == -1:
        print("not found start nor end of card block... weird.")
        print("Try opening the set file anyways when done; it might work still if I'm good at debugging.")
        if not stopper:
            startIndicator = startIndicator.replace("_", " ")
            endIndicator = endIndicator.replace("_", " ")
            return getFromSetFile(filepath, startIndicator, endIndicator, stopper=True)


    return txt[startOfBlock:endOfBlock]

def getTopFromSetFile(filepath):
    return getFromSetFile(filepath, endIndicator="card:\n")

def getBottomFromSetFile(filepath):
    return getFromSetFile(filepath, startIndicator="version_control:\n")

def getCardsFromSetFile(filepath):
    return getFromSetFile(filepath, startIndicator="card:\n", endIndicator="version_control:\n")

def emptyDir(path, ignore=[]):
    contents = os.listdir(path)

    for obj in contents:
        if obj == ".gitkeep" or obj in ignore:
            continue

        if os.path.isdir(path + obj):
            emptyDir(path + obj + "/")
            os.rmdir(path + obj) 
        else:
            os.remove(path + obj)

if __name__ == "__main__":
    main()