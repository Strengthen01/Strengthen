import time

class RuleController:
    """规则控制器：支持动态绿时、公交优先、应急优先、最短/最长绿时约束。"""
    def __init__(self, phases=['NS','EW'], min_green=8, max_green=90, yellow=3, all_red=1):
        self.phases = list(phases)
        self.min_green = min_green
        self.max_green = max_green
        self.yellow = yellow
        self.all_red = all_red
        self.current = 0
        self.phase_start = time.time()

    def elapsed(self):
        return time.time() - self.phase_start

    def dynamic_green_target(self, queue_len):
        q = max(0.0, float(queue_len))
        if q <= 5: return 30
        if q >= 15: return 90
        return 30 + (q-5) * 6.0  # linear interpolation

    def step(self, queues: dict, bus_request=False, emergency_request=False):
        elapsed = self.elapsed()
        # emergency 优先，若满足安全最短绿则切换
        if emergency_request and elapsed >= self.min_green:
            target = max(queues, key=lambda k: queues[k])
            self._switch_to(self.phases.index(target))
            return {'action':'switch','next_phase':self.current,'reason':'emergency','green_elapsed':elapsed}
        # 选择队列最大的相位作为候选
        target = max(queues, key=lambda k: queues[k])
        target_idx = self.phases.index(target)
        # 公交优先
        if bus_request and target_idx != self.current and elapsed >= self.min_green:
            self._switch_to(target_idx)
            return {'action':'switch','next_phase':self.current,'reason':'bus_or_queue','green_elapsed':elapsed}
        # 动态绿时/最长绿判断
        green_target = self.dynamic_green_target(queues[self.phases[self.current]])
        if elapsed >= max(green_target, self.min_green) or elapsed >= self.max_green:
            # 切换到目标相位或轮转
            next_idx = target_idx if target_idx != self.current else (self.current+1)%len(self.phases)
            self._switch_to(next_idx)
            return {'action':'switch','next_phase':self.current,'reason':'queue_pressure','green_elapsed':elapsed}
        return {'action':'stay','next_phase':self.current,'reason':'hold','green_elapsed':elapsed}

    def _switch_to(self, idx):
        self.current = idx
        self.phase_start = time.time()
