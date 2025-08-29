import collections, numpy as np

class QueueEstimator:
    """多方向队列估算器，带异常值抑制与滑窗。"""
    def __init__(self, phases=['NS','EW'], window_sec=30, fps=5):
        self.phases = list(phases)
        self.window = max(1, int(window_sec * fps))
        self.history = {p: collections.deque(maxlen=self.window) for p in self.phases}

    def _append(self, phase, val):
        hist = self.history[phase]
        if len(hist) >= 3:
            mean3 = float(np.mean(list(hist)[-3:]))
            if val > max(1.0, mean3) * 2.0:
                val = mean3
        hist.append(float(val))

    def update_counts(self, counts_by_phase):
        for p, v in counts_by_phase.items():
            if p in self.history:
                self._append(p, float(v))

    def queue_length(self, phase):
        hist = self.history.get(phase, [])
        return float(np.mean(hist)) if len(hist)>0 else 0.0

    def all_queues(self):
        return {p: self.queue_length(p) for p in self.phases}
