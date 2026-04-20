import docker, time
from typing import Dict, Any

class DockerSandbox:
    def __init__(self, image: str="python:3.10-slim"):
        self.client = docker.from_env()
        self.image = image
        
        try:
            self.client.images.get(self.image)
        except docker.errors.ImageNotFound:
            print(f"Pulling {self.image}...")
            self.client.images.pull(self.image)
    
    def execute_code(self, code: str, timeout: int=10) -> Dict[str, Any]:
        container=None
        try:
            container = self.client.containers.run(
                self.image,
                command=["python", "-c", code],
                detach=True,
                mem_limit="128m",
                nano_cpus=500_000_000,   
                pids_limit=64,
                network_disabled=True,
                read_only=True,
                tmpfs={"/tmp": "rw,noexec,nosuid,size=64m"},
                security_opt=["no-new-privileges"],
                user="1000:1000",
                cap_drop=["ALL"]
            )
            
            starttime = time.time()
            
            while container.status in ["created", "running"]:
                container.reload()
                if time.time() - starttime > timeout:
                    container.kill()
                    return {
                        "status": "error",
                        "stdout": "",
                        "stderr": f"TimeoutError: Code execution exceeded {timeout} seconds.",
                        "exit_code": 124
                    }            
                time.sleep(0.1)
            
            res = container.wait()
  
            stdout = container.logs(stdout=True, stderr=False).decode("utf-8")
            stderr = container.logs(stdout=False, stderr=True).decode("utf-8")
            
            return {
                "status": "success" if res["StatusCode"]==0 else "error",
                "stdout": stdout.strip(),
                "stderr": stderr.strip(),
                "exit_code": res["StatusCode"]
            } 
        except Exception as e:
            return {
                "status": "error",
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1
            } 
        finally:
            if container:
                try: container.remove(force=True)
                except: pass