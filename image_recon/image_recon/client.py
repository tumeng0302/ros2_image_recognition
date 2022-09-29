import cv2
import rclpy
import sys
import numpy as np
import os

from rclpy.node import Node
from cv_bridge import CvBridge
from my_interface.srv import Img

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('image_recongnition_client')
        self.cli = self.create_client(Img, 'image_recong')       # CHANGE
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Img.Request()

    def send_request(self):
        bridge = CvBridge()
        imagename=('/home/pi/ros2_ws/src/image_recon/image_recon/images/%s'%sys.argv[1])
        cv_image = cv2.imread(imagename)
        ros_image = bridge.cv2_to_imgmsg(cv_image)
        self.req.img=ros_image
        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)

    img_client=MinimalClientAsync()
    img_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(img_client)
        if img_client.future.done():
            try:
                response = img_client.future.result()
            except Exception as e:
                img_client.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                img_client.get_logger().info("%s"%response.result)
            break

    img_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
