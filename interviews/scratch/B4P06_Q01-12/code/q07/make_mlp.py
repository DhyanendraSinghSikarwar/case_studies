import sys, torch
torch.manual_seed(0)
m = torch.nn.Sequential(torch.nn.Linear(512, 2048), torch.nn.ReLU(), torch.nn.Linear(2048, 2048),
                        torch.nn.ReLU(), torch.nn.Linear(2048, 10)).eval()
torch.onnx.export(m, torch.zeros(1, 512), sys.argv[1], input_names=["x"], output_names=["y"],
                  dynamic_axes={"x": {0: "b"}, "y": {0: "b"}}, dynamo=False)
print("wrote", sys.argv[1])
