from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def hello():
    try:
        # Get the metadata endpoint from environment variables
        ecs_metadata_uri = os.environ.get('ECS_CONTAINER_METADATA_URI_V4')

        if not ecs_metadata_uri:
            return "Error: ECS_CONTAINER_METADATA_URI_V4 not found in environment variables.", 500

        # Fetch ECS Task Metadata
        task_metadata = requests.get(f"{ecs_metadata_uri}/task").json()

        # Extract task-level information
        task_arn = task_metadata.get("TaskARN", "N/A")
        task_id = task_arn.split('/')[-1]
        family = task_metadata.get("Family", "N/A")
        revision = task_metadata.get("Revision", "N/A")
        cluster_name = task_metadata.get("Cluster", "N/A").split('/')[-1]

        # Extract CPU and Memory limits from task-level metadata
        cpu_limit = task_metadata.get("Limits", {}).get("CPU", "N/A")
        memory_limit = task_metadata.get("Limits", {}).get("Memory", "N/A")

        # Retrieve public IP
        public_ip = requests.get('https://checkip.amazonaws.com/').text.strip()

        # Container-specific information
        containers_info = []
        containers = task_metadata.get("Containers", [])
        for container in containers:
            container_name = container.get("Name", "N/A")
            image = container.get("Image", "N/A")
            private_ip = container.get("Networks", [{}])[0].get("IPv4Addresses", ["N/A"])[0]

            # Use task-level CPU and Memory limits if container-level limits are not set
            container_cpu = container.get("Limits", {}).get("CPU", cpu_limit)
            container_memory = container.get("Limits", {}).get("Memory", memory_limit)

            containers_info.append({
                "container_name": container_name,
                "image": image,
                "private_ip": private_ip,
                "public_ip": public_ip,
                "cpu": container_cpu,
                "memory": container_memory
            })

        # Render the template with the data
        return render_template(
            'index.html',
            message="Hello from ECS!",
            task_id=task_id,
            family=family,
            revision=revision,
            cluster_name=cluster_name,
            cpu=cpu_limit,
            memory=memory_limit,
            containers=containers_info
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
