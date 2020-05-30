# import os

# directory = os.fsencode("anonymized")

# for file in os.listdir(directory):
#      filename = os.fsdecode(file)
#      if filename.endswith(".png") or filename.endswith(".png"): 
#          print(os.path.join(directory, filename))
#          continue
#      else:
#          continue
import os
import toS3
# for subdir, dirs, files in os.walk("anonymized"):
#     for file in files:
#         #print os.path.join(subdir, file)
#         filepath = subdir + os.sep + file

#         if filepath.endswith(".png"):
#             print (filepath)

# import zipfile

# def zipdir(path, ziph):
# 	# ziph is zipfile handle
# 	for root, dirs, files in os.walk(path):
# 		for file in files:
# 			ziph.write(os.path.join(root, file))

# zipf = zipfile.ZipFile('Test.zip','w',zipfile.ZIP_DEFLATED)
# zipdir('anonymized',zipf)
# zipf.close()
toS3.upload(True)