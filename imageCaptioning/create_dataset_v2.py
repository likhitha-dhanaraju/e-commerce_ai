import os
import json
import shutil

# get the path of the data obtained from ProductsScrappers
main_dir = '/home/likhitha/Documents/Internships 2020/Vectorised_ai/ImageCaptioning'

# data from the websites to be used
content_folders = [	['ajio_products', '1000'],
					['limeroad_products', '200'] ]
					#['myntra_products', 1000 ]
print(content_folders)
					
# final path of the image folder
cwd = os.getcwd()
image_dir = os.path.join(cwd,'images_v5')
if os.path.exists(image_dir)==False:
	os.mkdir(image_dir)

# filename of the annotations file
text = open('annotations_v5.txt','w')

for (main, number_items) in content_folders:
	
	# obtaining the full path of the data folder
	path = os.path.join(main_dir, main)

	for folder in os.listdir(path):

		# full path of sub category folder in the website folder
		folder_path = os.path.join(main_dir,main,folder)
		print(folder_path)


		# checking if products in the category are greater than the required quantity.
		if len(os.listdir(folder_path)) >= int(number_items) :

			counter = 0

			# looping through each product in the sub category folder
			for content_path in os.listdir(folder_path):

				if counter < int(number_items): 

					# getting the full path of the product folder
					contents = os.listdir(os.path.join(folder_path,content_path))
					
					# getting the list of all images of the product
					images = sorted([i for i in contents if '.json' not in i])
					
					# getting the annotation file name
					json_file = [i for i in contents if '.json' in i][0]
					
					# getting the full path of the json file.
					json_file = os.path.join(folder_path,content_path,json_file)
					
					# reading the product name
					f = open(json_file,'r')
					product_name =  json.load(f)['product_name']
					
					if len(images) > 2:
						for num in range(2):
							main_image = images[num]

							## creating annotations
							result = folder +'_'+ content_path + '{}.jpg\t'.format(str(num)) + product_name + '\t' + folder + '\n'
							text.write(result)
							## copying image
							img_source = os.path.join(folder_path, content_path, main_image)
							img_dest = os.path.join(image_dir,folder+'_'+ content_path + '{}.jpg'.format(str(num)))
							
							#if os.path.exists(img_dest):
							#	print("FILE ALREADY EXISTS")
							shutil.copy(img_source,img_dest)
						counter +=1

					else:
						main_image = images[0]

						## creating annotations
						result = folder+'_'+content_path+'.jpg\t'+product_name+'\t'+folder+'\n'
						text.write(result)

						## copying image
						img_source = os.path.join(folder_path, content_path, main_image)
						img_dest = os.path.join(image_dir,folder+'_'+ content_path + '.jpg')
						
						#if os.path.exists(img_dest):
						#	print("FILE ALREADY EXISTS")
						shutil.copy(img_source,img_dest)
						counter +=1

				else:
					break

			print(counter)

print(len(os.listdir(image_dir)))
text.close()



