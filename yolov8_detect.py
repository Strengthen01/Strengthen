from ultralytics import YOLO
import numpy as np

COCO_MAP = {2:'car', 3:'motorcycle', 5:'bus', 7:'truck'}

class Detector:
    """YOLOv8 封装：支持置信度阈值与应急类别标注。"""
    def __init__(self, model_path='models/yolov8n.pt', conf=0.3, emergency_label_ids=None):
        self.model = YOLO(model_path)
        self.conf = conf
        self.emergency_label_ids = set(emergency_label_ids or [])

    def process(self, frame):
        """处理一帧图像，返回 dets(list)、counts(dict)、emergency(bool)。"""
        res = self.model(frame, conf=self.conf)[0]
        dets = []
        emergency = False
        if res.boxes is None:
            return dets, {'car':0,'motorcycle':0,'bus':0,'truck':0}, False
        xyxy = res.boxes.xyxy.cpu().numpy()
        clss = res.boxes.cls.cpu().numpy().astype(int)
        confs = res.boxes.conf.cpu().numpy()
        counts = {'car':0,'motorcycle':0,'bus':0,'truck':0}
        for b, c, cf in zip(xyxy, clss, confs):
            dets.append({'xyxy': b.tolist(), 'cls': int(c), 'conf': float(cf)})
            name = COCO_MAP.get(int(c),'other')
            if name in counts:
                counts[name] += 1
            if int(c) in self.emergency_label_ids:
                emergency = True
        return dets, counts, emergency

    @staticmethod
    def bbox_center(b):
        x1,y1,x2,y2 = b
        return ((x1+x2)/2.0, (y1+y2)/2.0)
