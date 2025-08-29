import cv2, logging, time, argparse, os
from yolov8_detect import Detector, bbox_center
from queue_estimator import QueueEstimator
from rule_controller import RuleController
from data_recorder import DataRecorder
import socketio

# 日志
os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/traffic_control.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('--video', type=str, default='sample_video.mp4')
parser.add_argument('--camera', type=int, default=None)
parser.add_argument('--model', type=str, default='models/yolov8n.pt')
parser.add_argument('--panel', type=str, default='http://127.0.0.1:5000')
args = parser.parse_args()

# SocketIO 客户端用于推送面板
sio = socketio.Client(reconnection=True, logger=False, engineio_logger=False)
try:
    sio.connect(args.panel)
except Exception as e:
    print('未连接面板:', e)

detector = Detector(model_path=args.model, conf=0.35, emergency_label_ids=[])
phases = ['NS','EW']
qe = QueueEstimator(phases=phases, window_sec=30, fps=5)
controller = RuleController(phases=phases)
rec = DataRecorder()

# ROI 划分函数（左右两半）
def get_rois(frame):
    h,w = frame.shape[:2]
    return (0,0,w//2,h), (w//2,0,w,h)  # EW, NS

source = args.camera if args.camera is not None else args.video
cap = cv2.VideoCapture(source)
if not cap.isOpened():
    logging.error('Video capture open failed: %s', str(source))
    print('摄像头/视频打开失败，请检查路径或设备。')
    raise SystemExit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    dets, counts, emergency = detector.process(frame)
    roi_ew, roi_ns = get_rois(frame)
    dir_counts = {'EW':0, 'NS':0}
    for d in dets:
        cx,cy = bbox_center(d['xyxy'])
        if roi_ew[0] <= cx <= roi_ew[2]:
            dir_counts['EW'] += 1
        else:
            dir_counts['NS'] += 1
    qe.update_counts(dir_counts)
    queues = qe.all_queues()
    bus_request = counts.get('bus',0) > 0
    decision = controller.step(queues, bus_request=bus_request, emergency_request=emergency)

    # 记录
    rec.write(cars=counts.get('car',0), buses=counts.get('bus',0),
              ns_q=queues['NS'], ew_q=queues['EW'],
              phase=controller.current, reason=decision['reason'],
              green_elapsed=decision['green_elapsed'])
    # 推面板
    try:
        sio.emit('update', {'cars': counts.get('car',0), 'buses': counts.get('bus',0),
                            'phase': controller.current, 'decision': decision['reason']})
    except Exception:
        pass

    # 可视化与文本
    for d in dets:
        x1,y1,x2,y2 = map(int, d['xyxy'])
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
    cv2.putText(frame, f"NS_q={queues['NS']:.1f} EW_q={queues['EW']:.1f}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
    cv2.putText(frame, f"Phase={controller.current} Mode={decision['reason']}", (10,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    cv2.imshow('AI Traffic Demo', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
