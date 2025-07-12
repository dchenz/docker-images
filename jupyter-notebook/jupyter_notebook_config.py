import os

c.ServerApp.ip = "0.0.0.0"
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.IdentityProvider.token = ""
c.ServerApp.root_dir = os.path.expanduser("~/data")
c.KernelSpecManager.ensure_native_kernel = False
c.FileCheckpoints.checkpoint_dir = "/tmp/checkpoints"
