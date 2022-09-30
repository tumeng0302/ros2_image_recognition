import cv2
import rclpy
import image_recog.imageRec as recog

from my_interface.srv import Img
from cv_bridge import CvBridge
from rclpy.node import Node

class MinimalService(Node):

    def __init__(self):
        super().__init__('image_recognition_service')
        self.srv = self.create_service(Img, 'image_recog', self.image_recog_callback)

    def image_recog_callback(self, request, response):
        bridge = CvBridge()
        cv_image=bridge.imgmsg_to_cv2(request.img)
        self.get_logger().info('Incoming request!!')
        response.result=recog.main(cv_image)
        return response

def main(args=None):
    try:
        rclpy.init(args=args)
        img_service = MinimalService()
        rclpy.spin(img_service)
        rclpy.shutdown()
    except:
        pass

if __name__ == '__main__':
    main()
