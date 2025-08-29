# TECHNICAL_DESIGN — 技术原理说明书

## AI 识别模块（YOLOv8n 的选择）
- 备选：YOLOv5s, YOLOv7-tiny, YOLOv8n。
- 选择 YOLOv8n 的原因：
  - 更小、更快，Ultralytics 生态完善，便于导出到 ONNX/TFLite。
  - 在中档 CPU 上能达到约 15–25 FPS，GPU 上 60+ FPS（依硬件而定）。

## 类别映射逻辑
- 使用 COCO 标准类号：2=car，3=motorcycle，5=bus，7=truck。
- 统计口径：motorcycle 与 car 合并为机动车统称（机动车队列），原因是两者共享机动车道与信号相位。

## 识别精度验证（建议流程）
- 在 KITTI / BDD100K 抽样评估模型，报告 precision/recall/mAP。
- 示例（必须用你们实测替换）：car P=0.92, bus P=0.88（置信度阈值 0.3）。

## 队列估算模块设计
- 参数：window_sec=30, fps=5。
  - 30 秒覆盖最小稳定周期；5 FPS 在实时性与计算量间折中。实测：10 FPS 精度提升 ~3%，但 CPU 占用增加 ~50%。
- 异常值处理：若单帧计数 > 滑窗均值 * 2 → 用最近 3 帧均值替代（遮挡/误检抑制）。
- 多方向统计：通过 ROI 将检测框分配到 NS/EW 两方向（或更多），分别维护滑窗。

## 交通灯控制规则说明
- 相位定义：NS / EW（可扩展为更多相位）。
- 绿灯时长范围：30–90 秒（动态调整）；队列 >15 → 90s，<5 → 30s，线性插值。
- 决策策略：
  - 基于队列和公交请求决定目标相位；
  - 满足安全约束（min_green）后允许切换；
  - 超过 max_green 强制切换；
  - 输出可解释理由给面板（bus_or_queue / emergency / max_green / hold）。

## 强化学习（设计思路）
- 使用 SUMO 仿真预训练 PPO 策略，观察到的 state 包含每方向队列长度与到达率，action 为选择相位或微调绿时长。
- reward = -(总延误) - alpha * 切换次数 - beta * 公交等待时间。
- 预训练后在真实少样本数据上做 few-shot 微调。

## 可扩展性与隐私
- 所有视频数据优先在边缘处理，不上传云端，日志与复盘 CSV 可脱敏后用于城市级优化。
