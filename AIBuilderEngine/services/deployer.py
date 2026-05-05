import os
import boto3
import subprocess
import shutil
from core.config import settings

s3_client = boto3.client(
    's3',
    endpoint_url=settings.S3_ENDPOINT,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name=settings.S3_REGION
)


def deploy_client_site(project_id: str, port=8082):
    project_folder = f"projects/{project_id}"
    local_tmp_dir = f"tmp_{project_id}"
    image_name = f"client-site-{project_id}"
    container_name = f"container-{project_id}"

    try:
        print(f"📡 Downloading files for project {project_id}...")
        objects = s3_client.list_objects_v2(Bucket=settings.S3_BUCKET, Prefix=project_folder)

        if 'Contents' not in objects:
            print(f"❌ Project {project_id} files not found in MinIO.")
            return

        os.makedirs(local_tmp_dir, exist_ok=True)

        for obj in objects['Contents']:
            s3_path = obj['Key']
            relative_path = os.path.relpath(s3_path, project_folder)
            local_path = os.path.join(local_tmp_dir, relative_path)

            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3_client.download_file(settings.S3_BUCKET, s3_path, local_path)
            print(f"  - Downloaded: {relative_path}")

        print(f"🐳 Building Docker image: {image_name}...")
        subprocess.run(
            ["docker", "build", "-t", image_name, "."],
            cwd=local_tmp_dir,
            check=True
        )

        print(f"🚀 Starting container {container_name} on port {port}...")

        subprocess.run(["docker", "rm", "-f", container_name], stderr=subprocess.DEVNULL)

        subprocess.run([
            "docker", "run", "-d",
            "--name", container_name,
            "--network", "touchcraft_net",
            image_name
        ], check=True)

        print(f"✅ Deployment successful! Container {container_name} is live.")

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        raise e

    finally:
        if os.path.exists(local_tmp_dir):
            shutil.rmtree(local_tmp_dir)
            print(f"🧹 Temporary files for {project_id} removed.")

def stop_container(project_id: str):
    container_name = f"container-{project_id}"
    try:
        subprocess.run(["docker", "stop", container_name], check=True)
        print(f"⏸ Container {container_name} stopped.")
    except Exception as e:
        print(f"❌ Failed to stop {container_name}: {e}")
        raise e

def start_container(project_id: str):
    container_name = f"container-{project_id}"
    try:
        subprocess.run(["docker", "start", container_name], check=True)
        print(f"▶️ Container {container_name} started.")
    except Exception as e:
        print(f"❌ Failed to start {container_name}: {e}")
        raise e
