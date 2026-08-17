from ultralytics import YOLO

IMAGES_TO_TEST_PATH = r"tests/yolo_obb/images"
RESULTS_PATH = r"tests/yolo_obb/results"

# obb test on basic yolo with no training on custom dataset
def test_yolo26n_obb():
    model = YOLO("yolo26n.pt")  
    # model.predict(source=IMAGES_TO_TEST_PATH, show=True, save=True, conf=0.25, device=0, imgsz=640, save_dir=RESULTS_PATH, classes=[2,5,7])
    results = model("tests/yolo_obb/results/Screenshot 2026-08-08 165115.jpg")
    for r in results:
        r.show()

test_yolo26n_obb()