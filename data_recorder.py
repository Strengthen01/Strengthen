import csv, os
from datetime import datetime

class DataRecorder:
    """将每帧的数据写入 CSV，便于复盘与绘图。"""
    def __init__(self, out_dir='data', prefix='traffic'):
        os.makedirs(out_dir, exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.path = os.path.join(out_dir, f"{prefix}_{ts}.csv")
        with open(self.path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['time','cars','buses','NS_q','EW_q','phase','reason','green_elapsed'])

    def write(self, cars, buses, ns_q, ew_q, phase, reason, green_elapsed):
        with open(self.path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), cars, buses, f"{ns_q:.2f}", f"{ew_q:.2f}", phase, reason, f"{green_elapsed:.2f}"])
