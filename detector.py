from ultralytics import YOLO
from sklearn.cluster import DBSCAN
import numpy as np

class CrowdDetector:
    def __init__(
        self,
        model_path="yolov8n.pt",
        conf_threshold=0.3,          # 🔥 as requested
        crowd_threshold=3,
        distance_threshold=60
    ):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.crowd_threshold = crowd_threshold
        self.distance_threshold = distance_threshold

    def predict(self, image):
        results = self.model(image)[0]

        persons = []
        detections = []

        # ===== Detect people =====
        for box in results.boxes:
            conf = float(box.conf[0])
            if conf < self.conf_threshold:
                continue

            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]

            if class_name != "person":
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            persons.append((cx, cy))

            detections.append({
                "bbox": [x1, y1, x2, y2],
                "confidence": round(conf, 4),
                "class_name": "person"
            })

        # ===== Crowd Detection using DBSCAN =====
        crowd_results = []
        
        if len(persons) >= self.crowd_threshold:
            # Convert to numpy array for DBSCAN
            persons_array = np.array(persons)
            
            # DBSCAN clustering: eps=distance_threshold, min_samples=crowd_threshold
            clustering = DBSCAN(eps=self.distance_threshold, min_samples=self.crowd_threshold).fit(persons_array)
            labels = clustering.labels_
            
            # Extract clusters (labels >= 0, ignore noise points with label -1)
            unique_labels = set(labels)
            for label in unique_labels:
                if label == -1:  # Skip noise
                    continue
                
                cluster_indices = np.where(labels == label)[0]
                cluster_members = [persons[idx] for idx in cluster_indices]
                
                crowd_result = {
                    "count": len(cluster_members),
                    "members": cluster_members
                }
                crowd_results.append(crowd_result)

        return {
            "total_people": len(persons),
            "crowd_count": len(crowd_results),
            "crowds": crowd_results,
            "detections": detections
        }