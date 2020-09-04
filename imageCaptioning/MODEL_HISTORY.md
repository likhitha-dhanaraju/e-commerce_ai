# Versions of the Image Captioning model used

The model takes the image and the sequence the input and predicts one word at a time.


## Version 1

![Model 1](pictures/model1.png)

### Data used

T-shirt data from Ajio(90%) and Bewakoof(10%) initially.
Was later trained on data from other categories as well.

### Model

**Image Encoder** - Pre-trained VGG-16 network on the Imagenet dataset is used with global average pooling to the output of the last convolutional block whose output is a 2D Tensor. 

The idea of using global average pooling layer, is to reduce the dimensionality of the final vector and experimentation.

**Caption encoder** - Pre-trained GloVe vector embeddings were used to embed the captions, and an LSTM layer was added.

**Decoder** - The embeddings from the Image Encoder and Caption Encoder is combined and passed to the Dense layers.

### Performance

The model performed well on the T-shirt data. But poorly on the combination data of other categories. Reason being - the categories were not balanced.

--- 

## Version 2

![Model 2](pictures/model2.png)

### Data used

T-shirt data from Ajio(90%) and Bewakoof(10%) initially.
Was later trained on data from other categories as well.

### Model

**Image Encoder** - Pre-trained VGG-16 network on the Imagenet dataset is used with global average pooling to the output of the last convolutional block whose output is a 2D Tensor.

The idea of using global average pooling layer, is to reduce the dimensionality of the final vector and experimentation.

**Caption encoder** - Pre-trained GloVe vector embeddings were used to embed the captions, and a GRU layer was added. An attention layer was also added after it.

**Decoder** - The embeddings from the Image Encoder and Caption Encoder is combined and passed to the Dense layers.

### Performance

The model performed similar to Version 1

---

## Version 3

![Model 3](pictures/model3.png)

### Data used

3000 images from 13 categories from **AJIO**

- Categories:

-- Men's T-shirts
-- Men's Shirts
-- Men's Jeans
-- Men's Shoes
-- Men's Jackets

-- Women's Jackets
-- Women's Jeans
-- Women's Jewellery
-- Women's Kurtas
-- Women's Sarees
-- Women's Shoes
-- Women's Tops
-- Women's Shirts

### Model

**Image Encoder** - Pre-trained VGG-16 network on the Imagenet dataset is used with global *maximum* pooling to the output of the last convolutional block whose output is a 4D Tensor.

The intent of extracting a 4D vector from the pre-trained model from VGG16 model, is to add more Convolutional blocks.

**Caption encoder** - Untrained Embeddings were used to embed the captions, and 2 GRU layers were added. An attention layer was also added after it.

**Decoder** - The embeddings from the Image Encoder and Caption Encoder is combined and passed to the GRU and Dense layers.

### Performance

The model performed much better than the previous versions. Was predicting garbage values for a few test images, and a generalised caption for few categories such as Jackets, Jeans.

---

## Version 4

![Model 4](pictures/model4.png)

### Data used

3000 images from 13 categories from **AJIO**

- Categories:

-- Men's T-shirts
-- Men's Shirts
-- Men's Jeans
-- Men's Shoes
-- Men's Jackets

-- Women's Jackets
-- Women's Jeans
-- Women's Jewellery
-- Women's Kurtas
-- Women's Sarees
-- Women's Shoes
-- Women's Tops
-- Women's Shirts

### Model

**Image Encoder** - Pre-trained VGG-16 network on the Imagenet dataset is used with global *maximum* pooling to the output of the last convolutional block whose output is a 4D Tensor.

The intent of extracting a 4D vector from the pre-trained model from VGG16 model, is to add more Convolutional blocks.

**Caption encoder** - Untrained Embeddings were used to embed the captions, and 2 GRU layers were added. An attention layer was also added after it.

**Decoder** - The embeddings from the Image Encoder and Caption Encoder is combined and passed to the GRU and Dense layers to predict the caption.

**Category predictor** - The category of the product was also predicted by using the image encoder embeddings.

### Performance

The model performed much better than the previous versions. No garbage values were predicted. Generalised caption for few categories such as Jackets, Jeans were still being predicted.

---

Results can be viewed in the following document.

[Image Captioning results](https://docs.google.com/document/d/13UGWZkqLF0cvvN36hbTsZBkQjXkC2oQAPNR4MhzzEu4/edit?usp=sharing)




