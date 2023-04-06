import torch
import torchvision

def scale_bbox(xmin,ymin,xmax,ymax,perc=7):
  "https://techoverflow.net/2021/04/26/how-to-make-bounding-box-larger-by-a-percentage-in-python/"

  n = (perc/2) * 0.01
  xmin -= n * (xmax - xmin)
  xmax += n * (xmax - xmin)
  ymin -= n * (ymax - ymin)
  ymax += n * (ymax - ymin)

  return [xmin,ymin,xmax,ymax]

def convert_to_x1y1x2y2(bbxx):

  tensor_bbox = torch.tensor(bbxx, dtype=torch.int)
  tensor_bbox = tensor_bbox.unsqueeze(0)
  tensor_bbox = torchvision.ops.box_convert(tensor_bbox, in_fmt="xywh", out_fmt="xyxy")
  box = tensor_bbox.tolist()[0]
  return box


def convert_to_xywh(bbxs):

  out = []
  for bbxx in bbxs:
    bbxx = list(bbxx)
    bbx = bbxx[0]
    tensor_bbox = torch.tensor(bbx, dtype=torch.int)
    tensor_bbox = tensor_bbox.unsqueeze(0)
    tensor_bbox = torchvision.ops.box_convert(tensor_bbox, in_fmt="xyxy", out_fmt="xywh")
    bbxx[0] = tensor_bbox.tolist()[0]
    bbxx = tuple(bbxx)
    out.append(bbxx)
  return out