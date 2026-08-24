import docker
import os
import asyncio


class Sandbox():
    project_path = os.path.expanduser("~/Documents/Dev Projects/learning_classes")

    def __init__(self):

        self.client = docker.from_env()

    def make(self):

        image = self.client.images.get("sandbox:latest")
        print(image)
        if str(image) != "<Image: 'sandbox:latest'>":
            print("Need to create image")

            try:
                print()
                build = self.client.api.build(
                    path=self.project_path,
                    dockerfile="Dockerfile",
                    tag="sandbox:latest",
                    decode=True
                )
                    
            
                for message in build:
                    print(message)
            except Exception as e:
                
                print(f"An error occurred: {e}")
            print("Image found!")

        print("inspecting containers")
        self.containers = self.client.containers.list()


        container_running = False


        for container in self.containers:
            if "sandbox:latest" in container.image.tags:       
                print("container found")
                container_running = True
                break
        print("Is container running? : " + str(container_running))

        if container_running == True:
            self.container = self.client.containers.get("sandbox")
            print(container)
            print_command = container.exec_run(
            ["python3", "-c", 'print("Now in container")'], 
            stdout=True, stderr=True, stdin=True,  stream=False)
            print(print_command.output)

        else:
            print("Again:" + str(container_running))
            self.container = self.client.containers.get("sandbox")
            self.container.start()
            container_running = True
            print("started!:" + str(container_running))



    def execute(self, command):

        output = self.container.exec_run(
                command, 
                stdout=True, stderr=True, stdin=True,  stream=False)
        print(output.output)



sandbox = Sandbox()
sandbox.make()
sandbox.execute("pwd")















# print(container.id)

