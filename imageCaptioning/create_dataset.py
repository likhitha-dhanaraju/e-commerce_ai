import os
import json
import shutil

cwd = os.getcwd()
directory =os.path.dirname(os.getcwd())
main_dir = os.path.join(directory,'apps')
content_folders = [	'ajio_products']
					#'bewakoof_products']
					#limeroad_products']

image_dir = os.path.join(cwd,'images_v5')
if os.path.exists(image_dir)==False:
	os.mkdir(image_dir)

text = open('annotations_ajio_v4_full(2).txt','w')

for main in content_folders:
	path = os.path.join(main_dir, main)
	for folder in os.listdir(path):

		folder_path = os.path.join(main_dir,main,folder)
		print(folder_path)

		if len(os.listdir(folder_path)) > 3000 :

			counter = 0
			for content_path in os.listdir(folder_path):

				if counter < 3000: 

					contents = os.listdir(os.path.join(folder_path,content_path))
					images = sorted([i for i in contents if '.json' not in i])
					json_file = [i for i in contents if '.json' in i][0]
					json_file = os.path.join(folder_path,content_path,json_file)
					f = open(json_file,'r')
					product_name =  json.load(f)['product_name']
					main_image = images[0]

					## creating annotations
					result = folder+'_'+content_path+'.jpg\t'+product_name+'\t'+folder+'\n'
					text.write(result)
					## copying image
					img_source = os.path.join(folder_path, content_path, main_image)
					img_dest = os.path.join(image_dir,folder+'_'+content_path+'.jpg')
					
					if os.path.exists(img_dest):
						print("FILE ALREADY EXISTS")
					shutil.copy(img_source,img_dest)
					counter +=1
			print(counter)
		print(len(os.listdir(image_dir)))

text.close()



