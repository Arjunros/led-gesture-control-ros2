import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import cv2
import mediapipe as mp

class FingerDetectorNode(Node):
    def __init__(self):
        super().__init__('finger_detector')
        self.publisher_ = self.create_publisher(Int32, 'finger_count', 10)
        self.timer = self.create_timer(0.05, self.timer_callback)  # 20 FPS

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)

        self.TIP_IDS = [4, 8, 12, 16, 20]

    def count_fingers(self, hand_landmarks):
        fingers = []
        lm = hand_landmarks.landmark

        # Thumb
        if lm[self.TIP_IDS[0]].x < lm[self.TIP_IDS[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers
        for tip_id in self.TIP_IDS[1:]:
            if lm[tip_id].y < lm[tip_id - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        count = 0
        if results.multi_hand_landmarks:
            for hand_lm in results.multi_hand_landmarks:
                count = self.count_fingers(hand_lm)
                self.mp_draw.draw_landmarks(frame, hand_lm, self.mp_hands.HAND_CONNECTIONS)

        msg = Int32()
        msg.data = count
        self.publisher_.publish(msg)
        self.get_logger().info(f'Fingers detected: {count}')

        cv2.putText(frame, f'Fingers: {count}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.imshow('Finger Detection', frame)
        cv2.waitKey(1)

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = FingerDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()