import cv2
import os
#后续应该封装成一个算法类
def apply_image_enhancement(input_folder, output_folder,params):
    # 遍历输入文件夹中的所有图像文件
    for file in os.listdir(input_folder):
        if file.endswith('.jpg') or file.endswith('.png'):
            input_file = os.path.join(input_folder, file)

            img = cv2.imread(input_file,0)

            # 进行图像增强操作
            # 对图像进行模糊处理，内核大小为 5
            #             params = {"filter_type": "blur", "kernel_size": 5}格式
            filtered_img = custom_filter(img, params)

            # # 对图像进行阈值化处理，阈值为 200
            # params = {"filter_type": "threshold", "threshold": 200}
            # filtered_img = custom_filter(img, params)
            #
            # # 对图像进行多次腐蚀和膨胀操作，迭代次数为 3
            # params = {"iterations": 3}
            # filtered_img = custom_filter(img, params)

            # 保存增强后的图像
            file_name, file_ext = os.path.splitext(file)
            output_file = os.path.join(output_folder, str(file_name)+"%%"+str(params["filter_type"])+"%%"+str(params["kernel_size"])+str(file_ext))
            cv2.imwrite(output_file, filtered_img)


def custom_filter(image, parameters):
    #这种get 相当于有什么就拿什么 第二个参数是默认值
    """
    Applies a custom filter to an image based on the given parameters.
    """
    filter_type = parameters.get("filter_type", "blur")
    kernel_size = parameters.get("kernel_size", 3)
    threshold = parameters.get("threshold", 127)
    iterations = parameters.get("iterations", 1)

    if filter_type == "blur":
        filtered = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    elif filter_type == "threshold":
        _, filtered = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    else:
        filtered = image

    for i in range(iterations):
        filtered = cv2.erode(filtered, None, iterations=1)
        filtered = cv2.dilate(filtered, None, iterations=1)

    return filtered



# if __name__ == '__main__':
#     params = {"filter_type": "blur", "kernel_size": 5}
#
#     apply_image_enhancement("/Users/elona/Desktop/pythonProject/IQA_Software2/IQA_Software/need","/Users/elona/Desktop/pythonProject/IQA_Software2/IQA_Software/oout",params)
#
